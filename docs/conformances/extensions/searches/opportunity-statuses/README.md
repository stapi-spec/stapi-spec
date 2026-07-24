# Opportunity Search Records - Statuses

- **Conformance URI:**
  `https://stapi.example.com/v0.2.0/searches-opportunity-statuses`

See [Opportunity Search
Status](../../../../spec/opportunity/README.md#opportunity-search-status) for
details on the Opportunity Search Record Status object.

This extension is optional, but should be used when supporting Opportunity
Search Record status history.

## Opportunity Search Status Collection

To support returning a collection of Opportunity Search Status objects for a
given search, this extension defines an Opportunity Search Status Collection
object. This object has the following structure:

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `OpportunitySearchStatusCollection`. |
| stapi_version | string | **REQUIRED.** The STAPI version the Opportunity Search Status Collection implements. |
| statuses | \[[Opportunity Search Status](../../../../spec/opportunity/README.md#opportunity-search-status)\] | **REQUIRED.** A list of Opportunity Search Status objects in reverse chronological order. |
| links | \[[Link Object](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md#link-object)\] | **REQUIRED.** Links, e.g., for pagination. |
| numberMatched | integer | **OPTIONAL.** The number of statuses matched by the request, across all pages, if known and the implementation chooses to include it. |
