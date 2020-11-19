"""This module contains an abstract class inherited by the classes that
validate files content.
"""
from abc import abstractmethod

from validators.validator import Validator


class FileContentValidator(Validator):
    """This class is inherited by the classes that validate files content."""

    def __init__(self, file_content: dict, validation_message: str = ""):
        super().__init__(validation_message)
        self.file_content = file_content

    @abstractmethod
    def validate(self) -> bool:
        pass
