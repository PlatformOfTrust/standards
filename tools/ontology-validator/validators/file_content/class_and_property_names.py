"""This module has a class that validates that all property names are in camel
case and all class names are in pascal case.
"""
from utils.constants import _ID
from utils.spell_check import is_valid_camel_case, is_valid_pascal_case
from utils.validation import is_class, is_property

from validators.file_content.file_content import FileContentValidator


class ClassAndPropertyNames(FileContentValidator):
    """This class has a method validate that validates that all property names
    are in camel case and all class names are in pascal case.
    """

    def __init__(self, file_content: dict, validation_message: str):
        super().__init__(file_content, validation_message)

    def validate(self) -> bool:
        """Validates that all property names are in camel case and all class
        names are in pascal case.
        """
        json_content = self.file_content

        valid_naming = True
        for item in json_content:
            if _ID in json_content[item]:
                name = json_content[item][_ID].split(":")[-1].split("/")[-1]

                if is_property(json_content[item]):
                    if not is_valid_camel_case(name):
                        valid_naming = False
                        self.write_debug_message(
                            f"Property Name: '{name}' should be camel case")
                elif is_class(json_content[item]):
                    if not is_valid_pascal_case(name):
                        valid_naming = False
                        self.write_debug_message(
                            f"Class Name: '{name}' should be pascal case")
        if not valid_naming:
            self.write_validation_message()

        return valid_naming
