#
#  Copyright © 2023 Ingram Micro Inc. All rights reserved.
#
import pytest

from py_rql.filter_cls import FilterClass


@pytest.fixture
def filter_factory():
    def _filter(filters):
        class TestFilter(FilterClass):
            FILTERS = filters
        return TestFilter()
    return _filter
