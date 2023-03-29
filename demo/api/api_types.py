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
    stat_version: str
    stat_extensions: list[str]
    id: str
    title: str
    description: str
    # keywords: List[str]
    # license: str
    # providers: List[Provider]
    # links: List[Link]
    constraints: Optional[ProductConstraints] = Field(
        default=None,
        description="Query constraints that will filter the opportunity results list.",
    )
    parameters: Optional[ProductParameters] = Field(
        default=None,
        description="User supplied parameters that don't constrain tasking (e.g., output format)",
    )


# Copied and modified from stack_pydantic.item.ItemProperties
class OpportunityProperties(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0/item-spec/common-metadata.md#date-and-time-range
    """

    title: Optional[str] = Field(None, alias="title")
    description: Optional[str] = Field(None, alias="description")
    datetime: Optional[str] = Field(None, alias="datetime")
    product_id: Optional[str] = Field(None, alias="product_id")
    constraints: Optional[Dict[str, Any]] = Field(None, alias="constraints")

    # TODO need to ask if this is exactly like stac with .., /, single datetime etc.
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


# Copied and modified from stack_pydantic.api.search.Search
class Search(BaseModel):
    geometry: Optional[Geometry]

    datetime: str = Field(description="Slash separated datetime range.")
    product_id: Optional[str]
    constraints: Optional[Dict[str, Any]] = None
    limit: int = 10

    # TODO need to ask if this is exactly like stac with .., /, single datetime etc.
    @property
    def start_date(self) -> Datetime:
        values = self.datetime.split("/")
        return parse_datetime(values[0])

    @property
    def end_date(self) -> Datetime:
        values = self.datetime.split("/")
        return parse_datetime(values[1])
