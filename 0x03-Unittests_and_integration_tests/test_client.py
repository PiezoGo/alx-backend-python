#!/usr/bin/env python3

@patch.object(GithubOrgClient, "org", new_callable=unittest.mock.PropertyMock)
def test_public_repos_url(self, mock_org):
    mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}
    client = GithubOrgClient("test")
    result = client._public_repos_url
    self.assertEqual(result, "https://api.github.com/orgs/test/repos")
    mock_org.assert_called_once()

    @patch("client.get_json")
    @patch.object(GithubOrgClient, "_public_repos_url", new_callable=unittest.mock.PropertyMock)
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

        # Assertions
        self.assertEqual(result, ["repo1", "repo2", "repo3"])
        mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test/repos")


import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct payload
        and calls get_json with the right URL.
        """
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, expected_payload)


if __name__ == "__main__":
    unittest.main()
