"""This module has a class that validates that a file is a correct json
file.
"""

import json

from validators.structure.structure import StructureValidator


class JsonFormat(StructureValidator):
    """This class has a validate method that validates that a file is a correct
    json file.
    """

    def __init__(self, file_path: str, validation_message: str):
        super().__init__(file_path, validation_message)

    def validate(self) -> bool:
        """Validates that the file is a correct json file."""
        valid_json = False
        try:
            with open(self.path) as file:
                file_contents = file.read()
                json.loads(file_contents)

                valid_json = True
        except json.decoder.JSONDecodeError:
            self.write_debug_message("This file could not be parsed as json")

        if not valid_json:
            self.write_validation_message()

        return valid_json
