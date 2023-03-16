#
#  Copyright © 2023 Ingram Micro Inc. All rights reserved.
#
def extract_value(obj, prop):
    current = obj
    tokens = prop.split('.')
    for t in tokens:
        if not isinstance(current, dict) or t not in current:
            raise KeyError()
        current = current[t]
    return current


def apply_operator(prop, operator, value, obj):
    try:
        prop_value = extract_value(obj, prop)
    except KeyError:
        prop_value = None
    result = operator(prop_value, value)
    return result


def apply_logical_operator(operator_func, terms, obj):
    evaluated = [term(obj) for term in terms]
    return operator_func(evaluated)
