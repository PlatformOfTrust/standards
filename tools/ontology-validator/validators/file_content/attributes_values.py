"""This module has a class that validates that the property attributes values
defined in ontology file are the same with the attributes values defined in the
files from Vocabulary and ClassDefinitions.
"""
from utils.constants import CLASS_DEFINITIONS_FOLDER, \
    PREFIXED, REQUIRED, SUPP_ATTRIBUTE, SUPP_CLASS, VOCAB_FOLDER,\
    _ID, _TYPE
from utils.ontology import Ontology
from utils.validation import is_property

from validators.file_content.file_content import FileContentValidator


class AttributesValues(FileContentValidator):
    """This class has a method validate that validates that the property
    attributes values defined in ontology file are the same with the attributes
    values defined in the files from Vocabulary and ClassDefinitions.
    """

    def __init__(self, file_content: dict,
                 path: str, validation_message: str):
        super().__init__(file_content, validation_message)
        self.path = path

    def validate(self) -> bool:
        """Validates that the properties attribute the ontology file are the
        same with those from Vocabulary and ClassDefinitions:

        - @type from Vocabulary files
        - dli:required from ClassDefinitions files
        """
        valid_properties = True
        if VOCAB_FOLDER in self.path:
            valid_properties = self.check_type()

        if CLASS_DEFINITIONS_FOLDER in self.path:
            valid_properties = self.check_required()

        if not valid_properties:
            self.write_validation_message()
            return False

        return True

    def check_type(self):
        """Validates that ontology definitions for @type are the same with
        those from Vocabulary file.
        """
        valid_properties = True
        for item in self.file_content:
            if not is_property(self.file_content[item]):
                continue

            definition = Ontology.get_definition(self.file_content[item][_ID])

            if definition[_TYPE] != self.file_content[item][_TYPE]:
                self.write_debug_message(
                    f"The attribute '@type' of the '{item}' property in "
                    f"Vocabulary folder is '{self.file_content[item][_TYPE]}'"
                    f" and in ontology file is '{definition[_TYPE]}'")

                valid_properties = False

        return valid_properties

    def check_required(self):
        """Validates that ontology definitions for dli:required are the same with
        those from ClassDefinitions file.
        """
        valid_properties = True
        for item in self.file_content[PREFIXED[SUPP_CLASS]][
                PREFIXED[SUPP_ATTRIBUTE]]:
            prop = self.file_content[PREFIXED[SUPP_CLASS]][
                PREFIXED[SUPP_ATTRIBUTE]][item]

            definition = Ontology.get_definition(prop[_ID])
            if definition[PREFIXED[REQUIRED]] != prop[PREFIXED[REQUIRED]]:
                self.write_debug_message(
                    f"The attribute 'dli:required' of the '{item}' property "
                    "in ClassDefinitions folder is "
                    f"'{prop[PREFIXED[REQUIRED]]}' and in ontology "
                    f"file is '{definition[PREFIXED[REQUIRED]]}'")

                valid_properties = False

        return valid_properties
