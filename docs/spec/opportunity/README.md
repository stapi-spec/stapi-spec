# STAPI Opportunity Spec

- **Conformance URI:** `https://stapi.example.com/v0.2.0/opportunities`

An Opportunity in STAPI is an abstract, and often terse, representation
of data that will be delivered in the future. Because of the uncertainty
involved, an Opportunity may contain a range of values rather than
discrete known values. The amount of metadata fields contained within an
Opportunity will vary depending on the user requirements and what is known
by the provider at the time of request.

**An Opportunity is the minimum amount of metadata known about the data
that will be delivered**.

The optional `POST /products/{productId}/opportunities` endpoint provides
additional functionality on top of the core STAPI spec. It allows
a user to search and browse additional information about what could be
delivered after an order is made. The `opportunities` endpoint is specific
for a product and could be used before a user places an order with a call to
`POST /products/{productId}/orders`.

## Opportunity Request

The endpoint `POST /products/{productId}/opportunities` is parameterized in the
following way:

### Path Parameters

| Name | Type | Description |
| ---- | ---- | ----------- |
| productId | string | **REQUIRED.** Product identifier ([see Product Object](../product/README.md#product-object)) |

### Opportunity Request Object

The Opportunity Request object contains the parameters required to perform a
search for opportunities.

| Name | Type | Description |
| ---- | ---- | ----------- |
| search_parameters | [Search Parameters Object](../search-parameters/README.md) | **REQUIRED.** Parameters for scenes that would meet the Opportunity search's requirements |
| limit | integer | The maximum number of Opportunities to return in a single page. See [Paginating an opportunity search](#paginating-an-opportunity-search). |
| next | string | Opaque pagination token identifying the page to return, supplied by the `next` link of a previous response. A client **must not** construct one. See [Paginating an opportunity search](#paginating-an-opportunity-search). |

The `search_parameters` of an Opportunity Request is the same [Search
Parameters Object](../search-parameters/README.md) as the `search_parameters`
of an [Order Request](../order/README.md#order-request-object), so the
parameters of a search carry across to an Order unchanged; an Order
additionally supplies `order_parameters`. This is what a `create-order` link
does: it carries the search parameters of the Opportunity into the Order
request body.

### Paginating an opportunity search

An opportunity search is submitted with `POST`, so its pagination links cannot
be plain URLs retrieved with `GET`: the next page must be requested with the
same method and a body. A paginated Opportunity Collection therefore returns
pagination links carrying the `method`, `headers`, and `body` fields described
in [additional Link fields](../link/README.md#additional-link-fields), where
`body` repeats the original request with a `next` token added.

`limit` and `next` are the request-body equivalents of the `limit` query
parameter and the opaque page URL described in [API
Pagination](../pagination/README.md):

- `limit` is optionally supplied by the client on the initial request. It is an
  integer no smaller than 1, and as everywhere else in STAPI it is a maximum
  rather than an exact count. This specification sets no upper bound and no
  default page size; both are implementation concerns. A server repeats the
  limit it applied in the `body` of a `next` link, so a client following links
  does not resupply it.
- `next` is supplied only by the server, in the `body` of a `next` link. Its
  value is opaque, and a client **must** submit that body as given rather than
  construct a token itself, exactly as it follows a `next` link href unmodified
  elsewhere.

A `next` link is present only when a further page exists. Its absence is the
only indication that the last page has been reached. For example:

```json
{
    "rel": "next",
    "type": "application/geo+json",
    "href": "https://stapi.example.com/products/umbra_spotlight/opportunities",
    "method": "POST",
    "body": {
        "search_parameters": {
            "datetime": "2024-04-19T00:00:00Z/2024-04-23T00:00:00Z",
            "geometry": {
                "type": "Point",
                "coordinates": [13.403258555886767, 52.473696635108176]
            }
        },
        "limit": 20,
        "next": "8a35eba9c"
    }
}
```

Because `limit` and `next` control pagination of the search rather than
describe the data being requested, they are not part of the [Order Request
Object](../order/README.md#order-request-object), and they are not recorded in
an [Opportunity Search Record](#opportunity-search-record). A client reusing
the search parameters of an Opportunity Request as an Order Request omits them,
and a server that receives them on an Order request **must** ignore them.

## Opportunity Collection

An Opportunity Collection is returned when retrieving the results of an
opportunity search. It is a GeoJSON FeatureCollection.

In addition to the fields common to every [Collection
Object](../collection/README.md), an Opportunity Collection has the following
fields.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| type | string | **REQUIRED.** Type of the GeoJSON Object. **Must** be set to `FeatureCollection`. |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `OpportunityCollection`. |
| id | string | Identifier for the collection, if persisted (**required** for async search opportunity collections). |
| features | \[[Opportunity Object](#opportunity-object)\] | **REQUIRED.** A list of opportunities. |

### Opportunity Collection Links

Each link in the links array must be a [Link Object](../link/README.md).

In addition to standard links, the following are applicable to Opportunity Collections.

| rel type | Description |
| ---------- | ----------- |
| `next`, `prev`, `first`, `last` | Pagination links, as described in [API Pagination](../pagination/README.md). |
| `create-order` | **REQUIRED** if individual Opportunities do not include a `create-order` link, otherwise it is **strongly recommended**. This allows the user to resubmit the Opportunities request as an Order. |
| `search-record` | The search used to generate the Opportunities result. **strongly recommended** to point to `GET /searches/opportunities/{searchRecordId}` when the result of an async search |

### Opportunity Object

This object describes a STAPI Opportunity. The input fields will be contained
in the `properties` of each Feature in the GeoJSON response.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| type | string | **REQUIRED.** Type of the GeoJSON Object. **Must** be `Feature`. |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `Opportunity`. |
| stapi_version | string | **REQUIRED.** The STAPI version the Opportunity implements. |
| id | string | Provider identifier. This is not required, unless the provider tracks user requests and state for opportunities (as when supporting async searches). |
| geometry | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) | **REQUIRED.** Defines the estimated footprint or centroid of the Opportunity, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| bbox | [number] | **REQUIRED.** Bounding Box of the estimated extent of this Opportunity, formatted according to [RFC 7946, section 5](https://tools.ietf.org/html/rfc7946#section-5). |
| properties | [Properties Object](#properties-object) | **REQUIRED.** A dictionary of additional metadata for the Opportunity. |
| links | [[Link Object](../link/README.md)] | **REQUIRED.** List of link objects to resources and related URLs. See [Opportunity Links](#opportunity-links). |

#### bbox

Bounding Box of the Opportunity using either 2D or 3D
geometries, formatted according to [RFC 7946, section
5](https://tools.ietf.org/html/rfc7946#section-5).  The length of the array
must be 2\*n where n is the number of dimensions.  The array contains all axes
of the southwesterly most extent followed by all axes of the northeasterly most
extent specified in Longitude/Latitude or Longitude/Latitude/Elevation based on
[WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84).  When using 3D
geometries, the elevation of the southwesterly most extent is the minimum
depth/height in meters and the elevation of the northeasterly most extent is
the maximum.  This field enables more naive clients to easily index and search
geospatially.  Implementations are required to compute intersection
operations with the Opportunity's geometry field, not its bbox.

#### Properties Object

Additional metadata fields can be added to the GeoJSON Object Properties that
describe the Opportunity in more detail for the user. The only required fields
are `datetime` and `product_id` but it is recommended to add more fields as
required to describe the opportunity in meaningful terms to the requestor.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| datetime       | string                                                                     | **REQUIRED.** Datetime field is a [ISO8601 Time Interval](https://en.wikipedia.org/wiki/ISO_8601#Time_intervals) |
| product_id | string | **REQUIRED.** Product identifier ([see Product Object](../product/README.md#product-object)) |

#### Opportunity Links

Each link in the links array must be a [Link Object](../link/README.md).

| rel type | Description |
| ---------- | ----------- |
| `create-order` | **Strongly recommended**. Such a link allows the user to submit an Order specifically for the Opportunity. |

##### rel=create-order

This [Link Object](../link/README.md) fully describes the necessary HTTP
request to submit an Order for this Opportunity via
[Create Order](../order/README.md#create-order-request), using the [additional
Link fields](../link/README.md#additional-link-fields).

To conform to the Create Order spec, use `"method": "POST"`.

The `body` of the link must be a valid [Order Request
Object](../order/README.md#order-request-object) for ordering this
Opportunity.

It is **strongly recommended** to include a `rel=create-order` link on
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

## Async Opportunity Search

- **Conformance URI:** `https://stapi.example.com/v0.2.0/opportunities-async`

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
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `OpportunitySearchRecord`. |
| stapi_version | string | **REQUIRED.** The STAPI version the Opportunity Search Record implements. |
| id | string | **REQUIRED.** Opportunity search record ID. |
| product_id | string | **REQUIRED.** Product identifier. This should be a reference to the [Product](../product/README.md#product-object) being searched. |
| search_parameters | [Search Parameters Object](../search-parameters/README.md) | **REQUIRED.** The parameters of the search this record describes. These are the `search_parameters` of the Opportunity Request that initiated the search; the pagination fields of that request are not part of the search and are not recorded here. |
| status | [Opportunity Search Status](#opportunity-search-status) | **REQUIRED.** The current search status. |
| links | [[Link Object](../link/README.md)] | **REQUIRED.** List of link objects to resources and related URLs. See [Opportunity Search Links](#opportunity-search-links). |

#### Opportunity Search Links

##### rel=self

The `links` **must** include a [Link Object](../link/README.md) with the href to
retrieve the Opportunity Search Record directly.

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

This link **must** be included when the search is completed.

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
choose a default behavior to allow clients to successfully request opportunities
without specifying a preference.

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
| timestamp | datetime | **REQUIRED.** ISO 8601 timestamp for the search status |
| status_code | string | **REQUIRED.** Enumerated status code |
| reason_code | string | Enumerated reason code for why the status was set |
| reason_text | string | Textual description for why the status was set |
| links | [[Link Object](../link/README.md)] | **REQUIRED.** list of references to any relevant documents or resources. |

Links is intended to be the same data structure as links collection in STAC.
Links will be very provider specific.

#### Enumerated status codes

- received (indicates search received by provider and it passed format validation.)
- in_progress (indicates search is running)
- failed (indicates search will not be fulfilled for some error reason)
- cancelled (indicates search was cancelled for any reason)
- completed (indicates search has completed successfully and the results can be retrieved)

Providers must support these statuses.

State machine intent (currently no mandate to enforce)

- received -> in_progress or cancelled.
- in_progress -> completed, failed, or cancelled.
