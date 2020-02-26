from owlready2 import AnnotationProperty, get_ontology, rdfs, Thing, ThingClass


class readonly(AnnotationProperty):
    namespace = get_ontology("https://standard.oftrust.net#").get_namespace("https://standard.oftrust.net/")


class required(AnnotationProperty):
    namespace = get_ontology("https://standard.oftrust.net#").get_namespace("https://standard.oftrust.net/")


class nest(AnnotationProperty):
    namespace = get_ontology("https://standard.oftrust.net#").get_namespace("https://standard.oftrust.net/")


class label(AnnotationProperty):
    namespace = get_ontology("https://standard.oftrust.net#")


class comment(AnnotationProperty):
    namespace = get_ontology("https://standard.oftrust.net#")


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
    namespace = get_ontology("https://standard.oftrust.net#").get_namespace("https://standard.oftrust.net/")


class Identity(Thing):
    namespace = get_ontology("https://standard.oftrust.net#").get_namespace("https://standard.oftrust.net/")