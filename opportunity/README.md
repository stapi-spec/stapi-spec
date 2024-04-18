# STAT Opportunity Spec

- **Conformance URI:** <https://stat-api.example.com/v0.1.0/opportunities>

The STAT Opportunity describes a single business unit available for ordering.

## Opportunity Request

for POST /opportunities

| Field Name | Type                                                                       | Description |
| ---------- | -------------------------------------------------------------------------- | ----------- |
| datetime       | string                                                                     | **REQUIRED.** Datetime field is a [ISO8601 Time Interval](https://en.wikipedia.org/wiki/ISO_8601#Time_intervals) |
| product_id         | string                                                                     | **REQUIRED.** Product identifier. The ID should be unique and is a reference to the constraints which can be used in the constraints field. |
| geometry   | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) | **REQUIRED.** Defines the full footprint of the asset represented by this item, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| filter | CQL2 Object | A set of additional constraints in [CQL2 JSON](https://docs.ogc.org/DRAFTS/21-065.html) based on the constraints exposed in the product. |

## Opportunity Collection

for POST /opportunities

This is a GeoJSON FeatureCollection.

| Field Name    | Type                      | Description |
| ------------- | ------------------------- | ----------- |
| type          | string                    | **REQUIRED.** Always `FeatureCollection`. |
| features      | \[Opportunity Object\]    | **REQUIRED.** A list of opportunities. |
| links         | Map\<object, Link Object> | **REQUIRED.** Links for e.g. pagination. It is **strongly recommended** to include a link with relation type `create-order` link to allow the user to resubmit this Opportunities request as an Order if they do not wish to choose a specific Opportunity. |

### Opportunity Object

This object describes a STAT Opportunity. The input fields will be contained `properties` of each Feature in the GeoJSON response.

| Field Name | Type                                                                       | Description |
| ---------- | -------------------------------------------------------------------------- | ----------- |
| type       | string                                                                     | **REQUIRED.** Type of the GeoJSON Object. MUST be set to `Feature`. |
| id         | string                                                                     | Provider identifier. This is not required, unless the provider tracks user requests and state for opportunities. |
| geometry   | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) \| [null](https://tools.ietf.org/html/rfc7946#section-3.2) | **REQUIRED.** Defines the full footprint of the asset represented by this item, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| bbox       | \[number]                                                                  | **REQUIRED if `geometry` is not `null`.** Bounding Box of the asset represented by this Item, formatted according to [RFC 7946, section 5](https://tools.ietf.org/html/rfc7946#section-5). |
| properties | [Properties Object](#properties-object)                                    | **REQUIRED.** A dictionary of additional metadata for the Item. |
| links      | \[[Link Object](#link-object)]                                             | List of link objects to resources and related URLs. It is **strongly recommended** to include a `rel=create-order` link that allows the user to Order this opportunity. |

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
| product_id | string | **REQUIRED.**  Product identifier. The ID should be unique and is a reference to the constraints which can be used in the constraints field. |
