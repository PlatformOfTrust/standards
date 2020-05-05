"""This module has a class that validates that the version folder exists."""
from pathlib import Path

from validators.structure.structure import StructureValidator


class VersionFolderExists(StructureValidator):
    """This class validates that the root folder contains a folder with the
    version name.
    """

    def __init__(self, path: str, validation_message: str):
        super().__init__(path, validation_message)

    def validate(self) -> bool:
        """Validates that the root folder contains a folder with the version
        name.
        """
        folder_exists = Path(self.path).is_dir()
        if not folder_exists:
            self.write_validation_message()

        return folder_exists
