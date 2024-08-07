#
#  Copyright © 2023 Ingram Micro Inc. All rights reserved.
#

from functools import partial

import pytest
from lark.exceptions import LarkError

from py_rql.constants import ComparisonOperators, LogicalOperators
from py_rql.parser import RQLParser
from tests.test_parser.utils import LogicalTransformer


def logical_transform(tpl, operator=None, exp1=None, exp2=None):
    return LogicalTransformer().transform(RQLParser.parse(tpl.format(
        operator=operator, exp1=exp1, exp2=exp2 or exp1,
    )))


def check_expression(logical_operator, expression_str, logical_result):
    grammar_key = LogicalOperators.get_grammar_key(logical_operator)
    assert grammar_key in logical_result
    for element in logical_result[grammar_key][0]:
        b = element in expression_str
        if element == ComparisonOperators.EQ:
            b = b or ('=' in expression_str)
        assert b

    if logical_operator != LogicalOperators.NOT:
        assert logical_result[grammar_key][0] == logical_result[grammar_key][1]


base_and_logical_transform = partial(logical_transform, '{operator}({exp1},{exp2})')
alias_and_logical_transform = partial(logical_transform, '{exp1}{operator}{exp2}')
base_or_logical_transform = partial(logical_transform, '{operator}({exp1},{exp2})')
alias_or_logical_transform = partial(logical_transform, '({exp1}{operator}{exp2})')
not_logical_transform = partial(logical_transform, '{operator}({exp1})', LogicalOperators.NOT)

ok_expressions = ['p=v', 'eq(p,v1)', 'p.p1=ge=25', 't__z="v v"']
fail_expressions = ['p=', 'and =ge=or', "'p=v'"]


@pytest.mark.parametrize('operator', ['&', ','])
@pytest.mark.parametrize('expression', ok_expressions)
def test_and_ok(operator, expression):
    base_result = base_and_logical_transform(LogicalOperators.AND, expression)
    check_expression(LogicalOperators.AND, expression, base_result)

    alias_result = alias_and_logical_transform(operator, expression)
    assert alias_result == base_result


@pytest.mark.parametrize('operator', ['|', ';'])
def test_or_ok_3(operator):
    query = '({logical})'.format(logical=operator.join(['a=b'] * 3))
    result = logical_transform(query)

    assert result == {
        LogicalOperators.get_grammar_key(LogicalOperators.OR): [
            (ComparisonOperators.EQ, 'a', 'b'),
            (ComparisonOperators.EQ, 'a', 'b'),
            (ComparisonOperators.EQ, 'a', 'b'),
        ],
    }


@pytest.mark.parametrize('operator', ['|', ';'])
@pytest.mark.parametrize('expression', ok_expressions)
def test_or_ok_2(operator, expression):
    base_result = base_or_logical_transform(LogicalOperators.OR, expression)
    check_expression(LogicalOperators.OR, expression, base_result)

    alias_result = alias_or_logical_transform(operator, expression)
    assert alias_result == base_result


@pytest.mark.parametrize('expression', ok_expressions)
def test_not_ok(expression):
    base_result = not_logical_transform(expression)
    check_expression(LogicalOperators.NOT, expression, base_result)


@pytest.mark.parametrize('operator', ['&', ',', '|', ';'])
@pytest.mark.parametrize('expression', fail_expressions)
def test_and_or_expression_fail(operator, expression):
    with pytest.raises(LarkError):
        alias_or_logical_transform(operator, expression)


@pytest.mark.parametrize('expression', fail_expressions)
def test_not_fail(expression):
    with pytest.raises(LarkError):
        not_logical_transform(expression)


@pytest.mark.parametrize('query', [
    'p.p1=12&p', 'p=v|t=z', 'v=1,,f=g', 'and(or(v,k),b)', '(p=v|k=l)&n=m)',
])
def test_logical_fail(query):
    with pytest.raises(LarkError):
        logical_transform(query)


@pytest.mark.parametrize('query', [
    '((p1=v1|p1=ge=v2)&(p3=le=v4,gt(p5,v6));ne(p7,p8))',
    '(or(p1=v1,p1=ge=v2)&(p3=le=v4,gt(p5,v6));ne(p7,p8))',
    '(or(p1=v1,p1=ge=v2)&and(p3=le=v4,gt(p5,v6));ne(p7,p8))',
    'or(and((p1=v1|p1=ge=v2),(p3=le=v4,gt(p5,v6))),ne(p7,p8))',
])
def test_logical_nesting_or(query):
    result = logical_transform(query)

    and_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.AND)
    or_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.OR)

    assert result == {
        or_grammar_key: [{
            and_grammar_key: [{
                or_grammar_key: [
                    (ComparisonOperators.EQ, 'p1', 'v1'),
                    (ComparisonOperators.GE, 'p1', 'v2'),
                ],
            }, {
                and_grammar_key: [
                    (ComparisonOperators.LE, 'p3', 'v4'),
                    (ComparisonOperators.GT, 'p5', 'v6'),
                ],
            }],
        }, (ComparisonOperators.NE, 'p7', 'p8')],
    }


@pytest.mark.parametrize('query', [
    '((p1=v1,or(p2=v2,p3=v3),and(p4=v4,p5=v5)))',
    '(p1=v1,or(p2=v2,p3=v3),and(p4=v4,p5=v5))',
    'and(p1=v1,or(p2=v2,p3=v3),and(p4=v4,p5=v5))',
    'p1=v1,(p2=v2|p3=v3),(p4=v4,p5=v5)',
])
def test_logical_nesting_and(query):
    result = logical_transform(query)

    and_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.AND)
    or_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.OR)

    assert result == {
        and_grammar_key: [
            ('eq', 'p1', 'v1'),
            {
                or_grammar_key: [
                    ('eq', 'p2', 'v2'),
                    ('eq', 'p3', 'v3'),
                ],
            },
            {
                and_grammar_key: [
                    ('eq', 'p4', 'v4'),
                    ('eq', 'p5', 'v5'),
                ],
            },
        ],
    }


def test_and_chain():
    q = 'ne(p1,v1)&p2=ge=and,or=v3'
    result = logical_transform(q)
    and_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.AND)
    assert result == {
        and_grammar_key: [
            {
                and_grammar_key: [
                    (ComparisonOperators.NE, 'p1', 'v1'),
                    (ComparisonOperators.GE, 'p2', 'and'),
                ],
            },
            (ComparisonOperators.EQ, 'or', 'v3'),
        ],
    }
    assert result == logical_transform('((ne(p1,v1)&p2=ge=and),or=v3)')


@pytest.mark.parametrize('query', (
    '(ne(p1,v1)|(p2=ge=and;or=v3)|p4=v4)',
    'or(ne(p1,v1),(ge(p2,and);or=v3),p4=v4)',
))
def test_or_chain(query):
    or_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.OR)
    result = logical_transform(query)
    assert result == {
        or_grammar_key: [
            (ComparisonOperators.NE, 'p1', 'v1'),
            {
                or_grammar_key: [
                    (ComparisonOperators.GE, 'p2', 'and'),
                    (ComparisonOperators.EQ, 'or', 'v3'),
                ],
            },
            (ComparisonOperators.EQ, 'p4', 'v4'),
        ],
    }


@pytest.mark.parametrize(
    'query',
    (
        '(not(id=fg))',
        '((not(id=fg)))',
        'not(eq(id,fg))',
        '((((not(id=fg)))))',
        'not((eq(id,fg)))',
    ),
)
def test_logical_tuple_and_not(query):
    result = logical_transform(query)

    not_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.NOT)

    assert result == {
        not_grammar_key: [(ComparisonOperators.EQ, 'id', 'fg')],
    }


def test_logical_tuple_and_not_w_and_nesting():
    result = logical_transform('((not(eq(id,fg)))&(not(ge(external_id,fg))))')

    and_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.AND)
    not_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.NOT)

    assert result == {
        and_grammar_key: [
            {not_grammar_key: [(ComparisonOperators.EQ, 'id', 'fg')]},
            {not_grammar_key: [(ComparisonOperators.GE, 'external_id', 'fg')]},
        ],
    }


def test_logical_tuple_nesting_ands_and_ors():
    result = logical_transform(
        '((((eq(id,*baba*))&(eq(external_id,*baba*))))|(((eq(id,*dziad*)))))',
    )

    and_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.AND)
    or_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.OR)

    assert result == {
        or_grammar_key: [
            {
                and_grammar_key: [
                    (ComparisonOperators.EQ, 'id', '*baba*'),
                    (ComparisonOperators.EQ, 'external_id', '*baba*'),
                ],
            },
            (ComparisonOperators.EQ, 'id', '*dziad*'),
        ],
    }


@pytest.mark.parametrize('query', ('((not(ilike(id,*8684*))))', ))
def test_logical_tuple_not_and_ilike(query):
    result = logical_transform(query)

    not_grammar_key = LogicalOperators.get_grammar_key(LogicalOperators.NOT)

    assert not_grammar_key in result
