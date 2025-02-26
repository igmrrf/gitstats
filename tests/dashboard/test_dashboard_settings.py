import pytest
import json


def test_get_settings(auth_client):
    response = auth_client.get("/api/settings")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, dict)


def test_update_settings(auth_client):
    test_settings = {
        "theme": "dark",
        "chart_colors": "custom",
        "default_view": "repositories",
        "private_repos_visible": False,
    }

    response = auth_client.post(
        "/api/settings", data=json.dumps(test_settings), content_type="application/json"
    )
    assert response.status_code == 200

    # Verify settings were saved
    response = auth_client.get("/api/settings")
    data = response.get_json()
    assert data["theme"] == "dark"
    assert data["default_view"] == "repositories"
