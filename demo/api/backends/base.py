from typing import Protocol

from api.api_types import Search, ItemCollection

# backend protocol class
class Backend(Protocol):
    """Backend Python API"""

    async def find_future_items(
        self,
        search_request: Search,
        token: str,
    ) -> ItemCollection:
        return NotImplemented
