"""This module contains functions that use json objects."""
import json
import logging
from typing import List


def find_labels_by_name(json_content: dict, label_name: str) -> List[dict]:
    """Returns the values of all attributes with name label_name."""
    labels = []

    if isinstance(json_content, dict):
        for field in json_content:
            if field == label_name:
                labels.append(json_content[field])
            labels.extend(find_labels_by_name(json_content[field], label_name))
    elif isinstance(json_content, list):
        for item in json_content:
            labels.extend(find_labels_by_name(item, label_name))

    return labels


def search_content_by_root(json_content: dict, root: str) -> List[dict]:
    """ returns all keys and values that begins with root
    Attention: root must end with ":" """

    matches = []

    if isinstance(json_content, dict):
        for field in json_content:
            if field.startswith(root):
                matches.append(field)
            matches.extend(search_content_by_root(json_content[field], root))
    elif isinstance(json_content, list):
        for item in json_content:
            matches.extend(search_content_by_root(item, root))
    elif isinstance(json_content, str) and json_content.startswith(root):
        matches.append(json_content)

    return matches


def read_json_file(path: str) -> dict:
    """Reads a json file and returns content."""
    try:
        with open(path) as file:
            file_contents = file.read()
            json_content = json.loads(file_contents)

            return json_content
    except (IOError, json.decoder.JSONDecodeError):
        logging.debug("%s: file could not be read as a json file", path)

    return {}


def missing_required_attributes(item: dict, required_attributes: List[str])\
        -> bool:
    """Validates that an object has the required attributes."""
    missing_attributes = []
    for attribute in required_attributes:
        if attribute not in item:
            missing_attributes.append(attribute)

    return missing_attributes
