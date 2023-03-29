from typing import Any, Optional, Union
from geojson_pydantic.features import Feature, FeatureCollection
from pydantic import constr, root_validator, BaseModel
from stac_pydantic.item import ItemProperties
from stac_pydantic.shared import BBox
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

from datetime import datetime as pydatetime

# Copied and modified from stack_pydantic.item.Item
class Item(Feature[Any, ItemProperties]):

    id: constr(min_length=1)  # type: ignore

    # Should there be a stac_version?
    # stac_version: constr(min_length=1) = Field(STAC_VERSION, const=True)

    properties: ItemProperties
    # TODO should we have links
    # links: Links

    def to_dict(self, **kwargs: Any):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs: Any):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)

    @root_validator(pre=True)
    def validate_bbox(cls, values: dict[str, Any]):
        if values.get("geometry") and values.get("bbox") is None:
            raise ValueError("bbox is required if geometry is not null")
        return values

# Copied and modified from stack_pydantic.item.ItemCollection
class ItemCollection(FeatureCollection[Any, Any]):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0/item-spec/itemcollection-spec.md
    """

    # Should there be a stac_version?
    # stac_version: constr(min_length=1) = Field(STAC_VERSION, const=True)

    features: list[Item]

    # stac_extensions: Optional[List[AnyUrl]]

    # TODO should we have links
    # links: Links
    # context: Optional[ContextExtension] = None

    def to_dict(self, **kwargs: Any):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs: Any):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)


# Copied and modified from stack_pydantic.api.search.Search
class Search(BaseModel):

    bbox: Optional[BBox]
    intersects: Optional[
        Union[
            Point,
            MultiPoint,
            LineString,
            MultiLineString,
            Polygon,
            MultiPolygon,
            GeometryCollection,
        ]
    ]
    # Slash separated date time range
    datetime: str
    limit: int = 10

    # TODO need to ask if this is exactly like stac with .., /, single datetime etc.
    @property
    def start_date(self) -> pydatetime:
        values = self.datetime.split("/")
        return parse_datetime(values[0])

    @property
    def end_date(self) -> pydatetime:
        values = self.datetime.split("/")
        return parse_datetime(values[1])
