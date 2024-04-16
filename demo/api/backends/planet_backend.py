import os
import requests
import time


from api.api_types import Search, Opportunity, OpportunityCollection, Product, Provider


PLANET_BASE_URL = "https://api.staging.planet-labs.com"


def search_to_imaging_window_request(search_request: Search) -> dict:
    """
    :param search: search object as passed on to find_opportunities
    :return: a corresponding request to retrieve imaging windows
    """

    # pl_number and pl_product would need to always be provided in a prod setting,
    # providing defaults here only temporarily
    pl_number, pl_product = "PL-QA", "Assured Tasking"
    if search_request.product_id:
        pl_number, pl_product = search_request.product_id.split(':')

    return {
        "datetime": f"{search_request.start_date.isoformat()}/{search_request.end_date.isoformat()}",
        "pl_number": pl_number,
        "product": pl_product,
        "geometry": search_request.geometry.dict(),
    }


def get_imaging_windows(planet_request) -> list:
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
            "Header 'location' not found: %s, status %s, body %s" % (
                list(r.headers.keys()), r.status_code, r.text)
        )

    poll_url = f"{PLANET_BASE_URL}{r.headers['location']}"
    os.environ["PLANET_LAST_POLL_URL"] = poll_url

    while True:
        r = requests.get(poll_url, headers=headers)
        status = r.json()['status']
        if status == "DONE":
            return r.json()['imaging_windows']
        elif status == 'FAILED':
            raise ValueError(
                f"Retrieving Imaging Windows failed: {r.json['error_code']} - {r.json['error_message']}'")
        # todo async
        time.sleep(1)


def imaging_window_to_opportunity(iw, geom, search_request) -> Opportunity:
    """
    translates a Planet Imaging Window into an Opportunity
    :param iw: an element from the 'imaging_windows' array of a /imaging_windows/[search_id] response
    :return: a corresponding opportunity
    """

    return Opportunity(
        id=iw["id"],
        geometry=geom,
        properties={
            'title': 'Planet Assured Imaging Window @ ' + iw['start_time'],
            'datetime': f"{iw['start_time']}/{iw['end_time']}",
            'product_id': search_request.product_id,
            'constraints': {
                'off_nadir': [iw['start_off_nadir'], iw['end_off_nadir']],
                'cloud_cover': iw['cloud_forecast'][0]['prediction']
            }
        })


def find_assured_opportunities(search_request: Search) -> OpportunityCollection:
    planet_request = search_to_imaging_window_request(search_request)
    imaging_windows = get_imaging_windows(planet_request)
    opportunities = [
        imaging_window_to_opportunity(iw, planet_request["geometry"], search_request)
        for iw
        in imaging_windows
    ]
    return OpportunityCollection(features=opportunities)


def find_flexible_opportunities(search_request: Search) -> OpportunityCollection:
    opportunity = Opportunity(
        constraints=search_request.constraints, parameters=search_request.parameters
    )
    return OpportunityCollection(features=[opportunity, ])


def validate_search_request(search_request: Search) -> None:
    product = PRODUCTS[search_request.product_id]
    if not product:
        raise ValueError(f"Unsupported product id: {search_request.product_id}")
    if not search_request.constraints.get('scheduling_type') in product.constraints['scheduling_type']:
        raise ValueError(f"Unsupported scheduling type: {search_request.constraints['scheduling_type']}")


PRODUCTS = [
            Product(
                type="Product",
                stat_version="0.0.1",
                stat_extensions=[],
                id="PL-QA:Assured Tasking",
                title="Assured Tasking",
                description="An assured capture at a specific time and location.",
                license="Proprietary",
                links=[],
                keywords=[],
                providers=[Provider(name="planet")],
                constraints={
                    'allowed_geometry': ['Point', 'LineString'],

                    'max_aoi_size_sqkm': 500,
                    # this does not correspond to a value the customer would send, but to a
                    # property of the provided AOI that we'll validate

                    'scheduling_type': 'Assured',
                    # not a choice but using the constraints field to persist the product type

                    'satellite_types': ['SkySat'],

                    # calling `opportunities` for this product will return one opportunity per imaging window
                },
                parameters={
                    'exclusivity_days': [0, 30]
                    # or only [0] if exclusivity option not part of product
                    # would we still send this?
                }
            ),

            Product(
                type="Product",
                stat_version="0.0.1",
                stat_extensions=[],
                id="PL-QA:Assured Tasking",
                title="Assured Tasking",
                description="An assured capture at a specific time and location.",
                license="Proprietary",
                links=[],
                keywords=[],
                providers=[Provider(name="planet")],
                constraints={
                    'duration': Range('1d', '364d,23h,59m,59s'),
                    'sat_elevation_deg': Range(20, 90),
                    'sat_azimuth_deg': Range(-360, 360),
                    'solar_zenith_deg': Range(0, 85),
                    'solar_azimuth_deg': Range(-360, 360),
                    'imagery_type': ['Image', 'Video', 'Stereo'],
                    'allowed_geometry': ['Point', 'LineString', 'Polygon'],
                    'scheduling_type': ['Flexible'],
                    'satellite_types': ['SkySat'],
                    'max_aoi_size_sqkm': 500,

                    # calling `opportunities` for this product will most likely only return one
                    # opportunity which takes the user-provided constraints:
                    # - check if constraints are compatible with the above product specs
                    # - return a single opportunity with the same constraints as confirmation
                    #   and additional info like pricing
                },
                parameters={
                    'exclusivity_days': [0, 30]
                    # or only [0] if exclusivity option not part of product
                    # would we still send this?
                }
            )

        ]
class PlanetBackend:

    async def find_opportunities(
        self,
        search_request: Search,
        token: str,
    ) -> OpportunityCollection:

        validate_search_request(search_request)
        scheduling_type = search_request.constraints.get('scheduling_type')
        match (scheduling_type):
            case 'Assured':
                return find_assured_opportunities(search_request)
            case 'Flexible':
                return find_flexible_opportunities(search_request)

        raise NotImplementedError(f"Unsupported scheduling type: {scheduling_type}")

    async def find_products(self, token: str) -> list[Product]:
        # todo: get real list of products
        # todo: consider proper reactions for all types of products (i.e. non-assured)
        return PRODUCTS
