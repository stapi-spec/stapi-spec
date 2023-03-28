import pystac
from stac_pydantic import Item, ItemCollection
from stac_pydantic.api.search import Search


STAC_ITEM_URL = (
    "https://raw.githubusercontent.com/stac-utils/pystac/main/"
    "tests/data-files/item/sample-item.json"
)


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
