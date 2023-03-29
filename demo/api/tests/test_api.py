import datetime
import os

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.backends import BACKENDS

import logging
import json

LOGGER = logging.getLogger(__name__)

client = TestClient(app)

VALID_SEARCH_BODY = {
    "datetime": "2025-01-01T00:00:00Z/2025-01-02T00:00:00Z",
    "geometry": {
        "type": "Point",
        "coordinates": [39.95, 75.16]
    }
}

def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_post_to_opportunities_with_no_body():
    response = client.post("/opportunities")
    assert response.status_code == 422


def test_post_to_opportunities_with_opportunities_body():
    response = client.post(
        "/opportunities",
        json={"product_id": "landsat-c2-l2", **VALID_SEARCH_BODY},
    )
    assert response.status_code == 200
    assert "features" in response.json()


@pytest.mark.parametrize("backend", ["fake", "historical"])
def test_post_to_opportunities_with_opportunities_body_and_header(backend: str):
    response = client.post(
        "/opportunities",
        headers={"Backend": backend},
        json={"product_id": "landsat-c2-l2", **VALID_SEARCH_BODY},
    )
    assert response.status_code == 200
    assert "features" in response.json()



@pytest.mark.parametrize("backend", ["planet"])
def test_post_to_opportunities_with_opportunities_body_and_header_authenticated(backend: str):
    token_name = f"{backend.upper()}_TOKEN"

    if token_name not in os.environ:
        # skip endpoint if token not provided
        return
    token = os.environ[token_name]

    start_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)
    end_time = start_time + datetime.timedelta(days=3)

    search_body_now = {
        "datetime":  f"{start_time.isoformat()}/{end_time.isoformat()}",
        "geometry": {
            "type": "Point",
            "coordinates": [39.95, 75.16]
        }
    }

    response = client.post(
        "/opportunities",
        headers={"Backend": backend, "Authorization": f"Bearer {token}"},
        json=search_body_now,
    )
    assert response.status_code == 200
    assert "features" in response.json()
    LOGGER.info(json.dumps(response.json(), indent=2))


def test_post_to_opportunities_with_bad_backend_raises():
    response = client.post(
        "/opportunities",
        headers={"Backend": "foo"},
        json=VALID_SEARCH_BODY,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == f"Backend 'foo' not in options: {list(BACKENDS.keys())}"
