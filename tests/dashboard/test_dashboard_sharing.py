import pytest
from app.models import User


def test_generate_share_link(auth_client):
    response = auth_client.get("/api/generate-share-link")
    assert response.status_code == 200
    data = response.get_json()
    assert "share_url" in data
    assert "profile" in data["share_url"]


def test_view_shared_profile(client):
    # Create a user with a known profile URL
    test_user = User(
        github_id=12346, username="share_test_user", profile_url="test-profile-url"
    )
    with client.application.app_context():
        db.session.add(test_user)
        db.session.commit()

    response = client.get("/profile/test-profile-url")
    assert response.status_code == 200
    assert b"share_test_user" in response.data
