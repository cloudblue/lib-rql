#
#  Copyright © 2023 Ingram Micro Inc. All rights reserved.
#
from decimal import Decimal

from dateutil.parser import isoparse

from py_rql.constants import (
    RQL_EMPTY,
    RQL_FALSE,
    RQL_NULL,
    FilterTypes,
)


def cast_string(val):
    if val == RQL_EMPTY:
        return ''

    if val == RQL_NULL:
        return None

    return str(val)


def cast_boolean(val):
    if val == RQL_NULL:
        return None

    return val.lower() != RQL_FALSE


def get_default_cast_func_for_type(filter_type):
    mapping = {
        FilterTypes.INT: lambda val: None if val == RQL_NULL else int(val),
        FilterTypes.DECIMAL: lambda val: None if val == RQL_NULL else Decimal(val),
        FilterTypes.FLOAT: lambda val: None if val == RQL_NULL else float(val),
        FilterTypes.DATE: lambda val: None if val == RQL_NULL else isoparse(val).date(),
        FilterTypes.DATETIME: lambda val: None if val == RQL_NULL else isoparse(val),
        FilterTypes.STRING: cast_string,
        FilterTypes.BOOLEAN: cast_boolean,
    }
    return mapping[filter_type]
