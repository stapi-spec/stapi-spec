
## Overview

STOP takes much of the work done by the STAC community and applies the lessons learned into this specification. The major departure from STAC is the requirement for uncertainty in many of the STOP properties.

For example, a user requesting a data capture can provide a range of dates when that capture can occur. Conversly, a data provider cannot be certain of cloud cover in the future and must return a range of values to a user.

Tasking objects are represented in JSON format and are very flexible. Any JSON object that contains all the required fields is a valid tasking object. A tasking object contains a minimal set of required properties to be valid and can be extended through the use of constraints.

## Constraints

Constraints are limitations imposed by the user and the data provider as to what data is desired, and what data is available. In addition to space, time, and product limitations, constraints filter the needs of the user and capacity of the provider through an API negotiation. Constraints build off STAC extensions and modify them in order to support ranges of values.

Users of the Tasking API Should follow STAC Extension naming conventions when adding constraints.

## Parameters

Parameters are objects which do not affect the Tasking process, but are nevertheless useful. For example, a user may wish to select a preferred output format or a data provider may provide additional metadata about a product.