from typing import Protocol

from api.api_types import OpportunityCollection, Order, Product, Search


# backend protocol class
class Backend(Protocol):
    """Backend Python API"""

    async def find_opportunities(
        self,
        search: Search,
        token: str,
    ) -> OpportunityCollection:
        return NotImplemented

    async def find_products(
        self,
        token: str,
    ) -> list[Product]:
        return NotImplemented

    async def place_order(
        self,
        search: Search,
        token: str,
    ) -> Order:
        return NotImplemented
