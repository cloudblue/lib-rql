#
#  Copyright © 2022 Ingram Micro Inc. All rights reserved.
#
import pytest

from py_rql.constants import FilterLookups, FilterTypes, RESERVED_FILTER_NAMES
from py_rql.exceptions import RQLFilterLookupError
from py_rql.filter_cls import FilterClass


@pytest.mark.parametrize('filter_name', RESERVED_FILTER_NAMES)
def test_init_filters_reserved_names(filter_factory, filter_name):
    with pytest.raises(AssertionError) as cv:
        filter_factory([{'filter': filter_name, 'type': FilterTypes.STRING}])
    assert str(cv.value) == f"'{filter_name}' is a reserved filter name."


def test_init_filters_invalid_lookup(filter_factory):
    with pytest.raises(AssertionError) as cv:
        filter_factory(
            [
                {
                    'filter': 'prop',
                    'type': FilterTypes.INT,
                    'lookups': {FilterLookups.LIKE},
                },
            ],
        )
    assert str(cv.value) == (
        "Invalid lookups for filter 'prop' of type 'int': '{'like'}'"
    )


def test_init_filters_invalid_cast_func(filter_factory):
    with pytest.raises(AssertionError) as cv:
        filter_factory(
            [
                {
                    'filter': 'prop',
                    'cast_func': 'hello',
                },
            ],
        )
    assert str(cv.value) == "Invalid cast function for filter 'prop'."


def test_validate_lookup(filter_factory):
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.STRING}])
    assert flt.validate_lookup('prop', FilterLookups.EQ) is None


def test_validate_lookup_invalid_lookup(filter_factory):
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.STRING}])
    with pytest.raises(RQLFilterLookupError) as cv:
        flt.validate_lookup('prop', FilterLookups.LT)

    assert cv.value.details == {'error': 'Lookup lt not available for filter prop.'}


def test_transform_query(filter_factory):
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.STRING}])
    fn = flt.transform_query('eq(prop,value)')
    assert callable(fn) is True


def test_transform_query_cache(filter_factory):
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.STRING}])
    flt.transform_query('eq(prop,value)')
    key = hash('eq(prop,value)')
    assert key in flt._cache


def test_transform_query_hit_cache(mocker, filter_factory):
    mocked_parse = mocker.patch('py_rql.filter_cls.parse')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.STRING}])
    fn = mocker.MagicMock()
    key = hash('eq(prop,value)')
    flt._cache[key] = fn
    assert flt.transform_query('eq(prop,value)') == fn
    mocked_parse.assert_not_called()


def test_filter(mocker, filter_factory):
    fn = mocker.MagicMock()
    mocked_transform = mocker.patch.object(FilterClass, 'transform_query', return_value=fn)
    mocked_filter = mocker.patch('py_rql.filter_cls.filter')
    flt = filter_factory([{'filter': 'prop', 'type': FilterTypes.STRING}])
    flt.filter('query', 'iterable')
    mocked_transform.assert_called_once_with('query')
    mocked_filter.assert_called_once_with(fn, 'iterable')
