"""This module has a class that validates the files and folders structure for
version 1.
"""
from pathlib import Path

from utils.constants import ALL_JSONLD, CLASS_DEFINITIONS_FOLDER,\
    CONTEXT_FOLDER, IDENTITY, LINK, ONTOLOGY_FOLDER, VOCAB_FOLDER
from utils.validation import call_validators

from validators.structure.folder_content import FolderContent
from validators.structure.structure import StructureValidator
from validators.structure.version_folder_exists import VersionFolderExists


class StructureValidatorV1(StructureValidator):
    """This class has a method validate that validates the files and folders
    structure for version 1.
    """

    def __init__(self, path: str, validation_message: str):
        super().__init__(path, validation_message)

    def validate(self) -> bool:
        """validation for version 1 folder structure."""
        validators = [
            VersionFolderExists(self.path, "Version folder doesn\'t exist"),
            FolderContent(self.path, ["Vocabulary.jsonld"],
                          [CLASS_DEFINITIONS_FOLDER, CONTEXT_FOLDER,
                           ONTOLOGY_FOLDER, VOCAB_FOLDER],
                          "Structure validation failed"),
            FolderContent(str(Path(self.path) / CONTEXT_FOLDER), [],
                          [IDENTITY, LINK], "Structure validation failed"),
            FolderContent(str(Path(self.path) / ONTOLOGY_FOLDER),
                          [ALL_JSONLD], [], "Structure validation failed")]

        return call_validators(validators, True)
