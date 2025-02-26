import pytest
from unittest.mock import patch


def test_language_stats(auth_client):
    with patch("app.github_api.GitHubAPI.get_user_repos") as mock_repos, patch(
        "app.github_api.GitHubAPI.get_repo_languages"
    ) as mock_languages:

        mock_repos.return_value = [{"name": "test-repo", "full_name": "user/test-repo"}]
        mock_languages.return_value = {"Python": 1000, "JavaScript": 500}

        response = auth_client.get("/api/insights/languages")
        assert response.status_code == 200
        data = response.get_json()
        assert "languages" in data
        assert "Python" in data["languages"]


def test_commit_patterns(auth_client):
    with patch("app.github_api.GitHubAPI.get_user_repos") as mock_repos, patch(
        "app.github_api.GitHubAPI.get_commit_activity"
    ) as mock_activity:

        mock_repos.return_value = [{"name": "test-repo", "full_name": "user/test-repo"}]
        mock_activity.return_value = [{"days": [1, 2, 3, 4, 5, 6, 7]}]

        response = auth_client.get("/api/insights/commit-patterns")
        assert response.status_code == 200
        data = response.get_json()
        assert "daily_patterns" in data
        assert "peak_day" in data
