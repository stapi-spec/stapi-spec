from typing import Protocol

from api.models import Opportunity, Order, Product


class Backend(Protocol):
    """
    Protocol class that backend provider APIs must conform to

    In order to create a backend a provider must create a class
    with the methods defined in this Protocol.
    """

    async def find_products(
        self,
        token: str,
    ) -> list[Product]:
        """Get a list of all Products"""
        return NotImplemented

    async def place_order(
        self,
        search: Opportunity,
        token: str,
    ) -> Order:
        """Given an Opportunity, place an order"""
        return NotImplemented

    async def find_opportunities(
        self,
        search: Opportunity,
        token: str,
    ) -> list[Opportunity]:
        """Given an Opportunity, get a list of Opportunites that fulfill it"""
        return NotImplemented
