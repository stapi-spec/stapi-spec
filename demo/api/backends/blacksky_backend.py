from datetime import datetime, timedelta
import os
import requests

from api.api_types import Item, ItemCollection, Search

BLACKSKY_BASE_URL = "https://api.dev.blacksky.com/v1"

def stac_search_to_oppurtunities_request(search_request: Search):

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
        "item": {
            "name": "Blacksky_Request",
            "description": "STAC Sprint",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    lon,
                    lat,
                    0
                ]
            },
            "timeframe": {
                "lowerBoundType": "CLOSED",
                "lowerEndpoint": start_time,
                "upperBoundType": "CLOSED",
                "upperEndpoint": end_time
            },
            "frequency": "ONCE",
            "offeringId": "391327b7-f4ee-4e7f-a894-3cffef19cae0",
            "frequency": "ONCE",
            "offeringParamValues": {
                "priority": "STANDARD",
                "sensor": "blacksky"
            },
            "externalId": "1234"
        },
        "includeWeather": True
    }, first_intersect, bbox

#"os.getenv("BLACKSKY_TOKEN")
def get_oppurtunities(blacksky_request):

    print(os.getenv("BLACKSKY_TOKEN"))
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'authorization': '3LDM66SKLDXOJFUQLYM6UMGTWMR5JEZE'
    }

    # print(blacksky_request)
    r = requests.post(
        f"{BLACKSKY_BASE_URL}/feasibility/plan",
        headers=headers,
        json=blacksky_request
    )
    return r.json()['opportunities']


def oppurtunity_to_stac_item(iw, geom, bbox):

    """
    translates a Planet Imaging Windows into a STAC item
    :param iw: an element from the 'imaging_windows' array of a /imaging_windows/[search_id] response
    :return: a corresponding STAC item
    """

    item = Item(
        id=iw["satellite"],
        geometry=geom,
        bbox=bbox,
        properties={
            'datetime': iw['timestamp'],
            'constellation': iw['sensorId'],\
        })

    #item.ext.enable('view')
    #item.ext.enable('eo')
    #item.ext.view.off_nadir = iw['offNadirAngleDegrees']
    #item.ext.eo.cloud_cover = iw['weatherForecast']['cloudCover']

    return item

class BlackskyBackend:

    async def find_future_items(
            self,
            search_request: Search,
            token: str,
    ) -> ItemCollection:

        print("Here")
        blacksky_request, geom, bbox = stac_search_to_oppurtunities_request(search_request)
        oppurtunities = get_oppurtunities(blacksky_request)
        stac_items = [
            oppurtunity_to_stac_item(iw, geom, bbox)
            for iw
            in oppurtunities
        ]

        return ItemCollection(features=stac_items, links=[])
