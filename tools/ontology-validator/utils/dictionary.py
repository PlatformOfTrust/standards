"""This module has a class Dictionary used for validating words."""
import json
from typing import List

import enchant

import requests

from utils.constants import ACCEPTED_WORDS_SPELL_CHECK, CACHED_WORDS_FILE, WORD
from utils.json import read_json_file
from utils.structure import Structure


class Dictionary:
    """This class is used for validating words."""
    dictionary = enchant.Dict("EN-US")
    cached_words: dict = {}
    exceptions: List[str] = []

    @staticmethod
    def check_word(word: str) -> bool:
        """Receives a word and validates if is a correct word. A word is
        correct if either:

        - is empty
        - is uppercase (is an abbreviation)
        - is in accepted words list
        - is a correct english word
        - is compound by multiple correct words (joined by - or /)
        """
        is_correct = False
        is_correct |= (word == "")
        is_correct |= word.isupper()

        word = word.lower()

        if not Dictionary.exceptions:
            Dictionary.exceptions = Structure.\
                structure[ACCEPTED_WORDS_SPELL_CHECK]

        is_correct |= (word.lower() in Dictionary.exceptions)

        if not is_correct:
            is_correct |= Dictionary.dictionary.check(word)

        if not is_correct:
            is_correct |= Dictionary.call_api_for_word(word)

        if is_correct:
            return True

        component_words = []
        separators = ["-", "/"]

        for separator in separators:
            if word.find(separator) != -1:
                component_words = word.split(separator)
                break

        if not component_words:
            return False

        for component_word in component_words:
            if not Dictionary.check_word(component_word):
                return False

        return True

    @staticmethod
    def write_cached_words():
        """This method writes the cached words in a file."""
        if not Dictionary.cached_words:
            return

        with open(CACHED_WORDS_FILE, "w") as file:
            file.write(json.dumps(Dictionary.cached_words,
                                  sort_keys=True, indent=4))

    @staticmethod
    def read_cached_words():
        """Loads the words already searched with the API."""
        Dictionary.cached_words = read_json_file(CACHED_WORDS_FILE)

    @staticmethod
    def call_api_for_word(word: str) -> bool:
        """If the word is not already checked and cached, this function calls
        an API to validate a word."""
        if Dictionary.cached_words == {}:
            Dictionary.read_cached_words()

        if word in Dictionary.cached_words:
            return Dictionary.cached_words[word]

        url = f"https://api.datamuse.com/words?sp={word}"
        response = requests.get(url).json()

        for item in response:
            if item[WORD] == word:
                Dictionary.cached_words[word] = True
                return True

        Dictionary.cached_words[word] = False
        return False
