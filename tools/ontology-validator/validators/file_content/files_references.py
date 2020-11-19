"""This module has a class that validates that:
    - ClassDefinitions files has a @vocab file reference
    - Context files has @vocab and @classDefinition files references
"""
from utils.constants import CLASS_DEFINITIONS_FOLDER, CONTEXT_FOLDER,\
    _CLASS_DEFINITION, _CONTEXT, _VOCAB

from validators.file_content.file_content import FileContentValidator


class FilesReferences(FileContentValidator):
    """This class has a method that validates that:
        - ClassDefinitions files has a @vocab file reference
        - Context files has @vocab and @classDefinition files references
    """

    def __init__(self, file_content: dict, folder: str,
                 validation_message: str = ""):
        super().__init__(file_content, validation_message)
        self.folder = folder

    def validate(self) -> bool:
        """Validates that:
            - ClassDefinitions files has a @vocab file reference
            - Context files has @vocab and @classDefinition files references
        """
        valid_references = True

        if CONTEXT_FOLDER == self.folder:
            if _CLASS_DEFINITION not in self.file_content[_CONTEXT]:
                self.write_validation_message(
                    self.validation_message +
                    "Class definition reference missing")
                valid_references = False

            if _VOCAB not in self.file_content[_CONTEXT]:
                self.write_validation_message(
                    self.validation_message + "Vocabulary reference missing")
                valid_references = False

        if CLASS_DEFINITIONS_FOLDER == self.folder:
            if _VOCAB not in self.file_content[_CONTEXT]:
                self.write_validation_message(
                    self.validation_message + "Vocabulary reference missing")
                valid_references = False

        return valid_references
