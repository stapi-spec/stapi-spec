# Link Object

The STAPI Link Object is borrowed from STAC, and is the same as the [STAC Link
Object](https://github.com/radiantearth/stac-spec/blob/master/commons/links.md#link-object).
This object describes a relationship with another entity. Data providers are
advised to be liberal with links.

## Additional Link fields

In addition to supporting query parameters in the URL value of the `href` field,
the Link object can contain additional fields to support more complex HTTP requests:

- `method` to specify an HTTP method in uppercase (e.g. `GET` or `POST`),
- `headers` to add HTTP headers in the request,
- `body` with the entire body for the request.

## Relation types

The relation type `queryables` is to be used to link to the `GET
/products/{productId}/queryables` endpoint.

The relation type `order-parameters` is to be used to link to the `GET
/products/{productId}/order-parameters` endpoint.

A link with relation type `conformance` is to be used to link to the `GET
/products/{productId}/conformance` endpoint.

A link with relation type `create-order` **must** be provided in the landing
page if and only if a user can directly go from the products to the order
endpoint without going through the `POST /products/{productId}/opportunities`
endpoint.

Relation types used for paging through a list of entities are described in
[API Pagination](../pagination/README.md). Relation types specific to a given
entity are described alongside that entity, for example the [Opportunity
Collection Links](../opportunity/README.md#opportunity-collection-links), the
[Opportunity Links](../opportunity/README.md#opportunity-links), and the
[Opportunity Search Links](../opportunity/README.md#opportunity-search-links).
