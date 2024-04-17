# STAT feasibility Spec

The STAT feasibility describes a the feasibility for ordering. This was previously called opportunities, which might refer directly to physical/geometric accesses to satellites to AOI and might be confusing. Opportunities/acceses are proposed as an extension instead valid for feasibility as well as orders.


## Feasibility fields

This object describes a STAT feasibility. The input fields will be contained `properties` of each Feature in the GeoJSON response.

| Field Name      | Type                                                                                                                                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                           |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| type            | string                                                                                                                                | **REQUIRED.** Type of the GeoJSON Object. MUST be set to `Feature`.                                                                                                                                                                                                                                                                                                                                                                   |
| stat_version    | string                                                                                                                                | **REQUIRED.** The STAT version the Opportunity implements.                                                                                                                                                                                                                                                                                                                                                                            |
| stat_extensions | \[string]                                                                                                                             | A list of extensions the Opportunity implements.                                                                                                                                                                                                                                                                                                                                                                                      |
| product_id      | string                                                                                                                                | **REQUIRED.** Product identifier. The ID should be unique and is a reference to the constraints which can be used in the constraints field.                                                                                                                                                                                                                                                                                           |
| id              | string                                                                                                                                | Provider identifier. This is not required, unless the provider tracks user requests and state for opportunities.                                                                                                                                                                                                                                                                                                                      |
| geometry        | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) \| [null](https://tools.ietf.org/html/rfc7946#section-3.2) | **REQUIRED.** Defines the full footprint of the asset represented by this item, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| bbox            | \[number]                                                                                                                             | **REQUIRED if `geometry` is not `null`.** Bounding Box of the asset represented by this Item, formatted according to [RFC 7946, section 5](https://tools.ietf.org/html/rfc7946#section-5).                                                                                                                                                                                                                                            |
| links           | \[[Link Object](#link-object)]                                                                                                        | List of link objects to resources and related URLs.                                                                                                                                                                                                                                                                                                                                                                                   |
| constraints     | Map<string, \[\*]\|[Range Object](#range-object)\|[JSON Schema Object](#json-schema-object)>                                          | A map of opportunity constraints, either a set of values, a range of values or a JSON Schema.                                                                                                                                                                                                                                                                                                                                         |

### Additional Field Information

#### stat_extensions

A list of extensions the Feasibility implements.
The list consists of URLs to JSON Schema files that can be used for validation.
This list must only contain extensions that extend the Opportunity specification itself.

#### Opportunities/Accesses/Collections endpoint (however ends up being called)

This wlil describe the Feature collection that can be return by the provider.

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

### Properties Object

Additional metadata fields can be added to the GeoJSON Object Properties. The only required field
is `datetime` but it is recommended to add more fields, see [Additional Fields](#additional-fields)
resources below.

| Field Name     | Type         | Description                                                                                                                                                                                |
| -------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| start_datetime | string\|null | **REQUIRED.** The earliest datetime for the Opportunity, which must be in UTC. It is formatted according to [RFC 3339, section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6).      |
| end_datetime   | string\|null | **REQUIRED.** The last possible datetime for the Opportunity, which must be in UTC. It is formatted according to [RFC 3339, section 5.6](https://tools.ietf.org/html/rfc3339#section-5.6). |
