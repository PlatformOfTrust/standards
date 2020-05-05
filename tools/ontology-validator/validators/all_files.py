"""AllFiles class calls validations for all files."""
from pathlib import Path

from utils.constants import CONTEXT_FOLDER, IDENTITY, LINK
from utils.ontology import Ontology
from utils.validation import call_validators

from validators.file.common import FileValidatorCommon
from validators.file.group_files import GroupFiles
from validators.file_content.required_value_in_subproperties\
    import RequiredValueInSubproperties
from validators.structure.structure import StructureValidator


class AllFiles(StructureValidator):
    """This class has a method validate that calls validations for all
    files.
    """

    def __init__(self, path: str, validation_message: str):
        super().__init__(path, validation_message)

    def validate(self) -> bool:
        """Validates all files:
            - calls validation for all files in Context folder
            - calls ontology file validators
        """
        valid_files = True

        context_path = Path(self.path) / CONTEXT_FOLDER
        context_types = [IDENTITY, LINK]

        for context_type in context_types:
            context_type_path = context_path / context_type

            for item in context_type_path.iterdir():
                new_path = str(item)
                if item.is_file():
                    valid_files &= GroupFiles(
                        new_path, [],
                        f"{new_path}: File validation failed").validate()

        ontology_path = Ontology.get_ontology_file_path(self.path)
        ontology_validations = [
            FileValidatorCommon(ontology_path, ""),
            RequiredValueInSubproperties(
                "The 'dli:required' attribute value is false for subproperty"
                " but true for the base property")]

        if not call_validators(ontology_validations):
            self.write_validation_message(
                f"{ontology_path}: File validation failed")
            valid_files = False

        if not valid_files:
            self.write_validation_message()

        return valid_files
