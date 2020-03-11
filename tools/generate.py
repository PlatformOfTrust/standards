import json
from copy import deepcopy
from owlready2 import *
from models import RDFClass, RDFProperty
from export_templates import get_definition_pot, get_base_identity_pot, get_vocabulary_pot, POT_EXPORT
from utils import owl_property_to_python_for_definition, owl_property_context, class_get_full_id,\
    owl_property_to_python_for_vocabulary
from class_helpers import Link, Identity

pot = owl_world.get_ontology("https://standard.oftrust.net/")


def create_definition_from_rdf_class(rdf_class, context, onto, pot_export, template):
    vocabulary_dict = deepcopy(template)
    vocabulary = '{}Vocabulary/{}'.format(pot_export, context.get('id'))
    vocabulary_dict['@context']['@vocab'] = vocabulary
    supported_class = rdf_class.to_python(context)
    supported_attrs = {
        'data': {
            "@id": 'pot:data',
            "@type": "pot:SupportedAttribute",
            "rdfs:label": "data",
            "rdfs:comment": {
                "en-us": "data"
            },
            "pot:required": False,
        }
    }
    total_attributes = set()
    for a in onto.data_properties():
        if rdf_class.cls.ancestors().intersection(a.domain):
            total_attributes.add(a)

    for a in onto.object_properties():
        if rdf_class.cls.ancestors().intersection(a.domain):
            total_attributes.add(a)

    for rdf_attribute in total_attributes:
        supported_attrs[str(rdf_attribute.name)] = owl_property_to_python_for_definition(rdf_attribute)

    supported_attrs = OrderedDict(sorted(supported_attrs.items(), key=lambda t: t[0]))
    vocabulary_dict['@context']['description'] = {
        '@id': 'rdfs:comment',
        "@container": ['@language', '@set']
    }

    supported_class['pot:supportedAttribute'] = supported_attrs
    vocabulary_dict['pot:supportedClass'] = supported_class
    return vocabulary_dict


def create_identity_from_rdf_class(rdf_class, context, onto, pot_export, template):
    identity_dict = deepcopy(template)
    vocabulary = '{}ClassDefinitions/{}'.format(pot_export, context.get('id'))
    identity_dict['@vocab'] = '{}Vocabulary/{}'.format(pot_export, context.get('id'))
    identity_dict['@classDefinition'] = vocabulary
    total_attributes = set()
    for a in onto.data_properties():
        if rdf_class.cls.ancestors().intersection(a.domain):
            total_attributes.add(a)

    for a in onto.object_properties():
        if rdf_class.cls.ancestors().intersection(a.domain):
            total_attributes.add(a)

    for rdf_attribute in total_attributes:
        identity_dict[rdf_attribute.name] = owl_property_context(rdf_attribute)
    return {
        '@context': identity_dict
    }


def create_vocabulary_from_rdf_class(rdf_class, context, onto, template):
    vocabulary_dict = deepcopy(template)
    total_attributes = set()
    for a in onto.data_properties():
        if rdf_class.cls.ancestors().intersection(a.domain):
            total_attributes.add(a)

    for a in onto.object_properties():
        if rdf_class.cls.ancestors().intersection(a.domain):
            total_attributes.add(a)

    for rdf_attribute in total_attributes:
        vocabulary_dict[rdf_attribute.name] = owl_property_to_python_for_vocabulary(rdf_attribute)
    vocabulary_dict[rdf_class.cls.name] = rdf_class.to_python(context)
    vocabulary_dict['@context']['label'] = {
            '@id': 'rdfs:label',
            "@container": ['@language', '@set']
    }
    vocabulary_dict['@context']['comment'] = {
            '@id': 'rdfs:comment',
            "@container": ['@language', '@set']
    }

    for dependent in rdf_class.cls.subclasses():
        vocabulary_dict[dependent.name] = {
            'rdfs:subClassOf': {
                '@id': 'pot:{}'.format(class_get_full_id(dependent).replace(f'/{dependent.name}', ''))
            }
        }
    return vocabulary_dict


def parse(fname, export_pot_url):
    onto = get_ontology(fname).load()
    base_identity_template = get_base_identity_pot(export_pot_url)
    vocabulary_template = get_vocabulary_pot(export_pot_url)
    definition_template = get_definition_pot(export_pot_url)
    for c in [RDFClass(i) for i in onto.classes()]:
        files = c.get_files()
        for f in files:
            if (Link in c.cls.ancestors() or Identity in c.cls.ancestors()) and (c.cls != Link and c.cls != Identity):
                os.makedirs(os.path.join(CLASS_DEFINITIONS_DIR, f.get('dir')), exist_ok=True)
                data_to_dump = create_definition_from_rdf_class(c, f, onto, export_pot_url, definition_template)
                with open(os.path.join(CLASS_DEFINITIONS_DIR, f.get('dir'), f.get('filename')), 'w', encoding='utf-8') as rf:
                    rf.write(json.dumps(data_to_dump, indent=4, separators=(',', ': '), ensure_ascii=False))

                os.makedirs(os.path.join(CONTEXT_DIR, f.get('dir')), exist_ok=True)
                data_to_dump = create_identity_from_rdf_class(c, f, onto, export_pot_url, base_identity_template)
                with open(os.path.join(CONTEXT_DIR, f.get('dir'), f.get('filename')), 'w', encoding='utf-8') as rf:
                    rf.write(json.dumps(data_to_dump, indent=4, separators=(',', ': '), ensure_ascii=False))

            os.makedirs(os.path.join(VOCABULARY_DIR, f.get('dir')), exist_ok=True)
            data_to_dump = create_vocabulary_from_rdf_class(c, f, onto, vocabulary_template)
            with open(os.path.join(VOCABULARY_DIR, f.get('dir'), f.get('filename')), 'w', encoding='utf-8') as rf:
                rf.write(json.dumps(data_to_dump, indent=4, separators=(',', ': '), ensure_ascii=False))

    for p in [RDFProperty(i) for i in onto.properties()]:
        files = p.get_files()
        for f in files:
            os.makedirs(os.path.join(VOCABULARY_DIR, f.get('dir')), exist_ok=True)
            with open(os.path.join(VOCABULARY_DIR, f.get('dir'), f.get('filename')), 'w', encoding='utf-8') as rf:
                rf.write(json.dumps(p.to_python(vocabulary_template), indent=4, separators=(',', ': '), ensure_ascii=False))


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
    except IndexError:
        print('You have to select file to parse, please use: python parse.py <filename.owl>')
        exit()
    try:
        BASE_DIR = sys.argv[2]
    except IndexError:
        BASE_DIR = 'v1'
    try:
        _export_pot_url = sys.argv[3]
    except IndexError:
        _export_pot_url = POT_EXPORT
    VOCABULARY_DIR = os.path.join(BASE_DIR, 'Vocabulary')
    CONTEXT_DIR = os.path.join(BASE_DIR, 'Context')
    CLASS_DEFINITIONS_DIR = os.path.join(BASE_DIR, 'ClassDefinitions')
    parse(filename, _export_pot_url)
