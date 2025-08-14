#!/usr/bin/env python3
"""
Unit tests for client.py
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        test_payload = {"payload": True}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct link"""
        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            client = GithubOrgClient("test")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/test/repos"
            )

    @patch("client.get_json")
    @patch.object(
        GithubOrgClient,
        "_public_repos_url",
        new_callable=PropertyMock
    )
    def test_public_repos(self, mock_repos_url, mock_get_json):
        """
        Test that public_repos returns a list of repo names
        and that get_json is called with the correct URL.
        """
        mock_repos_url.return_value = "https://api.github.com/orgs/test/repos"
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        client = GithubOrgClient("test")
        result = client.public_repos()

        self.assertEqual(result, ["repo1", "repo2", "repo3"])
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/test/repos"
        )


if __name__ == "__main__":
    unittest.main()
