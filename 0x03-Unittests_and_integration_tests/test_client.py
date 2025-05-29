#!/usr/bin/env python3
"""
Unit and integration tests for GithubOrgClient in client.py.
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class methods.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct payload.

        Args:
            org_name (str): The organization name to test.
            mock_get_json (Mock): Mock for the get_json function.
        """
        expected = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected)

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct repos URL from the mocked organization payload.
        """
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the expected repository names.

        Args:
            mock_get_json (Mock): Mock for get_json returning a list of repos.
        """
        test_repos = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_repos

        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test has_license returns True only when the license matches the provided key.

        Args:
            repo (dict): The repository data containing license info.
            license_key (str): The expected license key to check against.
            expected (bool): The expected result (True if license matches).
        """
        client = GithubOrgClient("testorg")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([{
    "ORG_PAYLOAD": org_payload,
    "REPOS_PAYLOAD": repos_payload,
    "EXPECTED_REPOS": expected_repos,
    "APACHE2_REPOS": apache2_repos,
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient using real-like API payloads (fixtures).
    Only external calls to requests.get are mocked.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up a patcher for requests.get before running all tests in the class.
        Uses side_effect to return different fixture payloads depending on URL.
        """
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Define side_effect to return different mock JSON responses based on URL
        mock_get.side_effect = lambda url: Mock(json=lambda: (
            cls.ORG_PAYLOAD if url == "https://api.github.com/orgs/google" else
            cls.REPOS_PAYLOAD if url == "https://api.github.com/orgs/google/repos" else
            None
        ))

    @classmethod
    def tearDownClass(cls):
        """
        Stop the requests.get patcher after all tests in the class have run.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Integration test that public_repos returns the expected repository names.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.EXPECTED_REPOS)

    def test_public_repos_with_license(self):
        """
        Integration test that public_repos returns only repos with a given license.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.APACHE2_REPOS)
