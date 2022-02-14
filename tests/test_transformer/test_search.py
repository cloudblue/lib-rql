#
#  Copyright © 2022 Ingram Micro Inc. All rights reserved.
#
import pytest

from py_rql.cast import get_default_cast_func_for_type
from py_rql.constants import FilterTypes, SearchOperators
from py_rql.helpers import apply_operator
from py_rql.operators import get_operator_func_by_operator


@pytest.mark.parametrize('value', ('value', '*value', 'value*', '*value*'))
@pytest.mark.parametrize('op', (SearchOperators.LIKE, SearchOperators.I_LIKE))
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
