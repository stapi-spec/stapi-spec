## Overview

This document explains the structure of a STAT **Order** request which is used for placing orders. 

Ordering with loosely defined order values will give the provider more freedom to schedule. Define the values strictly to increase the chance of the preferred capture moment.

## Order Request

for POST /orders

| Field Name | Type                                                                       | Description |
| ---------- | -------------------------------------------------------------------------- | ----------- |
| datetime       | string                                                                     | **REQUIRED.** Datetime field is a [ISO8601 Time Interval](https://en.wikipedia.org/wiki/ISO_8601#Time_intervals) |
| product_id         | string                                                                     | **REQUIRED.** Product identifier. The ID should be unique and is a reference to the constraints which can be used in the constraints field. |
| geometry   | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) | **REQUIRED.** Defines the full footprint of the asset represented by this item, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| filter | CQL2 JSON | A set of additional constraints in [CQL2 JSON](https://docs.ogc.org/DRAFTS/21-065.html) based on the constraints exposed in the product. |

## Order Collection

for GET /orders

| Field Name | Type                      | Description |
| ---------- | ------------------------- | ----------- |
| orders     | \[Order Object\]          | **REQUIRED.** A list of orders. |
| links      | Map\<object, Link Object> | **REQUIRED.** Links for e.g. pagination. |

### Order Object

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| id   | string | Unique provider generated order ID |
| user | string | User or organization ID ? |
| status | OrderStatus | Enumerated Status of the Order |
| created | datetime | When the order was created |
| updated | datetime | When the order was last updated |
| links    | [string] | List of URIs or IDs of Items |
