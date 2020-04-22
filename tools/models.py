import os
from typing import Any, Dict, List, NoReturn

from owlready2 import Thing


class AbstractRDFEntity:
    SKIP_BASES = 1

    def __init__(self, entity: Any) -> NoReturn:
        """Abstract RDF entity initialization method.

        Args:
            entity (Any): 
                Entity, property or annotation class.
                Can be: ThingClass, DataPropertyClass, 
                        ObjectPropertyClass, AnnotationPropertyClass
        Attributes:
            entity (Thing): Class defined in the ontology.
            directories (None): Directories.

        """
        self.entity = entity
        self.directories = None

    @staticmethod
    def build_directories(entity: Any) -> List[str]:
        """Return list of RDF entity name and its parents names.

        Args:
            entity (Any): 
                Entity, property or annotation class.
                Can be: PropertyClass, ThingClass, 
                        DataPropertyClass, ObjectPropertyClass, 
                        AnnotationPropertyClass
        Returns:
            directories (list of str): List of directories.
        """
        parents = entity.is_a
        new_directories = []
        if len(parents):
            for parent in parents:
                directories = AbstractRDFEntity.build_directories(parent)
                for directory in directories:
                    new_directories.append(
                        os.path.join(directory, entity.name))
            return new_directories
        else:
            directories = [entity.name, ]
        return directories

    def get_files(self) -> List[Dict[str, str]]:
        """Return list of dictionaries with directory, filename and id of entity

        Returns:
            directories (list of dict of str: str): 
                List of dictionaries with directory, filename and id of entity
        """
        result_directories = []
        for result_directory in self.build_directories(self.entity):
            entities = result_directory.split(os.path.sep)
            result_directories.append({
                'dir': os.path.sep.join(entities[self.SKIP_BASES:-1]),
                'filename': f'{entities[-1]}.jsonld',
                'id': '/'.join(entities[self.SKIP_BASES:])
            })
        self.directories = result_directories
        return self.directories


class RDFProperty(AbstractRDFEntity):
    SKIP_BASES = 2

    def get_files(self) -> List[Dict[str, str]]:
        """Return list of dictionaries with directory, filename and id of entity

        Returns:
            (list of dict): 
                List of dictionaries with directory, filename and id of entity
        """
        directories = max(self.build_directories(self.entity), key=len)
        property_directories = directories.split(os.path.sep)[self.SKIP_BASES:]
        if property_directories[0] == 'topDataProperty':
            property_directories.pop(0)
        return [{
            'dir': os.path.sep.join(property_directories[:-1]),
            'filename': f'{property_directories[-1]}.jsonld',
            'id': '/'.join(property_directories[self.SKIP_BASES:])
        }]


class RDFClass(AbstractRDFEntity):
    pass
