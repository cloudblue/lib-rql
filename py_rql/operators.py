#
#  Copyright © 2023 Ingram Micro Inc. All rights reserved.
#
from operator import (  # noqa: F401
    eq,
    ge,
    gt,
    le,
    lt,
    ne,
)

from py_rql.constants import (
    ComparisonOperators,
    ListOperators,
    LogicalOperators,
    SearchOperators,
)


def and_op(iterable):
    return all(iterable)


def or_op(iterable):
    return any(iterable)


def not_op(a):
    return not a[0]


def in_op(a, b):
    return a in b


def out_op(a, b):
    return a not in b


def like(a, b):
    if b[0] == '*' and b[-1] == '*':
        return b[1:-1] in a

    if b[0] == '*':
        return a.endswith(b[1:])

    if b[-1] == '*':
        return a.startswith(b[:-1])
    return a == b


def ilike(a, b):
    return like(a.lower(), b.lower())


def get_operator_func_by_operator(op):
    mapping = {
        ComparisonOperators.EQ: eq,
        ComparisonOperators.NE: ne,
        ComparisonOperators.GE: ge,
        ComparisonOperators.GT: gt,
        ComparisonOperators.LE: le,
        ComparisonOperators.LT: lt,
        ListOperators.IN: in_op,
        ListOperators.OUT: out_op,
        f'{LogicalOperators.AND}_op': and_op,
        f'{LogicalOperators.OR}_op': or_op,
        f'{LogicalOperators.NOT}_op': not_op,
        SearchOperators.LIKE: like,
        SearchOperators.I_LIKE: ilike,
    }
    return mapping[op]
