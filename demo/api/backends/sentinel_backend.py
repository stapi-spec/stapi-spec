import datetime
import re
from datetime import timedelta
from typing import Any, Union

import pystac
from api.api_types import Opportunity, OpportunityCollection, OpportunityProperties, Search, Product
from pystac_client.client import Client
from stac_pydantic.item import ItemProperties
from geojson_pydantic.types import BBox

DEFAULT_MAX_ITEMS = 10
MAX_MAX_ITEMS = 100

LANDSAT_COLLECTION_ID = 'landsat-c2-l2'


# The api works by pretending the past is the future. It takes a users search request and searches for data in the
# past. This is the amount of time in the past we search from a request.
TIME_DELTA = timedelta(days=3*365)

MaybeDate = Union[str, Any]


def adjust_date_times(properties: dict[str, Any]) -> ItemProperties:
    def adjust_date_time(value: MaybeDate) -> Any:
        if isinstance(value, str) and re.match(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+.*', value):
            try:
                date = datetime.datetime.fromisoformat(value.replace('Z','+00:00'))
                value = (date + TIME_DELTA).isoformat()
            except Exception as e:
                print(f'Could not parse {value} as a datetime')
                raise e
        return value

    return OpportunityProperties(**{
        k: adjust_date_time(v)
        for k, v in properties.items()
    })


def stac_item_to_opportunity(item: pystac.Item) -> Opportunity:
    return Opportunity(
        geometry=item.geometry,
        properties=adjust_date_times(item.properties),
        id=item.id,
    )

class SentinelBackend:

    catalog: Client

    def __init__(self) -> None:
        self.catalog = Client.open('https://earth-search.aws.element84.com/v1')  # type: ignore


    async def find_opportunities(
        self,
        search: Search,
        token: str,
    ) -> OpportunityCollection:
        max_items = DEFAULT_MAX_ITEMS

        args: dict[str, Any] = {
            'collections': [LANDSAT_COLLECTION_ID],
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

        search = self.catalog.search(**args)
        item_coll = search.item_collection()

        # Convert the STAC items from earth search into future items
        opportunities: list[Opportunity] = [
            stac_item_to_opportunity(item)
            for item in item_coll.items
        ]

        opportunity_collection = OpportunityCollection(
            features=opportunities
        )

        return opportunity_collection

    async def find_products(self, token: str) -> list[Product]:
        self.catalog.get_collection(LANDSAT_COLLECTION_ID)

catalog = Client.open('https://earth-search.aws.element84.com/v1')  # type: ignore
c = catalog.get_collection(LANDSAT_COLLECTION_ID)

c.to_dict()
