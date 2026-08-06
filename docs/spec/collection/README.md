# Collection Object

Several STAPI endpoints return a collection: an object wrapping a list of
entities of a single type, together with the metadata and links needed to page
through the full result set. The name and type of the wrapped list, and any
other fields, are defined by the specification of each specific collection.

All STAPI collections share the following common fields.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to the collection type defined by the specification of the specific collection. |
| stapi_version | string | **REQUIRED.** The STAPI version the collection implements. |
| links | \[[Link Object](../link/README.md)\] | **REQUIRED.** Links, e.g., for pagination. |
| numberMatched | integer | **OPTIONAL.** The number of entities matched by the request, across all pages, if known and the implementation chooses to include it. |
| numberReturned | integer | **OPTIONAL.** The number of entities in this page, if the implementation chooses to include it. |

Paging through a collection is described in [API
Pagination](../pagination/README.md).

The following entities are STAPI collections:

- [Product Collection](../product/README.md#product-collection)
- [Opportunity Collection](../opportunity/README.md#opportunity-collection)
- [Order Collection](../order/README.md#order-collection)
- [Order Status Collection](../../conformances/extensions/order-statuses/README.md#order-status-collection)
- [Opportunity Search Record
  Collection](../../conformances/extensions/searches/opportunity/README.md#opportunity-search-record-collection)
- [Opportunity Search Status
  Collection](../../conformances/extensions/searches/opportunity-statuses/README.md#opportunity-search-status-collection)
