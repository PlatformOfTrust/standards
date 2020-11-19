"""This module has a class that validates that all properties are implemented
in all the classes from the domain.
"""
from utils.constants import IS_IN, SHOULD_BE_IN
from utils.ontology import Ontology
from utils.property import Property

from validators.validator import Validator


class TotalDomain(Validator):
    """This class has a method that validates that every property is in all the
    classes from the domain.
    """

    def validate(self) -> bool:
        """This method validates that every property is in all the classes from
        the domain.
        """
        valid_property_apparitions = True

        for _property in Property.property_apparitions:
            for item in Property.property_apparitions[_property][SHOULD_BE_IN]:
                if (item not in Property.property_apparitions[_property][IS_IN]
                        and item.startswith(Ontology.ontology_name)):
                    self.write_debug_message(
                        f"Property '{_property}' is not defined in '{item}'"
                        " class")
                    valid_property_apparitions = False

        if not valid_property_apparitions:
            self.write_validation_message()

        return valid_property_apparitions
