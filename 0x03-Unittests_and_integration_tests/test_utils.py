#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map (Tasks 0 and 1).
"""
import unittest
from typing import Any, Dict, Tuple
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self, nested_map: Dict[str, Any], path: Tuple[str, ...], expected: Any
    ) -> None:
        """Test correct return values for valid paths."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(
        self, nested_map: Dict[str, Any], path: Tuple[str, ...], expected_msg: str
    ) -> None:
        """Test that KeyError is raised for missing keys."""
        with self.assertRaisesRegex(KeyError, expected_msg):
            access_nested_map(nested_map, path)


if __name__ == "__main__":
    unittest.main()
