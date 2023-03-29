
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse

from api.backends.base import Backend
from api.backends import BACKENDS

from api.api_types import ItemCollection, Search

app = FastAPI(title="Tasking API")


@app.get("/")
async def redirect_home():
    return RedirectResponse("/docs")


@app.get("/pineapple", response_model=ItemCollection)
@app.post("/pineapple", response_model=ItemCollection)
async def post_pineapple(
    request: Request,
    pineapple: Search,
):

    print("Starting....")
    print(BACKENDS)
    # get the right token and backend from the header
    backend = request.headers.get("backend", "blacksky")

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

    item_collection = await impl.find_future_items(
        pineapple,
        token=token,
    )

    return item_collection
