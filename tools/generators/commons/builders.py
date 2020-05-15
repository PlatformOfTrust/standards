from typing import Any, Dict, List, Set
from owlready2 import Thing, default_world, base, locstr, label, comment

from generators.commons.extended_properties import restriction, required, domain, subClassOf, subPropertyOf
from generators.commons.extended_properties import range as owl_range
from generators.commons.extended_properties import label as pot_label
from generators.commons.extended_properties import comment as pot_comment


def build_nested_domains(d):
    parents = {}
    if d and not isinstance(d, str):
        for a in d.ancestors():
            parent, child = str(a).split('.')
            parents[child] = parent

        domains = []
        domains.append(d.name)
        child = d.name
        while parents[child] != 'pot' and parents[child] != "Vocabulary":
            domains.append(parents[child])
            child = parents[child]
    return domains


def build_nested_labels(owl_property: Any, PREFIX='pot') -> List[Dict[str, str]]:
    """Return list of dicts with nested labels.

        Args:
            owl_property (Any): 
                Property of entity.
                Can be:  AnnotationPropertyClass, DataPropertyClass, ObjectPropertyClass.

        Returns:
            nested_labels (list of dict of str: str): List of nested labels dicts
    """
    nested_labels = list()
    for l in owl_property.label:
        if l:
            property_nested_labels = list()
            for nested_label in label._get_indirect_values_for_class(l):
                if isinstance(nested_label, locstr):
                    property_nested_labels.append({
                        nested_label.lang: nested_label
                    })

            nested_labels_template = {'rdfs:label': {}}

            domains = list()
            for d in l.domain:
                if d and not isinstance(d, str):
                    domains.append('/'.join(build_nested_domains(d)[::-1]))

            for nl in property_nested_labels:
                for k, v in nl.items():
                    nested_labels_template['rdfs:label'][k] = v
                nested_labels_template['domain'] = [
                    f'{PREFIX}:{d}' for d in domains]
            nested_labels.append(nested_labels_template)

    return nested_labels


def build_nested_comments(owl_property: Any, PREFIX='pot') -> List[Dict[str, str]]:
    """Return list of dicts with nested comments.

        Args:
            owl_property (Any): 
                Property of entity.
                Can be:  AnnotationPropertyClass, DataPropertyClass, ObjectPropertyClass.

        Returns:
            nested_comments (list of dict of str: str): List of nested comments dicts
    """
    nested_comments = list()
    for c in owl_property.comment:
        if c:
            nested_comments_template = {'rdfs:comment': {}}

            domains = list()
            for d in c.domain:
                if d and not isinstance(d, str):
                    domains.append('/'.join(build_nested_domains(d)[::-1]))

            for k, v in build_comments(c).items():
                nested_comments_template['rdfs:comment'][k] = v
            nested_comments_template['domain'] = [
                f'{PREFIX}:{d}' for d in domains]
            nested_comments.append(nested_comments_template)
    return nested_comments


def build_labels(owl_property: Any) -> Dict[str, str]:
    """Return dict of labels.

        Args:
            owl_property (Any): 
                Property of entity.
                Can be:  AnnotationPropertyClass, DataPropertyClass, ObjectPropertyClass.

        Returns:
            labels (dict of str: str): Dict of labels
    """
    labels = {}
    for l in label._get_indirect_values_for_class(owl_property):
        labels[l.lang] = str(l)
    # ?
    if not labels.items():
        for l in pot_label._get_indirect_values_for_class(owl_property):
            if isinstance(l, locstr):
                labels[l.lang] = str(l)
    return labels


def build_comments(owl_property: Any) -> Dict[str, str]:
    """Return dict of comments.

        Args:
            owl_property (Any): 
                Property of entity.
                Can be:  AnnotationPropertyClass, DataPropertyClass, ObjectPropertyClass.

        Returns:
            comments (list of dict of str: str): Dict of comments
    """
    comments = {}
    for c in comment._get_indirect_values_for_class(owl_property):
        comments[c.lang] = str(c)
    # ?
    if not comments.items():
        for c in pot_comment._get_indirect_values_for_class(owl_property):
            if isinstance(c, locstr):
                comments[c.lang] = str(c)
    return comments


def build_ranges(owl_property: Any) -> List[str]:
    """Return list of ranges.

        Args:
            owl_property (Any): 
                Property of entity.
                Can be:  AnnotationPropertyClass, DataPropertyClass.

        Returns:
            result_ranges (list of str): List of property ranges
    """
    result_ranges = list()
    for range_type in owl_range._get_indirect_values_for_class(owl_property):
        if isinstance(range_type, type):
            result_ranges.append(
                str(default_world._unabbreviate(base._universal_datatype_2_abbrev[range_type])).replace(
                    'http://www.w3.org/2001/XMLSchema#', 'xsd:'))
        else:
            result_ranges.append(str(range_type).replace('XMLSchema.', 'xsd:'))
    return result_ranges


def build_restrictions(owl_property: Any) -> List[str]:
    """Return list of restrictions.

        Args:
            owl_property (Any): 
                Property of entity.
                Can be:  AnnotationPropertyClass, DataPropertyClass, ObjectPropertyClass.

        Returns:
            result_restrictions (list of str): List of property restrictions
    """
    result_restrictions = []
    for restriction_type in restriction._get_indirect_values_for_class(owl_property):
        # TODO
        try:
            result_restrictions.append(
                str(default_world._unabbreviate(base._universal_datatype_2_abbrev[restriction_type])).replace(
                    'http://www.w3.org/2001/XMLSchema#', 'xsd:'))
        except:
            result_restrictions.append(
                str(restriction_type).replace('XMLSchema.', 'xsd:'))
    return result_restrictions


def build_attributes(rdf_class, onto) -> Set[Any]:
    """Return list of attributes.

        Args:
            owl_property (Any): 
                Property of entity.
                Can be:  AnnotationPropertyClass, DataPropertyClass, ObjectPropertyClass.

        Returns:
            total_attributes (Any): List of attributes
    """
    total_attributes = set()

    for a in onto.data_properties():
        if rdf_class.entity.ancestors().intersection(a.domain):
            total_attributes.add(a)

    for a in onto.object_properties():
        if rdf_class.entity.ancestors().intersection(a.domain):
            total_attributes.add(a)

    return total_attributes


def build_required(owl_property: Any) -> bool:
    """Is property required.

        Args:
            owl_property (Any): 
                Property of entity.
                Can be:  AnnotationPropertyClass, DataPropertyClass, ObjectPropertyClass.

        Returns:
            required_attr (bool): Is property required
    """
    required_attr = required._get_indirect_values_for_class(owl_property)
    if required_attr:
        return required_attr[0]
    return False


def build_domains(owl_property: Any, PREFIX='pot') -> List[str]:
    """Return list of property domains.

        Args:
            owl_property (Any):                 
                Property of entity.
                Can be: ObjectPropertyClass, AnnotationPropertyClass, DataPropertyClass.
        Returns:
            domains (list of str): List of property domains.
    """
    domains = list()
    for d in domain._get_indirect_values_for_class(owl_property):
        domains.append(f'{PREFIX}:{"/".join(build_nested_domains(d)[::-1])}')
    return domains


def build_subclass(owl_property: Any) -> List[Any]:
    """Return list of subclasses of entity.

        Args:
            owl_property (Any):
                Property of entity.
                Can be: ObjectPropertyClass, AnnotationPropertyClass, DataPropertyClass.
        Returns:
            (list): List of subclasses.
    """
    return list(subClassOf._get_indirect_values_for_class(owl_property))


def build_subproperty(owl_property: Any) -> List[Any]:
    """Return list of subproperties of entity.

        Args:
            owl_property (Any):
                Property of entity.
                Can be: ObjectPropertyClass, AnnotationPropertyClass, DataPropertyClass.
        Returns:
            (list): List of subproperties.
    """
    return list(subPropertyOf._get_indirect_values_for_class(owl_property))


def prop_get_full_id(owl_property: Any) -> str:
    """Return property id.

        Args:
            owl_property (Any):
                Property of entity.
                Can be: ObjectPropertyClass, AnnotationPropertyClass, DataPropertyClass.
        Returns:
            (str): Combined property id and property name.
    """
    property_id = ''
    subproperties = build_subproperty(owl_property)
    if subproperties and subproperties[0].name != 'topDataProperty':
        property_id = f'{prop_get_full_id(subproperties[0])}/'
    return f'{property_id}{owl_property.name}'


def class_get_full_id(entity: Any) -> str:
    """Return ThingClass id.

        Args:
            entity (Any): ThingClass entity.

        Returns:
            (str): Combined class id and entity name.
    """
    class_id = ''
    subclass = build_subclass(entity)
    if subclass and subclass[0] != Thing:
        class_id = f'{class_get_full_id(subclass[0])}/'
    return f'{class_id}{entity.name}'
