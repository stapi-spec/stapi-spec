from typing import Protocol, Optional

from api.api_types import OpportunityCollection, Product, Search
import os


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


def get_token(backend: str) -> Optional[str]:
    token_name = f"{backend.upper()}_TOKEN"

    if token_name not in os.environ:
        # skip endpoint if token not provided
        return
    return os.environ[token_name]
