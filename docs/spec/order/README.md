# Overview

This document explains the structure of the STAPI **Order** entities: the
Order Request used for placing orders, and the Order Object and Order
Collection returned when retrieving them.

Ordering with loosely defined order values will give the provider more freedom
to schedule. Define the values strictly to increase the chance of the preferred
capture moment.

## POST /products/\{productId\}/orders

### Create Order Request

The endpoint `POST /products/{productId}/orders` is parameterized in the
following way:

### Path Parameters

| Name | Type | Description |
| ---- | ---- | ----------- |
| productId | string | **REQUIRED.** Product identifier ([see Product Object](../product/README.md#product-object)) |

### Order Request Object

| Name | Type | Description |
| ---- | ---- | ----------- |
| search_parameters | [Search Parameters Object](../search-parameters/README.md) | **REQUIRED.** Parameters for scenes that would meet the Order's requirements |
| order_parameters | JSON Object | Order Parameters to apply when creating the Order, as defined by the Product's [Order Parameters](../product/README.md#order-parameters) schema. May be omitted; omission is equivalent to providing an empty object (`{}`). |

#### order_parameters

Order Parameters are defined by the Product; see [Order
Parameters](../product/README.md#order-parameters) for what they are and how a
Product advertises them.

The `order_parameters` value—or `{}` when the field is omitted—must validate
against the Product's [Order Parameters](../product/README.md#order-parameters)
schema. A Product that marks one or more order parameters as required thereby
makes this field effectively required, as an empty object will fail
validation. A Product defining no order parameters accepts only an omitted or
empty `order_parameters` object.

### Create Order Response

The response must use HTTP status code 201. The `Location` header must
provide the location of the newly created order, pointing to
`GET /orders/{orderId}`, and the response body must be the newly created
[Order Object](#order-object).

Example:

```http
HTTP 201 Created
Location: https://example.com/orders/123
```

## GET /orders

### Get Orders Response

See [Order Collection](#order-collection).

## Order Collection

When fetching a list of Orders the response is an Order Collection, a GeoJSON
FeatureCollection where each Feature is an [Order Object](#order-object).

In addition to the fields common to every [Collection
Object](../collection/README.md), an Order Collection has the following fields.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| type | string | **REQUIRED.** Type of the GeoJSON Object. **Must** be set to `FeatureCollection`. |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `OrderCollection`. |
| features | \[[Order Object](#order-object)\] | **REQUIRED.** A list of orders. |

## GET /orders/\{orderId\}

### Path Parameters

| Name | Type | Description |
| ---- | ---- | ----------- |
| orderId | string | Order ID to retrieve |

### Get Order Response

See [Order Object](#order-object).

## Order Object

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| type | string | **REQUIRED.** Type of the GeoJSON Object. **Must** be set to `Feature`. |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `Order`. |
| stapi_version | string | **REQUIRED.** The STAPI version the Order implements. |
| id | string | **REQUIRED.** Unique provider generated order ID |
| geometry | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) | **REQUIRED.** Defines the estimated footprint or centroid of the area to be collected to fulfill this order, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| bbox | [number] | **REQUIRED.** Bounding Box of the estimated extent to be collected to fulfill this Order, formatted according to [RFC 7946, section 5](https://tools.ietf.org/html/rfc7946#section-5). |
| properties | [Order Properties Object](#order-properties-object) | **REQUIRED.** A dictionary of additional metadata for the Order. |
| links | \[[Link Object](../link/README.md)\] | **REQUIRED.** List of link objects to resources and related URLs. |

If the `GET /orders/{orderId}/statuses` endpoint is implemented, there must be
a link to the endpoint using the relation type `monitor`.

## Order Properties Object

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| product_id | string | **REQUIRED.** Product identifier. This should be a reference to the [Product](../product/README.md#product-object) being ordered. |
| created | datetime | **REQUIRED.** When the order was created |
| status | [Order Status Object](#order-status) | **REQUIRED.** Current Order Status object |
| order_request | [Order Request Object](#order-request-object) | **REQUIRED.** The request the Order was created from, as recorded by the server. It differs from the submitted Order Request Object in one respect: `order_parameters` is always present, and an Order created without them records an empty object (`{}`). |

## Order Status

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| timestamp | datetime | **REQUIRED.** ISO 8601 timestamp for the order status |
| status_code | string | **REQUIRED.** Enumerated status code |
| reason_code | string | Enumerated reason code for why the status was set |
| reason_text | string | Textual description for why the status was set |
| links | \[[Link Object](../link/README.md)\] | **REQUIRED.** list of references to documents, such as delivered asset, processing log, delivery manifest, etc. |

Links is intended to be the same data structure as links collection in STAC.
Links will be very provider specific.

### Enumerated status codes

#### Core status codes

* received (indicates order received by provider and it passed format
  validation.)
* accepted (indicates order has been accepted)
* rejected (indicates order will not be fulfilled)
* completed (indicates provider was able to successfully collect imagery)
* cancelled (indicates provider was unable to collect imagery)
* failed (indicates when an order could not be completed/processed
  successfully)
* expired (indicates the order request window has expired and no collection was
  made)

Providers must support these statuses.

State machine intent (currently no mandate to enforce)

* Received -> accepted or rejected.
* Accepted -> completed or cancelled.

#### Optional status codes

Providers may support these statuses.

* scheduled (indicates order has been scheduled, no longer subject to customer
  cancellation)
* held (order held for manual review)
* processing (indicates some sort of processing has taken place, such as data
  was downlinked, processed or delivered)
* reserved (action needed by customer prior to acceptance, such as payment)

#### Extension status codes

Providers may support additional statuses through extensions. For example:

* tasked (indicates tasking commands have been issued to the
  satellite/constellation)
* user_cancelled (indicates that the user cancelled the request)

### Enumerated reason codes

Code indicating why a status was set. These are just examples at the moment.
No consensus has been achieved as to what reasons should be core and handled in
the same way by all providers, and which should be by extension.

* invalid_geometry (invalid should be renamed, means that a valid geometry
  failed business rules)
* competition (e.g., failed tasking auction)
* cloud_cover (imagery rejected for cloud coverage)
* partial_delivery (indicates a file was processed and placed in catalog, used
  with processing)
