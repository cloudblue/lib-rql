#
#  Copyright © 2023 Ingram Micro Inc. All rights reserved.
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
