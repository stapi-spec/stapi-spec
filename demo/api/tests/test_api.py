import datetime
import json
import logging
import os
from typing import Optional, Tuple

import pytest
from api.backends import BACKENDS
from api.main import app
from api.models import Opportunity, Order
from fastapi.testclient import TestClient

LOGGER = logging.getLogger(__name__)

client = TestClient(app)

VALID_SEARCH_BODY = {
    "datetime": "2025-01-01T00:00:00Z/2025-01-02T00:00:00Z",
    "geometry": {"type": "Point", "coordinates": [-75.16, 39.95]},
    "product_id": "landsat-c2-l2",
}

PLANET_TOKEN = os.environ.get("PLANET_TOKEN")
BLACKSKY_TOKEN = os.environ.get("BLACKSKY_TOKEN")
UMBRA_TOKEN = os.environ.get("UMBRA_TOKEN")

PLANET_MARK = pytest.mark.skipif(not PLANET_TOKEN, reason="No PLANET_TOKEN in env")
BLACKSKY_MARK = pytest.mark.skipif(
    not BLACKSKY_TOKEN, reason="No BLACKSKY_TOKEN in env"
)
UMBRA_MARK = pytest.mark.skipif(not UMBRA_TOKEN, reason="No UMBRA_TOKEN in env")


@pytest.fixture(
    params=[
        pytest.param(("planet", PLANET_TOKEN), marks=PLANET_MARK),
        pytest.param(("blacksky", BLACKSKY_TOKEN), marks=BLACKSKY_MARK),
        pytest.param(("umbra", UMBRA_TOKEN), marks=UMBRA_MARK),
    ]
)
def backend_and_token(request):
    """
    Parameterize tests with all backends and tokens available.
    If token is not in env vars, skip the test for that backend.
    """
    return request.param


def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_post_to_opportunities_with_no_body():
    response = client.post("/opportunities")
    assert response.status_code == 422


def test_post_to_opportunities_with_opportunities_body():
    response = client.post(
        "/opportunities",
        json=VALID_SEARCH_BODY,
    )
    assert response.status_code == 200
    assert "features" in response.json()


@pytest.mark.parametrize("backend", ["fake", "earthsearch"])
def test_post_to_opportunities_with_opportunities_body_and_header(backend: str):
    response = client.post(
        "/opportunities",
        headers={"Backend": backend},
        json=VALID_SEARCH_BODY,
    )
    assert response.status_code == 200
    assert "features" in response.json()


def test_products_authenticated(backend_and_token: Tuple[str, str]):
    backend, token = backend_and_token
    _test_products(backend, token)


@pytest.mark.parametrize("backend", ["fake", "earthsearch"])
def test_products_unauthenticated(backend: str):
    _test_products(backend)


def _test_products(backend: str, token: Optional[str] = None):
    headers = {"Backend": backend}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = client.get(
        "/products",
        headers=headers,
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_post_to_opportunities_with_opportunities_body_and_header_authenticated(
    backend_and_token,
):
    backend, token = backend_and_token

    start_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=1
    )
    end_time = start_time + datetime.timedelta(days=1)

    search_body_now = {
        "datetime": f"{start_time.isoformat()}/{end_time.isoformat()}",
        "geometry": {"type": "Point", "coordinates": [-75.16, 39.95]},
        "product_id": "fake_product",
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
    assert (
        response.json()["detail"]
        == f"Backend 'foo' not in options: {list(BACKENDS.keys())}"
    )


def test_post_to_orders_raises_if_not_possible():
    response = client.post(
        "/orders",
        headers={"Backend": "earthsearch"},
        json=VALID_SEARCH_BODY,
    )
    assert response.status_code == 500
    assert (
        response.json()["detail"]
        == f"Unable to place an order for this product: 'landsat-c2-l2'"
    )


def test_post_to_orders():
    json_body = {
        "datetime": "2025-01-01T00:00:00Z/2025-05-02T00:00:00Z",
        "geometry": {"type": "Point", "coordinates": [-75.16, 39.95]},
        "product_id": "landsat-c2-l2",
    }
    response = client.post(
        "/orders",
        headers={"Backend": "earthsearch"},
        json=json_body,
    )
    assert response.status_code == 200
    assert response.json()["id"] == "LC09_L2SP_014032_20220501_02_T1"


@pytest.mark.parametrize("endpoint", ["/orders", "/opportunities"])
def test_token_is_passed_to_backend(endpoint):
    TOKEN = "fake-token-for-tests"

    class MockBackend:
        async def find_opportunities(
            self,
            search: Opportunity,
            token: str,
        ) -> list[Opportunity]:
            assert token == TOKEN
            return []

        async def place_order(
            self,
            search: Opportunity,
            token: str,
        ) -> Order:
            assert token == TOKEN
            return Order(id="blahblahblah")

    BACKENDS["mock"] = MockBackend()

    client.post(
        endpoint,
        headers={"Backend": "mock", "Authorization": f"Bearer {TOKEN}"},
        json=VALID_SEARCH_BODY,
    )
