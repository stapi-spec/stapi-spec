# Opportunity Search Records

- **Conformance URI:** `https://stapi.example.com/v0.1.0/searches-opportunity`

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

In addition to the fields common to every [Collection
Object](../../../../spec/collection/README.md), an Opportunity Search Record
Collection has the following fields.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `OpportunitySearchRecordCollection`. |
| records | \[[Opportunity Search Record](../../../../spec/opportunity/README.md#opportunity-search-record)\] | **REQUIRED.** A list of Opportunity Search Records. |
