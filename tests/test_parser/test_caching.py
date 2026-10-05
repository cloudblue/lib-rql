#
#  Copyright © 2025 CloudBlue. All rights reserved.
#
import pytest

from py_rql.exceptions import RQLFilterParsingError
from py_rql.parser import RQLParser


def test_cache():
    cache = RQLParser._cache
    cache.clear()

    ast = RQLParser.parse_query('a=b')
    assert RQLParser.parse_query('b=c&x=g')
    assert RQLParser.parse_query('a=b') == ast

    with pytest.raises(RQLFilterParsingError):
        RQLParser.parse_query('&')

    assert cache.maxsize == 1000
    assert cache.currsize == 2
    assert cache.get(hash('a=b')) == ast
    assert cache.get(hash('b=c&x=g'))


def test_query_over_length_limit_is_not_cached():
    cache = RQLParser._cache
    cache.clear()

    query = '&'.join(['a=b'] * 200)
    assert len(query) > RQLParser.CACHE_MAX_QUERY_LENGTH

    assert RQLParser.parse_query(query)
    assert cache.currsize == 0


def test_query_at_length_limit_is_cached():
    cache = RQLParser._cache
    cache.clear()

    query = 'a=' + 'b' * (RQLParser.CACHE_MAX_QUERY_LENGTH - 2)
    assert len(query) == RQLParser.CACHE_MAX_QUERY_LENGTH

    assert RQLParser.parse_query(query)
    assert cache.currsize == 1
