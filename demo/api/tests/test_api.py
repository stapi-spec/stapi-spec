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
        headers={"Authorization": "fake-token"},
        json={"bbox": [0,0,1,1]},
    )
    assert response.status_code == 200
    assert "bbox" in response.json()
    assert "features" in response.json()