## Overview

This document explains the structure of a STAT Order request which is used for finding opportunities and placing orders. 

# Order Spec

| Field Name | Type                                                                       | Description |
| ---------- | -------------------------------------------------------------------------- | ----------- |
| datetime       | string                                                                     | **REQUIRED.** Datetime field is a [ISO8601 Time Interval](https://en.wikipedia.org/wiki/ISO_8601#Time_intervals) |
| product_id         | string                                                                     | **REQUIRED.** Product identifier. The ID should be unique and is a reference to the constraints which can be used in the constraints field. |
| geometry   | [GeoJSON Geometry Object](https://tools.ietf.org/html/rfc7946#section-3.1) | **REQUIRED.** Defines the full footprint of the asset represented by this item, formatted according to [RFC 7946, section 3.1](https://tools.ietf.org/html/rfc7946#section-3.1). The footprint should be the default GeoJSON geometry, though additional geometries can be included. Coordinates are specified in Longitude/Latitude or Longitude/Latitude/Elevation based on [WGS 84](http://www.opengis.net/def/crs/OGC/1.3/CRS84). |
| constraints | Map<string, \[\*]\|[Range Object](#range-object)\|[JSON Schema Object](#json-schema-object)> | STRONGLY RECOMMENDED. A map of opportunity constraints, either a set of values, a range of values or a JSON Schema.

To know which constraints are available for which *product_id*, a user would have to first explore the [product](../product-spec/README.md#Product-Spec).

Ordering with losely defined order values will give the provider more freedom to schedule. Define the values strict to increase the chance of the prefered capture moment.

## Finding opportunities

Before ordering a user would be able to explore the opportunities which are available for chosen order configuration. The opportunities are represented in the a FeatureCollection, with order specific attributes and values in the feature properties. An example json response can be found [here](../examples/tasking-api/opportunities-response.json).
