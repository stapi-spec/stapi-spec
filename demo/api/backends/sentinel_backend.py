from typing import Any
from pystac_client.client import Client
from stac_pydantic import Item, ItemCollection
from stac_pydantic.api.search import Search



class SentinelBackend:


    async def find_future_items(
        self,
        search_request: Search,
        token: str,
    ) -> ItemCollection:
        catalog = Client.open('https://earth-search.aws.element84.com/v1')

        # https://earth-search.aws.element84.com/v1/collections/landsat-c2-l2/items

        args = search_request.dict()
        args['collections'] = 'landsat-c2-l2'
        args['max_items'] = 10

        search = catalog.search(**args)
        item_coll =  search.item_collection()

        item_collection = ItemCollection(links=[], **item_coll.to_dict())


        return item_collection
