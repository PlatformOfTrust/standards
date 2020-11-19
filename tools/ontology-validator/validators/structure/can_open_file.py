"""This module has a class that validates that you can read the content of a
file.
"""
from validators.structure.structure import StructureValidator


class CanOpenFile(StructureValidator):
    """This class has a method that validates that you can read the content of
    a file.
    """
    def __init__(self, file_path: str, validation_message: str):
        super().__init__(file_path, validation_message)

    def validate(self) -> bool:
        """Validates that you can read the content of the file."""
        file_can_be_opened = False
        try:
            with open(self.path) as file:
                file.read()
                file_can_be_opened = True
        except IOError:
            self.write_debug_message("This file could not be read")

        if not file_can_be_opened:
            self.write_validation_message()

        return file_can_be_opened
