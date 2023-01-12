#
#  Copyright © 2023 Ingram Micro Inc. All rights reserved.
#
from cachetools import LFUCache

from py_rql import parse
from py_rql.cast import get_default_cast_func_for_type
from py_rql.constants import RESERVED_FILTER_NAMES, FilterLookups, FilterTypes
from py_rql.exceptions import RQLFilterLookupError
from py_rql.transformer import RQLToFunctionTransformer


class FilterClass:

    FILTERS = []

    def __init__(self):
        self._cache = LFUCache(maxsize=1000)
        self._filters = self.init_filters()

    def init_filters(self):
        filters = {}
        for filter_decl in self.FILTERS:
            filter_name = filter_decl['filter']
            e = f"'{filter_name}' is a reserved filter name."
            assert filter_name not in RESERVED_FILTER_NAMES, e

            filter_type = filter_decl.get('type', FilterTypes.STRING)
            default_lookups = self.default_filter_lookups_for_type(filter_type)
            lookups = filter_decl.get('lookups', default_lookups)
            e = f"Invalid lookups for filter '{filter_name}' of type '{filter_type}': '{lookups}'"
            assert set(lookups).issubset(default_lookups), e

            cast_func = filter_decl.get(
                'cast_func',
                get_default_cast_func_for_type(filter_type),
            )
            e = f"Invalid cast function for filter '{filter_name}'."
            assert callable(cast_func), e

            filters[filter_name] = {
                'type': filter_type,
                'lookups': lookups,
                'cast_func': cast_func,
            }
        return filters

    def transform_query(self, query):
        key = hash(query)
        if key in self._cache:
            return self._cache[key]
        transformer = RQLToFunctionTransformer(self)
        filter_func = transformer.transform(parse(query))
        self._cache[key] = filter_func
        return filter_func

    def cast_value(self, prop, value):
        value = self.remove_quotes(value)
        cast_func = self._filters[prop]['cast_func']
        if isinstance(value, list):
            return [cast_func(el) for el in value]
        return cast_func(value)

    def filter(self, query, iterable):
        filter_func = self.transform_query(query)
        return filter(filter_func, iterable)

    def validate_lookup(self, prop, lookup):
        if lookup not in self._filters[prop]['lookups']:
            raise RQLFilterLookupError(
                details={'error': f'Lookup {lookup} not available for filter {prop}.'},
            )

    @staticmethod
    def default_filter_lookups_for_type(filter_type):
        lookups = {
            FilterTypes.INT: FilterLookups.numeric(),
            FilterTypes.DECIMAL: FilterLookups.numeric(),
            FilterTypes.FLOAT: FilterLookups.numeric(),
            FilterTypes.DATE: FilterLookups.numeric(),
            FilterTypes.DATETIME: FilterLookups.numeric(),
            FilterTypes.STRING: FilterLookups.string(),
            FilterTypes.BOOLEAN: FilterLookups.boolean(),
        }
        return lookups[filter_type]

    @staticmethod
    def remove_quotes(str_value):
        return str_value[1:-1] if str_value and str_value[0] in ('"', "'") else str_value
