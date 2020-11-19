"""This module has a class that is inherited by validators that validate files
and folders structure.
"""
from abc import abstractmethod

from validators.validator import Validator


class StructureValidator(Validator):
    """This class is inherited by validators that validate files and folders
    structure.
    """

    def __init__(self, path: str, validation_message: str = ""):
        super().__init__(validation_message)
        self.path = path

    @abstractmethod
    def validate(self) -> bool:
        pass
