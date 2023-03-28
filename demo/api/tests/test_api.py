import pytest
from fastapi.testclient import TestClient

from ..main import app


client = TestClient(app)

def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_post_to_pineapple_with_no_body():
    response = client.post("/pineapple")
    assert response.status_code == 200
    assert "bbox" in response.json()
    assert "features" in response.json()


def test_post_to_pineapple_with_pineapple_body():
    response = client.post(
        "/pineapple",
        json={"bbox": [0,0,1,1]},
    )
    assert response.status_code == 200
    assert "bbox" in response.json()
    assert "features" in response.json()


@pytest.mark.parametrize("backend", ["fake", "sentinel"])
def test_post_to_pineapple_with_pineapple_body_and_header(backend):
    response = client.post(
        "/pineapple",
        headers={"Backend": backend},
        json={"bbox": [0,0,1,1]},
    )
    assert response.status_code == 200
    assert "bbox" in response.json()
    assert "features" in response.json()


def test_post_to_pineapple_with_bad_backend_raises():
    response = client.post(
        "/pineapple",
        headers={"Backend": "foo"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Backend 'foo' not in options: ['fake', 'sentinel']"
