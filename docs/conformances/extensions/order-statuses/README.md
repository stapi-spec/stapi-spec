# Overview

- **Conformance URI:** `https://stapi.example.com/v0.2.0/order-statuses`

This document explains the structure of a STAPI **Order Statuses** request.
Operation returns a list/array of statuses that have affected an order.  The
most recent status code is the current status of the order.

The `GET /orders/{orderId}` endpoint must add a link to this endpoint using the
relation type `monitor`.

Endpoint: `GET /orders/{orderId}/statuses`

Pagination will follow the convention outlined in [the api
spec](../../../spec/pagination/README.md).

## Order Statuses Request

Get operation only.

## Order Status Collection

The response is an Order Status Collection with the following structure:

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `OrderStatusCollection`. |
| stapi_version | string | **REQUIRED.** The STAPI version the Order Status Collection implements. |
| statuses | \[OrderStatus\] | **REQUIRED.** History of statuses, in reverse chronological order. |
| links | \[Link Object\] | **REQUIRED.** A list of references to other endpoints. |
| numberMatched | integer | **OPTIONAL.** The number of statuses matched by the request, across all pages, if known and the implementation chooses to include it. |

The [Order Status](../../../spec/order/README.md#order-status) object is
described in the Order README.
