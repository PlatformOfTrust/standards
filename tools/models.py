import os
from owlready2 import label, comment, AnnotationProperty, owl_world, Thing
from class_helpers import subClassOf


class RDFClass:
    def __init__(self, cls):
        self.cls = cls
        self.directories = None
        self.parent_lines = None

    def get_files(self):
        if self.directories:
            return self.directories

        def build_directories(rdf_class):
            parents = rdf_class.is_a
            new_directories = []
            if len(parents):
                for i in parents:
                    directories = build_directories(i)
                    for directory in directories:
                        new_directories.append(os.path.join(directory, rdf_class.name))
                return new_directories
            else:
                directories = [rdf_class.name, ]
            return directories
        result_directories = []
        for rd in build_directories(self.cls):
            ar = rd.split(os.path.sep)
            result_directories.append({
                'dir': os.path.sep.join(ar[1:-1]),
                'filename': f'{ar[-1]}.jsonld',
                'id': '/'.join(ar[1:])
            })
        self.directories = result_directories
        return self.directories

    def to_python(self, context):
        result = {
            '@id': 'pot:{}'.format(context.get('id')),
            '@type': 'owl:Class'
        }
        if list(subClassOf._get_indirect_values_for_class(self.cls)):
            if subClassOf._get_indirect_values_for_class(self.cls)[0] != Thing:
                result['subClassOf'] = 'pot:{}'.format(str(subClassOf._get_indirect_values_for_class(self.cls)[0].name))


        #Labels
        labels = {}
        for l in label._get_indirect_values_for_class(self.cls):
            labels[l.lang] = str(l)

        if len(labels):
            result['rdfs:label'] = labels

        #Comments
        comments = {}
        for c in comment._get_indirect_values_for_class(self.cls):
            comments[c.lang] = str(c)

        if len(comments):
            result['rdfs:comment'] = comments

        return result
