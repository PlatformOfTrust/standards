"""This module contains mocks for unit testing."""
from typing import List
import pytest

from utils.constants import FI_FI


def camel_case_mock(string: str) -> bool:
    """Mock function for  utils.spell_check.is_valid_camel_case."""
    valid_camel_case = ["descriptionGeneral", "description"]
    if string in valid_camel_case:
        return True

    return False


def pascal_case_mock(string: str) -> bool:
    """Mock function for  utils.spell_check.is_valid_pascal_case."""
    valid_pascal_case = ["Building", "Car"]
    if string in valid_pascal_case:
        return True

    return False


@pytest.fixture
def mocked_pascal_and_camel_case(monkeypatch):
    """Mocks is_valid_pascal_case and is_valid_camel_case for testing
    ClassAndPropertyNames validator."""

    monkeypatch.setattr(
        "validators.file_content.class_and_property_names."
        "is_valid_pascal_case", pascal_case_mock)
    monkeypatch.setattr(
        "validators.file_content.class_and_property_names.is_valid_camel_case",
        camel_case_mock)


def spell_check_mock(string: str, language: str) -> List[str]:
    """Mock for spell_check."""
    if language == FI_FI:
        return []

    invalid_string = "WRONGGGG"
    if invalid_string in string:
        return [invalid_string]

    return []


@pytest.fixture
def mocked_spell_check(monkeypatch):
    """Mocks spell_check for Labels validator."""
    monkeypatch.setattr(
        "validators.file_content.labels.spell_check", spell_check_mock)
