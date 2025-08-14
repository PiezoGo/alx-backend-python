#!/usr/bin/env python3
"""
Unit tests for:
- utils.access_nested_map
- utils.get_json
- utils.memoize
"""
import unittest
from typing import Any, Dict, Tuple
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Dict[str, Any],
        path: Tuple[str, ...],
        expected: Any
    ) -> None:
        """Test correct return values for valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Dict[str, Any],
        path: Tuple[str, ...],
        expected_msg: str
    ) -> None:
        """Test that KeyError is raised for missing keys."""
        with self.assertRaisesRegex(KeyError, expected_msg):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for get_json (mocking HTTP calls)."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict[str, Any]
    ) -> None:
        """Test that get_json returns expected result."""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            self.assertEqual(get_json(test_url), test_payload)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator."""

    def test_memoize(self) -> None:
        """Test that memoize calls the method only once."""

        class TestClass:
            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                return self.a_method()

                test_obj = TestClass()
        with patch.object(
            TestClass,
            "a_method",
            return_value=42
        ) as mock_method:
            first_call = test_obj.a_property
            second_call = test_obj.a_property
            self.assertEqual(first_call, 42)
            self.assertEqual(second_call, 42)
            mock_method.assert_called_once()



if __name__ == "__main__":
    unittest.main()
