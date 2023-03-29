import pytest
from fastapi.testclient import TestClient

from ..main import app
from ..backends import BACKENDS


client = TestClient(app)

VALID_SEARCH_BODY = {
    "datetime": "2025-01-01T00:00:00Z/2025-01-02T00:00:00Z",
    "bbox": [0,0,1,1]
}

def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_post_to_pineapple_with_no_body():
    response = client.post("/pineapple")
    assert response.status_code == 422


def test_post_to_pineapple_with_pineapple_body():
    response = client.post(
        "/pineapple",
        json=VALID_SEARCH_BODY,
    )
    assert response.status_code == 200
    assert "bbox" in response.json()
    assert "features" in response.json()


@pytest.mark.parametrize("backend", ["fake", "sentinel"])
def test_post_to_pineapple_with_pineapple_body_and_header(backend: str):
    response = client.post(
        "/pineapple",
        headers={"Backend": backend},
        json=VALID_SEARCH_BODY,
    )
    assert response.status_code == 200
    assert "bbox" in response.json()
    assert "features" in response.json()

# TODO currently failing
# def test_post_to_planet():
#     response = client.post(
#         "/pineapple",
#         headers={"Backend": "planet"}, # , "Authorization": f"Bearer {API_TOKEN}"},
#         json={
#             "bbox": [0,0,1,1],
#             "datetime": "2023-03-30T17:20:13.061Z" # this should be start and end eventually
#         },
#     )
#     assert response.status_code == 200
#     assert "bbox" in response.json()
#     assert "features" in response.json()


def test_post_to_pineapple_with_bad_backend_raises():
    response = client.post(
        "/pineapple",
        headers={"Backend": "foo"},
        json=VALID_SEARCH_BODY,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == f"Backend 'foo' not in options: {list(BACKENDS.keys())}"
