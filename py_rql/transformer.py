#
#  Copyright © 2023 Ingram Micro Inc. All rights reserved.
#
import functools

from lark import Transformer, Tree

from py_rql.constants import RQL_PLUS, ComparisonOperators
from py_rql.helpers import apply_logical_operator, apply_operator
from py_rql.operators import get_operator_func_by_operator


class BaseRQLTransformer(Transformer):
    def _extract_comparison(self, args):
        if len(args) == 2:
            # Notation: id=1  # noqa: E800
            operation = ComparisonOperators.EQ
            prop_index = 0
            value_index = 1

        elif args[0].data == 'comp_term':
            # Notation: eq(id,1)  # noqa: E800
            operation = self._get_value(args[0])
            prop_index = 1
            value_index = 2

        else:
            # Notation: id=eq=1
            operation = self._get_value(args[1])
            prop_index = 0
            value_index = 2

        return self._get_value(args[prop_index]), operation, self._get_value(args[value_index])

    def _get_value(self, obj):
        while isinstance(obj, Tree):
            obj = obj.children[0]

        return obj.value

    def sign_prop(self, args):
        if len(args) == 2:
            # has sign
            return '{0}{1}'.format(
                self._get_value(args[0]), self._get_value(args[1]),
            ).lstrip(RQL_PLUS)  # Plus is not needed in ordering

        return self._get_value(args[0])

    def term(self, args):
        return args[0]

    def expr_term(self, args):
        return args[0]

    def start(self, args):
        return args[0]


class RQLToFunctionTransformer(BaseRQLTransformer):
    def __init__(self, filter_cls):

        self.filter_cls = filter_cls

        self.__visit_tokens__ = False

    def logical(self, args):
        operation = args[0].data
        children = args[0].children

        operator = get_operator_func_by_operator(operation)

        return functools.partial(
            apply_logical_operator, operator, children,
        )

    def comp(self, args):
        prop, operation, val = self._extract_comparison(args)
        return self._get_func_for_lookup(prop, operation, val)

    def listing(self, args):
        operation, prop = self._get_value(args[0]), self._get_value(args[1])
        return self._get_func_for_lookup(
            prop,
            operation,
            [self._get_value(vtree) for vtree in args[2:]],
        )

    def searching(self, args):
        # like, ilike
        operation, prop, val = tuple(self._get_value(args[index]) for index in range(3))
        return self._get_func_for_lookup(prop, operation, val)

    def _get_func_for_lookup(self, prop, operation, val):
        self.filter_cls.validate_lookup(prop, operation)

        operator = get_operator_func_by_operator(operation)

        return functools.partial(
            apply_operator,
            prop,
            operator,
            self.filter_cls.cast_value(prop, val),
        )
