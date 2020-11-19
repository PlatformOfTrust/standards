"""This module has the FileName class that validates that the filename
is correct.
"""
from pathlib import Path, PurePath

from utils.constants import ONTOLOGY_FOLDER
from utils.spell_check import is_valid_pascal_case

from validators.structure.structure import StructureValidator


class FileName(StructureValidator):
    """This class validates that a file file is in the Ontology folder or the
    name is Pascal Case format.
    """

    def __init__(self, file_path: str, validation_message: str):
        super().__init__(file_path, validation_message)

    def validate(self) -> bool:
        """Validates that the file is in the Ontology folder or the name is in
        Pascal Case format.
        """
        if PurePath(self.path).parts[-2] == ONTOLOGY_FOLDER:
            valid_name = True
        else:
            file_name = Path(self.path).stem

            valid_name = is_valid_pascal_case(file_name)

        if not valid_name:
            self.write_validation_message()

        return valid_name
