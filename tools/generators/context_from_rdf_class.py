from copy import deepcopy
from typing import Any, Dict

from generators.commons.extended_properties import nest
from generators.commons.builders import build_attributes, prop_get_full_id


def create_context_from_rdf_class(rdf_class, entity_file: Dict[str, Any], onto, export_onto_url: str, PREFIX='pot', VERSION=1.1) -> Dict[str, Any]:
    """Return dict of generated properties to create Context from rdf classes.

        Args:
            rdf_class (models.RDFClass): RDFClass model object
            entity_file (dict of str: Any):
                Dictionary with directory, filename and id of entity
            onto (namespace.Ontology): An ontology loaded with owlready2.
            export_onto_url (str): Link to base ontologies.
            PREFIX (str, optional): Id prefix.
            VERSION (number, optional): Version number
        Returns:
            context_template (dict of str: Any): Dictionary of required parameters
    """
    context_template = {
        '@version': VERSION,
        '@vocab': f"{export_onto_url}Vocabulary/{entity_file.get('id')}",
        '@classDefinition': f"{export_onto_url}ClassDefinitions/{entity_file.get('id')}",
        f'{PREFIX}': {
            '@id': f'{export_onto_url}Vocabulary/',
            '@prefix': True
        },
        'data': f'{PREFIX}:data',
        'metadata': f'{PREFIX}:metadata',
    }

    total_attributes = build_attributes(rdf_class, onto)
    for rdf_attribute in total_attributes:

        result = dict()
        nest_list = nest._get_indirect_values_for_class(rdf_attribute)
        if nest_list:
            result['@nest'] = nest_list[0].name
        result['@id'] = f'{PREFIX}:{prop_get_full_id(rdf_attribute)}'

        context_template[rdf_attribute.name] = result

    result = dict()
    result['@context'] = context_template
    result['@type'] = rdf_class.entity.name
    result['@schema'] = f"{export_onto_url}Schema/{entity_file.get('id')}"
    return result
