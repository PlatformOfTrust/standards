"""This module has a class that validates that URLs for types exists."""
from pathlib import Path

import requests

from utils.constants import JSONLD_EXT, _CONTEXT, _ID, _PREFIX, _TYPE
from utils.json import find_labels_by_name
from utils.structure import Structure

from validators.file_content.file_content import FileContentValidator


def is_valid_path_or_url(path: str) -> bool:
    """If path is an URL then validates that the response code is 200,
    else validates that the path exists locally.
    """
    if path in Structure.types_cache:
        return Structure.types_cache[path]

    if not path.startswith("http") and not path.startswith("https"):
        exists = Path(path).is_file()
        Structure.types_cache[path] = exists
        return exists

    request = requests.get(path)
    Structure.types_cache[path] = (request.status_code == 200)

    return Structure.types_cache[path]


class TypeFiles(FileContentValidator):
    """This class has a method that validates that URLs for types exists."""
    def __init__(self, file_content: dict, validation_message: str):
        super().__init__(file_content, validation_message)
        self.root_folder = Structure.root_folder
        self.url = Structure.structure["URL"]

    def validate(self) -> bool:
        """Validates that URLs for types exists."""
        if self.url[-1] != "/":
            self.url += "/"

        json_content = self.file_content

        prefix = {}
        for root in json_content[_CONTEXT]:
            if (isinstance(json_content[_CONTEXT][root], dict) and
                    _PREFIX in json_content[_CONTEXT][root] and
                    json_content[_CONTEXT][root][_PREFIX]):
                prefix[root] = json_content[_CONTEXT][root][_ID]

        valid_references = True
        invalid_references: dict = {}
        all_types = find_labels_by_name(json_content, _TYPE)
        for type_class in all_types:
            if not isinstance(type_class, str):
                continue

            root = type_class.split(":")[0]
            if root not in prefix:
                self.write_debug_message(f"Prefix '{root}' not defined")
                valid_references = False
                continue

            full_path = self.get_full_path(type_class, prefix[root])

            if not is_valid_path_or_url(full_path):
                invalid_references[full_path] = 1
                valid_references = False

        for invalid in invalid_references:
            self.write_debug_message(f"Url or path not found: {invalid}")

        if not valid_references:
            self.write_validation_message()

        return valid_references

    def get_full_path(self, path: str, root: str):
        """Relpaces the root part with actual root path."""
        name = path.split(":")[1]
        full_path = ""

        if root.find(self.url) == 0:
            root = root.replace(self.url, "")
            full_path = str(Path(self.root_folder) / Path(root) / name)
        else:
            if not root.endswith("/"):
                full_path = f"{root}/{name}"
            else:
                full_path = root + name

        if not full_path.endswith(JSONLD_EXT):
            full_path += JSONLD_EXT

        return full_path
