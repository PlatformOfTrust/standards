"""This module has a class that validates files from Vocabulary folder."""
from typing import List

from utils.constants import PROPERTY, RDFS_SUB_CLASS_OF, VOCAB_FOLDER, _ID
from utils.structure import Structure
from utils.validation import call_validators
from utils.validation import is_class, is_property

from validators.file_content.attributes_values import AttributesValues
from validators.file_content.class_and_property_names\
    import ClassAndPropertyNames
from validators.file_content.class_name_is_file_name import ClassNameIsFileName
from validators.file_content.domain import Domain
from validators.file_content.file_content import FileContentValidator
from validators.file_content.labels import Labels
from validators.file_content.list_field_type import ListFieldType
from validators.file_content.object_required_attributes\
    import ObjectRequiredAttributes
from validators.file_content.objects_defined import ObjectsDefined
from validators.file_content.properties_inheritance\
    import PropertiesInheritance
from validators.file_content.type_files import TypeFiles


class VocabularyFile(FileContentValidator):
    """This class validates files from Vocabulary folder."""

    def __init__(self, file_content: dict, path: str,
                 properties: List[str], validation_message: str):
        super().__init__(file_content, validation_message)
        self.properties = properties
        self.path = path

    def validate(self) -> bool:
        """Validates the file with all file validations for vocabulary
        files.
        """
        class_id = ""
        for item in self.file_content:
            if is_class(self.file_content[item]):
                class_id = self.file_content[item][_ID]
                break

        content_validators = [
            ClassAndPropertyNames(
                self.file_content,
                f"{self.path}: Class and Property names validation failed"),
            PropertiesInheritance(
                self.file_content, self.properties,
                f"{self.path}: Properties inheritance validation failed"),
            ListFieldType(self.file_content, f"{self.path}: Field should not"
                          " be a list"),
            ObjectRequiredAttributes(
                self.file_content, PROPERTY,
                f"{self.path}: Required attributes for Property missing"),
            Domain(self.file_content, class_id, self.properties,
                   f"{self.path}: Domain validation failed"),
            ObjectsDefined(
                self.file_content,
                f"{self.path}: Classes and properties are not defined"
                " in the ontology file"),
            ClassNameIsFileName(
                self.file_content, self.path,
                f"{self.path}: Class name is not the same with file name"),
            AttributesValues(
                self.file_content, self.path, f"{self.path}: Attribute type"
                " from ontology file and Vocabulary file differ"),
            TypeFiles(self.file_content, "Type file missing")]

        if Structure.spellcheck:
            content_validators.append(Labels(self.file_content, VOCAB_FOLDER,
                                             f"{self.path}: Labels validation "
                                             "failed"))

        return call_validators(content_validators)

    def get_properties(self) -> List[str]:
        """Returns a list with all the properties from the file."""
        properties = []

        for item in self.file_content:
            if is_property(self.file_content[item]):
                properties.append(item)

        return properties

    def get_derived_classes(self) -> List[str]:
        """Returns a list with all the subclasses of this class."""

        derived_classes = []
        for item in self.file_content:
            if RDFS_SUB_CLASS_OF in self.file_content[item]:
                derived_classes.append(item)
        return derived_classes
