#
#  Copyright © 2023 Ingram Micro Inc. All rights reserved.
#
import time
from threading import Thread

import pytest
from cachetools import LFUCache
from lark import Tree

from py_rql import parse
from py_rql.exceptions import RQLFilterParsingError
from py_rql.grammar import RQL_GRAMMAR
from py_rql.parser import RQLLarkParser


def test_parse_ok():
    assert isinstance(parse('a=b'), Tree)


def test_parse_fail():
    with pytest.raises(RQLFilterParsingError):
        parse('a=')


def test_parse_locks():
    class Cache(LFUCache):
        def pop(self, key):
            time.sleep(0.5)

            return super().pop(key)

    cache = Cache(maxsize=1)
    parser = RQLLarkParser(RQL_GRAMMAR, parser='lalr', start='start')
    parser._cache = cache
    parser.parse_query('a=b')

    def func1():
        parser.parse_query('b=c')

    has_exception = False

    def func2():
        nonlocal has_exception

        try:
            parser.parse_query('c=d')
        except KeyError:
            has_exception = True

    t1 = Thread(target=func1)
    t2 = Thread(target=func2)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert not has_exception
    assert hash('c=d') in cache
