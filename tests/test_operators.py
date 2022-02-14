#
#  Copyright © 2022 Ingram Micro Inc. All rights reserved.
#
import pytest

from py_rql import operators
from py_rql.constants import (
    ComparisonOperators, ListOperators,
    LogicalOperators, SearchOperators,
)


@pytest.mark.parametrize(
    ('op', 'iterable', 'expected'),
    (
        (operators.and_op, [True, True], True),
        (operators.and_op, [True, False], False),
        (operators.and_op, [False, False], False),
        (operators.or_op, [True, True], True),
        (operators.or_op, [True, False], True),
        (operators.or_op, [False, False], False),
    ),
)
def test_logical(op, iterable, expected):
    assert op(iterable) is expected


@pytest.mark.parametrize(
    ('op', 'iterable', 'expected'),
    (
        (operators.not_op, [True], False),
        (operators.not_op, [False], True),
    ),
)
def test_logical_not(op, iterable, expected):
    assert op(iterable) is expected


@pytest.mark.parametrize(
    ('op', 'a', 'b', 'expected'),
    (
        (operators.in_op, 'a', ['a', 'b'], True),
        (operators.in_op, 'c', ['a', 'b'], False),
        (operators.in_op, 'a', [], False),
        (operators.out_op, 'a', ['a', 'b'], False),
        (operators.out_op, 'c', ['a', 'b'], True),
        (operators.out_op, 'a', [], True),
    ),
)
def test_list(op, a, b, expected):
    assert op(a, b) is expected


@pytest.mark.parametrize(
    ('op', 'b', 'a', 'expected'),
    (
        (operators.like, 'test', 'test', True),
        (operators.like, 'test', 'This is a test', False),
        (operators.like, '*test', 'This is a test', True),
        (operators.like, '*test*', 'This is a test', True),
        (operators.like, 'test*', 'This is a test', False),
        (operators.like, 'This*', 'This is a test', True),
        (operators.like, 'TEST', 'test', False),
        (operators.like, 'TEST', 'This is a test', False),
        (operators.like, '*TEST', 'This is a test', False),
        (operators.like, '*TEST*', 'This is a test', False),
        (operators.like, 'TEST*', 'This is a test', False),
        (operators.like, 'THIS*', 'This is a test', False),
        (operators.ilike, 'test', 'test', True),
        (operators.ilike, 'test', 'This is a test', False),
        (operators.ilike, '*test', 'This is a test', True),
        (operators.ilike, '*test*', 'This is a test', True),
        (operators.ilike, 'test*', 'This is a test', False),
        (operators.ilike, 'This*', 'This is a test', True),
        (operators.ilike, 'TEST', 'test', True),
        (operators.ilike, 'TEST', 'This is a test', False),
        (operators.ilike, '*TEST', 'This is a test', True),
        (operators.ilike, '*TEST*', 'This is a test', True),
        (operators.ilike, 'TEST*', 'This is a test', False),
        (operators.ilike, 'THIS*', 'This is a test', True),
    ),
)
def test_search(op, a, b, expected):
    assert op(a, b) is expected


def get_operator_func_by_operator():
    assert ComparisonOperators.EQ == operators.eq
    assert ComparisonOperators.NE == operators.ne
    assert ComparisonOperators.GE == operators.ge
    assert ComparisonOperators.GT == operators.gt
    assert ComparisonOperators.LE == operators.le
    assert ComparisonOperators.LT == operators.lt
    assert ListOperators.IN == operators.in_op
    assert ListOperators.OUT == operators.out_op
    assert LogicalOperators.AND == operators.and_op
    assert LogicalOperators.OR == operators.or_op
    assert LogicalOperators.NOT == operators.not_op
    assert SearchOperators.LIKE == operators.like
    assert SearchOperators.I_LIKE == operators.ilike
