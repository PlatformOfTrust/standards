"""This module has a class that validates that objects have the required
attributes.
"""
from utils.constants import PREFIXED, PROPERTY, REQUIRED_ATTRIBUTES,\
    SUPPORTED_ATTRIBUTE, SUPP_ATTRIBUTE, SUPP_CLASS
from utils.json import missing_required_attributes
from utils.structure import Structure
from utils.validation import is_property

from validators.file_content.file_content import FileContentValidator


class ObjectRequiredAttributes(FileContentValidator):
    """This class has a method validate that validates that objects have the
    required attributes.
    """

    def __init__(self, file_content: dict, object_name: str,
                 validation_message: str):
        super().__init__(file_content, validation_message)
        self.required_attributes = \
            Structure.structure[REQUIRED_ATTRIBUTES][object_name]
        self.object_name = object_name

    def validate(self) -> bool:
        """Calls a function which validates that the object has the required
        attributes, depending on object name.
        """
        if self.object_name == PROPERTY:
            return self.check_properties()

        if self.object_name == SUPPORTED_ATTRIBUTE:
            return self.check_supported_attribute()

        return True

    def check_properties(self) -> bool:
        """Validates that properties have the required attributes."""
        json_content = self.file_content

        for item in json_content:
            if is_property(json_content[item]):
                _property = json_content[item]

                missing = missing_required_attributes(
                    _property, self.required_attributes)

                if missing:
                    missing = ", ".join(missing)
                    self.write_validation_message()
                    self.write_debug_message(
                        f"Property: '{item}' does not have the required"
                        f" attributes: {missing}")
                    return False
        return True

    def check_supported_attribute(self) -> bool:
        """Validates that SupportedAttributes have the required attributes."""
        json_content = self.file_content

        if (PREFIXED[SUPP_CLASS] in json_content and
                PREFIXED[SUPP_ATTRIBUTE] in
                json_content[PREFIXED[SUPP_CLASS]]):
            attributes =\
                json_content[PREFIXED[SUPP_CLASS]][PREFIXED[SUPP_ATTRIBUTE]]
            for item in attributes:
                _property = attributes[item]

                missing = missing_required_attributes(
                    _property, self.required_attributes)

                if missing:
                    missing = ", ".join(missing)
                    self.write_debug_message(
                        f"Supported Attribute: '{item}' does not"
                        f" have the required attributes: {missing}")
                    self.write_validation_message()
                    return False

        return True
