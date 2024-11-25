# Architectural Decision Records

The purpose of this document is record design decisions for this specification.

These decisions should follow the following list format:

- Context: `<use case/user story>`
- Concern: `<concern>`
- Decision: `<option>`
- Neglected: `<other options>`
- Acheivable: `<system qualities/desired consequences>`
- Acheivement: `<downside/undesired consequences>`
- Because: `<additional rationale>`

representing the Y-Statement sentence format:

```In the context of <use case/user story>, facing <concern>, we decided for <option> and neglected <other options>, to achieve <system qualities/desired consequences>, accepting <downside/undesired consequences>, because <additional rationale>.```

## Additional Object Fields

- Context: Entity definitions for the objects in returned by the API
- Concern: It is difficult to determine what the type of an entity is
- Decision: Every entity will have fields `stapi_type`, `stapi_version`, and `conformsTo`.
- Neglected: Heuristics should be used, such as mandatory fields, to distinguish between different types of objects
  that are all advertised as GeoJSON Features
- Acheivement: Easily identifiable object types
- Accepting: An additional field will be required
- Because: n/a
