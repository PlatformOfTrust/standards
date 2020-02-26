VERSION = 1.1
LABEL_REF = 'http://www.w3.org/2000/01/rdf-schema#label'
COMMENT_REF = 'http://www.w3.org/2000/01/rdf-schema#comment'
RANGE_REF = 'http://www.w3.org/2000/01/rdf-schema#range'
SUBCLASS_REF = 'http://www.w3.org/2000/01/rdf-schema#subClassOf'
POT_BASE = 'https://standards.oftrust.net/'
POT_EXPORT = 'https://standards.oftrust.net/v1/'
CONF_NAME = 'settings.conf'

BASE_IDENTITY_POT = {
    '@version': VERSION,
    '@vocab': "{}vocabularies/.jsonld#".format(POT_EXPORT),
    '@classDefinition':'',
    "pot": {
        "@id": "{}Vocabulary/".format(POT_EXPORT),
        "@prefix": True
    },
    "data": "pot:data",
    "metadata": "pot:metadata",
}

BASE_DIRECTORY_POT = {
    '@context': {
        '@version': VERSION,
        "pot": {
            "@id": "{}Vocabulary/".format(POT_EXPORT),
            "@prefix": True
        },
        "owl": {
            "@id": "http://www.w3.org/2002/07/owl#",
            "@prefix": True
        },
        "vs": {
            "@id": "http://www.w3.org/2003/06/sw-vocab-status/ns#",
            "@prefix": True
        },
        "xsd": {
            "@id": "http://www.w3.org/2001/XMLSchema#",
            "@prefix": True
        },
        "label": {
            '@id': 'rdfs:label',
            "@container": ['@language', '@set']
        },
        "comment": {
            '@id': 'rdfs:comment',
            "@container": ['@language', '@set']
        }
    }
}

BASE_DEFFINITION_POT = {
    "@context": {
        "@version": VERSION,
        "xsd": {
            "@id": "http://www.w3.org/2001/XMLSchema#",
            "@prefix": True
        },
        "pot": {
            "@id": "{}Vocabulary/".format(POT_EXPORT),
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


BASE_VOCABULARY_POT = {
    "@context": {
        '@version': VERSION,
        "pot": {
            "@id": "{}Vocabulary/".format(POT_EXPORT),
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
