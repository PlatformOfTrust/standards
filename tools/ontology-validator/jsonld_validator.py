"""This is the main module that receives a path to a version
folder and calls the validators for that version."""
import argparse
import logging
import sys
from pathlib import Path

from utils.constants import ONTOLOGY, add_prefixes
from utils.dictionary import Dictionary
from utils.ontology import Ontology
from utils.structure import Structure
from utils.validation import call_validators

from validators.all_files import AllFiles
from validators.file_content.total_domain import TotalDomain
from validators.structure.structure import StructureValidator
from validators.structure.versions.v1 import StructureValidatorV1
from validators.structure.versions.v2 import StructureValidatorV2


def get_structure_validator(root_path: str, version: str)\
        -> StructureValidator:
    """This method returns the structure validator. If we have a validator
    for this version it returns that validator, if not returns last version
    validator.
    """

    last_version = "2"
    validator_for_version = {
        "1": StructureValidatorV1(root_path, "Structure validation failed"),
        "2": StructureValidatorV2(root_path, "Structure validation failed"),
    }

    if version in validator_for_version:
        return validator_for_version[version]

    return validator_for_version[last_version]


def config_logging(level):
    """Configuration for logging to redirect output to stdout."""
    logging.basicConfig(level=level, format="%(message)s")

    root = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    root.handlers = [handler]


def main():
    """This is the main function that calls the validators."""
    args = parse_args()
    file_path = args.source
    version = args.version

    root_path = str(Path(file_path) / f"v{version}")

    if args.verbose:
        config_logging(logging.DEBUG)
    else:
        config_logging(logging.INFO)

    if args.translation:
        Structure.validate_fifi = True

    Structure.spellcheck = args.spellcheck

    logging.info("Version folder: %s", root_path.replace(file_path, ""))

    if args.resources:
        Structure.read_structure(args.resources)
    else:
        Structure.read_structure()

    if Structure.structure == {}:
        return False

    add_prefixes(Structure.structure["prefix"])
    Structure.set_root_folder(root_path)
    Structure.set_repository_folder(file_path)
    Structure.verbose = args.verbose

    content_validators = [
        AllFiles(root_path, "Files validation failed"),
        TotalDomain(
            "Properties are not defined in all classes from domain")]

    if get_structure_validator(root_path, version).validate():
        Ontology.ontology_name = Structure.structure[ONTOLOGY]
        Ontology.read_ontology_file(root_path)
        Ontology.preprocess()

        valid_overall = call_validators(content_validators)
    else:
        valid_overall = False

    logging.basicConfig(level=logging.INFO)
    if valid_overall:
        logging.info("\nValid structure and files")

    Dictionary.write_cached_words()

    return valid_overall


def str2bool(value):
    """Conversion from string to bool for arguments"""
    if isinstance(value, bool):
        return value

    if value.lower() in ("yes", "true", "t", "y", "1"):
        return True

    if value.lower() in ("no", "false", "f", "n", "0"):
        return False

    raise argparse.ArgumentTypeError("Boolean value expected.")


def parse_args():
    """Parses the arguments."""
    parser = argparse.ArgumentParser(
        description="Tool for validating JSON-LD Ontology structure and files")

    parser.add_argument("-s", "--source", required=True, help=HelpMsg.SRC)
    parser.add_argument("-v", "--version", required=True, help=HelpMsg.VERSION)
    parser.add_argument("-r", "--resources", required=False,
                        help=HelpMsg.RESOURCES)
    parser.add_argument("--spellcheck", required=False, type=str2bool,
                        default=True, help=HelpMsg.SPELLCHECK)
    parser.add_argument("-t", "--translation", required=False,
                        help=HelpMsg.TRANSLATION, action="store_true")
    parser.add_argument("--verbose", "--verbose", required=False,
                        help=HelpMsg.VERBOSE, action="store_true")

    return parser.parse_args()


class HelpMsg:
    """This class has help messages."""
    SRC = "Path to a folder that contains version folders"
    VERSION = "Version number"
    VERBOSE = "Print debug info"
    TRANSLATION = "If given as argument, validates that finnish language " +\
        "must be present as translation of english labels, descriptions, " +\
        "comments and titles"
    RESOURCES = "The path to the resources.json file which must be used for" +\
        " this version. Default value: resources.json"
    SPELLCHECK = "Specifies if the spell check for the english labels, " +\
        "descriptions, comments and titles will be made. Value type:" +\
        " boolean (true(t)/false(f), 1/0, yes(y)/no(n)). Default value: true"


if __name__ == "__main__":
    main()
