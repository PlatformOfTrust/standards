"""This method has a class that validates the content of a folder."""

import glob
from pathlib import Path
from typing import List

from validators.structure.structure import StructureValidator


class FolderContent(StructureValidator):
    """This class has a method validate that validates that the files and
    folders that should be in a folder are there.
    """

    def __init__(self, path: str, files: List[str], folders: List[str],
                 validation_message: str):
        super().__init__(path, validation_message)
        self.files = files
        self.folders = folders

    def validate(self) -> bool:
        """Validates that the files and folders that should be in the folder
        are there.
        """
        valid_content = True

        for file in self.files:
            match_files = glob.glob(str(Path(self.path) / file))

            if not match_files:
                valid_content = False
                self.write_debug_message(
                    f"{self.path}: {file} file does not exist")
            else:
                file_name = match_files[0]

                if not Path(file_name).is_file():
                    valid_content = False
                    self.write_debug_message(
                        f"{self.path}: {file_name} file does not exist")

        for folder in self.folders:
            match_folders = glob.glob(str(Path(self.path) / folder))

            if not match_folders:
                valid_content = False
                self.write_debug_message(
                    f"{self.path}: {folder} folder does not exist")
            else:
                folder_name = match_folders[0]
                if not Path(folder_name).is_dir():
                    valid_content = False
                    self.write_debug_message(
                        f"{self.path}: {file_name} folder does not exist")

        count = self.count_files_and_folders()

        if count > len(self.files) + len(self.folders):
            valid_content = False
            self.write_debug_message(
                f"{self.path}: Folder contains other files or folders")

        if not valid_content:
            self.write_validation_message()

        return valid_content

    def count_files_and_folders(self) -> int:
        """Returns how many files and folders are in the folder."""
        count = 0

        for _ in Path(self.path).iterdir():
            count += 1

        return count
