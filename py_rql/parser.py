#
#  Copyright © 2025 CloudBlue. All rights reserved.
#

from threading import Lock

from cachetools import LFUCache
from lark import Lark
from lark.exceptions import LarkError

from py_rql.exceptions import RQLFilterParsingError
from py_rql.grammar import RQL_GRAMMAR


class RQLLarkParser(Lark):
    CACHE_MAX_QUERY_LENGTH = 512

    def __init__(self, *args, **kwargs):
        super(RQLLarkParser, self).__init__(*args, **kwargs)

        self._cache = LFUCache(maxsize=1000)
        self._lock = Lock()

    def parse_query(self, query):
        cacheable = len(query) <= self.CACHE_MAX_QUERY_LENGTH

        if cacheable:
            cache_key = hash(query)

            try:
                return self._cache[cache_key]
            except KeyError:
                pass

        try:
            rql_ast = self.parse(query)
        except LarkError:
            raise RQLFilterParsingError()

        if cacheable:
            with self._lock:
                self._cache[cache_key] = rql_ast

        return rql_ast


RQLParser = RQLLarkParser(RQL_GRAMMAR, parser='lalr', start='start')
