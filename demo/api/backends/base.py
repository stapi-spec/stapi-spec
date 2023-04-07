from typing import Protocol

from api.models import Opportunity, Order, Product


# backend protocol class
class Backend(Protocol):
    """Backend Python API"""

    async def find_opportunities(
        self,
        search: Opportunity,
        token: str,
    ) -> list[Opportunity]:
        return NotImplemented

    async def find_products(
        self,
        token: str,
    ) -> list[Product]:
        return NotImplemented

    async def place_order(
        self,
        search: Opportunity,
        token: str,
    ) -> Order:
        return NotImplemented
