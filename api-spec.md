# About

The Sensor Tasking API (STAPI) defines a JSON-based web API to query for
spatio-temporal analytic and data products derived from remote sensing
(satellite or airborne) providers. The specification supports both products
derived from new tasking and products from provider archives.

Generally speaking, users of STAPI will review available Products from one or
more providers, request Opportunities that are possible Orders for those
Products, and then submit one or more Orders to receive Products from Providers
represented by one or more data artifacts.

The STAPI is primarily designed around machine-to-machine interactions.

## STAPI Description

### Endpoints

STAPI follows the modern web API practices of using HTTP Request Methods
("verbs") and the `Content-Type` header to drive behavior on resources
("nouns") in the endpoints listed below.

The following table describes the service resources available in a STAPI
implementation that supports all three of the foundation specifications. Note
that the 'Endpoint' column is more of an example in some cases.

| Endpoint | Specified in | Link Relationship | Returns | Description |
| -------- | ------------ | ----------------- | ------- | ----------- |
| `GET /` | Core | root | [Landing Page](#landing-page) | |
| `GET /conformance` | Core | `conformance` | JSON | API-level conformance classes |
| `GET /products` | Core | `products` | [Products Collection](./product/README.md) | Figure out which queryables are available for which `productId` |
| `GET /products/{productId}` | Core | `product` | [Product](./product/README.md) | |
| `GET /products/{productId}/conformance` | Core | `conformance` | JSON | Product-specific conformance classes |
| `GET /products/{productId}/queryables` | Core | `queryables` | JSON Schema | |
| `GET /products/{productId}/order-parameters` | Core | `order-parameters` | JSON Schema | |
| `GET /orders` | Core | `orders` | [Orders Collection](./order/README.md#order-collection) | |
| `GET /orders/{orderId}` | Core | `order` | [Order Object](./order/README.md#order-object) | |
| `GET /orders/{orderId}/statuses` | Order Statuses | `monitor` | [[Order Status ](./extensions/order-statuses/README.md#order-statuses-response)] | |
| `POST /products/{productId}/orders` | Core | `create-order` | - | Order a capture with a particular set of [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters) as defined in the products or a request that was provided through the opportunities endpoint. Accepts an [Order Request](./order/README.md#order-request). |
| `POST /products/{productId}/opportunities` | Opportunities | `opportunities` | Sync search: [Opportunities Collection](./opportunity/README.md#opportunities-collection); Async search: [Opportunity Search Record](./opportunity/README.md#opportunity-search-record) | Explore the opportunities available for a particular set of [parameters](https://github.com/Element84/stapi-spec/blob/main/product/README.md#parameters). Accepts an [Opportunity Request](./opportunity/README.md#opportunity-request). |
| `GET /products/{productId}/opportunities/{opportunityCollectionId}` | Opportunities (Async) | `opportunities` | [Opportunities Collection](./opportunity/README.md#opportunities-collection) | Get the opportunity collection for an async opportunity search |
| `GET /searches/opportunities` | Searches - Opportunity | `search-records` | [[Opportunity Search Record](./opportunity/README.md#opportunity-search-record)] | |
| `GET /searches/opportunities/{searchRecordId}` | Searches - Opportunity | `search-record` | [Opportunity Search Record](./opportunity/README.md#opportunity-search-record) | |
| `GET /searches/opportunities/{searchRecordId}/statuses` | Searches - Opportunity - Statuses | `monitor` | [[Opportunity Search Status](./opportunity/README.md#opportunity-search-status)] | |

## Conformance Classes

### API-level Conformance Classes

The STAPI uses OAFeat's
[Conformance](http://docs.opengeospatial.org/is/17-069r3/17-069r3.html#_declaration_of_conformance_classes)
JSON structure. For STAPI we reuse OGC conformance classes where possible, and
declare new STAPI-specific conformance classes with the core ones detailed in
the table below.  The core STAPI conformance classes communicate the
conformance JSON in the root (`/`) document, while OGC API requires they also
live at the `/conformance` endpoint. STAPI's root conformance structure is
detailed in the [core](core/). Conformance classes applicable to the root API
are listed in the table below.

| **Name** | **Specified in** | **Conformance URI** | **Description** |
| -------- | ---------------- | ------------------- | --------------- |
| STAPI - Core | [Core](core/) | https://stapi.example.com/v0.1.0/core | Specifies the STAPI Landing page `/`, communicating conformance and available endpoints. |
| STAPI - Order Statuses | [Order Statuses](extensions/order-statuses/README.md) | https://stapi.example.com/v0.1.0/order-statuses | |
| STAPI - Searches - Opportunity | [Searches - Opportunity](extensions/searches/opportunity/README.md) | https://stapi.example.com/v0.1.0/searches-opportunity | |
| STAPI - Searches - Opportunity - Statuses | [Searches - Opportunity - Statuses](extensions/searches/opportunity-statuses/README.md) | https://stapi.example.com/v0.1.0/searches-opportunity-statuses | |

### Product Conformance Classes

Products also advertise conformance classes to communicate what support is
available on a per-product basis, as not all Products may support the same
features or parameter types. The conformance classes applicable at the Product
level are listed in the following table.

| **Name** | **Specified in** | **Conformance URI** | **Description** |
| -------- | ---------------- | ------------------- | --------------- |
| STAPI - Opportunities | [Opportunities](opportunity/README.md) | https://stapi.example.com/v0.1.0/opportunities | Enables sync request of potential tasking opportunities |
| STAPI - Opportunities (Async) | [Opportunities](opportunity/README.md) | https://stapi.example.com/v0.1.0/opportunities-async | Enables async request of potential tasking opportunities |
| STAPI - Core | Core | https://geojson.org/schema/Point.json | Allows submitting orders with GeoJSON points |
| STAPI - Core | Core | https://geojson.org/schema/LineString.json | Allows submitting orders with GeoJSON linestrings |
| STAPI - Core | Core | https://geojson.org/schema/Polygon.json | Allows submitting orders with GeoJSON polygons |
| STAPI - Core | Core | https://geojson.org/schema/MultiPoint.json | Allows submitting orders with GeoJSON multi points |
| STAPI - Core | Core | https://geojson.org/schema/MultiPolygon.json | Allows submitting orders with GeoJSON multi polygons |
| STAPI - Core | Core | https://geojson.org/schema/MultiLineString.json | Allows submitting orders with GeoJSON multi linestring |

Products must advertise at least one of the geometry conformance classes.

## Pagination

STAPI supports paging through hypermedia links for all endpoints returning a
list of entities, including the following:

- `GET /products`
- `POST /products/{productId}/opportunities`
- `GET /products/{productId}/opportunities/{opportunityCollectionId}`
- `GET /orders`
- `GET /orders/{orderId}/statuses`
- `GET /searches/opportunities/`

The following relation types may be available for pagination:

- `next` to provide a link to the next page
- `prev` to provide a link to the previous page (optional)
- `first` to provide a link to the first page (optional)
- `last` to provide a link to the last page (optional)

This link href must contain any request parameters that are necessary
for the implementation to understand how to provide the next page of results,
e.g., the query parameters `page`, `next`, or `token`.

For example, the links array could look like this for a API that supports
a parameter `page` and is currently on page 2:

```json
    "links": [
        {
            "rel": "prev",
            "type": "application/json",
            "href": "https://stapi.example.com/products?page=1",
            "title": "Next page"
        },
        {
            "rel": "next",
            "type": "application/json",
            "href": "https://stapi.example.com/products?page=3",
            "title": "Next page"
        }
    ]
```

The href may contain any arbitrary URL parameter, which is implementation-specific:

- `https://stapi.example.com/products?page=2`
- `https://stapi.example.com/products?next=8a35eba9c`
- `https://stapi.example.com/products?token=f32890a0bdb09ac3`

In addition to supporting query parameters in the URL value of the `href` field,
the Link object can contain additional fields to support more complex HTTP requests:

- `method` to specify an HTTP method in uppercase (e.g. `GET` or `POST`),
- `headers` to add HTTP headers in the request,
- `body` with the entire body for the request.

The specification is compatible to pagination mechanisms defined in STAC API.
