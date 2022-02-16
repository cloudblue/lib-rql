#
#  Copyright © 2022 Ingram Micro Inc. All rights reserved.
#
from unittest.mock import call

import pytest

from py_rql.constants import FilterTypes, LogicalOperators
from py_rql.helpers import apply_logical_operator
from py_rql.operators import get_operator_func_by_operator


@pytest.mark.parametrize('op', (LogicalOperators.AND, LogicalOperators.OR))
def test_logical_operators(mocker, filter_factory, op):
    functools = mocker.patch('py_rql.transformer.functools')
    children = [mocker.MagicMock(), mocker.MagicMock()]
    functools.partial.side_effect = children + [mocker.MagicMock()]
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.STRING}])
    term1 = 'eq(prop,val1)'
    term2 = 'like(prop,*val2*)'
    query = f'{op}({term1},{term2})'
    flt.filter(query, [])
    assert functools.partial.mock_calls[-1] == call(
        apply_logical_operator,
        get_operator_func_by_operator(f'{op}_op'),
        children,
    )
