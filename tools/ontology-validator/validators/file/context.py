"""This module has a class used that validates and parses files from Context
folder.
"""
from pathlib import Path
from typing import List

from utils.constants import CONTEXT_FOLDER, JSONLD_EXT, _CLASS_DEFINITION,\
    _CONTEXT, _PREFIX
from utils.structure import Structure
from utils.validation import call_validators

from validators.file_content.file_content import FileContentValidator
from validators.file_content.files_references import FilesReferences
from validators.file_content.list_field_type import ListFieldType


class ContextFile(FileContentValidator):
    """This class has methods used for validation and parsing files from
    Context folder.
    """

    def __init__(self, file_content: dict, path: str, validation_message: str):
        super().__init__(file_content, validation_message)
        self.path = path

    def validate(self) -> bool:
        """Validates Context files content."""

        content_validators = [
            ListFieldType(self.file_content, f"{self.path}:"
                          " Field should not be a list"),
            FilesReferences(self.file_content, CONTEXT_FOLDER,
                            f"{self.path}: ")]

        return call_validators(content_validators)

    def get_properties(self) -> List[str]:
        """Returns a list with all the properties from the file."""
        properties = []

        for item in self.file_content[_CONTEXT]:
            if (isinstance(self.file_content[_CONTEXT][item], dict) and
                    _PREFIX not in self.file_content[_CONTEXT][item]):
                properties.append(item)

        return properties

    def get_class_definition(self) -> str:
        """Returns the corresponding file from ClassDefinitions."""
        if _CLASS_DEFINITION not in self.file_content[_CONTEXT]:
            return ""

        relative_path = self.file_content[_CONTEXT][_CLASS_DEFINITION].\
            replace(Structure.structure["URL"], "")
        path = Path(Structure.root_folder) / Path(relative_path)
        class_definition = str(path) + JSONLD_EXT

        return class_definition
