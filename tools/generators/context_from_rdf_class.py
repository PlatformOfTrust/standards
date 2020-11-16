from typing import Any, Dict

from generators.commons.extended_properties import nest, Identity
from generators.commons.builders import prop_get_full_id, build_attributes


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
    # Define main Context template
    context_template = {
        '@version': VERSION,
        '@vocab': f"{export_onto_url}Vocabulary/{entity_file.get('id')}",
        '@classDefinition': f"{export_onto_url}ClassDefinitions/{entity_file.get('id')}",
        rdf_class.entity.name: {"@id": rdf_class.entity.name},
        '@schema': f"{export_onto_url}Schema/{entity_file.get('id')}",
        f'{PREFIX}': {
            '@id': f'{export_onto_url}Vocabulary/',
            '@prefix': True
        },
        'data': f'{PREFIX}:data',
        'metadata': f'{PREFIX}:metadata',
    }
    if Identity in rdf_class.entity.ancestors():
        context_template["@base"] = "https://api.oftrust.net/identities/v1/"

    # Define and fill propeties for each supported attribute
    total_attributes = build_attributes(rdf_class, onto)
    for rdf_attribute in total_attributes:
        attribute_properties = dict()
        attribute_properties['@id'] = f'{PREFIX}:{prop_get_full_id(rdf_attribute)}'

        nest_list = nest._get_indirect_values_for_class(rdf_attribute)
        if nest_list:
            attribute_properties['@nest'] = nest_list[0].name

        context_template[rdf_attribute.name] = attribute_properties

    context_wrapper = {'@context': context_template}
    return context_wrapper
