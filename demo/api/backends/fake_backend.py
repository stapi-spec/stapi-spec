from api.models import Product, Provider, Opportunity


class FakeBackend:
    async def find_opportunities(
        self,
        search: Opportunity,
        token: str,
    ) -> list[Opportunity]:
        return [search]

    async def find_products(self, token: str) -> list[Product]:
        return [
            Product(
                id="fake product",
                title="fake product",
                description="",
                license="",
                links=[],
                keywords=[],
                providers=[Provider(name="fake")],
                constraints={},
                parameters={},
            )
        ]
