import pytest
from fastapi.testclient import TestClient

from insnail_ai_tools.web import create_fast_api_app, create_flask_app

fast_app = create_fast_api_app(cors=True, health_check=True)
fast_client = TestClient(fast_app)

flask_app = create_flask_app(__name__)
flask_client = flask_app.test_client()


def test_fast_api_health_check():
    response = fast_client.get("/health-check")
    assert response.status_code == 200


def test_flask_app_health_check():
    rv = flask_client.get("/health-check")
    assert rv.status_code == 200
