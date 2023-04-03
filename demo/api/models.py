from datetime import datetime as Datetime
from typing import Any, Dict, List, Literal, Optional, Union

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
from pydantic import BaseModel, Field
from pydantic.datetime_parse import parse_datetime
from stac_pydantic.collection import Range
from stac_pydantic.links import Link
from stac_pydantic.shared import Provider

Geometry = Union[
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
    GeometryCollection,
]


ProductConstraints = Dict[str, Union[Range, List[Any], Dict[str, Any]]]
ProductParameters = Dict[str, Union[Range, List[Any], Dict[str, Any]]]


class Order(BaseModel):
    id: str


class Product(BaseModel):
    """https://github.com/Element84/sat-tasking-sprint/tree/main/product-spec"""

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
    keywords: List[str] = Field(
        default=[], description="List of keywords describing the Product."
    )
    # license: str = Field(description="Product's license(s), either a SPDX License identifier, various if multiple licenses apply or proprietary for all other cases.")
    # providers: List[Provider] = Field(description="A list of providers, which may include all organizations capturing or processing the data or the hosting provider. Providers should be listed in chronological order with the most recent provider being the last element of the list.")
    # links: List[Link] = Field(description="A list of references to other documents.")
    constraints: Optional[ProductConstraints] = Field(
        default=None,
        description="Query constraints that will filter the opportunity results list.",
    )
    parameters: Optional[ProductParameters] = Field(
        default=None,
        description="User supplied parameters that don't constrain tasking (e.g., output format)",
    )


class Search(BaseModel):
    """
    Request body for `/opportunities` and `/orders`

    https://github.com/Element84/sat-tasking-sprint/blob/main/order-spec
    """

    geometry: Geometry = Field(description="Point contained within opportunity")
    datetime: str = Field(description="Slash separated datetime range")
    product_id: str = Field(
        description="Product identifier. The ID should be unique per provider."
    )
    constraints: Optional[Dict[str, Any]] = Field(
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


# Copied and modified from stack_pydantic.item.ItemProperties
class OpportunityProperties(BaseModel):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    datetime: str = Field(description="Slash separated datetime range")
    product_id: str = Field(
        description="Product identifier. The ID should be unique per provider."
    )
    constraints: Optional[Dict[str, Any]] = Field(
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


# Copied and modified from stack_pydantic.item.Item
class Opportunity(Feature[Geometry, OpportunityProperties]):
    id: Optional[str]
    properties: OpportunityProperties

    def to_dict(self, **kwargs: Any):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs: Any):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)


# Copied and modified from stack_pydantic.item.ItemCollection
class OpportunityCollection(FeatureCollection):  # type: ignore
    features: list[Opportunity]

    def to_dict(self, **kwargs: Any) -> Dict[str, Any]:
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)  # type: ignore

    def to_json(self, **kwargs: Any) -> str:
        return self.json(by_alias=True, exclude_unset=True, **kwargs)  # type: ignore
