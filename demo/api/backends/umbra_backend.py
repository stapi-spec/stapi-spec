import asyncio
import os
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID, uuid4

import requests
from api.api_types import (
    Geometry,
    Opportunity,
    OpportunityCollection,
    OpportunityProperties,
    Product,
    Search,
)
from api.backends.base import Backend
from pydantic import BaseModel, Field
from pystac import ProviderRole
from stac_pydantic.shared import Provider

UMBRA_BASE_URL = os.getenv("UMBRA_BASE_URL")
UMBRA_FEASIBILITIES_URL = f"{UMBRA_BASE_URL}/tasking/feasibilities"

GET_UMBRA_OPPORTUNITIES_DELAY_SECONDS = 1
GET_UMBRA_OPPORTUNITIES_RETRY_LIMIT = 30


def search_to_feasibility_request_payload(search: Search) -> Dict[str, Any]:
    start_date = search.start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = search.end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    geometry = search.geometry
    if not geometry:
        raise Exception("No geometry")

    coordinates: Any = geometry.coordinates  # type: ignore
    return {
        "imagingMode": "SPOTLIGHT",
        "spotlightConstraints": {
            "geometry": {
                "type": "Point",
                "coordinates": [coordinates[0], coordinates[1]],
            },
            "polarization": "VV",
            "rangeResolutionMinMeters": 1,
            "multilookFactor": 1,
            # TODO: set these from constraints
            "grazingAngleMinDegrees": 30,
            "grazingAngleMaxDegrees": 70,
            "targetAzimuthAngleStartDegrees": 0,
            "targetAzimuthAngleEndDegrees": 360,
        },
        "windowStartAt": start_date,
        "windowEndAt": end_date,
    }


def umbra_opportunity_to_opportunity(
    opportunity: Dict[str, Any], geom: Optional[Geometry]
) -> Opportunity:
    return Opportunity(
        id=None,
        geometry=geom,
        properties=OpportunityProperties(
            title=f"umb-spotlight: {str(uuid4())}",
            description="",
            datetime=f"{opportunity['windowStartAt']}/{opportunity['windowEndAt']}",
            product_id="umb-spotlight",
            constraints={
                "target_azimuth": [
                    opportunity["targetAzimuthAngleStartDegrees"],
                    opportunity["targetAzimuthAngleEndDegrees"],
                ],
                "grazing": [
                    opportunity["grazingAngleStartDegrees"],
                    opportunity["grazingAngleEndDegrees"],
                ],
            },
        ),
    )


def get_feasibility_request_id(search_request: Search, headers: Dict[str, str]) -> str:
    payload = search_to_feasibility_request_payload(search_request)
    response = requests.post(
        UMBRA_FEASIBILITIES_URL,
        headers=headers,
        json=payload,
    )
    try:
        response.raise_for_status()
    except Exception:
        print(f"Error getting feasibility request id: {response.text}")
        raise
    return response.json()["id"]


def get_umbra_opportunities(
    feasibility_request_id: str, headers: Dict[str, str]
) -> Optional[List[Dict[str, Any]]]:
    response = requests.get(
        f"{UMBRA_FEASIBILITIES_URL}/{feasibility_request_id}",
        headers=headers,
    )
    try:
        response.raise_for_status()
    except Exception:
        print(f"Error getting Umbra opportunites: {response.text}")
        raise
    data = response.json()
    if data["status"] == "RECEIVED":
        return None
    return data["opportunities"]


class UmbraSpotlightParameters(BaseModel):
    data_products: List[
        Literal["GEC"] | Literal["SICD"] | Literal["SIDD"] | Literal["CPHD"]
    ] = Field(title="Requested Data Products", default_factory=lambda: ["GEC"])
    delivery_config_id: UUID | None = Field(title="DeliveryConfig ID", default=None)
    task_name: str = Field(title="Task Name")
    user_order_id: str | None = Field(
        title="User Order ID",
        default=None,
        description="User provided value that can be used to identify this request in the user's system.",
    )

    class Config:
        alias_generator = lambda x: f"umb:{str(x)}"


class UmbraBackend(Backend):
    async def find_opportunities(
        self,
        search: Search,
        token: str,
    ) -> OpportunityCollection:
        print(f"Umbra - find_opportunities, search: {search}")

        if not UMBRA_BASE_URL:
            raise Exception("Set UMBRA_BASE_URL before running the server")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

        feasibility_request_id = get_feasibility_request_id(search, headers)
        print(f"feasibility_request_id: {feasibility_request_id}")

        umbra_opportunities = None
        for i in range(GET_UMBRA_OPPORTUNITIES_RETRY_LIMIT):
            print(
                f"Getting Umbra opportunities, attempt {i + 1}/{GET_UMBRA_OPPORTUNITIES_RETRY_LIMIT}"
            )
            umbra_opportunities = get_umbra_opportunities(
                feasibility_request_id, headers
            )
            if umbra_opportunities is not None:
                break
            await asyncio.sleep(GET_UMBRA_OPPORTUNITIES_DELAY_SECONDS)

        if not umbra_opportunities:
            print("No Umbra opportunities found")
            return OpportunityCollection(features=[])

        print(f"Found {len(umbra_opportunities)} Umbra opportunities")
        return OpportunityCollection(
            features=[
                umbra_opportunity_to_opportunity(umbra_opportunity, search.geometry)
                for umbra_opportunity in umbra_opportunities
            ]
        )

    async def find_products(self, token: str) -> list[Product]:
        return [
            Product(
                stat_version="0.0.1",
                stat_extensions=["SAR"],
                id="umb-spotlight",
                title="Umbra 4x4km Spotlight SAR Image",
                description="...",
                keywords=["sar", "spotlight"],
                license=" CC-BY-4.0",
                providers=[
                    Provider(
                        name="Umbra",
                        description="",
                        roles=[
                            ProviderRole.LICENSOR,
                            ProviderRole.PROCESSOR,
                            ProviderRole.PRODUCER,
                            ProviderRole.HOST,
                        ],
                        url="https://umbra.space",
                    )
                ],
                links=[],
                constraints={
                    "sar:resolution_range": [0.25, 0.5, 1.0],
                    "sar:resolution_azimuth": [0.25, 0.5, 1.0],
                    "target_azimuth": {"minimum": 0, "maximum": 360},
                    "grazing": {"minimum": 10, "maximum": 70},
                    "sar:polarizations": ["VV", "HH"],
                },
                parameters={
                    "product_types": ["GEC", "SICD", "SIDD", "CPHD"],
                    "task_name": {
                        "type": "string",
                        "required": True,
                    },
                    "user_order_id": {
                        "type": "string",
                    },
                    "delivery_config_id": {
                        "type": "string",
                    },
                },
            )
        ]
