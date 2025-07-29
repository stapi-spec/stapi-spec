# Conformance Classes

## API-level Conformance Classes

The STAPI uses OAFeat's
[Conformance](http://docs.opengeospatial.org/is/17-069r3/17-069r3.html#_declaration_of_conformance_classes)
JSON structure. For STAPI we reuse OGC conformance classes where possible, and
declare new STAPI-specific conformance classes with the core ones detailed in
the table below.  The core STAPI conformance classes communicate the
conformance JSON in the root (`/`) document, while OGC API requires they also
live at the `/conformance` endpoint. STAPI's root conformance structure is
detailed in the [core](core/README.md). Conformance classes applicable to the
root API are listed in the table below.

| **Name** | **Specified in** | **Conformance URI** | **Description** |
| -------- | ---------------- | ------------------- | --------------- |
| STAPI - Core | [Core](core/README.md) | https://stapi.example.com/v0.1.0/core | Specifies the STAPI Landing page `/`, communicating conformance and available endpoints. |
| STAPI - Order Statuses | [Order Statuses](extensions/order-statuses/README.md) | https://stapi.example.com/v0.1.0/order-statuses | |
| STAPI - Searches - Opportunity | [Searches - Opportunity](extensions/searches/opportunity/README.md) | https://stapi.example.com/v0.1.0/searches-opportunity | |
| STAPI - Searches - Opportunity - Statuses | [Searches - Opportunity - Statuses](extensions/searches/opportunity-statuses/README.md) | https://stapi.example.com/v0.1.0/searches-opportunity-statuses | |

## Product Conformance Classes

Products also advertise conformance classes to communicate what support is
available on a per-product basis, as not all Products may support the same
features or parameter types. The conformance classes applicable at the Product
level are listed in the following table.

| **Name** | **Specified in** | **Conformance URI** | **Description** |
| -------- | ---------------- | ------------------- | --------------- |
| STAPI - Opportunities | [Opportunities](../spec/opportunity/README.md) | https://stapi.example.com/v0.1.0/opportunities | Enables sync request of potential tasking opportunities |
| STAPI - Opportunities (Async) | [Opportunities](../spec/opportunity/README.md) | https://stapi.example.com/v0.1.0/opportunities-async | Enables async request of potential tasking opportunities |
| STAPI - Core | Core | https://geojson.org/schema/Point.json | Allows submitting orders with GeoJSON points |
| STAPI - Core | Core | https://geojson.org/schema/LineString.json | Allows submitting orders with GeoJSON linestrings |
| STAPI - Core | Core | https://geojson.org/schema/Polygon.json | Allows submitting orders with GeoJSON polygons |
| STAPI - Core | Core | https://geojson.org/schema/MultiPoint.json | Allows submitting orders with GeoJSON multi points |
| STAPI - Core | Core | https://geojson.org/schema/MultiPolygon.json | Allows submitting orders with GeoJSON multi polygons |
| STAPI - Core | Core | https://geojson.org/schema/MultiLineString.json | Allows submitting orders with GeoJSON multi linestring |

Products must advertise at least one of the geometry conformance classes.
