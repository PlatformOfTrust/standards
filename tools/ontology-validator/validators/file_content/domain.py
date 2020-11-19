"""This module has a class that validates that the class is in the domain of
all properties.
"""
from typing import List

from utils.constants import DOMAIN
from utils.property import Property
from utils.validation import is_property

from validators.file_content.file_content import FileContentValidator


class Domain(FileContentValidator):
    """This class has a method validate that validates that the class is in the
    domain of all properties.
    """

    def __init__(self, file_content: dict, class_name: str,
                 properties: List[str], validation_message: str):
        super().__init__(file_content, validation_message)
        self.properties = properties
        self.class_name = class_name

    def validate(self) -> bool:
        """Validates that the class is in the domain of all properties (if not
        derived) Property.property_apparitions has all the classes that contain
        a property and which classes should contain it.
        """

        json_content = self.file_content
        valid_domain = True

        for item in json_content:
            if is_property(json_content[item]):
                _property = json_content[item]

                domain = {}
                if DOMAIN in _property:
                    domain = _property[DOMAIN]

                if self.class_name in domain:
                    Property.add_class_to_property(item, self.class_name,
                                                   domain)
                elif item not in self.properties:
                    self.write_debug_message(
                        f"Class name ({self.class_name}) is not in the "
                        f"domain of '{item}' property")
                    valid_domain = False

        if not valid_domain:
            self.write_validation_message()

        return valid_domain
