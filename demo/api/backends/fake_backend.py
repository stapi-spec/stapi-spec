import pystac
from api.api_types import Opportunity, Search


STAC_ITEM_URL = (
    "https://raw.githubusercontent.com/stac-utils/pystac/main/"
    "tests/data-files/item/sample-item.json"
)


class FakeBackend():
    async def find_opportunities(
        self,
        search: Search,
        token: str,
    ) -> Opportunity:

        item = pystac.Item.from_file(STAC_ITEM_URL)
        opportunities = Opportunity(geometry=item.geometry, properties=item.properties)
        return opportunities