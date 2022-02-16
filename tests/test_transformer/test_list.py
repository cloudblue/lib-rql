#
#  Copyright © 2022 Ingram Micro Inc. All rights reserved.
#
import pytest

from py_rql.cast import get_default_cast_func_for_type
from py_rql.constants import FilterTypes, ListOperators, RQL_EMPTY, RQL_NULL
from py_rql.helpers import apply_operator
from py_rql.operators import get_operator_func_by_operator


@pytest.mark.parametrize(
    'value',
    (
        ['10', '10.3', '0.00004831666666'],
        ['10', '-10.3', RQL_NULL],
    ),
)
@pytest.mark.parametrize('filter_type', (FilterTypes.DECIMAL, FilterTypes.FLOAT))
@pytest.mark.parametrize('op', (ListOperators.IN, ListOperators.OUT))
def test_numeric(mocker, filter_factory, filter_type, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': filter_type}])
    query = f'{op}(prop,({",".join(value)}))'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(filter_type)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        [cast_func(v) for v in value],
    )


@pytest.mark.parametrize('value', (['10', '-103', '0', RQL_NULL],))
@pytest.mark.parametrize('op', (ListOperators.IN, ListOperators.OUT))
def test_numeric_int(mocker, filter_factory, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.INT}])
    query = f'{op}(prop,({",".join(value)}))'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.INT)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        [cast_func(v) for v in value],
    )


@pytest.mark.parametrize('value', (['2020-01-01', '1932-03-31', RQL_NULL],))
@pytest.mark.parametrize('op', (ListOperators.IN, ListOperators.OUT))
def test_numeric_date(mocker, filter_factory, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.DATE}])
    query = f'{op}(prop,({",".join(value)}))'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.DATE)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        [cast_func(v) for v in value],
    )


@pytest.mark.parametrize('value', (['2022-02-08T07:57:57+01:00', '2022-02-08T07:57:57', RQL_NULL],))
@pytest.mark.parametrize('op', (ListOperators.IN, ListOperators.OUT))
def test_numeric_datetime(mocker, filter_factory, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.DATETIME}])
    query = f'{op}(prop,({",".join(value)}))'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.DATETIME)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        [cast_func(v) for v in value],
    )


@pytest.mark.parametrize('value', (['value', RQL_EMPTY, RQL_NULL],))
@pytest.mark.parametrize('op', (ListOperators.IN, ListOperators.OUT))
def test_string(mocker, filter_factory, op, value):
    functools = mocker.patch('py_rql.transformer.functools')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.STRING}])
    query = f'{op}(prop,({",".join(value)}))'
    flt.filter(query, [])
    cast_func = get_default_cast_func_for_type(FilterTypes.STRING)
    functools.partial.assert_called_once_with(
        apply_operator,
        'prop',
        get_operator_func_by_operator(op),
        [cast_func(v) for v in value],
    )
