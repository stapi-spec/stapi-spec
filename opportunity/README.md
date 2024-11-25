# STAPI Opportunity Spec

- **Conformance URI:** <https://stapi.example.com/v0.1.0/opportunities>

The STAPI Opportunity describes a single business unit available for ordering.

## Opportunity Request

for `POST /products/{productId}/opportunities`

| Field Name | Type                                                                       | Description |
|------------| -------------------------------------------------------------------------- | ----------- |
| datetime   | string                                                                     | **REQUIRED.** Time interval with a solidus (forward slash, `/`)  separator, using [RFC 3339](https://tools.ietf.org/html/rfc3339#section-5.6) datetime, empty string, or `..` values. |
| productId  | string                                                                     | **REQUIRED.** Product identifier. The ID should be unique and is a reference to the [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) which can be used in the [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) field. |
| geometry   | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) | **REQUIRED.** Defines the full footprint of the asset represented by this item, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| filter     | CQL2 Object | A set of additional [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) in [CQL2 JSON](https://docs.ogc.org/DRAFTS/21-065.html) based on the [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) exposed in the product. |

#### datetime

The datetime parameter represents a time interval with which the temporal property of the results must intersect. This parameter allows a subset of the allowed values for a [ISO 8601 Time Interval](https://en.wikipedia.org/wiki/ISO_8601#Time_intervals) or a 
[OAF datetime](http://docs.opengeospatial.org/is/17-069r3/17-069r3.html#_parameter_datetime) parameter.
This allows for either
open or closed intervals, with end definitions separated by a solidus (forward slash, `/`) separator. Closed ends are represented by
[RFC 3339](https://datatracker.ietf.org/doc/html/rfc3339) datetimes. Open ends are represented
by either an empty string or `..`. Only singly-open intervals are allowed.  Examples of valid datetime intervals include `2024-04-18T10:56:00+01:00/2024-04-25T10:56:00+01:00`, `2024-04-18T10:56:00Z/..`, and `/2024-04-25T10:56:00+01:00`

## Opportunity Collection

for `POST /products/{productId}/opportunities`

This is a GeoJSON FeatureCollection.

| Field Name    | Type                      | Description |
| ------------- | ------------------------- | ----------- |
| type          | string                    | **REQUIRED.** Always `FeatureCollection`. |
| features      | \[Opportunity Object\]    | **REQUIRED.** A list of opportunities. |
| links         | Map\<object, Link Object> | **REQUIRED.** Links for e.g. pagination. It is **strongly recommended** to include a link with relation type `create-order` link to allow the user to resubmit this Opportunities request as an Order if they do not wish to choose a specific Opportunity. |

### Opportunity Object

This object describes a STAPI Opportunity. The input fields will be contained `properties` of each Feature in the GeoJSON response.

| Field Name | Type                                                                       | Description |
| ---------- | -------------------------------------------------------------------------- | ----------- |
| type       | string                                                                     | **REQUIRED.** Type of the GeoJSON Object. MUST be set to `Feature`. |
| stapi_type   | string | **REQUIRED.** Type of the STAPI Object. MUST be set to `Opportunity`.  |
| stapi_version   | string | **REQUIRED.** The STAPI version the Opportunity implements. |
| id         | string                                                                     | Provider identifier. This is not required, unless the provider tracks user requests and state for opportunities. |
| conformsTo      | \[string\]                                       | Conformance classes that apply to the opportunity specifically. |
| geometry   | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) \| [null](https://tools.ietf.org/html/rfc7946#section-3.2) | **REQUIRED.** Defines the full footprint of the asset represented by this item, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| bbox       | \[number]                                                                  | **REQUIRED if `geometry` is not `null`.** Bounding Box of the asset represented by this Item, formatted according to [RFC 7946, section 5](https://tools.ietf.org/html/rfc7946#section-5). |
| properties | [Properties Object](#properties-object)                                    | **REQUIRED.** A dictionary of additional metadata for the Item. |
| links      | \[[Link Object](#link-object)]                                             | List of link objects to resources and related URLs. There **must** be a `rel=create-order` link that allows the user to Order this opportunity. See [Link Object - rel=create-order](#rel=create-order) below. |

#### bbox

Bounding Box of the asset represented by this Item using either 2D or 3D geometries,
formatted according to [RFC 7946, section 5](https://tools.ietf.org/html/rfc7946#section-5).
The length of the array must be 2\*n where n is the number of dimensions.
The array contains all axes of the southwesterly most extent followed by all axes of the northeasterly most extent specified in
Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84).
When using 3D geometries, the elevation of the southwesterly most extent is the minimum depth/height in meters
and the elevation of the northeasterly most extent is the maximum.
This field enables more naive clients to easily index and search geospatially.
STAC compliant APIs are required to compute intersection operations with the Item's geometry field, not its bbox.

#### Properties Object

Additional metadata fields can be added to the GeoJSON Object Properties that describe the Opportunity in more detail for the user. The only required fields are  `datetime` but it is recommended to add more fields, see [Additional Fields](#additional-fields)
resources below.

| Field Name | Type         | Description                                                  |
| ---------- | ------------ | ------------------------------------------------------------ |
| datetime       | string                                                                     | **REQUIRED.** Datetime field is a [ISO8601 Time Interval](https://en.wikipedia.org/wiki/ISO_8601#Time_intervals) |
| product_id | string | **REQUIRED.**  Product identifier. The ID should be unique and is a reference to the [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) which can be used in the [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) field. |

#### Link Object

Each link in the links array must be a [Link](https://github.com/radiantearth/stac-spec/blob/master/commons/links.md#link-object) Object.

##### rel=create-order

This Link object fully describes the necessary HTTP request to submit an Order for this Opportunity via [Create Order](https://github.com/stapi-spec/stapi-spec/tree/main/order#create-order-request).

To conform to the Create Order spec, use `"method": "POST"`.

If no Body parameters apply to an Opportunity, use `"body": {}`.
