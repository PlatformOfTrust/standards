"""This module has test functions for validators defined in validators.file
module."""
import pytest
import responses
from utils.dictionary import Dictionary
from utils.constants import WORD


def mock_call_api_for_word(_: str) -> bool:
    """Mock for call_api_for_word."""
    return False


@pytest.mark.parametrize(
    "word, expected",
    [("", True),
     ("ABAC", True),
     ("iamaccepted", True),
     ("house", True),
     ("carrr", False)])
def test_dictionary_check_word(word: str, expected: bool):
    """Test Dictionary.check_word."""
    true_call_api_for_word = Dictionary.call_api_for_word
    Dictionary.call_api_for_word = mock_call_api_for_word
    Dictionary.exceptions.append("iamaccepted")
    assert Dictionary.check_word(word) == expected
    Dictionary.call_api_for_word = true_call_api_for_word


@responses.activate
def test_dictionary_cached_words():
    """Test Dictionary.cached_words."""
    responses.add(responses.GET,
                  "https://api.datamuse.com/words?sp=word",
                  json=[{WORD: WORD}], status=200)

    Dictionary.cached_words["house"] = True
    Dictionary.cached_words["houss"] = False

    assert Dictionary.call_api_for_word("word")
    assert Dictionary.call_api_for_word("word")
    assert Dictionary.call_api_for_word("house")
    assert not Dictionary.call_api_for_word("houss")

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url ==\
        "https://api.datamuse.com/words?sp=word"
    assert responses.calls[0].response.text == "[{\"word\": \"word\"}]"
