#!/usr/bin/env python3
"""
Unit tests for utils.py functions:
- access_nested_map
- get_json
- memoize decorator
"""

from parameterized import parameterized
from unittest.mock import patch, Mock
import pytest
from utils import access_nested_map, get_json, memoize


@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(nested_map, path, expected):
    """Test that access_nested_map returns the expected value"""
    assert access_nested_map(nested_map, path) == expected


@parameterized.expand([
    ({}, ("a",)),
    ({"a": 1}, ("a", "b")),
])
def test_access_nested_map_exception(nested_map, path):
    """Test that access_nested_map raises KeyError with invalid path"""
    with pytest.raises(KeyError) as excinfo:
        access_nested_map(nested_map, path)
    missing_key = excinfo.value.args[0]
    # Check the missing key matches expected last key in path that fails
    expected_key = path[len(path) - 1]
    assert missing_key == expected_key


@parameterized.expand([
    ("http://example.com", {"payload": True}),
    ("http://holberton.io", {"payload": False}),
])
def test_get_json(test_url, test_payload):
    """Test that get_json returns the expected payload from a URL"""
    mock_response = Mock()
    mock_response.json.return_value = test_payload

    with patch("utils.requests.get", return_value=mock_response) as mock_get:
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        assert result == test_payload


def test_memoize():
    """Test that a memoized method is only called once"""

    class TestClass:
        def a_method(self):
            return 42

        @memoize
        def a_property(self):
            return self.a_method()

    with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
        test_instance = TestClass()
        result1 = test_instance.a_property
        result2 = test_instance.a_property

        assert result1 == 42
        assert result2 == 42
        mock_method.assert_called_once()
