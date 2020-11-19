"""This module has a class that validates that a class implements all the
inherited properties.
"""
from typing import List

from validators.validator import Validator


class PropertiesDefined(Validator):
    """This class has a method validate that validates that the class
    implements all the inherited properties.
    """

    def __init__(self, all_properties: List[str],
                 defined_properties: List[str], validation_message: str):
        super().__init__(validation_message)
        self.all_properties = all_properties
        self.defined_properties = defined_properties

    def validate(self) -> bool:
        """Validates that the class implements all the inherited properties."""
        properties_defined = True

        for _property in self.all_properties:
            if _property not in self.defined_properties:
                properties_defined = False
                self.write_debug_message(
                    f"Property: '{_property}' is not defined")

        if not properties_defined:
            self.write_validation_message()

        return properties_defined
