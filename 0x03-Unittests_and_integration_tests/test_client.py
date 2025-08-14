#!/usr/bin/env python3
"""
Unit and Integration tests for client.py
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license returns True if repo has the license_key,
        otherwise returns False.
        """
        client = GithubOrgClient("test")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD[0][0],
        "repos_payload": TEST_PAYLOAD[0][1],
        "expected_repos": TEST_PAYLOAD[0][2],
        "apache2_repos": TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and GithubOrgClient.org before tests"""
        config = {
            "return_value.json.side_effect": [
                cls.org_payload, cls.repos_payload
            ]
        }
        cls.get_patcher = patch("requests.get", **config)
        cls.mock_get = cls.get_patcher.start()

        cls.org_patcher = patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value=cls.org_payload
        )
        cls.mock_org = cls.org_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop all patches after tests"""
        cls.get_patcher.stop()
        cls.org_patcher.stop()

    def test_public_repos(self):
        """Test public_repos without license filter"""
        client = GithubOrgClient("test")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with a license filter"""
        client = GithubOrgClient("test")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


if __name__ == "__main__":
    unittest.main()
