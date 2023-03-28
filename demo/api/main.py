import pystac
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from stac_pydantic import Item, ItemCollection
from stac_pydantic.api.search import Search

app = FastAPI(title="Tasking API")

STAC_ITEM_URL = (
    "https://raw.githubusercontent.com/stac-utils/pystac/main/"
    "tests/data-files/item/sample-item.json"
)
STAC_JSON = {
    "id": "12345",
    "type": "Feature",
    "stac_extensions": ["https://stac-extensions.github.io/eo/v1.0.0/schema.json"],
    "geometry": {"type": "Point", "coordinates": [0, 0]},
    "properties": {
        "datetime": "2020-03-09T14:53:23.262208+00:00",
        "eo:cloud_cover": 25,
    },
    "links": [],
    "assets": [],
    "bbox": [0, 0, 1, 1],
}


@app.get("/")
async def redirect_home():
    return RedirectResponse("/docs")


@app.get("/pineapple", response_model=ItemCollection)
async def get_pineapple():
    pystac_item = pystac.Item.from_file(STAC_ITEM_URL)

    item = Item(**pystac_item.to_dict())
    item_collection = ItemCollection(features=[item], links=[])
    return item_collection


# Backed api example
def find_future_items(
    search_request: Search,
    request_headers: dict[str, str] = {}
) -> ItemCollection:
    pass
