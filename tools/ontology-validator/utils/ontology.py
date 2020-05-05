"""This module has a class that contains information about the structure of the
files and folders we validate."""
from pathlib import Path

from utils.constants import JSONLD_EXT, NAME, ONTOLOGY_FOLDER, PARENT,\
    PREFIXED, REQUIRED, SUB_CLASS_OF, SUB_PROPERTY_OF, _ID, _TYPE
from utils.json import read_json_file


class Ontology:
    """This class contains information about the structure of the files and
    folders we validate."""

    file_content: dict = {}
    defines: dict = {}
    ontology_name: str = ""

    @staticmethod
    def preprocess():
        """Preprocess the ontology file to be easy to use."""
        if "defines" not in Ontology.file_content:
            return

        for item in Ontology.file_content["defines"]:
            Ontology.defines[item[_ID]] = {}
            define = Ontology.defines[item[_ID]]
            define[NAME] = item[_ID].split(":")[-1]
            define[_TYPE] = item[_TYPE]
            define[_ID] = item[_ID]

            if SUB_CLASS_OF in item:
                define[PARENT] = item[SUB_CLASS_OF]
            if SUB_PROPERTY_OF in item:
                define[PARENT] = item[SUB_PROPERTY_OF]

            if PREFIXED[REQUIRED] in item:
                define[PREFIXED[REQUIRED]] = item[PREFIXED[REQUIRED]]

    @staticmethod
    def has_class(item: str) -> bool:
        """Returns true if Ontology file has defined the class or property
        received as argument."""
        if item in Ontology.defines:
            return True
        return False

    @staticmethod
    def get_path_recursively(item: str) -> str:
        """Constructs the full path of a class or property."""
        if item not in Ontology.defines:
            return ""

        if PARENT not in Ontology.defines[item]:
            return f"{Ontology.defines[item][NAME]}/"

        parent = Ontology.get_path_recursively(Ontology.defines[item][PARENT])
        current = Ontology.defines[item][NAME]
        return f"{parent}{current}/"

    @staticmethod
    def get_ontology_file_path(root_path: str) -> str:
        """Returns the path to the ontology file."""
        file_name = Ontology.ontology_name + JSONLD_EXT
        path = Path(root_path) / ONTOLOGY_FOLDER / file_name
        return str(path)

    @staticmethod
    def read_ontology_file(root_path: str):
        """Reads the ontology file."""
        path = Ontology.get_ontology_file_path(root_path)
        Ontology.file_content = read_json_file(path)

    @staticmethod
    def get_definition(definition_id: str) -> dict:
        """Returns the ontology definition for a class or property."""
        first_part = definition_id.split(":")[0]
        last_part = definition_id.split(":")[-1].split("/")[-1]
        definition_id = f"{first_part}:{last_part}"

        if definition_id not in Ontology.defines:
            return {_TYPE: "", _ID: "", NAME: "", PARENT: "",
                    PREFIXED[REQUIRED]: ""}
        return Ontology.defines[definition_id]
