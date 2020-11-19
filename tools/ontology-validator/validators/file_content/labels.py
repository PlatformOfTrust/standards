"""This module contains a class that validates dli:title, dli:description,
rdfs:label, rdfs:comment attributes.
"""
from typing import List

from utils.constants import CLASS_DEFINITIONS_FOLDER, COMMENT, DESCRIPTION,\
    EN_US, FI_FI, LABEL, NAME, PREFIXED, RDFS_LABEL, SUPP_ATTRIBUTE,\
    SUPP_CLASS, TITLE, TYPE, VOCAB_FOLDER, _CONTEXT, _TYPE
from utils.spell_check import spell_check
from utils.structure import Structure

from validators.file_content.file_content import FileContentValidator


class Labels(FileContentValidator):
    """This class contains a method validate that validates dli:title,
    dli:description, rdfs:label, rdfs:comment attributes.
    """

    def __init__(self, file_content: dict, folder: str,
                 validation_message: str):
        super().__init__(file_content, validation_message)
        self.folder = folder

    def validate(self) -> bool:
        """English spelling check for all labels. Validate that
        dli:description, rdfs:label and rdfs:comment have at least "us-en" and
        "fi-fi" languages specified.
        """
        valid_labels = True

        if self.folder == VOCAB_FOLDER:
            valid_labels = self.validate_vocabulary_file_labels()

        if self.folder == CLASS_DEFINITIONS_FOLDER:
            valid_labels &= self.validate_class_definitions_file_labels()

        if not valid_labels:
            self.write_validation_message()

        return valid_labels

    def validate_vocabulary_file_labels(self):
        """Validate the labels from a vocabulary type file."""
        valid_labels = True
        vocab_labels = [RDFS_LABEL, COMMENT, DESCRIPTION, TITLE]
        for label in vocab_labels:
            all_labels = self.find_labels_in_vocabulary_file(label)

            for current_label in all_labels:
                if not self.check_label(label, current_label):
                    valid_labels = False

        return valid_labels

    def find_labels_in_vocabulary_file(self, label: str) -> List[dict]:
        """Find all apartions of the label in vocabulary file."""
        all_apparitions = []
        for item in self.file_content:
            if item != _CONTEXT and label in self.file_content[item]:
                apparition = {}
                apparition[NAME] = item
                apparition[TYPE] = self.file_content[item][_TYPE]
                apparition[LABEL] = self.file_content[item][label]
                all_apparitions.append(apparition)

        return all_apparitions

    def validate_class_definitions_file_labels(self):
        """Validate the labels from a class definitions type file."""
        valid_labels = True

        titles = self.find_labels_in_class_definitions_file(TITLE)
        for title in titles:
            valid_labels &= self.check_title(title)

        labels = [RDFS_LABEL, DESCRIPTION, COMMENT]
        for label in labels:
            all_labels = self.find_labels_in_class_definitions_file(label)

            for current_label in all_labels:
                valid_labels &= self.check_label(label, current_label)

        return valid_labels

    def find_labels_in_class_definitions_file(self, label: str) -> List[dict]:
        """Find all apartions of label in class definitions file."""
        all_apparitions = []

        if label in self.file_content[PREFIXED[SUPP_CLASS]]:
            apparition = {}
            apparition[NAME] = PREFIXED[SUPP_CLASS]
            apparition[TYPE] = self.file_content[PREFIXED[SUPP_CLASS]][_TYPE]
            apparition[LABEL] = self.file_content[PREFIXED[SUPP_CLASS]][label]
            all_apparitions.append(apparition)

        properties =\
            self.file_content[PREFIXED[SUPP_CLASS]][PREFIXED[SUPP_ATTRIBUTE]]

        for prop in properties:
            if label in properties[prop]:
                apparition = {}
                apparition[NAME] = prop
                apparition[TYPE] = properties[prop][_TYPE]
                apparition[LABEL] = properties[prop][label]
                all_apparitions.append(apparition)

        return all_apparitions

    def check_label(self, label_name: str, apparition: dict) -> bool:
        """Validates that the label has defined "en-us" and "fi-fi" languages
        and the spelling check validation passes.
        """
        label = apparition[LABEL]
        if not isinstance(label, dict):
            return False

        valid_label = True
        if EN_US not in label:
            self.write_debug_message(
                f"'{EN_US}' language missing for '{label_name}' in "
                f"'{apparition[NAME]}' ({apparition[TYPE]})")
            valid_label = False

        if Structure.validate_fifi and FI_FI not in label:
            self.write_debug_message(
                f"'{FI_FI}' language missing for '{label_name}' in "
                f"'{apparition[NAME]}' ({apparition[TYPE]})")
            valid_label = False

        for language in label:
            if not isinstance(label[language], str):
                self.write_debug_message(
                    f"'{apparition[NAME]}' ({apparition[TYPE]}): "
                    f"'{label_name}', language '{language}' is not a string\n")

                valid_label = False
                continue

            wrong_words = spell_check(label[language], language)

            if not wrong_words:
                continue

            wrong_words = ", ".join(wrong_words)
            debug_message = f"'{apparition[NAME]}' ({apparition[TYPE]}): " +\
                f"Spell check for '{label_name}', language '{language}': " +\
                f"'{label[language]}' failed for: {wrong_words}"

            self.write_debug_message(debug_message)
            valid_label = False

        return valid_label

    def check_title(self, apparition):
        """Does spelling check for a title label."""
        if not isinstance(apparition[LABEL], str):
            self.write_debug_message(
                f"'{apparition[NAME]}' ({apparition[TYPE]}): '{TITLE}'"
                " is not a string\n")

            return False

        wrong_words = spell_check(apparition[LABEL], EN_US)
        if not wrong_words:
            return True

        debug_message = f"'{apparition[NAME]}' ({apparition[TYPE]}): Spell " +\
            f"check for '{TITLE}': '{apparition[LABEL]}' failed\n" +\
            f"Wrong words: {wrong_words}\n"

        self.write_debug_message(debug_message)

        return False
