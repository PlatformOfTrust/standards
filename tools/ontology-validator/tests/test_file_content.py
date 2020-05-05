"""This module has test functions for the validations of the files contents."""
from typing import List, Tuple
from pathlib import Path
import pytest
from testfixtures import LogCapture

from utils.constants import _ID, _TYPE, _PREFIX, RDF_PROPERTY, DOMAIN, FIELDS_WITH_TYPE_LIST, PARENT,\
    FIELDS_TYPES_RESTRICTIONS, SHOULD_BE_IN, POT_CLASS, PREFIXED, PROPERTY,\
    REQUIRED, REQUIRED_ATTRIBUTES, NAME, IS_IN, TEST_FILE_REFERENCES_PATH,\
    CONTEXT_FOLDER, CLASS_DEFINITIONS_FOLDER, VOCAB_FOLDER, _CONTEXT, SUPP_CLASS, SUPP_ATTRIBUTE, add_prefixes

from utils.structure import Structure
from utils.json import read_json_file
from utils.property import Property
from utils.ontology import Ontology

from validators.file_content.class_and_property_names\
    import ClassAndPropertyNames
from validators.file_content.files_references import FilesReferences
from validators.file_content.labels import Labels
from validators.file_content.list_field_type import ListFieldType
from validators.file_content.object_required_attributes\
    import ObjectRequiredAttributes
from validators.file_content.class_name_is_file_name\
    import ClassNameIsFileName
from validators.file_content.properties_inheritance\
    import PropertiesInheritance
from validators.file_content.properties_defined import PropertiesDefined
from validators.file_content.domain import Domain
from validators.file_content.total_domain import TotalDomain
from validators.file_content.objects_defined import ObjectsDefined
from validators.file_content.required_value_in_subproperties\
    import RequiredValueInSubproperties
from validators.file_content.attributes_values import AttributesValues
from validators.file_content.type_files import TypeFiles


@pytest.mark.parametrize(
    "file, expected",
    [("./tests/data/Files/ClassNameCamelCase.jsonld", False),
     ("./tests/data/Files/ClassNameUnexistingWord.jsonld", False),
     ("./tests/data/Files/Correct class and property naming.jsonld", True),
     ("./tests/data/Files/PropertyNamePascalCase.jsonld", False),
     ("./tests/data/Files/PropertyNameUnexistingWord.jsonld", False)])
def test_class_and_property_names_validator(file: str, expected: bool,
                                            mocked_pascal_and_camel_case):
    """This function tests ClassAndPropertyNames validator."""
    file_content = read_json_file(file)
    assert ClassAndPropertyNames(
        file_content,
        "Class and Property names validation failed").validate() == expected


@pytest.mark.parametrize(
    "file, folder, messages, expected",
    [("./tests/data/Files/test_labels/voc1.jsonld", VOCAB_FOLDER,
      ["'Building' (pot:Class): 'rdfs:label', language 'en-us' is not a "
       "string", "'fi-fi' language missing for 'rdfs:comment' in "
       "'descriptionGeneral' (rdf:Property)"], False),
     ("./tests/data/Files/test_labels/voc2.jsonld", VOCAB_FOLDER,
      ["'BuildingElement' (pot:Class): Spell check for 'rdfs:label', language"
       " 'en-us': 'Building WRONGGGG' failed"], False),
     ("./tests/data/Files/test_labels/vocpass.jsonld", VOCAB_FOLDER, [], True),
     ("./tests/data/Files/test_labels/clsdef1.jsonld",
      CLASS_DEFINITIONS_FOLDER,
      ["'data' (dli:SupportedAttribute): 'dli:title' is not a string",
       "'fi-fi' language missing for 'dli:description' in 'createdAt' "
       "(dli:SupportedAttribute)"], False),
     ("./tests/data/Files/test_labels/clsdef2.jsonld",
      CLASS_DEFINITIONS_FOLDER,
      ["'data' (dli:SupportedAttribute): Spell check for 'dli:description', "
       "language 'en-us': 'Data WRONGGGG' failed"], False),
     ("./tests/data/Files/test_labels/clsdefpass.jsonld",
      CLASS_DEFINITIONS_FOLDER, [], True)])
def test_labels_validation(file: str, folder: str, messages: str,
                           expected: bool, mocked_spell_check):
    """This function tests Labels validator."""
    file_content = read_json_file(file)
    Structure.validate_fifi = True

    with LogCapture() as logs:
        assert Labels(file_content, folder, "Labels validation failed"
                      ).validate() == expected

        for message in messages:
            assert message in str(logs)


@pytest.mark.parametrize(
    "file_content, expected",
    [({"other": ["smth"]}, False),
     ({"othr": {"smth": {"smth": "ds", "smthelse": []}}}, False),
     ({DOMAIN: []}, True),
     ({DOMAIN: [], "smth": []}, False),
     ({}, True)])
def test_list_field_type_validator(file_content: dict, expected: bool):
    """This function tests ListFieldType validator."""
    Structure.structure[FIELDS_TYPES_RESTRICTIONS] = {}
    Structure.structure[FIELDS_TYPES_RESTRICTIONS][FIELDS_WITH_TYPE_LIST] =\
        [DOMAIN]
    assert ListFieldType(
        file_content,
        "Field should not be a list").validate() == expected


@pytest.mark.parametrize(
    "file_content, expected",
    [({"p1": {_TYPE: RDF_PROPERTY}}, False),
     ({"p1": {_TYPE: ":Propert"}}, True),
     ({"p1": {_TYPE: RDF_PROPERTY, "atr": "val"},
       "p2": {_TYPE: RDF_PROPERTY, "atrs": "val"}}, False),
     ({"p1": {_TYPE: RDF_PROPERTY, "atr": "val"},
       "p2": {_TYPE: RDF_PROPERTY, "atr": "val"},
       "p3": {_TYPE: ":Propert", "atrs": "val"}}, True),
     ({}, True)])
def test_properties_required_attributes_validator(file_content: dict,
                                                  expected: bool):
    """This function tests ObjectRequiredAttributes validator."""
    Structure.structure[REQUIRED_ATTRIBUTES][PROPERTY] = ["atr"]

    assert ObjectRequiredAttributes(
        file_content, PROPERTY,
        "Required attributes for Property missing").validate() == expected


@pytest.mark.parametrize(
    "file_content, properties, expected",
    [({"p1": {}}, ["p2"], False),
     ({"p1": {}}, ["p1", "p2"], False),
     ({"p1": {}, "p2": {}}, ["p1", "p2", "p3"], False),
     ({"p1": {}, "p2": {}, "p3": {}}, ["p1", "p2", "p3"], True),
     ({}, [], True)])
def test_properties_inheritance_validator(file_content: dict,
                                          properties: List[str],
                                          expected: bool):
    """This function tests PropertiesInheritance validator."""
    assert PropertiesInheritance(
        file_content, properties,
        "Properties inheritance validation failed").validate() == expected


@pytest.mark.parametrize(
    "defined_properties, all_properties, expected",
    [([], [], True),
     (["p1", "p2"], [], True),
     ([], ["p1"], False),
     (["p1", "p2"], ["p1", "p2", "p3"], False),
     (["p1", "p2", "p3"], ["p1", "p2"], True)])
def test_properties_defined_validator(defined_properties: List[str],
                                      all_properties: List[str],
                                      expected: bool):
    """This function tests PropertiesDefined validator."""
    assert PropertiesDefined(
        all_properties, defined_properties,
        "Some properties are not defined in ClassDefinitions"
        ).validate() == expected


@pytest.mark.parametrize(
    "file_content, class_name, properties, expected",
    [({"p1": {_TYPE: RDF_PROPERTY, DOMAIN: ["clsName1"]}},
      "clsName", ["p2"], False),
     ({"p1": {_TYPE: RDF_PROPERTY, DOMAIN: ["clsName"]}},
      "clsName", ["p2"], True),
     ({"p1": {_TYPE: RDF_PROPERTY, DOMAIN: ["clsName1"]}},
      "clsName", ["p1"], True),
     ({"p1": {_TYPE: RDF_PROPERTY, DOMAIN: ["clsName"]},
       "p2": {_TYPE: RDF_PROPERTY, DOMAIN: ["clsName1"]}},
      "clsName", ["p2"], True)])
def test_domain_validator(file_content: dict, class_name: str,
                          properties: List[str], expected: bool):
    """This function tests Domain validator."""
    assert Domain(file_content, class_name, properties,
                           "Domain validation failed").validate() == expected


@pytest.mark.parametrize(
    "property_apparitions, expected",
    [({"p1": {SHOULD_BE_IN: ["pot:A"], IS_IN: ["pot:A"]}}, True),
     ({"p1": {SHOULD_BE_IN: ["pot:A", "pot:B"], IS_IN: ["pot:A"]}}, False),
     ({"p1": {SHOULD_BE_IN: ["pot:A", "pot:B"], IS_IN: ["pot:A", "pot:B"]}},
      True),
     ({"p1": {SHOULD_BE_IN: ["pot:A"], IS_IN: ["pot:A"]},
       "p2": {SHOULD_BE_IN: ["pot:A"], IS_IN: []}}, False),
     ({"p1": {SHOULD_BE_IN: ["pot:A"], IS_IN: ["pot:A"]},
       "p2": {SHOULD_BE_IN: ["dli:A"], IS_IN: []}}, True)])
def test_total_domain_validator(property_apparitions: dict, expected: bool):
    """This function tests TotalDomain validator."""
    Ontology.ontology_name = "pot"
    Property.property_apparitions = property_apparitions
    assert TotalDomain(
        "Some properties are not defined in ClassDefinitions"
        ).validate() == expected


@pytest.mark.parametrize(
    "file_content, expected",
    [({"p1": {_TYPE: RDF_PROPERTY, _ID: "pot:p1"},
       "Cls": {_TYPE: POT_CLASS, _ID: "pot:Cls"}}, False),
     ({"p3": {_TYPE: RDF_PROPERTY, _ID: "pot:p3"},
       "Cls": {_TYPE: POT_CLASS, _ID: "pot:Cls"}}, True),
     ({"p1": {_TYPE: RDF_PROPERTY, _ID: "pot:p1"},
       "Cls": {_TYPE: POT_CLASS, _ID: "pot:Clss"}}, False),
     ({"p1": {_TYPE: RDF_PROPERTY, _ID: "pot:p3/p2/p1"},
       "Cls": {_TYPE: POT_CLASS, _ID: "pot:Cls"}}, True)
     ])
def test_class_and_property_in_ontology_validator(file_content: dict,
                                                  expected: bool):
    """This function tests ObjectsDefined validator."""
    Ontology.defines["pot:Cls"] = {}
    Ontology.defines["pot:p1"] = {NAME: "p1", PARENT: "pot:p2"}
    Ontology.defines["pot:p2"] = {NAME: "p2", PARENT: "pot:p3"}
    Ontology.defines["pot:p3"] = {NAME: "p3"}

    assert ObjectsDefined(
        file_content,
        "Some classes and properties are not defined in the ontology file"
        ).validate() == expected


@pytest.mark.parametrize(
    "defines, expected",
    [({"p1": {_TYPE: RDF_PROPERTY}}, True),
     ({"p1": {_TYPE: RDF_PROPERTY, PARENT: "p2", "dli:required": False},
       "p2": {_TYPE: RDF_PROPERTY, "dli:required": True}}, False),
     ({"p1": {_TYPE: RDF_PROPERTY, PARENT: "p2", "dli:required": True},
       "p2": {_TYPE: RDF_PROPERTY, PARENT: "p3", "dli:required": True},
       "p3": {_TYPE: RDF_PROPERTY, "dli:required": False}}, True),
     ({"p1": {_TYPE: RDF_PROPERTY, PARENT: "p2", "dli:required": True},
       "p2": {_TYPE: RDF_PROPERTY, PARENT: "p3", "dli:required": False},
       "p3": {_TYPE: RDF_PROPERTY, "dli:required": False},
       "c1": {_TYPE: POT_CLASS}}, True)])
def test_required_value_in_subproperties_validator(defines: dict,
                                                   expected: bool):
    """This function tests RequiredValueInSubproperties validator."""
    Ontology.defines = defines
    add_prefixes('dli')

    assert RequiredValueInSubproperties(
        "Subproperty has different value for dli:required than the base "
        "property").validate() == expected


@pytest.mark.parametrize(
    "file_content, path, expected",
    [({"class": {_TYPE: POT_CLASS, _ID: "pot:base/class"}},
      "Vocabulary/class.jsonld", True),
     ({"other": {_TYPE: POT_CLASS, _ID: "pot:base/other"}},
      "Vocabulary/class.jsonld", False),
     ({"dli:supportedClass": {_ID: "pot:class"}},
      "ClassDefinitions/class.jsonld", True),
     ({"dli:supportedClass": {_ID: "pot:base/other"}},
      "ClassDefinitions/class.jsonld", False),
     ({"dli:supportedClass": {_ID: "pot:base1/base2/class"}},
      "ClassDefinitions/class.jsonld", True)])
def test_class_name_is_file_name_validator(file_content: dict, path: str,
                                           expected: bool):
    """This function tests ClassNameIsFileName."""
    add_prefixes('dli')

    assert ClassNameIsFileName(
        file_content, path, "Class name is not the same with file name"
    ).validate() == expected


@pytest.mark.parametrize(
    "file_content, path, defines, expected",
    [({"p1": {_TYPE: RDF_PROPERTY, _ID: "pot:p1"},
       "p2": {_TYPE: RDF_PROPERTY, _ID: "pot:p2"},
       "c1": {_TYPE: POT_CLASS, _ID: "pot:c1"}},
      "Vocabulary/class.jsonld",
      {"pot:p1": {_TYPE: RDF_PROPERTY},
       "pot:p2": {_TYPE: RDF_PROPERTY},
       "pot:c1": {_TYPE: "pot:Cls"}}, True),
     ({"p1": {_TYPE: RDF_PROPERTY, _ID: "pot:p1"},
       "p2": {_TYPE: "dli:Property", _ID: "pot:p2"},
       "c1": {_TYPE: "pot:Class", _ID: "pot:c1"}},
      "Vocabulary/class.jsonld",
      {"pot:p1": {_TYPE: RDF_PROPERTY},
       "pot:p2": {_TYPE: RDF_PROPERTY},
       "pot:c1": {_TYPE: "pot:Cls"}}, False),
     ({"dli:supportedClass":
       {"dli:supportedAttribute":
        {"p1": {"dli:required": False, _ID: "pot:p1"},
         "p2": {"dli:required": True, _ID: "pot:p2"}}}},
      "ClassDefinitions/class.jsonld",
      {"pot:p1": {"dli:required": False},
       "pot:p2": {"dli:required": True},
       "pot:c1": {"dli:required": True}}, True),
     ({"dli:supportedClass":
       {"dli:supportedAttribute":
        {"p1": {"dli:required": True, _ID: "pot:p1"},
         "p2": {"dli:required": False, _ID: "pot:p2"}}}},
      "ClassDefinitions/class.jsonld",
      {"pot:p1": {"dli:required": True},
       "pot:p2": {"dli:required": True},
       "pot:c1": {"dli:required": True}}, False)])
def test_ontology_defined_property_fields_validator(file_content: dict,
                                                    path: str,
                                                    defines: dict,
                                                    expected: bool):
    """This function tests AttributesValues validator."""
    Ontology.defines = defines

    assert AttributesValues(
        file_content, path, "Ontology defined property attributes"
    ).validate() == expected


@pytest.mark.parametrize(
    "file_content, expected",
    [({_CONTEXT: {"pot": {_ID: "https://targetURL/v1/folder",
                          _PREFIX: True}},
       "class": {_TYPE: "pot:class", _ID: "pot:base/class"}}, True),
     ({_CONTEXT:
       {"pot": {_ID: "https://targetURL/v1/folder", _PREFIX: True}},
       "class": {"deep": {"deep": {_TYPE: "pot:class",
                                   _ID: "pot:base/class"}}}}, True),
     ({_CONTEXT: {"pot": {_ID: "https://otherURL/v1/folder",
                          _PREFIX: True}},
       "class1": {_TYPE: "pot:class1"},
       "class2": {_TYPE: "pot:class2"}}, True),
     ({_CONTEXT: {"pot": {_ID: "https://targetURL/v1/folder",
                          _PREFIX: True}},
       "class": {_TYPE: POT_CLASS}}, False),
     ({_CONTEXT: {"pot": {_ID: "https://otherURL/v1/folder",
                          _PREFIX: True}},
       "class": {_TYPE: POT_CLASS}}, False)
     ])
def test_type_files_validator(file_content: dict, expected: bool):
    """This function tests TypeFiles validator."""
    Structure.root_folder = "path"
    Structure.structure = {}
    Structure.structure["URL"] = "https://targetURL"
    Structure.types_cache = {}
    Structure.types_cache[str(Path("path/v1/folder/class.jsonld"))] = True
    Structure.types_cache["https://otherURL/v1/folder/class1.jsonld"] = True
    Structure.types_cache["https://otherURL/v1/folder/class2.jsonld"] = True
    Structure.types_cache["https://otherURL/v1/folder/Class.jsonld"] = False
    Structure.types_cache[str(Path("path/v1/folder/Class.jsonld"))] = False

    assert TypeFiles(file_content, "Type file missing").validate() == expected

@pytest.mark.parametrize(
    "path, folder, expected",
    [(f"{TEST_FILE_REFERENCES_PATH}ClassDefinitions without @vocab.jsonld",
      CLASS_DEFINITIONS_FOLDER, False),
     (f"{TEST_FILE_REFERENCES_PATH}Context without @classDefinition.jsonld",
      CONTEXT_FOLDER, False),
     (f"{TEST_FILE_REFERENCES_PATH}Context without @vocab.jsonld",
      CONTEXT_FOLDER, False),
     (f"{TEST_FILE_REFERENCES_PATH}Context correct.jsonld",
      CONTEXT_FOLDER, True),
     (f"{TEST_FILE_REFERENCES_PATH}ClassDefinitions correct.jsonld",
      CLASS_DEFINITIONS_FOLDER, True)])
def test_files_references_validator(path: str, folder: str, expected: bool):
    """This function tests FilesReferences validator."""
    file_content = read_json_file(path)

    assert FilesReferences(file_content, folder).validate() == expected
