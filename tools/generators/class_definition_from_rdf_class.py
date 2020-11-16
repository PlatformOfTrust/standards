from typing import Any, Dict
from owlready2 import Thing, default_world

from generators.commons.extended_properties import readonly
from generators.commons.builders import prop_get_full_id, build_attributes, build_subclass, build_subproperty
from generators.commons.builders import build_comments, build_nested_comments, build_labels, build_nested_labels
from generators.commons.builders import build_required, build_restrictions, build_ranges


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
    # Define main ClassDefinition template
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
    # Define and fill entity propeties: subclasses, labels, comments
    entity_properties = dict()
    entity_properties['@id'] = f'{PREFIX}:{entity_file.get("id")}'
    entity_properties['@type'] = 'owl:Class'

    subclasses = build_subclass(rdf_class.entity)
    if subclasses and subclasses[0] != Thing:
        entity_properties['subClassOf'] = f'{PREFIX}:{subclasses[0].name}'

    labels = build_labels(rdf_class.entity)
    if labels:
        entity_properties['rdfs:label'] = labels

    comments = build_comments(rdf_class.entity)
    if comments:
        entity_properties['rdfs:comment'] = comments

    # Define supported attributes template
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

    # Define and fill propeties for each supported attribute
    total_attributes = build_attributes(rdf_class, onto)
    for rdf_attribute in total_attributes:
        attribute_properties = dict()
        attribute_properties['@id'] = f'{PREFIX}:{prop_get_full_id(rdf_attribute)}'
        attribute_properties['@type'] = default_world._unabbreviate(rdf_attribute._owl_type).replace(
            'http://www.w3.org/2002/07/owl#', 'owl:')

        subproperties = build_subproperty(rdf_attribute)
        if subproperties:
            attribute_properties[
                'subPropertyOf'] = f'{PREFIX}:{prop_get_full_id(subproperties[0])}'

        labels = build_labels(rdf_attribute)
        if labels.items():
            attribute_properties["rdfs:label"] = labels

        comments = build_comments(rdf_attribute)
        if comments.items():
            attribute_properties["rdfs:comment"] = comments

        nested_labes = build_nested_labels(rdf_attribute)
        if nested_labes:
            attribute_properties["label"] = nested_labes

        nested_comments = build_nested_comments(rdf_attribute)
        if nested_comments:
            attribute_properties["comment"] = nested_comments

        ranges = build_ranges(rdf_attribute)
        if ranges:
            attribute_properties[f'{PREFIX}:valueType'] = ranges

        restrictions = build_restrictions(rdf_attribute)
        if restrictions:
            attribute_properties['xsd:restriction'] = restrictions

        is_required = build_required(rdf_attribute)
        attribute_properties[f'{PREFIX}:required'] = is_required

        is_readonly = readonly._get_indirect_values_for_class(rdf_attribute)
        if is_readonly:
            attribute_properties[f'{PREFIX}:readonly'] = is_readonly[0]

        supported_attrs[str(rdf_attribute.name)] = attribute_properties

    # Add attribute propeties to ClassDefinition template
    entity_properties[f'{PREFIX}:supportedAttribute'] = supported_attrs
    definition_template[f'{PREFIX}:supportedClass'] = entity_properties

    return definition_template
