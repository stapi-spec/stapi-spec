from typing import Annotated, Protocol

import pystac
from fastapi import FastAPI, Header
from fastapi.responses import RedirectResponse
from stac_pydantic import Item, ItemCollection
from stac_pydantic.api.search import Search
from api.backends.sentinel_backend import SentinelBackend

app = FastAPI(title="Tasking API")

STAC_ITEM_URL = (
    "https://raw.githubusercontent.com/stac-utils/pystac/main/"
    "tests/data-files/item/sample-item.json"
)


@app.get("/")
async def redirect_home():
    return RedirectResponse("/docs")


@app.get("/pineapple", response_model=ItemCollection)
@app.post("/pineapple", response_model=ItemCollection)
async def post_pineapple(pineapple: Annotated[Search, Header()] = Search()):

    # get the right token and backend from the header
    token = "this-is-not-a-real-token"
    backend = "sentinel"

    impl: Backend = None

    if backend == "fake":
        impl = FakeBackend()
    elif backend == 'sentinel':
        impl = SentinelBackend()

    item_collection = await impl.find_future_items(
        pineapple,
        token=token,
    )

    return item_collection


class FakeBackend():

    async def find_future_items(
        self,
        search_request: Search,
        token: str,
    ) -> ItemCollection:

        pystac_item = pystac.Item.from_file(STAC_ITEM_URL)

        item = Item(**pystac_item.to_dict())
        item_collection = ItemCollection(features=[item], links=[])
        return item_collection


# backend protocol class
class Backend(Protocol):
    """Backend Python API"""

    async def find_future_items(
        self,
        search_request: Search,
        token: str,
    ) -> ItemCollection:
        return NotImplemented
