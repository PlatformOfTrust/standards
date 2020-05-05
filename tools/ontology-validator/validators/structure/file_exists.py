"""This module has a class that validates that a file exists."""
from validators.structure.structure import StructureValidator


class FileExists(StructureValidator):
    """This class has a validate method that validates that a file exists."""

    def __init__(self, file_path: str, validation_message: str):
        super().__init__(file_path, validation_message)

    def validate(self) -> bool:
        """Validates that the file exists."""
        file_exists = False
        try:
            with open(self.path):
                file_exists = True
        except IOError:
            self.write_debug_message("This file could not be opened")

        if not file_exists:
            self.write_validation_message()

        return file_exists
