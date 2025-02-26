import pytest
from unittest.mock import patch


def test_generate_resume(auth_client):
    with patch("openai.ChatCompletion.create") as mock_openai, patch(
        "app.github_api.GitHubAPI.get_user_repos"
    ) as mock_repos:

        mock_repos.return_value = [
            {
                "name": "test-repo",
                "description": "A test repository",
                "stargazers_count": 10,
            }
        ]

        mock_openai.return_value.choices[0].message.content = "Test Resume Content"

        response = auth_client.get("/api/generate-resume")
        assert response.status_code == 200
        data = response.get_json()
        assert "resume" in data
        assert data["resume"] == "Test Resume Content"
