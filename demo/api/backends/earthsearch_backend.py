from datetime import datetime, timedelta
from typing import Any

import pystac
from api.models import (
    Opportunity,
    Order,
    Product,
    ProductConstraints,
    ProductParameters,
    Provider,
)
from geojson_pydantic.geometries import Point
from pystac import Collection, ItemCollection
from pystac_client.client import Client

DEFAULT_MAX_ITEMS = 10
MAX_MAX_ITEMS = 100

LANDSAT_COLLECTION_ID = "landsat-c2-l2"
SENTINEL_L1C_COLLECTION_ID = "sentinel-2-l1c"
SENTINEL_L2A_COLLECTION_ID = "sentinel-2-l2a"

PRODUCT_IDS = [LANDSAT_COLLECTION_ID, SENTINEL_L1C_COLLECTION_ID, SENTINEL_L2A_COLLECTION_ID]

# The api works by pretending the past is the future. It takes a users search request and searches for data in the
# past. This is the amount of time in the past we search from a request.
TIME_DELTA = timedelta(days=3 * 365)


def adjust_datetime(value: datetime) -> str:
    date = value + TIME_DELTA
    return f"{date.isoformat()}/{date.isoformat()}"


def stac_item_to_opportunity(item: pystac.Item, product_id: str) -> Opportunity:
    point_vals = (item.geometry or {}).get("coordinates", [[[0, 0]]])[0][0]

    return Opportunity(
        geometry=Point(coordinates=(point_vals[0], point_vals[1])),
        product_id=product_id,
        datetime=adjust_datetime(item.datetime)
        if item.datetime
        else f"{item.properties['start_datetime']/item.properties['end_datetime']}",
        id=item.id,
    )


def stac_collection_to_product(collection: Collection) -> Product:
    constraints: ProductConstraints = {}
    parameters: ProductParameters = {}
    summaries = collection.summaries.to_dict()

    if "gsd" in summaries:
        constraints["gsd"] = (min(*summaries["gsd"]), max(*summaries["gsd"]))

    return Product(
        id=collection.id,
        title=collection.title or collection.id,
        description=collection.description,
        constraints=constraints,
        parameters=parameters,
        license="",
        links=[],
        keywords=[],
        providers=[Provider(name="EarthSearch")],
    )


class EarthSearchBackend:
    catalog: Client

    def __init__(self) -> None:
        self.catalog = Client.open("https://earth-search.aws.element84.com/v1")  # type: ignore

    def _search(self, search) -> ItemCollection:
        max_items = DEFAULT_MAX_ITEMS

        args: dict[str, Any] = {
            "collections": [search.product_id],
            "max_items": max_items,
            "limit": max_items,
        }

        if search.geometry:
            args["intersects"] = search.geometry

        if search.start_date and search.end_date:
            args["datetime"] = [
                search.start_date - TIME_DELTA,
                search.end_date - TIME_DELTA,
            ]
        else:
            raise Exception("A datetime range must be specified")

        search_obj = self.catalog.search(**args)
        return search_obj.item_collection()

    async def find_opportunities(
        self,
        search: Opportunity,
        token: str,
    ) -> list[Opportunity]:
        # Convert the STAC items from earth search into opportunities
        item_collection = self._search(search)
        opportunities: list[Opportunity] = [
            stac_item_to_opportunity(item, product_id=search.product_id)
            for item in item_collection.items
        ]
        return opportunities

    async def find_products(self, token: str) -> list[Product]:
        def safe_get_coll(product_id: str) -> Collection:
            coll = self.catalog.get_collection(product_id)
            if coll is None:
                raise Exception(f"Could not find collection {product_id}")
            return coll

        return [
            stac_collection_to_product(safe_get_coll(product_id))
            for product_id in PRODUCT_IDS
        ]

    async def place_order(
        self,
        search: Opportunity,
        token: str,
    ) -> Order:
        """Get the first item off the search output and return that ID"""
        item_collection = self._search(search)

        if len(item_collection.items) == 0:
            raise ValueError(
                f"Unable to place an order for this product: '{search.product_id}'"
            )

        best_guess = item_collection.items[0]
        return Order(id=best_guess.id)
