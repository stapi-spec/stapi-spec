from typing import Any, Optional, Union, Dict
from geojson_pydantic.features import Feature
from pydantic import BaseModel, Field
from pydantic.datetime_parse import parse_datetime
from geojson_pydantic.geometries import (
    GeometryCollection,
    LineString,
    MultiLineString,
    MultiPoint,
    MultiPolygon,
    Point,
    Polygon,
)
from stac_pydantic.shared import DATETIME_RFC339

from datetime import datetime as Datetime

Geometry = Union[
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    Polygon,
    MultiPolygon,
    GeometryCollection,
]

class OpportunityProperties(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0/item-spec/common-metadata.md#date-and-time-range
    """

    title: Optional[str] = Field(None, alias="title")
    description: Optional[str] = Field(None, alias="description")
    start_datetime: Optional[Datetime] = Field(None, alias="start_datetime")
    end_datetime: Optional[Datetime] = Field(None, alias="end_datetime")
    product_id: Optional[str] = Field(None, alias="product_id")
    constraints: Optional[Dict[str, Any]] = Field(None, alias="constraints")

    class Config:
        json_encoders = {Datetime: lambda v: v.strftime(DATETIME_RFC339)}


# Copied and modified from stack_pydantic.item.Item
class Opportunity(Feature[Geometry, OpportunityProperties]):
    id: Optional[str]
    properties: OpportunityProperties

    def to_dict(self, **kwargs: Any):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs: Any):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)



# Copied and modified from stack_pydantic.api.search.Search
class Search():
    geometry: Optional[Geometry]

    # Slash separated date time range
    datetime: str
    product_id: str
    constraints: Optional[Dict[str, Any]]

    # TODO need to ask if this is exactly like stac with .., /, single datetime etc.
    @property
    def start_date(self) -> Datetime:
        values = self.datetime.split("/")
        return parse_datetime(values[0])

    @property
    def end_date(self) -> Datetime:
        values = self.datetime.split("/")
        return parse_datetime(values[1])