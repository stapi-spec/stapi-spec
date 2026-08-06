# Core

- **Conformance URI:** `https://stapi.example.com/v0.2.0/core`
- [OpenAPI document](../../api.md)
- [Rendered API documentation](https://stapi-spec.github.io/stapi-spec/dev/)

The core of STAPI includes the `/products` endpoint and the `/orders` endpoint.

To know which parameters are available for which `productId`, users first
explore [/products](../../spec/product/README.md). These parameters can be used to form
a POST to the `/products/{productId}/orders` endpoint.

## Landing Page

- [Example](./examples/landingpage.json)

Fields that can be included in the response body for `GET /`.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| id | string | **REQUIRED.** Identifier for the API. |
| conformsTo | [string] | **REQUIRED.** Conformance classes that apply to the API globally. |
| title | string | A short descriptive one-line title for the API. |
| description | string | **REQUIRED.** Detailed multi-line description to fully explain the API. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation. |
| links | [[Link Object](../../spec/link/README.md)] | **REQUIRED.** A list of references to other documents and endpoints. See [Landing Page Links](#landing-page-links). |

### Landing Page Links

Each link in the links array must be a [Link
Object](../../spec/link/README.md).

| rel type | Description |
| ---------- | ----------- |
| `self` | **REQUIRED.** Links to the landing page itself. |
| `conformance` | **REQUIRED.** Links to the `GET /conformance` endpoint. |
| `products` | **REQUIRED.** Links to the `GET /products` endpoint. |
| `orders` | **REQUIRED.** Links to the `GET /orders` endpoint. |
| `search-records` | **REQUIRED** if the [Searches - Opportunity](../extensions/searches/opportunity/README.md) conformance class is advertised. Links to the `GET /searches/opportunities` endpoint. |
| `create-order` | **REQUIRED** if and only if a user can go directly from the products to the order endpoint without going through the `POST /products/{productId}/opportunities` endpoint. |
| `service-desc` | **RECOMMENDED.** Links to the machine-readable API definition. |
| `service-doc` | **RECOMMENDED.** Links to the human-readable API documentation. |
