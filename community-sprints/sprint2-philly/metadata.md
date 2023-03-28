# Metadata workstream

We are discussing the response to a user query

Minimum User Request
- space
- time
- product
- arbitrary constraints based on product

## Feasibility Response

Feasibility Responses are *like* STAC Items, but not actually STAC,
this is why:

- A single task request might be multiple individual collects (which may be individual Items)
- `id`: There is no ID for a feasibility response, because it is ephemeral
- `geometry`: The minimum guaranteed area that will be collected (could be < 100% coverage
unless precluded by user)
- `temporal`
- `assets` don't exist
- `datetime` does not belong
- `start_datetime` and `end_datetime`
- `properties` will be ranges (min, max, or nomimal/uncertain)
- `Links` should not be required (but useful, e.g., order, product, help)

Commom metadata properties
- `start_datetime`
- `end_datetime`
- `license` and `provider` at product level
- `platform`, `instruments`, `constellation`, `mission` are optional
- `gsd` optional, but should bea range

