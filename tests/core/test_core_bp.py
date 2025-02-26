import pytest

from src import create_app
from src.common.db import db


@pytest.fixture
def client():
    """Flask test client with a database"""
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


def test_core_index(client):
    """Test the index client route"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"health": "healthy"}
