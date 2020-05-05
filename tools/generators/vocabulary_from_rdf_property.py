from typing import Any, Dict
from owlready2 import default_world

from generators.commons.extended_properties import domain
from generators.commons.builders import prop_get_full_id, build_subproperty
from generators.commons.builders import build_comments, build_nested_comments, build_labels, build_nested_labels
from generators.commons.builders import build_restrictions, build_ranges, build_domains


def create_vocabulary_from_rdf_property(rdf_property: Any, export_onto_url: str, PREFIX='pot', VERSION=1.1):
    """Return dict of generated properties to create Vocabulary from rdf property.

        Args:
            rdf_property (models.RDFProperty): RDFProperty model object
            export_onto_url (str): Link to base ontologies.
            PREFIX (str, optional): Id prefix.
            VERSION (number, optional): Version number
        Returns:
            vocabulary_template (dict of str: Any): Dictionary of required parameters
    """
    # Define main Vocabulary template for property
    vocabulary_template = {
        '@context': {
            '@version': VERSION,
            f'{PREFIX}': {
                '@id': f'{export_onto_url}Vocabulary/',
                '@prefix': True
            },
            'rdf': {
                '@id': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                '@prefix': True
            },
            'rdfs': {
                '@id': 'http://www.w3.org/2000/01/rdf-schema#',
                '@prefix': True
            },
            'owl': {
                '@id': 'http://www.w3.org/2002/07/owl#',
                '@prefix': True
            },
            'vs': {
                '@id': 'http://www.w3.org/2003/06/sw-vocab-status/ns#',
            },
            'xsd': {
                '@id': 'http://www.w3.org/2001/XMLSchema#',
                '@prefix': True
            },
            'label': {
                '@id': 'rdfs:label',
                "@container": ['@language', '@set']
            },
            'comment': {
                '@id': 'rdfs:comment',
                "@container": ['@language', '@set']
            }
        }
    }
    # Define and fill entity propeties: subclasses, labels, comments
    entity_properties = dict()
    entity_properties['@id'] = f'{PREFIX}:{prop_get_full_id(rdf_property.entity)}'
    entity_properties['@type'] = default_world._unabbreviate(rdf_property.entity._owl_type).replace(
        'http://www.w3.org/2002/07/owl#', 'owl:')

    subproperties = build_subproperty(rdf_property.entity)
    if subproperties:
        entity_properties['subPropertyOf'] = f'{PREFIX}:{prop_get_full_id(subproperties[0])}'

    labels = build_labels(rdf_property.entity)
    if labels.items():
        entity_properties["rdfs:label"] = labels

    comments = build_comments(rdf_property.entity)
    if comments.items():
        entity_properties["rdfs:comment"] = comments

    nested_labes = build_nested_labels(rdf_property.entity)
    if nested_labes:
        entity_properties["label"] = nested_labes

    nested_comments = build_nested_comments(rdf_property.entity)
    if nested_comments:
        entity_properties["comment"] = nested_comments

    ranges = build_ranges(rdf_property.entity)
    if ranges:
        entity_properties[f'{PREFIX}:valueType'] = ranges

    restrictions = build_restrictions(rdf_property.entity)
    if restrictions:
        entity_properties['xsd:restriction'] = restrictions

    domains = build_domains(rdf_property.entity)
    if domains:
        entity_properties['domain'] = domains

    vocabulary_template[rdf_property.entity.name] = entity_properties

    return vocabulary_template
