"""This module contains functions used for spell checking."""
import re
import string
from typing import List

from utils.constants import EN_US
from utils.dictionary import Dictionary


def validate_words(words: List[str]) -> List[str]:
    """Validates all the words from the words list by calling the word checker
    from Dictionary."""
    wrong_words = []
    for word in words:
        if not Dictionary.check_word(word):
            wrong_words.append(word)

    return wrong_words


def is_valid_pascal_case(string_to_check: str) -> bool:
    """Checks if the received string is formed by correct words and is in
    pascal case format."""
    if not string_to_check[0].isupper():
        return False

    return is_valid_camel_case(string_to_check)


def is_valid_camel_case(string_to_check: str) -> bool:
    """Checks if the received string is formed by correct words and is in camel
    case format."""

    splitted = re.sub("([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1",
                                                      string_to_check)).split()

    return not validate_words(splitted)


def spell_check(string_to_check: str, language: str) -> List[str]:
    """Does spell spelling check for the received string.
    For now only english spell checker is available.
    """

    if language == EN_US:
        splitted = [word.strip(string.punctuation)
                    for word in string_to_check.split()]

        return validate_words(splitted)

    return []
