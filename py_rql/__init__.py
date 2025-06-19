#
#  Copyright © 2025 CloudBlue. All rights reserved.
#

from py_rql.parser import RQLParser


def parse(query):
    """ Parses RQL query string into a syntax tree.

    :param str query: RQL query
    :return: Parsed tree
    :rtype: lark.Tree
    :raises: py_rql.exceptions.RQLFilterError
    """
    return RQLParser.parse_query(query)
