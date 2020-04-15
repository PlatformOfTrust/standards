from copy import deepcopy
from typing import Any, Dict

from owlready2 import Thing

from generators.commons.extended_properties import domain
from generators.commons.builders import build_comments, build_labels, build_attributes, build_subclass, owl_property_to_python_base, class_get_full_id, build_domains


def create_vocabulary_from_rdf_class(rdf_class, entity_file: Dict[str, Any], onto, export_onto_url, PREFIX='pot', VERSION=1.1) -> Dict[str, Any]:
    """Return dict of generated properties to create Vocabulary from rdf classes.

        Args:
            rdf_class (models.RDFClass): RDFClass model object
            entity_file (dict of str: Any):
                Dictionary with directory, filename and id of entity
            onto (namespace.Ontology): An ontology loaded with owlready2.
            export_onto_url (str): Link to base ontologies.
            PREFIX (str, optional): Id prefix.
            VERSION (number, optional): Version number
        Returns:
            vocabulary_template (dict of str: Any): Dictionary of required parameters
    """
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

    total_attributes = build_attributes(rdf_class, onto)
    for rdf_attribute in total_attributes:

        attributes = owl_property_to_python_base(rdf_attribute)
        domains = build_domains(rdf_attribute)
        if domains:
            attributes['domain'] = domains
        vocabulary_template[rdf_attribute.name] = attributes

    result = dict()
    result['@id'] = f'{PREFIX}:{entity_file.get("id")}'
    result['@type'] = 'owl:Class'

    subclasses = build_subclass(rdf_class.entity)
    if subclasses and subclasses[0] != Thing:
        result['subClassOf'] = f'{PREFIX}:{subclasses[0].name}'

    labels = build_labels(rdf_class.entity)
    if labels:
        result['rdfs:label'] = labels

    comments = build_comments(rdf_class.entity)
    if comments:
        result['rdfs:comment'] = comments

    vocabulary_template[rdf_class.entity.name] = result

    for dependent in rdf_class.entity.subclasses():
        vocabulary_template[dependent.name] = {
            'rdfs:subClassOf': {
                '@id': f'{PREFIX}:{class_get_full_id(dependent).replace(f"/{dependent.name}", "")}'
            }
        }

    return vocabulary_template
