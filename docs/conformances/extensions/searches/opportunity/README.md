# Opportunity Search Records

- **Conformance URI:** `https://stapi.example.com/v0.1.0/searches-opportunity`

See
[Opportunity](../../../../spec/opportunity/README.md#opportunity-search-record)
for details on search records.

This extension is required for Async Opportunity Searches, and optional for
Sync Opportunity Search.

## Endpoints Provided

| Endpoint | Link Relationship | Returns | Description |
| -------- | ----------------- | ------- | ----------- |
| `GET /searches/opportunities` | `search-records` | [Opportunity Search Record Collection](#opportunity-search-record-collection) | List all Opportunity Search Records |
| `GET /searches/opportunities/{searchRecordId}` | `search-record` | [Opportunity Search Record](../../../../spec/opportunity/README.md#opportunity-search-record) | Fetch a specific Opportunity Search Record |

## Opportunity Search Record Collection

An Opportunity Search Record Collection is the response object returned when
listing Opportunity Search Records. The list of records returned [can be
paginated](../../../../spec/pagination/README.md).

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| records | \[[Opportunity Search Record]()../../../../spec/opportunity/README.md#opportunity-search-record\] | **REQUIRED.** A list of orders. |
| links | \[[Link Object](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#link-object)\] | **REQUIRED.** Links for e.g. pagination. |
