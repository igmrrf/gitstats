import pytest
from unittest.mock import patch
from src.auth.models import User


def test_login_route(client):
    response = client.get("/auth/login")
    assert response.status_code == 302
    assert "github.com/login/oauth/authorize" in response.location


def test_github_callback(client):
    with patch("requests.post") as mock_post, patch("requests.get") as mock_get:
        mock_post.return_value.json.return_value = {"access_token": "test_token"}
        mock_get.return_value.json.return_value = {"id": 12345, "login": "test_user"}

        response = client.get("/auth/callback?code=test_code")
        assert response.status_code == 302

        user = User.query.filter_by(github_id=12345).first()
        assert user is not None
        assert user.username == "test_user"


def test_logout(auth_client):
    response = auth_client.get("/auth/logout")
    assert response.status_code == 302
