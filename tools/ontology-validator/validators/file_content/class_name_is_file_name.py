"""This module has a class that validates that the class name is the same with
the filename.
"""
from pathlib import Path

from utils.constants import CLASS_DEFINITIONS_FOLDER, PREFIXED, SUPP_CLASS,\
    VOCAB_FOLDER, _ID
from utils.validation import is_class

from validators.file_content.file_content import FileContentValidator


class ClassNameIsFileName(FileContentValidator):
    """This class has a method validate that validates that the class name is
    the same with the filename.
    """

    def __init__(self, file_content: dict, path: str,
                 validation_message: str):
        super().__init__(file_content, validation_message)

        self.path = path

    def validate(self) -> bool:
        """Validates that the class name is the same with the filename."""
        file_name = Path(self.path).name.split(".")[0]

        if VOCAB_FOLDER in self.path:
            class_name = ""
            for item in self.file_content:
                if is_class(self.file_content[item]):
                    class_name = self.file_content[item][_ID]
                    class_name = class_name.split(":")[-1].split("/")[-1]
                    break

            if class_name != file_name:
                self.write_validation_message()
                file_name = Path(self.path).name
                self.write_debug_message(
                    f"File name should be '{class_name}.jsonld' but is "
                    f"'{file_name}'")

                return False
            return True

        if CLASS_DEFINITIONS_FOLDER in self.path:
            class_name = self.file_content[PREFIXED[SUPP_CLASS]][_ID]
            class_name = class_name.split(":")[-1].split("/")[-1]

            if class_name != file_name:
                self.write_validation_message()
                file_name = Path(self.path).name
                self.write_debug_message(
                    f"File name should be '{class_name}.jsonld' but is "
                    f"'{file_name}'")

                return False

            return True

        return False
