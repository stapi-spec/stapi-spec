# API Pagination

STAPI supports paging through hypermedia links for all endpoints returning a
list of entities, including the following:

- `GET /products`
- `POST /products/{productId}/opportunities`
- `GET /products/{productId}/opportunities/{opportunityCollectionId}`
- `GET /orders`
- `GET /orders/{orderId}/statuses`
- `GET /searches/opportunities/`

The following relation types may be available for pagination:

- `next` to provide a link to the next page
- `prev` to provide a link to the previous page (optional)
- `first` to provide a link to the first page (optional)
- `last` to provide a link to the last page (optional)

This link href must contain any request parameters that are necessary
for the implementation to understand how to provide the next page of results,
e.g., the query parameters `page`, `next`, or `token`.

For example, the links array could look like this for a API that supports
a parameter `page` and is currently on page 2:

```json
    "links": [
        {
            "rel": "prev",
            "type": "application/json",
            "href": "https://stapi.example.com/products?page=1",
            "title": "Previous page"
        },
        {
            "rel": "next",
            "type": "application/json",
            "href": "https://stapi.example.com/products?page=3",
            "title": "Next page"
        }
    ]
```

The href may contain any arbitrary URL parameter, which is implementation-specific:

- `https://stapi.example.com/products?page=2`
- `https://stapi.example.com/products?next=8a35eba9c`
- `https://stapi.example.com/products?token=f32890a0bdb09ac3`

A pagination link is not limited to URL query parameters alone to express a
page request. The Link Object can also carry the `method`, `headers`, and
`body` fields described in [additional Link
fields](../link/README.md#additional-link-fields).

The specification is compatible to pagination mechanisms defined in STAC API.
