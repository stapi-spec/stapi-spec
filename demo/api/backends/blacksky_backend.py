from datetime import datetime, timedelta
import os
import requests

from api.api_types import Opportunity, OpportunityCollection, Search

BLACKSKY_BASE_URL = "https://api.dev.blacksky.com/v1"

def stac_search_to_oppurtunities_request(search_request: Search):


    """
    :param search_request: STAC search as passed on to find_future_items
    :return: a triple of iw request body, geom and bbox (geom and bbox needed again later to construct STAC answers)
    """
    bs_number, bs_product = "BS-TEST", "Standard"
    if search_request.product_id:
        bs_number, bs_product = search_request.product_id.split(':')

    return {
            "item": {
                "name": "Blacksky_Request",
                "description": "STAC Sprint",
                "timeframe": {
                    "lowerBoundType": "CLOSED",
                    "lowerEndpoint": search_request.start_date.isoformat(),
                    "upperBoundType": "CLOSED",
                    "upperEndpoint": search_request.end_date.isoformat()
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        39.95,
                        75.16,
                        0
                    ]
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
        }

def get_oppurtunities(blacksky_request):

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'authorization': os.getenv("BLACKSKY_TOKEN")
    }

    r = requests.post(
        f"{BLACKSKY_BASE_URL}/feasibility/plan",
        headers=headers,
        json=blacksky_request
    )
    print (r.json())
    return r.json()['opportunities']


def oppurtunity_to_stac_item(iw):

    """
    translates a Planet Imaging Windows into a STAC item
    :param iw: an element from the 'imaging_windows' array of a /imaging_windows/[search_id] response
    :return: a corresponding STAC item
    """

    item = Opportunity(
        id=iw["satellite"],
        geometry={
                'type': 'Point',
                     'coordinates': [
                         iw['longitude'],
                         iw['latitude'],
                         0
                     ]
        },
        properties={
            'title': '',
            'datetime': iw['timestamp'],
            'constraints': {
                'off_nadir': iw['offNadirAngleDegrees'],
                'cloud_cover': iw['weatherForecast']['cloudCover']
            }
        })

    return item

class BlackskyBackend:

    async def find_opportunities(
            self,
            search_request: Search,
            token: str,
    ) -> OpportunityCollection:

        print("CSM_")
        blacksky_request = stac_search_to_oppurtunities_request(search_request)
        oppurtunities = get_oppurtunities(blacksky_request)
        stac_items = [
            oppurtunity_to_stac_item(iw)
            for iw
            in oppurtunities
        ]

        return OpportunityCollection(features=stac_items, links=[])
