VERSION = 1.1
POT_EXPORT = 'https://standards.oftrust.net/v1/'


def get_base_identity_pot(pot_export_url):
    return {
        '@version': VERSION,
        '@vocab': "{}vocabularies/.jsonld#".format(pot_export_url),
        '@classDefinition': '',
        "pot": {
            "@id": "{}Vocabulary/".format(pot_export_url),
            "@prefix": True
        },
        "data": "pot:data",
        "metadata": "pot:metadata",
    }


def get_definition_pot(pot_export_url):
    return {
        "@context": {
            "@version": VERSION,
            "xsd": {
                "@id": "http://www.w3.org/2001/XMLSchema#",
                "@prefix": True
            },
            "pot": {
                "@id": "{}Vocabulary/".format(pot_export_url),
                "@prefix": True
            },
            "description": {},
            "label": {
                '@id': 'rdfs:label',
                "@container": ['@language', '@set']
            },
            "comment": {
                '@id': 'rdfs:comment',
                "@container": ['@language', '@set']
            }
        },
    }


def get_vocabulary_pot(pot_export_url):
    return {
        "@context": {
            '@version': VERSION,
            "pot": {
                "@id": "{}Vocabulary/".format(pot_export_url),
                "@prefix": True
            },
            "rdf": {
                "@id": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "@prefix": True
            },
            "rdfs": {
                "@id": "http://www.w3.org/2000/01/rdf-schema#",
                "@prefix": True
            },
            "owl": {
                "@id": "http://www.w3.org/2002/07/owl#",
                "@prefix": True
            },
            "vs": {
                "@id": "http://www.w3.org/2003/06/sw-vocab-status/ns#",
            },
            "xsd": {
                "@id": "http://www.w3.org/2001/XMLSchema#",
                "@prefix": True
            },
            "label": "",
            "comment": ""
        }
    }
