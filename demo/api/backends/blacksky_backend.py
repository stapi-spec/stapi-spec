import requests
from api.models import Opportunity

BLACKSKY_BASE_URL = "https://api.dev.blacksky.com/v1"


def stat_to_oppurtunities_request(search_request: Opportunity):
    """
    :param search_request: STAC search as passed on to find_future_items
    :return: a triple of iw request body, geom and bbox (geom and bbox needed again later to construct STAC answers)
    """
    bs_number, bs_product = "BS-TEST", "Standard"
    if search_request.product_id:
        bs_number, bs_product = search_request.product_id.split(":")

    return {
        "item": {
            "name": "Blacksky_Request",
            "description": "STAC Sprint",
            "timeframe": {
                "lowerBoundType": "CLOSED",
                "lowerEndpoint": search_request.start_date.isoformat(),
                "upperBoundType": "CLOSED",
                "upperEndpoint": search_request.end_date.isoformat(),
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    search_request.geometry.dict()["coordinates"][0],
                    search_request.geometry.dict()["coordinates"][1],
                    0,
                ],
            },
            "frequency": "ONCE",
            "offeringId": "391327b7-f4ee-4e7f-a894-3cffef19cae0",
            "frequency": "ONCE",
            "offeringParamValues": {"priority": "STANDARD", "sensor": "blacksky"},
            "externalId": "1234",
        },
        "includeWeather": True,
    }


def get_oppurtunities(blacksky_request, token):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": token,
    }

    r = requests.post(
        f"{BLACKSKY_BASE_URL}/feasibility/plan", headers=headers, json=blacksky_request
    )
    return r.json()["opportunities"]


def blacksky_oppurtunity_to_opportunity(iw):
    """
    translates a Planet Imaging Windows into a STAC item
    :param iw: an element from the 'imaging_windows' array of a /imaging_windows/[search_id] response
    :return: a corresponding STAC item
    """

    opportunity = Opportunity(
        id=iw["satellite"],
        product_id="BS-Test:Standard",
        geometry={"type": "Point", "coordinates": [iw["longitude"], iw["latitude"], 0]},
        datetime=f"{iw['timestamp']}/{iw['timestamp']}",
        constraints={
            "off_nadir": iw["offNadirAngleDegrees"],
            "cloud_cover": iw["weatherForecast"]["cloudCover"],
        },
    )

    return opportunity


class BlackskyBackend:
    async def find_opportunities(
        self,
        search_request: Opportunity,
        token: str,
    ) -> list[Opportunity]:
        blacksky_request = stat_to_oppurtunities_request(search_request)
        oppurtunities = get_oppurtunities(blacksky_request, token)
        return [blacksky_oppurtunity_to_opportunity(iw) for iw in oppurtunities]
