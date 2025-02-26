import pytest
from src import create_app, db
from src.auth.models.user import User


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client):
    test_user = User(github_id=12345, username="test_user", access_token="test_token")
    with client.application.app_context():
        db.session.add(test_user)
        db.session.commit()
    return client
