# Core

- **Conformance URI:** `https://stapi.example.com/v0.1.0/core`
- [OpenAPI document](https://github.com/stapi-spec/stapi-spec/blob/main/openapi/openapi.yaml)
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
| conformsTo | [string] | **REQUIRED.** Conformance classes that apply to the  API globally. |
| title | string | A short descriptive one-line title for the API. |
| description | string | **REQUIRED.** Detailed multi-line description to fully  explain the API. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used  forrich text representation. |
| links | [Link Object] | **REQUIRED.** A list of references to other documents  and endpoints. |
