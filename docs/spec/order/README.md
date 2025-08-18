# Overview

This document explains the structure of a STAPI **Order** request which is used
for placing orders.

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
| productId | string | Product identifier. The ID should be unique and is a reference to the [queryables](../product/README.md#queryables) which can be used in the filter field. |

### Body Fields

| Name | Type | Description |
| ---- | ---- | ----------- |
| search_parameters | [Search Parameter Object](../search-parameters/README.md) | **REQUIRED.** Parameters for scenes that would meet the Order's requirements |
| order_parameters | JSON Object | **REQUIRED.** Order Parameters properties that can be used when creating an Order, reference [Order Parameters](../product/README.md#order-parameters) |

#### order_parameters

Order Parameters define Product options that can be used when creating an
Order.  These are different than Product Queryables, in that they do not
constrain (filter) the desired results, but rather define general properties of
an entire order. For example, an order parameter might define what file format
to use delivery or what location to deliver to.

By default, the absence of any defined order parameters on a product would
indicate that only an empty object is valid.

### Create Order Response

The response is using HTTP status code 201 and provides the location of the
newly created order, which points to `GET /order/{orderId}`.

Example:

```http
HTTP 201 Created
Location: https://example.com/orders/123
```

## GET /orders

### Get Orders Response

When fetching a list of Orders the response is a GeoJSON Feature Collection,
where each Feature in the collection is an [Order Object](#order-object).

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| type | string | **REQUIRED.** Type of the GeoJSON Object. **Must** be set to `FeatureCollection`. |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `OrderCollection`. |
| stapi_version | string | **REQUIRED.** The STAPI version the Order Collection implements. |
| features | \[[Order Object](#order-object)\] | **REQUIRED.** A list of orders. |
| links | \[[Link Object](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#link-object)\] | **REQUIRED.** Links, e.g., for pagination. |

## GET /orders/\{id\}

### Path Parameters

| Name | Type | Description |
| ---- | ---- | ----------- |
| id | string | Order ID to retrieve |

### Get Order Response

See [Order Object](#order-object).

## Order Object

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| type | string | **REQUIRED.** Type of the GeoJSON Object. **Must** be set to `Feature`. |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `Order`. |
| stapi_version | string | **REQUIRED.** The STAPI version the Order implements. |
| id | string | **REQUIRED.** Unique provider generated order ID |
| geometry | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) \| [null](https://tools.ietf.org/html/rfc7946#section-3.2) | **REQUIRED.** Defines the estimated footprint or centroid of the area to be collected to fulfill this order, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| bbox | [number] | **REQUIRED if `geometry` is `null`.** Bounding Box of the estimated extent to be collected to fulfill this Order, formatted according to [RFC 7946, section 5](https://tools.ietf.org/html/rfc7946#section-5). |
| properties | [Order Properties Object](#order-properties-object) | **REQUIRED.** A dictionary of additional metadata for the Order. |
| links | \[[Link Object](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#link-object)\] | |

If the `GET /orders/{orderId}/statuses` endpoint is implemented, there must be
a link to the endpoint using the relation type `monitor`.

## Order Properties Object

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| product_id | string | **REQUIRED.** Product identifier. This should be a reference to the [Product](../product/README.md) being ordered. |
| created | datetime | **REQUIRED.** When the order was created |
| status | [Order Status Object](#order-status) | **REQUIRED.** Current Order Status object |
| order_request | [Order Request Object](#body-fields) | **REQUIRED.** Object with the request search and order parameters |
| owner | JSON Object \| `null` | Optional object with any properties required for identifying the entity that placed the order (user, organization, etc). |

## Order Status

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| timestamp | datetime | **REQUIRED.** ISO 8601 timestamp for the order status |
| status_code | string | **REQUIRED.** Enumerated status code |
| reason_code | string | Enumerated reason code for why the status was set |
| reason_text | string | Textual description for why the status was set |
| links | \[Link Object\] | **REQUIRED.** list of references to documents, such as delivered asset, processing log, delivery manifest, etc. |

Links is intended to be the same data structure as links collection in STAC.
Links will be very provider specific.

### Enumerated status codes

#### Code status codes

* received (indicates order received by provider and it passed format
  validation.)
* accepted (indicates order has been accepted)
* rejected (indicates order will not be fulfilled)
* completed (indicates provider was able to successfully collect imagery)
* cancelled (indicates provider was unable to collect imagery)
* failed (indicates when an order could not be completed/proccesed
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
