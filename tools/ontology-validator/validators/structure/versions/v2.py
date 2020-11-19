"""This module has a class that validates the files and folders structure for
version 2.
"""
from pathlib import Path

from utils.constants import ALL_JSONLD, CLASS_DEFINITIONS_FOLDER,\
    CONTEXT_FOLDER, IDENTITY, LINK, ONTOLOGY_FOLDER, VOCAB_FOLDER
from utils.validation import call_validators

from validators.structure.folder_content import FolderContent
from validators.structure.structure import StructureValidator
from validators.structure.version_folder_exists import VersionFolderExists


class StructureValidatorV2(StructureValidator):
    """This class has a method validate that validates the files and folders
    structure for version 2.
    """

    def __init__(self, path: str, validation_message: str):
        super().__init__(path, validation_message)

    def validate(self) -> bool:
        """validation for version 2 folder structure."""
        validators = [
            VersionFolderExists(self.path, "Version folder doesn\'t exist"),
            FolderContent(self.path, [".DS_Store", ".gitkeep"],
                          [CLASS_DEFINITIONS_FOLDER, CONTEXT_FOLDER,
                           ONTOLOGY_FOLDER, VOCAB_FOLDER, "Schema"],
                          "Structure validation failed"),
            FolderContent(str(Path(self.path) / CONTEXT_FOLDER), [],
                          [IDENTITY, LINK], "Structure validation failed"),
            FolderContent(str(Path(self.path) / ONTOLOGY_FOLDER),
                          [ALL_JSONLD, "pot.obda", "pot.owl",
                           "pot.properties"], [],
                          "Structure validation failed")]

        return call_validators(validators, True)
