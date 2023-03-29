from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse

from api.backends.base import Backend
from api.backends import BACKENDS

from api.api_types import Search, OpportunityCollection

app = FastAPI(title="Tasking API")


@app.get("/")
async def redirect_home():
    return RedirectResponse("/docs")


@app.get("/products/{id}/opportunities", response_model=OpportunityCollection)
@app.post("/products/{id}/opportunities", response_model=OpportunityCollection)
async def product_opportunities(
    id: str,
    request: Request,
    search: Search,
):
    search.product = id
    return await opportunities(request, search)


@app.get("/opportunities", response_model=OpportunityCollection)
@app.post("/opportunities", response_model=OpportunityCollection)
async def opportunities(
    request: Request,
    search: Search,
):
    # get the right token and backend from the header
    backend = request.headers.get("backend", "sentinel")

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

    opportunities = await impl.find_opportunities(
        search,
        token=token,
    )

    return opportunities
