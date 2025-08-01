# STAPI Specification

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
| `GET /` | Core | root | Landing Page | Returns API metadata and links |
| `GET /conformance` | Core | `conformance` | JSON | API-level conformance classes |
| `GET /products` | Core | `products` | [Products Collection](./product/README.md#product-collection) | Figure out which queryables are available for which `productId` |
| `GET /products/{productId}` | Core | `product` | [Product](./product/README.md#product-object) | |
| `GET /products/{productId}/conformance` | Core | `conformance` | JSON | Product-specific conformance classes |
| `GET /products/{productId}/queryables` | Core | `queryables` | JSON Schema | |
| `GET /products/{productId}/order-parameters` | Core | `order-parameters` | JSON Schema | |
| `GET /orders` | Core | `orders` | [Orders Collection](./order/README.md#get-orders-response) | |
| `GET /orders/{orderId}` | Core | `order` | [Order Object](./order/README.md#order-object) | |
| `GET /orders/{orderId}/statuses` | Order Statuses | `monitor` | [[Order Status](../conformances/extensions/order-statuses/README.md#order-statuses-response)] | |
| `POST /products/{productId}/orders` | Core | `create-order` | - | Place an Order. Accepts an [Order Request](./order/README.md#create-order-request). |
| `POST /products/{productId}/opportunities` | Opportunities | `opportunities` | Sync search: [Opportunities Collection](./opportunity/README.md#opportunity-collection); Async search: [Opportunity Search Record](./opportunity/README.md#opportunity-search-record) | Explore available Opportunities. Accepts an [Opportunity Request](./opportunity/README.md#opportunity-request). |
| `GET /products/{productId}/opportunities/{opportunityCollectionId}` | Opportunities (Async) | `opportunities` | [Opportunities Collection](./opportunity/README.md#opportunity-collection) | Get the opportunity collection for an async opportunity search |
| `GET /searches/opportunities` | [Searches - Opportunity](../conformances/extensions/searches/opportunity/README.md) | `search-records` | [Opportunity Search Record Collection](../conformances/extensions/searches/opportunity/README.md#opportunity-search-record-collection)] | List all Opportunity Search Records |
| `GET /searches/opportunities/{searchRecordId}` | [Searches - Opportunity](../conformances/extensions/searches/opportunity/README.md) | `search-record` | [Opportunity Search Record](./opportunity/README.md#opportunity-search-record) | Fetch a specific Opportunity Search Record |
| `GET /searches/opportunities/{searchRecordId}/statuses` | [Searches - Opportunity - Statuses](../conformances/extensions/searches/opportunity-statuses/README.md) | `monitor` | [[Opportunity Search Status](./opportunity/README.md#opportunity-search-status)] | Get status history for an Opportunity Search Record |
