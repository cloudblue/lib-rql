#
#  Copyright © 2022 Ingram Micro Inc. All rights reserved.
#
import pytest

from py_rql.cast import get_default_cast_func_for_type
from py_rql.constants import ComparisonOperators, FilterTypes, RQL_EMPTY, RQL_NULL
from py_rql.helpers import apply_operator
from py_rql.operators import get_operator_func_by_operator


@pytest.mark.parametrize(
    'value',
    ('10', '10.3', '0.00004831666666'),
)
@pytest.mark.parametrize(
    'filter_type',
    (FilterTypes.DECIMAL, FilterTypes.FLOAT),
)
@pytest.mark.parametrize(
    'op',
    (
        ComparisonOperators.EQ, ComparisonOperators.NE,
        ComparisonOperators.GE, ComparisonOperators.GT,
        ComparisonOperators.LE, ComparisonOperators.LT,
    ),
)
def test_numeric(mocker, filter_factory, filter_type, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': filter_type}])
    query = f'{op}(prop,{value})'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(filter_type)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        cast_func(value),
    )


@pytest.mark.parametrize(
    'value',
    ('10', '-10', '0'),
)
@pytest.mark.parametrize(
    'op',
    (
        ComparisonOperators.EQ, ComparisonOperators.NE,
        ComparisonOperators.GE, ComparisonOperators.GT,
        ComparisonOperators.LE, ComparisonOperators.LT,
    ),
)
def test_numeric_int(mocker, filter_factory, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.INT}])
    query = f'{op}(prop,{value})'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.INT)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        cast_func(value),
    )


@pytest.mark.parametrize(
    'filter_type',
    (
        FilterTypes.INT, FilterTypes.DECIMAL, FilterTypes.FLOAT,
        FilterTypes.DATE, FilterTypes.DATETIME,
    ),
)
@pytest.mark.parametrize('op', (ComparisonOperators.EQ, ComparisonOperators.NE))
def test_numeric_null(mocker, filter_factory, filter_type, op):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': filter_type}])
    query = f'{op}(prop,null())'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(filter_type)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        cast_func('null()'),
    )


@pytest.mark.parametrize(
    'op',
    (
        ComparisonOperators.EQ, ComparisonOperators.NE,
        ComparisonOperators.GE, ComparisonOperators.GT,
        ComparisonOperators.LE, ComparisonOperators.LT,
    ),
)
def test_numeric_date(mocker, filter_factory, op):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.DATE}])
    query = f'{op}(prop,2020-01-01)'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.DATE)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        cast_func('2020-01-01'),
    )


@pytest.mark.parametrize(
    'op',
    (
        ComparisonOperators.EQ, ComparisonOperators.NE,
        ComparisonOperators.GE, ComparisonOperators.GT,
        ComparisonOperators.LE, ComparisonOperators.LT,
    ),
)
def test_numeric_datetime(mocker, filter_factory, op):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.DATETIME}])
    query = f'{op}(prop,2022-02-08T07:57:57+01:00)'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.DATETIME)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        cast_func('2022-02-08T07:57:57+01:00'),
    )


@pytest.mark.parametrize('value', ('value', RQL_EMPTY, RQL_NULL))
@pytest.mark.parametrize('op', (ComparisonOperators.EQ, ComparisonOperators.NE))
def test_string(mocker, filter_factory, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.STRING}])
    query = f'{op}(prop,{value})'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.STRING)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        cast_func(value),
    )


@pytest.mark.parametrize(
    'value',
    ('true', 'false', 'TRUE', 'FALSE', RQL_NULL),
)
@pytest.mark.parametrize('op', (ComparisonOperators.EQ, ComparisonOperators.NE))
def test_boolean(mocker, filter_factory, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.BOOLEAN}])
    query = f'{op}(prop,{value})'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.BOOLEAN)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        cast_func(value),
    )
