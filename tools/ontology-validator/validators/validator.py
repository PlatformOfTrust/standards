"""This module has a class inherited by more specific validators."""
import logging
from abc import ABC, abstractmethod

from utils.structure import Structure


class Validator(ABC):
    """Base class inherited by more specific validators."""

    def __init__(self, validation_message: str):
        self.validation_message = validation_message

    @abstractmethod
    def validate(self) -> bool:
        """Each class implements this method with a specific validation."""

    def write_validation_message(self, message: str = ""):
        """Writes validation message."""
        if message != "":
            message = message.replace(Structure.repository_folder, "")
            logging.info("%s", message)
        else:
            self.validation_message = self.validation_message.replace(
                Structure.repository_folder, "")
            logging.info("%s", self.validation_message)
        logging.debug("")

    @staticmethod
    def write_debug_message(message: str):
        """Writes debug message if needded."""
        logging.debug("%s", message)
