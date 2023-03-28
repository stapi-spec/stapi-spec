from typing import Protocol

from stac_pydantic import ItemCollection
from stac_pydantic.api.search import Search


# backend protocol class
class Backend(Protocol):
    """Backend Python API"""

    async def find_future_items(
        self,
        search_request: Search,
        token: str,
    ) -> ItemCollection:
        return NotImplemented
