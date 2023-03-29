from datetime import datetime, timedelta
import os
import requests

from api.api_types import Item, ItemCollection, Search

PLANET_BASE_URL = "https://api.staging.planet-labs.com"


def stac_search_to_imaging_window_request(search_request: Search):
    """

    :param search_request: STAC search as passed on to find_future_items
    :return: a triple of iw request body, geom and bbox (geom and bbox needed again later to construct STAC answers)
    """
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

    if 'datetime' not in sr:
        raise ValueError("Please provide datetime! Provided fields: %s" % list(sr.keys()))
    start_time, end_time = sr["datetime"].split('/')

    return {
        "start_time": start_time,
        "end_time": end_time,
        "pl_number": "PL-QA",  # this would need to be provided in addition to the token
        "product": "Assured Tasking",  # this as well
        "geometry": {
            "type": "Point",
            "coordinates": [
                lat,
                lon
            ]
        },
    }, first_intersect, bbox


def get_imaging_windows(planet_request):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'authorization': os.getenv("PLANET_TOKEN")
    }

    r = requests.post(
        f"{PLANET_BASE_URL}/tasking/v2/imaging-windows/search",
        headers=headers,
        json=planet_request
    )

    if 'location' not in r.headers:
        raise ValueError(
            "Header 'location' not found: %s, status %s, body %s, token %s" % (
                list(r.headers.keys()), r.status_code, r.text, os.getenv("PLANET_TOKEN"))
        )

    poll_url = r.headers['location']

    r = requests.get(
        f"{PLANET_BASE_URL}/{poll_url}",
        headers=headers
    )

    return r.json()['imaging_windows']


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

        planet_request, geom, bbox = stac_search_to_imaging_window_request(search_request)
        imaging_windows = get_imaging_windows(planet_request)
        stac_items = [
            imaging_window_to_stac_item(iw, geom, bbox)
            for iw
            in imaging_windows
        ]

        return ItemCollection(features=stac_items, links=[])
