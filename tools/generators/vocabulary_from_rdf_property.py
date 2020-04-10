from typing import Any, Dict

from generators.commons.extended_properties import domain
from generators.commons.builders import owl_property_to_python_base, build_domains


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
    result = owl_property_to_python_base(rdf_property.entity)

    domains = build_domains(rdf_property.entity)
    if domains:
        result['domain'] = domains

    vocabulary_template[rdf_property.entity.name] = result

    return vocabulary_template
