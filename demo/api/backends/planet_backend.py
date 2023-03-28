from datetime import datetime, timedelta
import os
import requests

from typing import Any
from pystac_client.client import Client
from stac_pydantic import Item, ItemCollection
from stac_pydantic.api.search import Search

PLANET_BASE_URL = "https://api.staging.planet-labs.com"


def imaging_window_to_stac_item(iw, geom, bbox):
    """
    translates a Planet Imaging Windows into a STAC item
    :param iw: an element from the 'imaging_windows' array of a /imaging_windows/[search_id] response
    :return: a corresponding STAC item
    """

    item = Item(
        id=iw["id"],
        geometry=geom,
        bbox=bbox,
        properties={
            'start_datetime': iw['start_time'],
            'end_datetime': iw['end_time'],
            'constellation': 'planet-skysat',
            'providers': ['planet']
        })
    item.ext.enable('view')
    item.ext.enable('eo')
    item.ext.view.off_nadir = (iw['start_off_nadir'] + iw['end_off_nadir']) / 2
    # TODO this is an example of something that will have to be reflected as a range
    item.ext.eo.cloud_cover = iw['cloud_forecast'][0]['prediction']
    return item



class PlanetBackend:

    async def find_future_items(
        self,
        search_request: Search,
        token: str,
    ) -> ItemCollection:
        sr = search_request.dict()
        bbox = None
        first_intersect = None
        if 'bbox' in sr:
            bbox = sr['bbox']
            if len(bbox) == 4:
                xmin, ymin, xmax, ymax = bbox
            else:
                xmin, ymin, min_elev, xmax, ymax, max_elev = bbox
            lon = xmin + (xmax - xmin) / 2
            lat = ymin + (ymax - ymin) / 2
        elif 'intersects' in sr:
            first_intersect = sr['intersects'][0]
            raise NotImplementedError("passing on geometry via intersects not yet implement please use bbox")
        else:
            raise ValueError("Please provide either 'bbox' or 'intersects'")

        if 'datetime' not in search_request:
            raise ValueError("Please provide datetime!")
        start_time = sr["datetime"] # "2023-03-30T17:20:13.061Z"
        end_time_dt = datetime.fromisoformat(start_time) + timedelta(days=7)
        end_time = end_time_dt.isoformat(timespec='milliseconds') + 'Z'

        planet_request = {
            "start_time":  start_time,
            "end_time": end_time,
            "pl_number": "PL-QA", # this would need to be provided in addition to the token
            "product": "Assured Tasking", # this as well
            "geometry": {
                "type": "Point",
                "coordinates": [
                    lat,
                    lon
                ]
            },
        }

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'authorization': os.getenv("PLANET_TOKEN")
        }

        r = requests.post(
            f"{PLANET_BASE_URL}/tasking/v2/imaging-windows/search",
            headers=headers,
            data=planet_request
        )

        poll_url = r.headers['location']

        r = requests.get(
            f"{PLANET_BASE_URL}/{poll_url}",
            headers=headers
        )

        stac_items = [
            imaging_window_to_stac_item(iw, first_intersect, bbox)
            for iw
            in r.json()['imaging_windows']
        ]

        item_collection = ItemCollection()
        item_collection.features = stac_items
        return item_collection
