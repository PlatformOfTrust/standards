"""This module has a class used for properties implementation validation."""
from typing import List

from utils.constants import IS_IN, SHOULD_BE_IN


class Property:
    """This class is used to check if all the classes from the domain of a
    property implement that property."""
    property_apparitions: dict = {}

    @staticmethod
    def add_property(property_name: str, domain: List[str]):
        """This method adds a property."""
        Property.property_apparitions[property_name] = {}
        Property.property_apparitions[property_name][SHOULD_BE_IN] = domain
        Property.property_apparitions[property_name][IS_IN] = []

    @staticmethod
    def add_class_to_property(property_name: str, class_name: str,
                              domain: List[str]):
        """This method adds a class to the list of classes that implement the
        property."""
        if property_name not in Property.property_apparitions:
            Property.add_property(property_name, domain)

        Property.property_apparitions[property_name][IS_IN].append(class_name)
