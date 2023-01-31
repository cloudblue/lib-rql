#
#  Copyright © 2023 Ingram Micro Inc. All rights reserved.
#
import pytest

from py_rql.cast import get_default_cast_func_for_type
from py_rql.constants import FilterTypes, ListOperators
from py_rql.helpers import apply_operator
from py_rql.operators import get_operator_func_by_operator


@pytest.mark.parametrize(
    'value',
    (
        ['10', '10.3'],
        ['10', '-10.3'],
    ),
)
@pytest.mark.parametrize('filter_type', (FilterTypes.DECIMAL, FilterTypes.FLOAT))
@pytest.mark.parametrize('op', (ListOperators.RANGE,))
def test_numeric(mocker, filter_factory, filter_type, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': filter_type}])
    query = f'{op}(prop,{",".join(value)})'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(filter_type)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        [cast_func(v) for v in value],
    )


@pytest.mark.parametrize('value', (['10', '-103'],))
@pytest.mark.parametrize('op', (ListOperators.RANGE,))
def test_numeric_int(mocker, filter_factory, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.INT}])
    query = f'{op}(prop,{",".join(value)})'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.INT)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        [cast_func(v) for v in value],
    )


@pytest.mark.parametrize('value', (['2020-01-01', '1932-03-31'],))
@pytest.mark.parametrize('op', (ListOperators.RANGE,))
def test_numeric_date(mocker, filter_factory, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.DATE}])
    query = f'{op}(prop,{",".join(value)})'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.DATE)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        [cast_func(v) for v in value],
    )


@pytest.mark.parametrize('value', (['2022-02-08T07:57:57+01:00', '2022-02-08T07:57:57'],))
@pytest.mark.parametrize('op', (ListOperators.RANGE,))
def test_numeric_datetime(mocker, filter_factory, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.DATETIME}])
    query = f'{op}(prop,{",".join(value)})'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.DATETIME)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        [cast_func(v) for v in value],
    )
