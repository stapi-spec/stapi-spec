
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from stac_pydantic import ItemCollection
from stac_pydantic.api.search import Search

from api.backends.base import Backend
from api.backends import BACKENDS

app = FastAPI(title="Tasking API")


@app.get("/")
async def redirect_home():
    return RedirectResponse("/docs")


@app.get("/pineapple", response_model=ItemCollection)
@app.post("/pineapple", response_model=ItemCollection)
async def post_pineapple(
    request: Request,
    pineapple: Search = Search(),
):
    print(BACKENDS)
    # get the right token and backend from the header
    backend = request.headers.get("backend", "sentinel")

    token = "this-is-not-a-real-token"
    if authorization := request.headers.get("authorization"):
        token = authorization.replace("Bearer ", "")

    impl: Backend = None

    if backend in BACKENDS:
        impl = BACKENDS[backend]()
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Backend '{backend}' not in options: {list(BACKENDS.keys())}"
        )

    item_collection = await impl.find_future_items(
        pineapple,
        token=token,
    )

    return item_collection
