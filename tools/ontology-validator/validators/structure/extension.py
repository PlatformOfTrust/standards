"""This module has a class that validates that a file has 'jsonld'
extension.
"""
from utils.constants import JSONLD_EXT

from validators.structure.structure import StructureValidator


class Extension(StructureValidator):
    """This class validates that the file has 'jsonld' extension."""

    def __init__(self, file_path: str, validation_message: str):
        super().__init__(file_path, validation_message)

    def validate(self) -> bool:
        """Validates that the file has 'jsonld' extension."""
        valid_extension = self.path.endswith(JSONLD_EXT)

        if not valid_extension:
            self.write_validation_message()

        return valid_extension
