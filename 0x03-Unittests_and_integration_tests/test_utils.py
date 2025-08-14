#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map (Task 0).
"""
import unittest
from typing import Any, Dict, Tuple
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map (happy paths)."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self, nested_map: Dict[str, Any], path: Tuple[str, ...], expected: Any
    ) -> None:
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == "__main__":
    unittest.main()
