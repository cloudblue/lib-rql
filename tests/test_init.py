#
#  Copyright © 2022 Ingram Micro Inc. All rights reserved.
#
import pytest
from lark import Tree

from py_rql import parse
from py_rql.exceptions import RQLFilterParsingError


def test_parse_ok():
    assert isinstance(parse('a=b'), Tree)


def test_parse_fail():
    with pytest.raises(RQLFilterParsingError):
        parse('a=')
