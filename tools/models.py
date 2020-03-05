import os
from copy import deepcopy

from owlready2 import label, comment, Thing
from class_helpers import subClassOf
from utils import owl_property_to_python_for_vocabulary


class AbstractRDFEntity:
    SKIP_BASES = 1

    def __init__(self, cls):
        self.cls = cls
        self.directories = None

    @staticmethod
    def build_directories(rdf_entity):
        parents = rdf_entity.is_a
        new_directories = []
        if len(parents):
            for i in parents:
                directories = AbstractRDFEntity.build_directories(i)
                for directory in directories:
                    new_directories.append(os.path.join(directory, rdf_entity.name))
            return new_directories
        else:
            directories = [rdf_entity.name, ]
        return directories

    def get_files(self):
        result_directories = []
        for rd in self.build_directories(self.cls):
            ar = rd.split(os.path.sep)
            result_directories.append({
                'dir': os.path.sep.join(ar[self.SKIP_BASES:-1]),
                'filename': f'{ar[-1]}.jsonld',
                'id': '/'.join(ar[self.SKIP_BASES:])
            })
        self.directories = result_directories
        return self.directories


class RDFProperty(AbstractRDFEntity):
    SKIP_BASES = 2

    def get_files(self):
        directory = max(self.build_directories(self.cls), key=len)
        ar = directory.split(os.path.sep)[self.SKIP_BASES:]
        ar = ar[1:] if ar[0] == 'topDataProperty' else ar
        return [{
            'dir': os.path.sep.join(ar[:-1]),
            'filename': f'{ar[-1]}.jsonld',
            'id': '/'.join(ar[self.SKIP_BASES:])
        }]

    def to_python(self, vocabulary_template):
        vocabulary_dict = deepcopy(vocabulary_template)
        vocabulary_dict['@context']['label'] = {
            '@id': 'rdfs:label',
            "@container": ['@language', '@set']
        }
        vocabulary_dict['@context']['comment'] = {
            '@id': 'rdfs:comment',
            "@container": ['@language', '@set']
        }
        vocabulary_dict[self.cls.name] = owl_property_to_python_for_vocabulary(self.cls)
        return vocabulary_dict


class RDFClass(AbstractRDFEntity):

    def to_python(self, context):
        result = {
            '@id': 'pot:{}'.format(context.get('id')),
            '@type': 'owl:Class'
        }
        if list(subClassOf._get_indirect_values_for_class(self.cls)):
            if subClassOf._get_indirect_values_for_class(self.cls)[0] != Thing:
                result['subClassOf'] = 'pot:{}'.format(str(subClassOf._get_indirect_values_for_class(self.cls)[0].name))

        labels = {}
        for l in label._get_indirect_values_for_class(self.cls):
            labels[l.lang] = str(l)

        if len(labels):
            result['rdfs:label'] = labels

        comments = {}
        for c in comment._get_indirect_values_for_class(self.cls):
            comments[c.lang] = str(c)

        if len(comments):
            result['rdfs:comment'] = comments

        return result


