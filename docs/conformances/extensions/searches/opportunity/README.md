# Opportunity Search Records

- **Conformance URI:** `https://stapi.example.com/v0.2.0/searches-opportunity`

See [Opportunity Search
Record](../../../../spec/opportunity/README.md#opportunity-search-record)
for details on search records.

This extension is required for Async Opportunity Searches, and optional for
Sync Opportunity Search.

## Endpoints Provided

| Endpoint | Link Relation | Returns | Description |
| -------- | ----------------- | ------- | ----------- |
| `GET /searches/opportunities` | `search-records` | [Opportunity Search Record Collection](#opportunity-search-record-collection) | List all Opportunity Search Records |
| `GET /searches/opportunities/{searchRecordId}` | `search-record` | [Opportunity Search Record](../../../../spec/opportunity/README.md#opportunity-search-record) | Fetch a specific Opportunity Search Record |

## Opportunity Search Record Collection

An Opportunity Search Record Collection is the response object returned when
listing Opportunity Search Records. The list of records returned [can be
paginated](../../../../spec/pagination/README.md).

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `OpportunitySearchRecordCollection`. |
| stapi_version | string | **REQUIRED.** The STAPI version the Opportunity Search Record Collection implements. |
| records | \[[Opportunity Search Record](../../../../spec/opportunity/README.md#opportunity-search-record)\] | **REQUIRED.** A list of Opportunity Search Records. |
| links | \[[Link Object](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#link-object)\] | **REQUIRED.** Links for e.g. pagination. |
| numberMatched | integer | **OPTIONAL.** The number of Opportunity Search Records matched by the request, across all pages, if known and the implementation chooses to include it. |
