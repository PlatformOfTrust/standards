from collections import OrderedDict
from typing import Any, Dict

from owlready2 import Thing

from generators.commons.extended_properties import readonly
from generators.commons.builders import build_comments, build_labels, build_attributes, build_subclass, build_required, owl_property_to_python_base


def create_definition_from_rdf_class(rdf_class, entity_file: Dict[str, str], onto, export_onto_url: str, PREFIX='pot', VERSION=1.1) -> Dict[str, Any]:
    """Return dict of generated properties to create ClassDefinition from rdf classes.

        Args:
            rdf_class (models.RDFClass): RDFClass model object
            entity_file (dict of str: Any):
                Dictionary with directory, filename and id of entity
            onto (namespace.Ontology): An ontology loaded with owlready2.
            export_onto_url (str): Link to base ontologies.
            PREFIX (str, optional): Id prefix.
            VERSION (number, optional): Version number
        Returns:
            definition_template (dict of str: Any): Dictionary of required parameters
    """
    definition_template = {
        '@context': {
            '@version': VERSION,
            '@vocab': f"{export_onto_url}Vocabulary/{entity_file.get('id')}",
            'xsd': {
                '@id': 'http://www.w3.org/2001/XMLSchema#',
                '@prefix': True
            },
            f'{PREFIX}': {
                '@id': f'{export_onto_url}Vocabulary/',
                '@prefix': True
            },
            'description': {
                '@id': 'rdfs:comment',
                '@container': ['@language', '@set']
            },
            'label': {
                '@id': 'rdfs:label',
                '@container': ['@language', '@set']
            },
            'comment': {
                '@id': 'rdfs:comment',
                '@container': ['@language', '@set']
            }
        },
    }

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

    supported_class = result
    supported_attrs = {
        'data': {
            '@id': f'{PREFIX}:data',
            '@type': f'{PREFIX}:SupportedAttribute',
            'rdfs:label': 'data',
            'rdfs:comment': {
                'en-us': 'data'
            },
            f'{PREFIX}:required': False,
        }
    }

    total_attributes = build_attributes(rdf_class, onto)
    for rdf_attribute in total_attributes:

        result = owl_property_to_python_base(rdf_attribute)

        is_required = build_required(rdf_attribute)
        result[f'{PREFIX}:required'] = is_required

        is_readonly = readonly._get_indirect_values_for_class(rdf_attribute)
        if is_readonly:
            result[f'{PREFIX}:readonly'] = is_readonly[0]

        supported_attrs[str(rdf_attribute.name)] = result

    supported_attrs = OrderedDict(
        sorted(supported_attrs.items(), key=lambda t: t[0]))
    supported_class[f'{PREFIX}:supportedAttribute'] = supported_attrs

    definition_template[f'{PREFIX}:supportedClass'] = supported_class

    return definition_template
