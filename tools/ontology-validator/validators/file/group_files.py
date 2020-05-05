"""This module has a class that validates a group of files formed by the file
from Context folder, the coresponding files in ClassDefinitions and Vocabulary
and their derived classes.
"""
from pathlib import Path
from typing import List, Optional

from utils.constants import JSONLD_EXT
from utils.json import read_json_file

from validators.file.class_definition import ClassDefinitionFile
from validators.file.common import FileValidatorCommon
from validators.file.context import ContextFile
from validators.file.vocabulary import VocabularyFile
from validators.file_content.properties_defined import PropertiesDefined
from validators.structure.structure import StructureValidator


class GroupFiles(StructureValidator):
    """This class has a method validate that validates a group of files formed
    by the file from Context folder, the coresponding files in ClassDefinitions
    and Vocabulary and their derived classes.
    """
    def __init__(self, path: str, properties: List[str],
                 validation_message: str):
        super().__init__(path, validation_message)
        self.properties = properties

    def validate(self) -> bool:
        """Calls validation for the file from Context, and corresponding files
        from ClassDefinitions and Vocabulary.

        Then checks if all properties from Context and Vocabulary are
        defined in ClassDefinition. After that, calls GroupFiles validator for
        derived classes.
        """
        valid_files = True

        context_validator = get_context_validator(self.path)
        if not context_validator:
            return False
        valid_files &= context_validator.validate()

        class_definition_file = context_validator.get_class_definition()
        class_definition_validator = get_class_definition_validator(
            class_definition_file)
        if not class_definition_validator:
            return False
        valid_files &= class_definition_validator.validate()

        vocabulary_file = class_definition_validator.get_vocabulary_file()
        vocabulary_validator = self.get_vocabulary_validator(
            vocabulary_file)
        if not vocabulary_validator:
            return False
        valid_files &= vocabulary_validator.validate()

        defined_properties = class_definition_validator.\
            get_defined_properties()
        context_properties = context_validator.get_properties()
        vocabulary_properties = vocabulary_validator.get_properties()

        valid_files &= self.validate_properties(
            vocabulary_properties, context_properties, defined_properties,
            vocabulary_file)

        derived_classes = vocabulary_validator.get_derived_classes()
        valid_files &= self.validate_derived_classes(
            derived_classes, vocabulary_properties)

        return valid_files

    def get_vocabulary_validator(self, path: str) -> Optional[VocabularyFile]:
        """Returns a validator for this vocabulary file if the file passes
        validation, else returns None.
        """
        if path == "":
            return None

        if not validate_file(path):
            return None

        vocabulary_validator = VocabularyFile(
            read_json_file(path), path, self.properties,
            f"{path}: file validation failed")

        return vocabulary_validator

    def validate_properties(self, vocabulary_properties: List[str],
                            context_properties: List[str],
                            defined_properties: List[str],
                            vocabulary_file: str) -> bool:
        """This function calls validators that validate that all properties
        from Vocabulary and Context are in ClassDefinitions.
        """
        valid_properties = True
        if not PropertiesDefined(
                context_properties, defined_properties,
                f"{self.path}: Some properties are not defined in "
                "ClassDefinitions").validate():
            self.write_validation_message(
                f"{self.path}: file validation failed")

            valid_properties = False

        if not PropertiesDefined(
                vocabulary_properties, defined_properties,
                f"{vocabulary_file}: Some properties are not defined in"
                " ClassDefinitions").validate():
            self.write_validation_message(
                f"{vocabulary_file}: file validation failed")

            valid_properties = False

        return valid_properties

    def validate_derived_classes(self, derived_classes: List[str],
                                 vocabulary_properties: List[str]) -> bool:
        """This function calls group validation for derived classes."""
        valid_file = True

        if derived_classes:
            folder_name = Path(self.path.replace(JSONLD_EXT, ""))

            for derived_class in derived_classes:
                new_path = folder_name / (derived_class + JSONLD_EXT)
                valid_file &= GroupFiles(
                    str(new_path), vocabulary_properties.copy(),
                    self.validation_message).validate()

        return valid_file


def validate_file(path: str) -> bool:
    """Validates that the file exists in correct format."""
    valid_file = FileValidatorCommon(path, "").validate()

    if not valid_file:
        return False

    return True


def get_context_validator(path: str) -> Optional[ContextFile]:
    """Returns a validator for this context file if the file passes
    validation, else returns None.
    """
    if not validate_file(path):
        return None

    context_validator = ContextFile(read_json_file(path), path,
                                    f"{path}: file validation failed")

    return context_validator


def get_class_definition_validator(path: str) -> \
        Optional[ClassDefinitionFile]:
    """Returns a validator for this class definition file if the file
    passes validation, else returns None.
    """
    if path == "":
        return None

    if not validate_file(path):
        return None

    class_definition_validator = ClassDefinitionFile(
        read_json_file(path), path, f"{path}: file validation failed")

    return class_definition_validator
