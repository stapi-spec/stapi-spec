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
            "title": "Next page"
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

In addition to supporting query parameters in the URL value of the `href` field,
the Link object can contain additional fields to support more complex HTTP requests:

- `method` to specify an HTTP method in uppercase (e.g. `GET` or `POST`),
- `headers` to add HTTP headers in the request,
- `body` with the entire body for the request.

The specification is compatible to pagination mechanisms defined in STAC API.
