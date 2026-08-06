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

Which links an entity must carry, and with which relation types, is part of the
specification of that entity containing a Link, rather than of the Link Object.
See each defined entity for the specific set of relevant relation types.
