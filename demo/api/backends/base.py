from typing import Protocol

from api.api_types import Opportunity, Search, OpportunityCollection

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
