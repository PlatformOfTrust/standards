"""This module has test functions for validators defined in validators.file
module."""
from typing import List
from pathlib import Path
import pytest
from testfixtures import LogCapture

from validators.file.context import ContextFile
from validators.file.vocabulary import VocabularyFile
from validators.file.class_definition import ClassDefinitionFile
from validators.all_files import AllFiles
from utils.structure import Structure
from utils.ontology import Ontology
from utils.json import read_json_file
from utils.constants import ONTOLOGY, SUPP_CLASS, SUPP_ATTRIBUTE,\
    PREFIXED, RDFS_SUB_CLASS_OF, _CONTEXT, _CLASS_DEFINITION,\
    _VOCAB, _TYPE, _PREFIX, RDF_PROPERTY, DOMAIN, FIELDS_TYPES_RESTRICTIONS,\
    FIELDS_WITH_TYPE_LIST, add_prefixes


@pytest.mark.parametrize(
    "file_content, expected",
    [({_CONTEXT: {"smth": []}}, False),
     ({_CONTEXT: {}}, False),
     ({_CONTEXT: {_CLASS_DEFINITION: ""}}, False),
     ({_CONTEXT: {_CLASS_DEFINITION: "", _VOCAB: ""}, "smth": []},
      False),
     ({_CONTEXT: {_CLASS_DEFINITION: "", _VOCAB: ""}}, True)])
def test_context_file_validator_validate(file_content: dict,
                                         expected: bool):
    """This method tests that ContextFile.validate() works."""
    Structure.structure[FIELDS_TYPES_RESTRICTIONS] = {}
    Structure.structure[FIELDS_TYPES_RESTRICTIONS][FIELDS_WITH_TYPE_LIST] =\
        [DOMAIN]

    validator = ContextFile(file_content, "", "Context file validation failed")

    assert validator.validate() == expected


@pytest.mark.parametrize(
    "file_content, expected",
    [({_CONTEXT: {"smth": []}}, []),
     ({_CONTEXT: {"p1": []}}, []),
     ({_CONTEXT: {"p1": {_PREFIX: True}, "p2": {"a": "b"}}}, ["p2"]),
     ({_CONTEXT: {_VOCAB: "", "p1": {}, "smth": []}}, ["p1"]),
     ({_CONTEXT: {"p1": "", "p2": {"a": "b"}, "p3": {}}}, ["p2", "p3"])])
def test_context_file_validator_get_properties(file_content: dict,
                                               expected: bool):
    """This method tests that ContextFile.get_properties() works."""
    validator = ContextFile(file_content, "", "Context file validation failed")
    assert validator.get_properties() == expected


def test_context_file_validator_get_class_definition():
    """This method tests that ContextFile.get_class_definition() works."""
    Structure.structure["URL"] = "https://"
    Structure.root_folder = "local_path"
    file_content = {_CONTEXT: {_CLASS_DEFINITION: "https://location"}}
    expected = str(Path("local_path") / Path("location.jsonld"))
    validator = ContextFile(file_content, "", "Context file validation failed")

    assert validator.get_class_definition() == expected


@pytest.mark.parametrize(
    "file_content, expected",
    [({"cls1": {RDFS_SUB_CLASS_OF: ""}}, ["cls1"]),
     ({"cls1": {RDFS_SUB_CLASS_OF: ""},
       "cls2": {RDFS_SUB_CLASS_OF: ""}}, ["cls1", "cls2"]),
     ({_CONTEXT: {_CLASS_DEFINITION: ""}}, [])])
def test_vocabulary_file_validator_get_derived_classes(file_content: dict,
                                                       expected: List[str]):
    """This method tests that VocabularyFile.get_class_definition() works."""
    validator = VocabularyFile(file_content, "", [],
                               "Vocabulary file validation failed")

    assert validator.get_derived_classes() == expected


@pytest.mark.parametrize(
    "file, message, expected",
    [("tests/data/Files/Vocabulary/OwnerAt.jsonld",
      "Class name is not the same with file name", False)
     ])
def test_vocabulary_file_validator(file: str, message: str,
                                   expected: List[str]):
    """This method tests that VocabularyFile validator works."""
    file_content = read_json_file(file)

    Structure.read_structure()
    Structure.set_root_folder("tests/data/v6")

    Ontology.ontology_name = Structure.structure[ONTOLOGY]
    Ontology.read_ontology_file("tests/data/v6")
    Ontology.preprocess()

    validator = VocabularyFile(file_content, file, [],
                               "Vocabulary file validation failed")
    with LogCapture() as logs:
        assert validator.validate() == expected
        assert message in str(logs)


@pytest.mark.parametrize(
    "file_content, expected",
    [({_CONTEXT: {"p1": []}}, []),
     ({_CONTEXT: {"p1": {_PREFIX: True}}, "p2": {_TYPE: RDF_PROPERTY}},
      ["p2"]),
     ({_CONTEXT: {"p1": {_PREFIX: True}}, "p2": {_TYPE: "rdf:Propery"}},
      []),
     ({_CONTEXT: {}, "p1": {_TYPE: RDF_PROPERTY}, "p2": {"a": "b"},
       "p3": {_TYPE: RDF_PROPERTY}}, ["p1", "p3"])])
def test_vocabulary_file_validator_get_properties(file_content: dict,
                                                  expected: bool):
    """This method tests that VocabularyFile.get_properties() works."""
    validator = VocabularyFile(file_content, "", [],
                               "Vocabulary file validation failed")
    assert validator.get_properties() == expected


def test_class_definition_file_validator_get_vocabulary_file():
    """This method tests that ClassDefinitionFile.get_vocabulary_file() works.
    """
    Structure.structure["URL"] = "https://"
    Structure.root_folder = "local_path"
    file_content = {_CONTEXT: {_VOCAB: "https://location"}}
    expected = str(Path("local_path") / Path("location.jsonld"))
    validator = ClassDefinitionFile(
        file_content, "", "Class Definition file validation failed")

    assert validator.get_vocabulary_file() == expected


@pytest.mark.parametrize(
    "file_content, expected",
    [({_CONTEXT: {"p1": []}}, []),
     ({_CONTEXT: {"p1": {_PREFIX: True}},
       PREFIXED[SUPP_CLASS]: {PREFIXED[SUPP_ATTRIBUTE]: {"p1": ""}}},
      ["p1"]),
     ({PREFIXED[SUPP_CLASS]: {PREFIXED[SUPP_ATTRIBUTE]:
                         {"p1": "", "p2": {}}},
       "prop": {_TYPE: RDF_PROPERTY}}, ["p1", "p2"])])
def test_class_definition_file_validator_get_defined_properties(
        file_content: dict, expected: bool):
    """This method tests ClassDefinitionFile validator works."""
    validator = ClassDefinitionFile(
        file_content, "", "Class Definition file validation failed")
    assert validator.get_defined_properties() == expected


@pytest.mark.parametrize(
    "version_folder, messages, expected",
    [("./tests/data/v12", [], True),
     ("./tests/data/v6",
      ["File doesn't exist",
       "File format validation failed",
       "File extension validation failed"], False),
     ("./tests/data/v4",
      ["Some properties are not defined in ClassDefinitions",
       "Class and Property names validation failed",
       "Labels validation failed",
       "Class and Property names validation failed",
       "Some properties are not defined in ClassDefinitions",
       "Properties inheritance validation failed",
       "Vocabulary reference missing",
       "Class definition reference missing",
       "Field should not be a list",
       "Required attributes for Property missing",
       "Required attributes for SupportedAttribute missing",
       "'data' (dli:SupportedAttribute): 'dli:title' is not a string"], False),
     ("./tests/data/v5",
      ["Properties inheritance validation failed",
       "Attribute type from ontology file and Vocabulary file differ",
       "Attribute 'dli:required' value from ontology file and "
       "ClassDefinitions file differ",
       "Classes and properties are not defined in the ontology file",
       "Class name is not the same with file name",
       "The 'dli:required' attribute value is false for subproperty but true"
       " for the base property",
       "Type file missing"], False)
     ])
def test_all_files_validator(version_folder: str, messages: List[str],
                             expected: bool):
    """Test AllFiles validator."""
    Structure.read_structure()
    Structure.set_root_folder(version_folder)
    add_prefixes("dli")

    Ontology.ontology_name = Structure.structure[ONTOLOGY]
    Ontology.read_ontology_file(version_folder)
    Ontology.preprocess()


    with LogCapture() as logs:
        assert AllFiles(
            version_folder, "Files validation failed").validate() == expected
        for message in messages:
            assert message in str(logs)
