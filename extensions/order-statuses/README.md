# Overview

- **Conformance URI:** <https://stapi.example.com/v0.1.0/order-statuses>

This document explains the structure of a STAPI **Order Statuses** request.
Operation returns a list/array of statuses that have affected an order.  The
most recent status code is the current status of the order.

The `GET /orders/{orderId}` endpoint must add a link to this endpoint using the
relation type `monitor`.

Endpoint: `GET /orders/{orderId}/statuses`

Pagination will follow the convention outlined in [the api
spec](../../api-spec.md#pagination).

## Order Statuses Request

Get operation only.

## Order Statuses Response

Response has two fields:

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| statuses | \[OrderStatus\] | **REQUIRED.** History of statuses |
| links | \[Link Object\] | **REQUIRED.** A list of references to other endpoints. |

The [Order Status](../../order/README.md#order-status) object is described in
the Order README.
