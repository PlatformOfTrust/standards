"""This module has a class that validates and parses files from
ClassDefinitions folder.
"""
from pathlib import Path
from typing import List

from utils.constants import CLASS_DEFINITIONS_FOLDER, JSONLD_EXT, PREFIXED,\
    SUPPORTED_ATTRIBUTE, SUPP_ATTRIBUTE, SUPP_CLASS, _CONTEXT, _VOCAB
from utils.structure import Structure
from utils.validation import call_validators

from validators.file_content.attributes_values import AttributesValues
from validators.file_content.class_name_is_file_name import ClassNameIsFileName
from validators.file_content.file_content import FileContentValidator
from validators.file_content.files_references import FilesReferences
from validators.file_content.labels import Labels
from validators.file_content.list_field_type import ListFieldType
from validators.file_content.object_required_attributes\
    import ObjectRequiredAttributes
from validators.file_content.type_files import TypeFiles


class ClassDefinitionFile(FileContentValidator):
    """This class has methods used for validation and parsing files from
    ClassDefinitions folder.
    """

    def __init__(self, file_content: dict, path: str,
                 validation_message: str):
        super().__init__(file_content, validation_message)
        self.path = path

    def validate(self) -> bool:
        """Validates ClassDefinitions files content."""

        content_validators = [
            ListFieldType(
                self.file_content, f"{self.path}: Field should not be a list"),
            ObjectRequiredAttributes(
                self.file_content, SUPPORTED_ATTRIBUTE,
                f"{self.path}: Required attributes for"
                " SupportedAttribute missing"),
            ClassNameIsFileName(
                self.file_content, self.path,
                f"{self.path}: Class name is not the same with file name"),
            AttributesValues(
                self.file_content, self.path, f"{self.path}: "
                "Attribute 'dli:required'"
                " value from ontology file and ClassDefinitions file differ"),
            TypeFiles(self.file_content, f"{self.path}: Type file missing"),
            FilesReferences(self.file_content, CLASS_DEFINITIONS_FOLDER,
                            f"{self.path}: ")]

        if Structure.spellcheck:
            content_validators.append(Labels(self.file_content,
                                             CLASS_DEFINITIONS_FOLDER,
                                             f"{self.path}: Labels validation"
                                             " failed"))

        return call_validators(content_validators)

    def get_defined_properties(self) -> List[str]:
        """Returns a list with all properties defined in ClassDefinitions."""
        defined_properties = []

        if (PREFIXED[SUPP_CLASS] not in self.file_content or
                PREFIXED[SUPP_ATTRIBUTE] not in
                self.file_content[PREFIXED[SUPP_CLASS]]):
            return []

        for _property in self.\
                file_content[PREFIXED[SUPP_CLASS]][PREFIXED[SUPP_ATTRIBUTE]]:
            defined_properties.append(_property)

        return defined_properties

    def get_vocabulary_file(self) -> str:
        """Returns the corresponding file from Vocabulary."""
        if _VOCAB not in self.file_content[_CONTEXT]:
            return ""

        relative_path = self.file_content[_CONTEXT][_VOCAB].\
            replace(Structure.structure["URL"], "")
        path = Path(Structure.root_folder) / Path(relative_path)
        vocab_file = str(path) + JSONLD_EXT

        return vocab_file
