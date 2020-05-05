"""This module implements test functions for structure validators."""
from typing import List
import pytest

from validators.structure.version_folder_exists import VersionFolderExists
from validators.structure.folder_content import FolderContent
from validators.structure.versions.v1 import StructureValidatorV1
from validators.structure.extension import Extension
from validators.structure.json_format import JsonFormat
from utils.constants import CONTEXT_FOLDER, ONTOLOGY_FOLDER, VOCAB_FOLDER,\
    CLASS_DEFINITIONS_FOLDER, IDENTITY, LINK, ALL_JSONLD


@pytest.mark.parametrize("version_folder, expected",
                         [("./tests/data/v1", True),
                          ("./tests/data/v2", False)])
def test_version_folder_exists(version_folder: str, expected: bool):
    """Test VersionFolderExists."""
    assert VersionFolderExists(
        version_folder, "Version folder doesn't exist").validate() == expected


@pytest.mark.parametrize(
    "path, files, folders, expected",
    [("./tests/data/v1", ["Vocabulary.jsonld"], [
        CLASS_DEFINITIONS_FOLDER, CONTEXT_FOLDER, ONTOLOGY_FOLDER,
        VOCAB_FOLDER], True),
     ("./tests/data/v1/Context", [], [IDENTITY, LINK], True),
     ("./tests/data/v1/Ontology", [ALL_JSONLD], [], True),
     ("./tests/data/v3", ["Vocabulary.jsonld"], [
         CLASS_DEFINITIONS_FOLDER, CONTEXT_FOLDER, ONTOLOGY_FOLDER,
         VOCAB_FOLDER], False),
     ("./tests/data/v3/Context", [], [IDENTITY, LINK], False),
     ("./tests/data/v3/Ontology", [ALL_JSONLD], [], False)])
def test_folder_content(path: str, files: List[str], folders: List[str],
                        expected: bool):
    """Test FolderContent validator."""
    assert FolderContent(
        path, files, folders, "Structure validation failed"
    ).validate() == expected


@pytest.mark.parametrize("version_folder, expected",
                         [("./tests/data/v1", True),
                          ("./tests/data/v3", False)])
def test_structure_validator_version_1(version_folder: str, expected: bool):
    """Test StructureValidatorV1."""
    assert StructureValidatorV1(version_folder, "Structure validation failed"
                                ).validate() == expected


@pytest.mark.parametrize("path, expected",
                         [("./tests/data/v3/Ontology/pot.json", False),
                          ("./tests/data/v1/Vocabulary.jsonld", True)])
def test_extension(path: str, expected: bool):
    """Test Extension validator."""
    assert Extension(path, "Correct extension failed").validate() == expected


@pytest.mark.parametrize("path, expected",
                         [("./tests/data/Files/NotJson.jsonld", False),
                          ("./tests/data/Files/Building.jsonld", True)])
def test_json_format(path: str, expected: bool):
    """Test JsonFormat validator."""
    assert JsonFormat(path, "Json format failed").validate() == expected
