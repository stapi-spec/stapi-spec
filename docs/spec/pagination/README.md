# API Pagination

STAPI supports paging through hypermedia links for all endpoints returning a
list of entities.

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

A pagination link is not limited to expressing the request as URL query
parameters: the Link Object can also carry the `method`, `headers`, and `body`
fields described in [additional Link
fields](../link/README.md#additional-link-fields).

Because the parameters carried by a pagination link are implementation-specific,
a client **must** follow the link as given rather than construct the next
request itself. This specification therefore does not define a query parameter
for requesting a particular page.

## Page size

Endpoints returning a list of entities accept an optional `limit` query
parameter on the initial request, giving the maximum number of entities to
return in a single page:

- `https://stapi.example.com/products?limit=50`

`limit` is an integer between 1 and 100 inclusive, and defaults to 10 when it
is not supplied. It is a maximum, not an exact count: a server **may** return
fewer entities than requested, and a page containing fewer entities than the
limit does not by itself indicate that the last page has been reached. Only the
absence of a `next` link does.

Paginated collection responses may also include a `numberMatched` field, as
described in the [Collection Object](../collection/README.md).

The specification is compatible to pagination mechanisms defined in STAC API.
