from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse

from datetime import datetime, timedelta

from geojson_pydantic import Point

from api.backends.base import Backend, get_token
from api.backends import BACKENDS

from api.api_types import Search, OpportunityCollection, Product, Order

app = FastAPI(title="Tasking API")

import os
DEFAULT_BACKEND = os.environ.get("DEFAULT_BACKEND", "historical")

@app.get("/")
async def redirect_home():
    return RedirectResponse("/docs")


@app.get("/products", response_model=list[Product])
async def get_products(
        request: Request,
):
    # get the right token and backend from the header
    backend = request.headers.get("backend", DEFAULT_BACKEND)

    token = "this-is-not-a-real-token"
    if authorization := request.headers.get("authorization"):
        token = authorization.replace("Bearer ", "")

    if not token:
        token = get_token(backend)

    if backend in BACKENDS:
        impl: Backend = BACKENDS[backend]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Backend '{backend}' not in options: {list(BACKENDS.keys())}"
        )

    return  await impl.find_products(
        token=token,
    )



@app.get("/products/{id}/opportunities", response_model=OpportunityCollection)
async def get_product_opportunities(
    id: str,
    request: Request,
    search: Search | None = None,
):
    """Get opportunities for a given product

    Example: /products/landsat-c2-l2/opportunities
    """
    if search is None:
        start_datetime = datetime.now()
        end_datetime = start_datetime + timedelta(days=40)
        search = Search(
            geometry=Point(coordinates=(45, 45)),
            datetime=f"{start_datetime.isoformat()}/{end_datetime.isoformat()}",
            limit=10,
        )
    search.product_id = id

    return await post_opportunities(request, search)

@app.get("/opportunities", response_model=OpportunityCollection)
async def get_opportunities(
        request: Request,
        search: Search | None = None,
):
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

    return await post_opportunities(request, search)


@app.post("/opportunities", response_model=OpportunityCollection)
async def post_opportunities(
        request: Request,
        search: Search,
):
    # get the right token and backend from the header
    backend = request.headers.get("backend", DEFAULT_BACKEND)

    token = "this-is-not-a-real-token"
    if authorization := request.headers.get("authorization"):
        token = authorization.replace("Bearer ", "")

    if not token:
        token = get_token(backend)

    if backend in BACKENDS:
        impl: Backend = BACKENDS[backend]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Backend '{backend}' not in options: {list(BACKENDS.keys())}"
        )

    opportunity_collection = await impl.find_opportunities(
        search,
        token=token,
    )

    return opportunity_collection


@app.post("/orders", response_model=Order)
async def post_order(
    request: Request,
    search: Search,
):
    # get the right token and backend from the header
    backend = request.headers.get("backend", "historical")

    token = "this-is-not-a-real-token"
    if authorization := request.headers.get("authorization"):
        token = authorization.replace("Bearer ", "")

    if backend in BACKENDS:
        impl: Backend = BACKENDS[backend]
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Backend '{backend}' not in options: {list(BACKENDS.keys())}"
        )

    try:
        order = await impl.place_order(
            search,
            token=token,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )

    return order
