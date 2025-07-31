# STAPI Search Parameters Object

The Search Parameters Object contains the necessary values to determine what
could possibly fulfill a request. For example, the Search Parameters Object is
used as the request body for Opportunity searches, and as part of the request
body when placing an Order. In the former case it is used to constrain the set
of Opportunities returned to the user. In the latter case it is used by the
data provider to identify what data to task/deliver to meet the user's needs.

## Search Parameters Object

| Name | Type | Description |
| ---- | ---- | ----------- |
| datetime | string | **REQUIRED.** Time interval with a solidus (forward slash, `/`)  separator, using  [RFC 3339](https://tools.ietf.org/html/rfc3339#section-5.6) datetime, empty string, or `..` values. |
| geometry | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) | **REQUIRED.**  Defines the full footprint that the tasked data will be within. |
| filter | CQL2 Object | A set of additional filter terms in [CQL2 JSON](https://docs.ogc.org/DRAFTS/21-  065.html) format based on the [queryables](../product/README.md#queryables) exposed in the product. |

### datetime

The datetime parameter represents a time interval with which the temporal
property of the results must intersect. This parameter allows a subset of the
allowed values for a [ISO 8601 Time
Interval](https://en.wikipedia.org/wiki/ISO_8601#Time_intervals) or a [OAF
datetime](http://docs.opengeospatial.org/is/17-069r3/17-069r3.html#_parameter_datetime)
parameter.  This allows for either open or closed intervals, with end
definitions separated by a solidus (forward slash, `/`) separator. Closed ends
are represented by [RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339)
datetimes. Open ends are represented by either an empty string or `..`. Only
singly-open intervals are allowed.  Examples of valid datetime intervals
include `2024-04-18T10:56:00+01:00/2024-04-25T10:56:00+01:00`,
`2024-04-18T10:56:00Z/..`, and `/2024-04-25T10:56:00+01:00`

### geometry

Provides a GeoJSON Geometry Object, which **must** be an embedded GeoJSON
object compliant to [RFC 7946, section
3.1](https://tools.ietf.org/html/rfc7946#section-3.1). Coordinates are
specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS
84](http://www.opengis.net/def/crs/OGC/1.3/CRS84).
