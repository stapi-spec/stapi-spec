# Architectural Decision Records

The purpose of this document is record design decisions for this specification.

These decisions should follow the following list format:

- Context: `<use case/user story>`
- Concern: `<concern>`
- Decision: `<option>`
- Neglected: `<other options>`
- Acheivable: `<system qualities/desired consequences>`
- Accepting: `<downside/undesired consequences>`
- Because: `<additional rationale>`

representing the Y-Statement sentence format:

```In the context of <use case/user story>, facing <concern>, we decided for <option> and neglected <other options>, to achieve <system qualities/desired consequences>, accepting <downside/undesired consequences>, because <additional rationale>.```

## Queryables Endpoint

- Context: advertising terms which can be used in CQL2 filter expressions
- Concern: where to retrieve the JSON Schema queryables definition from
- Decision: the JSON Schema queryables should be at a separate endpoint `./queryables`
- Neglected: the JSON Schema should be embedded within the Product entity
- Acheivable: a semantically-consistent set of resources that minimizes network requests
- Accepting: clients will need to retrieve two resources (the product and the product queryables endpoint)
  in order to search against the product's opportunities
- Because: the queryables are metadata about the product's metadata, rather than product metadata itself.
  Therefore, including it in the product metadata is not an appropriate place to add it.

## Opportunity Search and Order Create body format

- Context: JSON body format to POST endpoints for Opportunity Search and Order Create
- Concern: what attributes should be supported for searching/creating 
- Decision: a single attribute `filter` supporting a CQL2 expression
- Neglected: separate `datetime` (interval), `geometry` (intersecting geometry?), and `filter` attributes
- Acheivable: to provide the simplest interface that supports maximum expressiveness
- Accepting: API users will need to always use CQL2 expressions even when only using spatial and temporal constraints.
- Because: `datetime` and `geometry` fields are duplicates of what can be expressed in CQL2 expressions.
  Most users will not be writing CQL2 statements directly, but instead interacting with the API via a client, which can provide whatever shorthand (e.g., separate properties on a search object) for these "special" fields that it wishes to.
