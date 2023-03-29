from typing import List, Literal
from uuid import UUID

from pydantic import BaseModel, Field

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
    async def find_products(self, token: str) -> list[Product]:
        return [
            Product(
                id="umb-spotlight",
                provider="Umbra",
                title="Umbra 4x4km Spotlight SAR Image",
                extends=["SAR"],
                description="...",
                constraints={
                    # Does the same key provided here override the default ranges in
                    # base "SAR" Product extension?
                    "sar:resolution_range": [0.25, 1.0],
                    "sar:resolution_azimuth": [0.25, 1.0],
                    "target_azimuth": [0, 360],
                    "grazing": [10, 70],
                    # This doesn't match constraints typing, a [float, float] is required?
                    "polarization": ["VV", "HH"],
                },
                parameters={
                    # This doesn't match constraints typing, a str | float | int is required
                    "umb:data_products": ["GEC", "SICD", "SIDD", "CPHD"],
                    # This doesn't match constraints typing, a str | float | int is required
                    "umb:delivery_config_id": None,
                    "umb:task_name": "",
                    # This doesn't match constraints typing, a str | float | int is required
                    "umb:user_order_id": None,
                },
                properties={},
            )
        ]
