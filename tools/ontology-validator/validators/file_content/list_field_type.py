"""This module contains a class that validates that only the attributes
specified in resources.json are lists.
"""
from utils.constants import FIELDS_TYPES_RESTRICTIONS, FIELDS_WITH_TYPE_LIST
from utils.structure import Structure

from validators.file_content.file_content import FileContentValidator


class ListFieldType(FileContentValidator):
    """This class has a method validate that validates that only the attributes
    specified in resources.json are lists.
    """

    def __init__(self, file_content: dict, validation_message: str):
        super().__init__(file_content, validation_message)
        self.fields_with_type_list = Structure.\
            structure[FIELDS_TYPES_RESTRICTIONS][FIELDS_WITH_TYPE_LIST]

    def validate(self) -> bool:
        """Validates that only the attributes from fields_with_type_list are
        lists.
        """
        json_content = self.file_content
        valid_field_types = self.recursive_check(json_content)

        if not valid_field_types:
            self.write_validation_message()

        return valid_field_types

    def recursive_check(self, json_content: dict) -> bool:
        """Deep validation for all attributes."""
        check = True
        if isinstance(json_content, dict):
            for field in json_content:
                if isinstance(json_content[field], list):
                    if field not in self.fields_with_type_list:
                        self.write_debug_message(
                            f"Field: '{field}' should not be a list")
                        check = False
                if not self.recursive_check(json_content[field]):
                    check = False
        elif isinstance(json_content, list):
            for item in json_content:
                if not self.recursive_check(item):
                    check = False

        return check
