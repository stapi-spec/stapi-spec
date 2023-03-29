from typing import List, Literal
from uuid import UUID

from pydantic import BaseModel, Field
from pystac import Provider, ProviderRole

from api.api_types import Product
from api.backends.base import Backend


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
    async def find_products(self, token: str) -> List[Product]:
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
                parameters=UmbraSpotlightParameters.schema(),
            )
        ]
