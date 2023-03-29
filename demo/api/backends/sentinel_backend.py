import datetime
import re
from datetime import timedelta
from typing import Any, Union

import pystac
from api.api_types import Opportunity, OpportunityCollection, OpportunityProperties, Search
from pystac_client.client import Client
from stac_pydantic.item import ItemProperties
from geojson_pydantic.types import BBox

DEFAULT_MAX_ITEMS = 10
MAX_MAX_ITEMS = 100


def get_max_items(search_request: Search) -> int:
    max_items = DEFAULT_MAX_ITEMS
    if search_request.limit:
        max_items = search_request.limit
    return min(max_items, MAX_MAX_ITEMS)

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
    async def find_opportunities(
        self,
        search: Search,
        token: str,
    ) -> OpportunityCollection:
        catalog = Client.open('https://earth-search.aws.element84.com/v1')  # type: ignore

        # https://earth-search.aws.element84.com/v1/collections/landsat-c2-l2/items


        max_items = get_max_items(search)

        args: dict[str, Any] = {
            'collections': 'landsat-c2-l2',
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

        search = catalog.search(**args)
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
