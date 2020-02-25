import owlready2
from owlready2 import label, comment, locstr, default_world, Thing
from class_helpers import readonly, required, subPropertyOf, range, restriction, subClassOf, domain, nest
from class_helpers import label as pot_label
from class_helpers import comment as pot_comment


def prop_get_full_id(prop):
    res = ''
    if list(subPropertyOf._get_indirect_values_for_class(prop)) and subPropertyOf._get_indirect_values_for_class(prop)[0].name != 'topDataProperty':
        res = prop_get_full_id(subPropertyOf._get_indirect_values_for_class(prop)[0])+'/'
    return res+prop.name


def class_get_full_id(prop):
    res = ''
    if list(subClassOf._get_indirect_values_for_class(prop)):
        if subClassOf._get_indirect_values_for_class(prop)[0] != Thing:
            res = class_get_full_id(subClassOf._get_indirect_values_for_class(prop)[0])+'/'
    return res+prop.name


def owl_property_context(prop):
    result = {
        '@id': 'pot:{}'.format(prop_get_full_id(prop)),
    }
    if nest._get_indirect_values_for_class(prop):
        result['@nest'] = nest._get_indirect_values_for_class(prop)[0].name
    return result


def build_annotations(prop, annotation, pot_annotation):
    labels = {}
    for l in annotation._get_indirect_values_for_class(prop):
        labels[l.lang] = str(l)

    if not labels.items():
        for l in pot_annotation._get_indirect_values_for_class(prop):
            if isinstance(l, locstr):
                labels[l.lang] = str(l)
    return labels


def build_ranges(prop, range_type):
    result_range = []
    for x in range_type._get_indirect_values_for_class(prop):
        try:
            result_range.append(
                str(default_world._unabbreviate(owlready2.base._universal_datatype_2_abbrev[x])).replace(
                    'http://www.w3.org/2001/XMLSchema#', 'xsd:'))
        except:
            result_range.append(str(x).replace('XMLSchema.', 'xsd:'))
    return result_range


def owl_property_to_python_base(prop):
    _type = default_world._unabbreviate(prop._owl_type).replace('http://www.w3.org/2002/07/owl#', 'owl:')
    result = {
        '@id': 'pot:{}'.format(prop_get_full_id(prop)),
        '@type': _type,
    }

    if list(subPropertyOf._get_indirect_values_for_class(prop)):
        result['subPropertyOf'] = 'pot:{}'.format(prop_get_full_id(subPropertyOf._get_indirect_values_for_class(prop)[0]))

    labels = build_annotations(prop, label, pot_label)

    if labels.items():
        result["rdfs:label"] = labels

    comments = build_annotations(prop, comment, pot_comment)
    if comments.items():
        result["rdfs:comment"] = comments
    return result

def owl_property_to_python_for_definition(prop):
    result = owl_property_to_python_base(prop)
    try:
        result['pot:required'] = required._get_indirect_values_for_class(prop)[0]
    except:
        pass

    try:
        result['pot:readonly'] = readonly._get_indirect_values_for_class(prop)[0]
    except:
        pass

    if list(range._get_indirect_values_for_class(prop)):
        result['pot:valueType'] = build_ranges(prop, range)

    if list(restriction._get_indirect_values_for_class(prop)):
        result['xsd:restriction'] = build_ranges(prop, restriction)

    return result


def owl_property_to_python_for_vocabulary(prop):
    result = owl_property_to_python_base(prop)

    if list(range._get_indirect_values_for_class(prop)):
        result['pot:valueType'] = build_ranges(prop, range)

    if list(restriction._get_indirect_values_for_class(prop)):
        result['xsd:restriction'] = build_ranges(prop, restriction)

    domains = []
    for d in domain._get_indirect_values_for_class(prop):
        domains.append('pot:{}'.format(d.name))
    if domains:
        result['domain'] = domains

    return result
