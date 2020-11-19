"""This module has a class that contains information about the structure of the
files and folders we validate."""
from utils.constants import RESOURCES_FILE
from utils.json import read_json_file


class Structure:
    """This class contains information about the structure of the files and
    folders we validate."""

    structure: dict = {}
    root_folder: str = ""
    verbose = False
    types_cache: dict = {}
    repository_folder: str = ""
    validate_fifi: bool = False
    spellcheck: bool = True

    @staticmethod
    def read_structure(path: str = RESOURCES_FILE):
        """Reads the structure file."""
        Structure.structure = read_json_file(path)

    @staticmethod
    def set_root_folder(root_folder: str):
        """Sets root folder."""
        Structure.root_folder = root_folder

    @staticmethod
    def set_repository_folder(repository_folder: str):
        """Sets repository folder."""
        Structure.repository_folder = repository_folder
