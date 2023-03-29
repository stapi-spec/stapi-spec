import datetime
import re
from datetime import timedelta
from typing import Any, Union

import pystac
from api.api_types import (Opportunity, OpportunityCollection,
                           OpportunityProperties, Product, ProductConstraints,
                           Search, Provider)
from pystac import Collection
from pystac_client.client import Client

DEFAULT_MAX_ITEMS = 10
MAX_MAX_ITEMS = 100

LANDSAT_COLLECTION_ID = 'landsat-c2-l2'
SENTINEL_COLLECTION_ID = 'sentinel-2-l1c'

PRODUCT_IDS = [
    LANDSAT_COLLECTION_ID,
    SENTINEL_COLLECTION_ID
]

# The api works by pretending the past is the future. It takes a users search request and searches for data in the
# past. This is the amount of time in the past we search from a request.
TIME_DELTA = timedelta(days=3*365)

MaybeDate = Union[str, Any]


def adjust_date_times(properties: dict[str, Any]) -> OpportunityProperties:
    def adjust_date_time(value: MaybeDate) -> Any:
        if isinstance(value, str) and re.match(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+.*', value):
            try:
                date = datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
                value = f"{(date + TIME_DELTA).isoformat()}/{(date + TIME_DELTA).isoformat()}"
            except Exception as e:
                print(f'Could not parse {value} as a datetime')
                raise e
        return value
    return OpportunityProperties(**{
        k: adjust_date_time(v)
        for k, v in properties.items()
    })


def stac_item_to_opportunity(item: pystac.Item, product_id: str) -> Opportunity:
    return Opportunity(
        geometry=item.geometry,  # type: ignore
        properties=adjust_date_times({"product_id": product_id, **item.properties}),
        id=item.id,
    )

def stac_collection_to_product(collection: Collection) -> Product:
    constraints: ProductConstraints = {}
    summaries = collection.summaries.to_dict()

    if 'gsd' in summaries:
        constraints['gsd'] = (min(*summaries['gsd']), max(*summaries['gsd']))

    return Product(
        provider='EarthSearch',
        id=collection.id,
        title=collection.title or collection.id,
        extends=[],
        description=collection.description,
        constraints=constraints,
        parameters={},
        properties=summaries,
        stat_version="0.0.1",
        stat_extensions=[],
        license="",
        links=[],
        keywords=[],
        providers=[Provider(name="Sentinel")],

    )

class HistoricalBackend:
    catalog: Client

    def __init__(self) -> None:
        self.catalog = Client.open('https://earth-search.aws.element84.com/v1')  # type: ignore

    async def find_opportunities(
        self,
        search: Search,
        token: str,
    ) -> OpportunityCollection:
        max_items = min(search.limit, MAX_MAX_ITEMS)

        args: dict[str, Any] = {
            'collections': [search.product_id],
            'max_items': max_items,
            'limit': max_items,
        }

        if search.geometry:
            args['intersects'] = search.geometry

        if search.start_date and search.end_date:
            args['datetime'] = [
                search.start_date - TIME_DELTA,
                search.end_date - TIME_DELTA,
            ]
        else:
            raise Exception('A datetime range must be specified')

        search_obj = self.catalog.search(**args)
        item_coll = search_obj.item_collection()

        # Convert the STAC items from earth search into opportunities
        opportunities: list[Opportunity] = [
            stac_item_to_opportunity(item, product_id=search.product_id)
            for item in item_coll.items
        ]
        opportunity_collection = OpportunityCollection(
            features=opportunities
        )

        return opportunity_collection

    async def find_products(self, token: str) -> list[Product]:
        def safe_get_coll(product_id: str) -> Collection:
            coll = self.catalog.get_collection(product_id)
            if coll is None:
                raise Exception(f'Could not find collection {product_id}')
            return coll

        return [
            stac_collection_to_product(safe_get_coll(product_id))
            for product_id in PRODUCT_IDS
        ]
