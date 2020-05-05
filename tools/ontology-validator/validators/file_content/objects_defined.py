"""This module has a class that validates that every class and property from
the file is defined in the ontology file.
"""
from utils.constants import _ID
from utils.ontology import Ontology
from utils.validation import is_class, is_property

from validators.file_content.file_content import FileContentValidator


def validate_id(property_id: str) -> bool:
    """This method validates if an id is defined in Ontology file."""
    first_part = property_id.split(":")[0]
    last_part = property_id.split(":")[-1].split("/")[-1]
    simple_id = f"{first_part}:{last_part}"

    ontology_id_path = Ontology.get_path_recursively(simple_id)
    property_name = property_id.split(":")[-1]
    return ontology_id_path == f"{property_name}/"


class ObjectsDefined(FileContentValidator):
    """This class has a method validate that validates that every class and
    property from the file is defined in the ontology file.
    """

    def __init__(self, file_content: dict, validation_message: str):
        super().__init__(file_content, validation_message)

    def validate(self) -> bool:
        """This method validates that every class and property from the file is
        defined in the ontology file.
        """

        json_content = self.file_content
        valid_file = True

        for item in json_content:
            if _ID in json_content[item]:
                if is_property(json_content[item]):
                    if not validate_id(json_content[item][_ID]):
                        valid_file = False
                        self.write_debug_message(
                            f"Property: '{json_content[item][_ID]}' is"
                            " not defined in ontology")
                elif is_class(json_content[item]):
                    if not Ontology.has_class(json_content[item][_ID]):
                        valid_file = False
                        self.write_debug_message(
                            f"Class: '{json_content[item][_ID]}' is not"
                            " defined in ontology")
        if not valid_file:
            self.write_validation_message()

        return valid_file
