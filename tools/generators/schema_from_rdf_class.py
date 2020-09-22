from typing import Any, Dict

from generators.commons.extended_properties import domain, nest
from generators.commons.builders import prop_get_full_id, build_attributes
from generators.commons.builders import build_comments, build_nested_comments, build_labels, build_nested_labels
from generators.commons.builders import build_required


def create_schema_from_rdf_class(rdf_class, entity_file: Dict[str, Any], onto, export_onto_url: str) -> Dict[str, Any]:
    """Return dict of generated properties to create Schema from rdf classes.

        Args:
            rdf_class (models.RDFClass): RDFClass model object
            entity_file (dict of str: Any):
                Dictionary with directory, filename and id of entity
            onto (namespace.Ontology): An ontology loaded with owlready2.
            export_onto_url (str): Link to base ontologies.
        Returns:
            schema (dict of str: Any): Dictionary of required parameters
    """
    properties = set()
    parents = set()
    labels = dict()
    comments = dict()
    examples = dict()
    required_attrs = list()

    # Define and fill propeties for each supported attribute
    total_attributes = build_attributes(rdf_class, onto)
    for attr in total_attributes:
        # Build required
        if build_required(attr):
            required_attrs.append(attr.name)

        # Build labels according to schema specifications
        attr_labels = build_labels(attr)
        if attr_labels.get('en-us'):
            labels[attr.name] = attr_labels['en-us']
        else:
            attr_nested_labels = build_nested_labels(attr)
            if attr_nested_labels:
                labels[attr.name] = attr_nested_labels[0]['rdfs:label']['en-us']
            else:
                labels[attr.name] = ''

        # Build comments according to schema specifications
        attr_comments = build_comments(attr)
        if attr_comments.get('en-us'):
            comments[attr.name] = attr_comments['en-us']
        else:
            attr_nested_comments = build_nested_comments(attr)
            if attr_nested_comments:
                for c in attr_nested_comments:
                    for d in c.get('domain'):
                        if rdf_class.entity.name == d.split(':')[-1]:
                            attr_nested_comment = c['rdfs:comment']
                            if attr_nested_comment.get('en-us'):
                                comments[attr.name] = attr_nested_comment['en-us']
                            else:
                                comments[attr.name] = ''
            else:
                comments[attr.name] = ''

        examples[attr.name] = attr.example if attr.example else ''

        # Build parent properties
        parent = nest._get_indirect_values_for_class(
            attr)[0] if nest._get_indirect_values_for_class(attr) else None
        if parent:
            properties.add((parent.name, attr.name))
        else:
            parents.add(attr.name)

    properties_dict = {}
    for k, v in properties:
        if k in properties_dict:
            properties_dict[k].append(v)
        else:
            properties_dict[k] = [v]

    for p in parents:
        if p not in properties_dict:
            properties_dict[p] = []

    result = dict()
    result["@context"] = {
        "type": "string",
        "minLength": 1,
        "const": f"{export_onto_url}Context/{entity_file.get('id')}/"
    }
    result["@type"] = {
        "type": "string",
        "minLength": 1,
        "enum": [rdf_class.entity.name],
        "const": rdf_class.entity.name
    }

    required_attrs.append("@context")
    required_attrs.append("@type")

    if 'id' in required_attrs:
        required_attrs.remove('id')
        required_attrs.append("@id")

    prop_parent = {v[0] for v in properties}
    for i in parents:
        if i in prop_parent:
            result[i] = {"title": "", "description": "", "type": "object", "properties": {}}
        else:
            result[i] = {"title": "", "description": "", "type": "string"}

    for key, values in properties_dict.items():
        if values:
            for v in values:
                result[key]["title"] = labels[key]
                result[key]["description"] = comments[key]
                result[key]["properties"][v] = {
                    "title": labels[v] if v in labels else '',
                    "description": comments[v] if v in comments else '',
                    "type": "string"
                }
                if examples[key]:
                    result[key]["examples"] = examples[key]
                if key in result and examples[v]:
                    result[key]["properties"][v]["examples"] = examples[v]
        else:
            if key in labels and key in comments:
                result[key]["title"] = labels[key]
                result[key]["description"] = comments[key]

    if 'id' in result:
        result['@id'] = result['id']
        del result['id']

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema",
        "type": "object",
        "properties": result,
        "required": required_attrs
    }

    return schema
