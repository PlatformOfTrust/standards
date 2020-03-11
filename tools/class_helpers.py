from owlready2 import AnnotationProperty, get_ontology, rdfs, Thing, ThingClass
ONTO_BASE = "https://standards.oftrust.net/"
NAMESPACE = "https://standards.oftrust.net/v1/Vocabulary/"


class readonly(AnnotationProperty):
    namespace = get_ontology(ONTO_BASE).get_namespace(NAMESPACE)


class required(AnnotationProperty):
    namespace = get_ontology(ONTO_BASE).get_namespace(NAMESPACE)


class nest(AnnotationProperty):
    namespace = get_ontology(ONTO_BASE).get_namespace(NAMESPACE)


class label(AnnotationProperty):
    namespace = get_ontology(ONTO_BASE)


class comment(AnnotationProperty):
    namespace = get_ontology(ONTO_BASE)


class subPropertyOf(AnnotationProperty):
    namespace = rdfs


class subClassOf(AnnotationProperty):
    namespace = rdfs


class range(AnnotationProperty):
    namespace = rdfs


class domain(AnnotationProperty):
    namespace = rdfs


class restriction(AnnotationProperty):
    namespace = get_ontology('http://www.w3.org/2001/XMLSchema#')


class Link(Thing):
    namespace = get_ontology(ONTO_BASE).get_namespace(NAMESPACE)


class Identity(Thing):
    namespace = get_ontology(ONTO_BASE).get_namespace(NAMESPACE)
