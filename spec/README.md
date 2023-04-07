# About

The SpatioTemporal Asset Tasking (STAT) API define a JSON-based web API to query for potential future data
and place orders ("tasking") for data from remote sensing data providers (satellite or airborne) that 
will be collected in the future.

The STAT specifications define several new entities (Products, Opportunities, and Orders) that are  
derived from the [SpatioTemporal Asset Catalog](stac-spec/) (STAC) specification. Ideally, tasking requests
to providers will be ultimately fulfilled via delivery of a STAC Item, so STAT aims to align
with STAC core and extension field names where appropriate.

The core STAT specification provides a structure and language to describe Products, Opportunities, and Orders.
The process of interacting with a data provider is done through a REST API.

## STAT API Description

### Core

The [Core](core/) of STAT API supports Products returned via the `/products` endpoint, and 


returns JSON with a description of the STAT API specifications to which it conforms.
The `links` section is the jumping-off point for the more powerful capabilities - it contains a list of URLs with
link 'relationships' (`rel`) and descriptions to indicate their functionality. Note that the [STAT Core specification](stac-spec)
provides most of the content of API responses - the STAT API is primarily concerned with the return of STAT Product and Order objects.

The idea is that the /order endpoint can be 

### Opportunities

The `/opportunities` endpoint provides an additional feature on top of core. It allows users more fine-grained 
control and selection of available tasking opportunities.

## Endpoints

STAC APIs follow the modern web API practices of using HTTP Request Methods ("verbs") and
the `Content-Type` header to drive behavior on resources ("nouns") in the endpoints listed below.

The following table describes the service resources available in a STAC API implementation that
supports all three of the foundation specifications. Note that the 'Endpoint'
column is more of an example in some cases. OGC API makes some endpoint locations required, those will be bolded below.

| Endpoint                       | Specified in   | Returns                       | Description  |
| ------------------------------ | -------------- | ----------------------------- | ------------ |
| `/`                            | Core           | [?]()                         | |
| `/products`                    | Core           | [ProductsCollection]()        | |
| `/orders`                      | Core           | [OrdersCollection]()          | |
| POST `/orders`                 | Core           | [Order]()                     | |
| `/products/{productId}`        | Core           | [Product]()                   | |
| `/opportunities`               | Opportunities  | [OpportunitiesCollection]()   | |
| POST `/opportunities`          | Opportunities  | [Opportunity]()               | |

## Conformance Classes

STAT API utilizes OGC API Features [Conformance](http://docs.opengeospatial.org/is/17-069r3/17-069r3.html#_declaration_of_conformance_classes)
JSON structure. For STAT API, we declare new STAC conformance classes, with the core ones detailed in the table below.

The core STAT conformance classes communicate the conformance JSON only in the root (`/`) document, while OGC API
requires they also live at the `/conformance` endpoint. STAT's conformance structure is detailed in the
[core](core/). Note all conformance URIs serve up a rendered HTML version of the corresponding OpenAPI document at the given location.

### Conformance Class Table

| **Name**               | **Specified in**                            | **Conformance URI**                                    | **Description**                                                                                                 |
| ---------------------- | ------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| STAT API - Core        | [Core](core)                                |            | Specifies the STAT Landing page `/`, communicating conformance and available endpoints.                         |
| STAT API - Opportunities | [Opportunities](opportunity)                  |    | Enables request of potential tasking opportunities |                            |


## Example Landing Page

When all three conformance classes (Core, Features, Item Search) are implemented, the relationships among
various resources are shown in the following diagram. In each node, there is also a `self` and `root` link
that are not depicted to keep the diagram more concise.

![Diagram of STAC link relations](stac-api.png)

The Landing Page will at least have the following `conformsTo` and `links`:

```json
{
    "stat_version": "0.1.0",
    "id": "example-stat-api",
    "title": "A simple STAT API Example",
    "description": "This API demonstrated the landing page for a SpatioTemporal Asset Tasking API",
    "conformsTo" : [
        "https://stat-api.example.com/v0.1.0/core"
    ],
    "links": [
        {
            "rel": "conformance",
            "type": "application/json",
            "href": "https://stat-api.example.com/conformance"
        },
        {
            "rel": "service-desc",
            "type": "application/vnd.oai.openapi+json;version=3.0",
            "href": "https://stat-api.example.com/api"
        },
        {
            "rel": "service-doc",
            "type": "text/html",
            "href": "https://stat-api.example.com/api.html"
        },
    ]
}
```