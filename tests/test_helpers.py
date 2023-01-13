#
#  Copyright © 2023 Ingram Micro Inc. All rights reserved.
#
import pytest

from py_rql.helpers import apply_logical_operator, apply_operator, extract_value


@pytest.mark.parametrize(
    ('src', 'path', 'expected'),
    (
        ({'root': 'val'}, 'root', 'val'),
        ({'root': None}, 'root', None),
        ({'root': True}, 'root', True),
        ({'root': {'level1': 'val'}}, 'root.level1', 'val'),
        ({'root': {'level1': None}}, 'root.level1', None),
        ({'root': {'level1': True}}, 'root.level1', True),
        ({'root': {'level1': True}}, 'root', {'level1': True}),
        ({'root': {'level1': {'level2': 'val'}}}, 'root.level1.level2', 'val'),
        ({'root': {'level1': {'level2': None}}}, 'root.level1.level2', None),
        ({'root': {'level1': {'level2': True}}}, 'root.level1.level2', True),
        ({'root': {'level1': {'level2': True}}}, 'root.level1', {'level2': True}),
        ({'root': {'level1': {'level2': True}}}, 'root', {'level1': {'level2': True}}),
    ),
)
def test_extract_value(src, path, expected):
    assert extract_value(src, path) == expected


@pytest.mark.parametrize(
    ('src', 'path'),
    (
        ({'root': 'val'}, 'other'),
        ({'root': {'level1': 'val'}}, 'root.other'),
        ({'root': {'level1': {'level2': 'val'}}}, 'root.level1.other'),
    ),
)
def test_extract_value_keyerror(src, path):
    with pytest.raises(KeyError):
        extract_value(src, path)


def test_apply_operator(mocker):
    mocked_op = mocker.MagicMock(return_value=True)
    assert apply_operator('root', mocked_op, 'value_b', {'root': 'value_a'}) is True
    mocked_op.assert_called_once_with('value_a', 'value_b')


def test_apply_operator_prop_not_found(mocker):
    mocked_op = mocker.MagicMock(return_value=True)
    assert apply_operator('other', mocked_op, 'value_b', {'root': 'value_a'}) is False
    mocked_op.assert_not_called()


def test_apply_logical_operator(mocker):
    mocked_op = mocker.MagicMock(return_value=True)
    children = [mocker.MagicMock(return_value=True), mocker.MagicMock(return_value=False)]
    assert apply_logical_operator(mocked_op, children, {'root': 'value_a'}) is True
    mocked_op.assert_called_once_with([True, False])
    for child in children:
        child.assert_called_once_with({'root': 'value_a'})
