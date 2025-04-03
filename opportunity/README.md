# STAPI Opportunity Spec

- **Conformance URI:** <https://stapi.example.com/v0.1.0/opportunities>

The STAPI Opportunity describes a single business unit available for ordering.

## Opportunity Request

for `POST /products/{productId}/opportunities`

| URL Parameter Name | Type | Description |
| ------------------ | ---- | ----------- |
| productId  | string | **REQUIRED.** Product identifier. The ID should be unique and is a reference to the [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) which can be used in the [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) field. |

### Opportunity Request Object

| Request Field Name | Type | Description |
| ------------------ | ---- | ----------- |
| datetime   | string | **REQUIRED.** Time interval with a solidus (forward slash, `/`)  separator, using [RFC 3339](https://tools.ietf.org/html/rfc3339#section-5.6) datetime, empty string, or `..` values. |
| geometry   | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) | **REQUIRED.** Defines the full footprint of the asset represented by this item, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| filter     | CQL2 Object | A set of additional [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) in [CQL2 JSON](https://docs.ogc.org/DRAFTS/21-065.html) based on the [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) exposed in the product. |

#### datetime

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

## Opportunity Collection

for `POST /products/{productId}/opportunities`

This is a GeoJSON FeatureCollection.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| type | string | **REQUIRED.** Always `FeatureCollection`. |
| id | string | Identifier for the collection, if persisted (**required** for async search opportunity collections). |
| features | \[Opportunity Object\] | **REQUIRED.** A list of opportunities. |
| links | [[Link Object](#opportunity-collection-links)] | |

### Opportunity Collection Links

Each link in the links array must be a
[Link](https://github.com/radiantearth/stac-spec/blob/master/commons/links.md#link-object)
Object.

#### Pagination links

Appropriate links for pagination (`next`, `prev`, `first`, `last) are required,
as supported and applicable, when the response is paginated.

#### rel=create-order

The spec **strongly recommends** the inclusion of a link with relation type
`create-order` to allow the user to resubmit the Opportunities request as an
Order if they do not wish to choose a specific Opportunity.

In the case where individual Opportunities do not include a `create-order` link
then it should be considered **required** to include a `create-order` link at
the OpportunityCollection level.

#### rel=search-record

This link is to allow Opportunity Collections created as the result of async
opportunity searches to point back to the record of the search for which the
Opportunity Collection is the result. In other words, when an Opportunity
Collection is the result of an async search it **should** include a link with
`rel-search-record` pointing to `GET /searches/opportunities/{searchRecordId}`
with the `searchRecordId` of the parent search.

### Opportunity Object

This object describes a STAPI Opportunity. The input fields will be contained
`properties` of each Feature in the GeoJSON response.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| type | string | **REQUIRED.** Type of the GeoJSON Object. **Must** be `Feature`. |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `Opportunity`. |
| stapi_version | string | **REQUIRED.** The STAPI version the Opportunity implements. |
| id | string | Provider identifier. This is not required, unless the provider tracks user requests and state for opportunities (as when supporting async searches). |
| geometry | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) \| [null](https://tools.ietf.org/html/rfc7946#section-3.2) | **REQUIRED.** Defines the full footprint of the asset represented by this item, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| bbox | [number] | **REQUIRED if `geometry` is not `null`.** Bounding Box of the asset represented by this Item, formatted according to [RFC 7946, section 5](https://tools.ietf.org/html/rfc7946#section-5). |
| properties | [Properties Object](#properties-object) | **REQUIRED.** A dictionary of additional metadata for the Item. |
| links | [[Link Object](#opportunity-links)] | List of link objects to resources and related URLs. |

#### bbox

Bounding Box of the asset represented by this Item using either 2D or 3D
geometries, formatted according to [RFC 7946, section
5](https://tools.ietf.org/html/rfc7946#section-5).  The length of the array
must be 2\*n where n is the number of dimensions.  The array contains all axes
of the southwesterly most extent followed by all axes of the northeasterly most
extent specified in Longitude/Latitude or Longitude/Latitude/Elevation based on
[WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84).  When using 3D
geometries, the elevation of the southwesterly most extent is the minimum
depth/height in meters and the elevation of the northeasterly most extent is
the maximum.  This field enables more naive clients to easily index and search
geospatially.  STAC compliant APIs are required to compute intersection
operations with the Item's geometry field, not its bbox.

#### Properties Object

Additional metadata fields can be added to the GeoJSON Object Properties that
describe the Opportunity in more detail for the user. The only required fields
are `datetime` and `product_id` but it is recommended to add more fields as
required to describe the opportunity in meaningful terms to the requestor.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| datetime       | string                                                                     | **REQUIRED.** Datetime field is a [ISO8601 Time Interval](https://en.wikipedia.org/wiki/ISO_8601#Time_intervals) |
| product_id | string | **REQUIRED.**  Product identifier. The ID should be unique and is a reference to the [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) which can be used in the [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) field. |

#### Opportunity Links

Each link in the links array must be a
[Link](https://github.com/radiantearth/stac-spec/blob/master/commons/links.md#link-object)
Object.

##### rel=create-order

This Link object fully describes the necessary HTTP request to submit an Order
for this Opportunity via
[Create Order](https://github.com/stapi-spec/stapi-spec/tree/main/order#create-order-request).

To conform to the Create Order spec, use `"method": "POST"`.

If no Body parameters apply to an Opportunity, use `"body": {}`.

It is **strongly recommended** to include include a `rel=create-order` link on
an Opportunity to allow the user to order the Opportunity. Consider the
inclusion of this link **required** where ordering of an individual Opportunity
is supported by the given Product. Omission of this link is valid when
Opportunities are considered informational-only and cannot be ordered directly
(i.e., the precision of the Opportunities exceeds the implementation's limits
with regard to valid order parameters, such as when orders have a minimum
datetime range greater than any individual Opportunity's datetime range).

When Opportunity `create-order` links are not included then it is **required**
to include the `create-order` link on the OpportunityCollection. Similarly,
when a `create-order` link is not included at the OpportunityCollection level
then consider it **required** to have a `create-order` link on each
Opportunity.

#####

## Async Opportunity Search

- **Conformance URI:** <https://stapi.example.com/v0.1.0/async-opportunities>

STAPI has an optional conformance class providing support for async opportunity
searches, to accommodate searches for products that require more time to
complete than is a typical or desirable HTTP request duration. Products that
support async opportunity searches should advertise this conformance class.

Async support requires persisting the search state and matching opportunities
outside the context of the initial request, so they are available for retrieval
at a later time by the requestor. The Opportunity Search Record is an
additional entity defined to model the required search state.

### Opportunity Search Record

Returned by an async opportunity search. Can also be retrieved directly.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| id         | string | **REQUIRED.** Opportunity search record ID. |
| product_id | string | **REQUIRED.** Product identifier. This should be a reference to the [Product](https://github.com/Element84/stapi-spec/blob/main/product/README.md) being searched. |
| request    | [Opportunity Request Object] | **REQUIRED.** The search parameters for the opportunity request. |
| status     | [Opportunity Search Status](#opportunity-search-status) | **REQUIRED.** The current search status. |
| links      | [[Link Object](#opportunity-search-links)] | List of link objects to resources and related URLs. |

#### Opportunity Search Links

##### rel=self

The `links` **must** include a Link Object with the href to retrieve the
Opportunity Search Record directly.

##### rel=monitor

If the `GET /searches/opportunities/{searchRecordId}/statuses` endpoint is
implemented, there **must** be a link to that endpoint using the relation type
`monitor`.

##### rel=opportunities

This Link object provides the means of retrieving the search results when the
search is completed. That is, it should include the equivalent of `GET
/products/{productId}/opportunities/{opportunityCollectionId}` where
`productId` is the product being searched and `opportunityCollectionId` is the
ID of the opportunity collection containing the results of the search.

This link is **must** be included when the search is completed.

#### Async search response

In the event of an async opportunity search, `POST
/products/{productId}/opportunities` must return a 201 status. The body of the
response must be the created Opportunity Search Record. The `Location` HTTP
header of the response should point to the direct link of the Opportunity
Search Record (`/searches/opportunities/{searchRecordId}`).

### Advertising Support for Opportunity Searching

Products **must** advertise support for sync and/or async searching via the two
opportunity conformance classes, or lack of any opportunity search support by
omitting both of these conformance classes. In the case where a product
advertises support for both sync and async behavior, implementations must
choose a default behavior to allow clients to succesfully request opportunities
without specifiying a preference.

Clients can request sync vs async operation via the HTTP `Prefer` header.
Possible values for the `Prefer` header are `respond-async` or `wait`, where
the former requests as async response and the latter requests a sync response.
The server must always respond with the HTTP `Preference-Applied` header
indicating whether the preference specified by the client was honored. If async
was requested then that request should be honored. If sync was requested but
the product does not support it then that request cannot be honored.

### Opportunity Search Status

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| timestamp | datetime | **REQUIRED.** ISO 8601 timestamp for the order status |
| status_code | string | **REQUIRED.** Enumerated status code |
| reason_code | string | Enumerated reason code for why the status was set |
| reason_text | string | Textual description for why the status was set |
| links | [Link Object] | **REQUIRED.** list of references to any relevant documents or resources. |

Links is intended to be the same data structure as links collection in STAC.
Links will be very provider specific.

#### Enumerated status codes

- received (indicates search received by provider and it passed format validation.)
- in_progress (indicates search is running)
- failed (indicates search will not be fulfilled for some error reason)
- canceled (indicates search was canceled for any reason)
- completed (indicates search has completed successfully and the results can be retrieved)

Providers must support these statuses.

State machine intent (currently no mandate to enforce)

- received -> in_progress or canceled.
- in_progress -> completed, failed, or canceled.
