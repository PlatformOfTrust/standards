"""This module contains a class that validates that a file exists and has
correct format.
"""
from utils.validation import call_validators

from validators.structure.can_open_file import CanOpenFile
from validators.structure.extension import Extension
from validators.structure.file_exists import FileExists
from validators.structure.json_format import JsonFormat
from validators.structure.structure import StructureValidator


class FileValidatorCommon(StructureValidator):
    """This class contains a method validate that validates that a file exists
    and has correct format.
    """

    def __init__(self, path: str, validation_message: str):
        super().__init__(path, validation_message)

    def validate(self) -> bool:
        """Validates that the file exists and has correct format."""

        file_validators = [
            FileExists(self.path, f"{self.path}: File doesn't exist"),
            Extension(self.path, f"{self.path}:"
                      " File extension validation failed"),
            CanOpenFile(self.path, f"{self.path}: File can not be openned"),
            JsonFormat(self.path, f"{self.path}:"
                       " File format validation failed")]

        return call_validators(file_validators, True)
