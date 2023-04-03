import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Tuple

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from geojson_pydantic import Point

from api.api_types import OpportunityCollection, Order, Product, Search
from api.backends import BACKENDS
from api.backends.base import Backend

app = FastAPI(title="Tasking API")

DEFAULT_BACKEND = os.environ.get("DEFAULT_BACKEND", "historical")


def throw(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )

    return wrapper


def _get_backend_and_token(request: Request) -> Tuple[Backend, str]:
    """Get the right token and backend from the header"""
    backend_name = request.headers.get("backend", DEFAULT_BACKEND)

    token: str = "this-is-not-a-real-token"
    if authorization := request.headers.get("authorization"):
        token = authorization.replace("Bearer ", "")

    if backend_name in BACKENDS:
        backend: Backend = BACKENDS[backend_name]()
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Backend '{backend_name}' not in options: {list(BACKENDS.keys())}",
        )
    return (backend, token)


@app.get("/")
async def redirect_home():
    return RedirectResponse("/docs")


@app.get("/products", response_model=list[Product])
@throw
async def get_products(request: Request):
    backend, token = _get_backend_and_token(request)

    return await backend.find_products(token=token)


@app.get("/products/{id}/opportunities", response_model=OpportunityCollection)
@throw
async def get_product_opportunities(
    id: str,
    request: Request,
    search: Search | None = None,
):
    """Get opportunities for a given product

    Example: /products/landsat-c2-l2/opportunities
    """
    backend, token = _get_backend_and_token(request)

    if search is None:
        start_datetime = datetime.now()
        end_datetime = start_datetime + timedelta(days=40)
        search = Search(
            geometry=Point(coordinates=(45, 45)),
            datetime=f"{start_datetime.isoformat()}/{end_datetime.isoformat()}",
            limit=10,
        )
    search.product_id = id

    return await backend.find_opportunities(
        search,
        token=token,
    )


@app.get("/opportunities", response_model=OpportunityCollection)
@throw
async def get_opportunities(
    request: Request,
    search: Search | None = None,
):
    backend, token = _get_backend_and_token(request)

    if search is None:
        start_datetime = datetime.now()
        end_datetime = start_datetime + timedelta(days=40)
        product_id = "landsat-c2-l2"
        search = Search(
            geometry=Point(coordinates=(45, 45)),
            datetime=f"{start_datetime.isoformat()}/{end_datetime.isoformat()}",
            limit=10,
            product_id=product_id,
        )

    return await backend.find_opportunities(
        search,
        token=token,
    )


@app.post("/opportunities", response_model=OpportunityCollection)
@throw
async def post_opportunities(
    request: Request,
    search: Search,
):
    backend, token = _get_backend_and_token(request)

    return await backend.find_opportunities(
        search,
        token=token,
    )


@app.post("/orders", response_model=Order)
@throw
async def post_order(
    request: Request,
    search: Search,
):
    backend, token = _get_backend_and_token(request)

    return await backend.place_order(
        search,
        token=token,
    )
