from typing import Protocol

from api.api_types import Opportunity, Search

# backend protocol class
class Backend(Protocol):
    """Backend Python API"""

    async def find_opportunities(
        self,
        search: Search,
        token: str,
    ) -> list[Opportunity]:
        return NotImplemented
