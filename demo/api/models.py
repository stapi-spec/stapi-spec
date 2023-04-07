from datetime import datetime as Datetime
from typing import Any, Dict, Literal, Optional, Union

from geojson_pydantic.features import Feature, FeatureCollection
from geojson_pydantic.geometries import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from pydantic import BaseModel, Field, constr
from pydantic.datetime_parse import parse_datetime
from stac_pydantic.collection import Range
from stac_pydantic.links import Link

Geometry = Union[
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
    GeometryCollection,
]


ProductConstraints = Dict[str, Union[Range, tuple, list[Any], Dict[str, Any]]]
ProductParameters = Dict[str, Union[Range, tuple, list[Any], Dict[str, Any]]]


# derived from stac_pydantic.shared.Provider
class Provider(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0/collection-spec/collection-spec.md#provider-object
    """

    name: constr(min_length=1)
    description: Optional[str] = Field(default=None)
    roles: Optional[list[str]] = Field(default=None)
    url: Optional[str] = Field(default=None)


class Order(BaseModel):
    id: str


class Product(BaseModel):
    """
    One element in response body for `/products`

    https://github.com/Element84/sat-tasking-sprint/tree/main/spec/product
    """

    type: Literal["Product"] = Field(const=True, default="Product")
    stat_version: str = Field(
        const=True,
        default="0.0.1",
        description="The STAT version the Product implements",
    )
    stat_extensions: list[str] = Field(
        default=[],
        description="A list of extension identifiers the Product implements.",
    )
    id: str = Field(
        description="Identifier for the Product that is unique across the provider."
    )
    title: Optional[str] = Field(
        default=None, description="A short descriptive one-line title for the Product."
    )
    description: Optional[str] = Field(
        default=None,
        description="Detailed multi-line description to fully explain the Product.",
    )
    keywords: list[str] = Field(
        default=[], description="List of keywords describing the Product."
    )
    license: str = Field(
        description="Product's license(s), either a SPDX License identifier, various if multiple licenses apply or proprietary for all other cases."
    )
    providers: list[Provider] = Field(
        description="A list of providers, which may include all organizations capturing or processing the data or the hosting provider. Providers should be listed in chronological order with the most recent provider being the last element of the list."
    )
    links: list[Link] = Field(description="A list of references to other documents.")
    constraints: Optional[ProductConstraints] = Field(
        default=None,
        description="Query constraints that will filter the opportunity results list.",
    )
    parameters: Optional[ProductParameters] = Field(
        default=None,
        description="User supplied parameters that don't constrain tasking (e.g., output format)",
    )


class ProductCollection(BaseModel):
    products: list[Product]


# Copied and modified from stack_pydantic.item.ItemProperties
class OpportunityProperties(BaseModel):
    datetime: str = Field(description="Slash separated datetime range")
    product_id: str = Field(
        description="Product identifier. The ID should be unique per provider."
    )
    constraints: Optional[ProductConstraints] = Field(
        default=None,
        description="A map of opportunity constraints, either a set of values, a range of values or a JSON Schema.",
    )

    @property
    def start_date(self) -> Datetime:
        values = self.datetime.split("/")
        return parse_datetime(values[0])

    @property
    def end_date(self) -> Datetime:
        values = self.datetime.split("/")
        return parse_datetime(values[1])


class OpportunityFeature(Feature[Geometry, OpportunityProperties]):
    id: Optional[str] = Field(default=None)
    properties: OpportunityProperties

    def to_dict(self, **kwargs: Any):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs: Any):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)


class Opportunity(OpportunityProperties):
    """
    Request body for `/opportunities` and `/orders`

    https://github.com/Element84/sat-tasking-sprint/blob/main/spec/order
    """

    id: Optional[str] = Field(default=None)
    geometry: Geometry = Field(description="Point contained within opportunity")

    def to_feature(self) -> OpportunityFeature:
        return OpportunityFeature(
            id=self.id,
            geometry=self.geometry,
            properties=OpportunityProperties(
                product_id=self.product_id,
                datetime=self.datetime,
                constraints=self.constraints,
            ),
        )


class OpportunityCollection(FeatureCollection):  # type: ignore
    """
    Resonse body from `/opportunities`

    https://github.com/Element84/stat-api-spec/blob/main/examples/OpportunityCollection.json
    """

    features: list[Feature[Geometry, OpportunityProperties]]

    def to_dict(self, **kwargs: Any) -> Dict[str, Any]:
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)  # type: ignore

    def to_json(self, **kwargs: Any) -> str:
        return self.json(by_alias=True, exclude_unset=True, **kwargs)  # type: ignore

    @classmethod
    def from_opportunities(
        cls, opportunities: list[Opportunity]
    ) -> "OpportunityCollection":
        return cls(features=[o.to_feature() for o in opportunities])
