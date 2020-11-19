"""This module contains constants used in this project"""

RESOURCES_FILE = "./resources.json"
CACHED_WORDS_FILE = "./cached words.json"

EN_US = "en-us"
FI_FI = "fi-fi"
JSONLD_EXT = ".jsonld"
ALL_JSONLD = "*.jsonld"
ONTOLOGY = "ontology"

ONTOLOGY_FOLDER = "Ontology"
VOCAB_FOLDER = "Vocabulary"
CLASS_DEFINITIONS_FOLDER = "ClassDefinitions"
CONTEXT_FOLDER = "Context"
IDENTITY = "Identity"
LINK = "Link"

SUPPORTED_ATTRIBUTE = "SupportedAttribute"

RDFS_LABEL = "rdfs:label"
COMMENT = "rdfs:comment"
TITLE = "dli:title"
DESCRIPTION = "dli:description"
RDFS_SUB_CLASS_OF = "rdfs:subClassOf"
SUB_CLASS_OF = "subClassOf"
SUB_PROPERTY_OF = "subPropertyOf"

_CONTEXT = "@context"
_VOCAB = "@vocab"
_CLASS_DEFINITION = "@classDefinition"
_ID = "@id"
_TYPE = "@type"
_PREFIX = "@prefix"
REQUIRED = "required"

PROPERTY = "Property"
RDF_PROPERTY = "rdf:Property"
CLASS = "Class"
POT_CLASS = "pot:Class"

DOMAIN = "domain"
SUCCESS = "success"
PARENT = "parent"
NAME = "name"
TYPE = "type"
WORD = "word"
LABEL = "label"

SHOULD_BE_IN = "shouldBeIn"
IS_IN = "isIn"
FIELDS_WITH_TYPE_LIST = "fieldsWithTypeList"
ACCEPTED_WORDS_SPELL_CHECK = "acceptedWordsSpellCheck"
FIELDS_TYPES_RESTRICTIONS = "fieldsTypesRestrictions"
REQUIRED_ATTRIBUTES = "requiredAttributes"


TEST_FILE_REFERENCES_PATH = "tests\\data\\Files\\test_file_references\\"
SUPP_ATTRIBUTE = "Supported Attribute"
SUPP_CLASS = "Supported Class"


PREFIXED = {
    SUPP_CLASS: ":supportedClass",
    SUPP_ATTRIBUTE: ":supportedAttribute",
    REQUIRED: ":required",
}


def add_prefixes(prefix: str):
    """Add the prefix from config file."""
    for const in PREFIXED:
        if PREFIXED[const].startswith(":"):
            PREFIXED[const] = prefix + PREFIXED[const]
