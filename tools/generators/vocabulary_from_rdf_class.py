from typing import Any, Dict
from owlready2 import Thing, default_world

from generators.commons.extended_properties import domain
from generators.commons.builders import prop_get_full_id, class_get_full_id, build_attributes, build_subclass, build_subproperty
from generators.commons.builders import build_comments, build_nested_comments, build_labels, build_nested_labels
from generators.commons.builders import build_required, build_restrictions, build_ranges, build_domains


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
    # Define main Vocabulary template for class
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

    vocabulary_template[rdf_class.entity.name] = entity_properties

    for dependent in rdf_class.entity.subclasses():
        vocabulary_template[dependent.name] = {
            'rdfs:subClassOf': {
                '@id': f'{PREFIX}:{class_get_full_id(dependent).replace(f"/{dependent.name}", "")}'
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

        domains = build_domains(rdf_attribute)
        if domains:
            attribute_properties['domain'] = domains

        vocabulary_template[rdf_attribute.name] = attribute_properties

    return vocabulary_template
