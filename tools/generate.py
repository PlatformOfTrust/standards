import json
import os
import sys
import argparse
from typing import Any, Dict, NoReturn

from owlready2 import get_ontology, Ontology

from models import RDFClass, RDFProperty
from generators.commons.extended_properties import Link, Identity
from generators.class_definition_from_rdf_class import create_definition_from_rdf_class
from generators.context_from_rdf_class import create_context_from_rdf_class
from generators.vocabulary_from_rdf_class import create_vocabulary_from_rdf_class
from generators.vocabulary_from_rdf_property import create_vocabulary_from_rdf_property
from generators.schema_from_rdf_class import create_schema_from_rdf_class


def is_link_identity_relations(rdf_class) -> bool:
    """Return is either not rdf_class entity RDF class relations with Link or Identity

        Args:
            rdf_class (models.RDFClass): RDF class.

        Returns:
            (bool) : Check result
    """
    return (Link in rdf_class.entity.ancestors() or Identity in rdf_class.entity.ancestors()) and (rdf_class.entity != Link and rdf_class.entity != Identity)


def write_dump_to_file(dir_context: str, entity_file: Dict[str, str], data_to_dump: Dict[str, Any]) -> NoReturn:
    """Function to write all entities into various stuctured files.

        Args:
            dir_context (str): Entity directory.
            entity_file (dict of str: str): Entity stucture dict.
            data_to_dump (dict of str: Any): Entity.
    """

    entity_dir_path = os.path.join(dir_context, entity_file.get('dir'))
    entity_file_path = os.path.join(
        entity_dir_path, entity_file.get('filename'))
    os.makedirs(entity_dir_path, exist_ok=True)

    if data_to_dump.get('$schema'):
        entity_file_path = entity_file_path[:-2]
    with open(entity_file_path, 'w', encoding='utf-8') as rf:
        rf.write(json.dumps(data_to_dump, indent=4,
                            separators=(',', ': '), ensure_ascii=False))


def build_rdf_clasess(onto, export_onto_url: str) -> NoReturn:
    """Function to build rdf classes from ontology.

        Args:
            onto (namespace.Ontology): An ontology loaded with owlready2.
            export_onto_url (str): Link to base ontologies.
            definition_template (dict of str: str): Template for definitions.
            base_identity_template (dict of str: str): Template for identities.
            vocabulary_template (dict of str: str): Template for vocabularies.
    """
    # Transform ontology classes into our class models
    rdf_classes = [RDFClass(i) for i in onto.classes()]
    for rdf_class in rdf_classes:
        files = rdf_class.get_files()
        for entity_file in files:
            if is_link_identity_relations(rdf_class):

                data_to_dump = create_definition_from_rdf_class(
                    rdf_class, entity_file, onto, export_onto_url)
                write_dump_to_file(CLASS_DEFINITIONS_DIR,
                                   entity_file, data_to_dump)

                data_to_dump = create_context_from_rdf_class(
                    rdf_class, entity_file, onto, export_onto_url)
                write_dump_to_file(CONTEXT_DIR, entity_file, data_to_dump)

                data_to_dump = create_schema_from_rdf_class(
                    rdf_class, entity_file, onto, export_onto_url)
                write_dump_to_file(SCHEMA_DIR, entity_file, data_to_dump)

            data_to_dump = create_vocabulary_from_rdf_class(
                rdf_class, entity_file, onto, export_onto_url)
            write_dump_to_file(VOCABULARY_DIR, entity_file, data_to_dump)


def build_rdf_properties(onto) -> NoReturn:
    """Function to build rdf properties from ontology.

        Args:
            onto (namespace.Ontology): An ontology loaded with owlready2.
            vocabulary_template (dict of str: str): Template for vocabularies.
    """
    properties = [RDFProperty(i) for i in onto.properties()]
    for rdf_property in properties:
        files = rdf_property.get_files()
        for property_file in files:
            data_to_dump = create_vocabulary_from_rdf_property(
                rdf_property, export_onto_url)
            write_dump_to_file(VOCABULARY_DIR, property_file, data_to_dump)


def parse(fname: str, export_onto_url: str) -> NoReturn:
    """Main ontology parser.

        Args:
            fname (str): File that contains ontology. <file.owl>
            export_onto_url (str): Link to base ontologies.
    """
    onto = get_ontology(fname).load()

    build_rdf_clasess(onto, export_onto_url)
    build_rdf_properties(onto)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", help="You have to select file to parse: <filename.owl>")
    parser.add_argument("output_dir", help="You have to pass output folder")
    parser.add_argument(
        "export_url", help="You have to select export pot url: https://<my-onto.test>")
    args = parser.parse_args()

    filename = args.filename
    BASE_DIR = args.output_dir
    export_onto_url = args.export_url

    VOCABULARY_DIR = os.path.join(BASE_DIR, 'Vocabulary')
    CONTEXT_DIR = os.path.join(BASE_DIR, 'Context')
    CLASS_DEFINITIONS_DIR = os.path.join(BASE_DIR, 'ClassDefinitions')
    SCHEMA_DIR = os.path.join(BASE_DIR, 'Schema')

    parse(filename, export_onto_url)
