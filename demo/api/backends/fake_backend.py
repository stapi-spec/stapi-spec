import pystac
from api.api_types import Item, ItemCollection, Search


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
        item_collection = ItemCollection(features=[item])
        return item_collection
