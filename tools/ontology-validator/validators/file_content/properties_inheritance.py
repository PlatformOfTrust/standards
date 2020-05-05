"""This module has a class that validates that the class implements all the
inherited properties.
"""
from typing import List

from validators.file_content.file_content import FileContentValidator


class PropertiesInheritance(FileContentValidator):
    """This class has a method validate that validates that the class
    implements all the inherited properties.
    """

    def __init__(self, file_content: dict,
                 properties: List[str],
                 validation_message: str):
        super().__init__(file_content, validation_message)
        self.properties = properties

    def validate(self) -> bool:
        """Validates that the class implements all the inherited properties."""
        json_content = self.file_content

        valid_inheritance = True
        for _property in self.properties:
            if _property not in json_content:
                self.write_debug_message(
                    f"Property: '{_property}' is not inherited")
                valid_inheritance = False

        if not valid_inheritance:
            self.write_validation_message()

        return valid_inheritance
