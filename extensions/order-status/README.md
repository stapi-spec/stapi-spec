# Overview

This document explains the structure of a STAT **Order Status** request. Operation returns a list/array of statuses that have affected an order.  The most recent status code is the current status of the order.


Endpoint: GET /order/{id}/status

## Order Status Request

List operation only in specced API.

## Order Status Response

### Order Status Response

Response has two fields:
| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| current | OrderStatus | The current/official status object |
| history | [OrderStatus] | History of statuses |

### Order Status Object

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| timestamp  | datetime | Timestamp for the order status (required) |
| status_code | string | Enumerated status code (required) |
| reason_code | string | Enumerated reason code for why the status was set (optional) |
| reason_text | string | Textual description for why the status was set (optional) |
| links | [Link] | list of references to documents, such as delivered asset, processing log, delivery manifest, etc. (required, may be empty) |

### Enumerated status codes

Providers must support these statuses.

* received (indicates order received by provider and it passed format validation.)
* accepted (indicates order has been accepted)
* rejected (indicates order will not be fulfilled)
* completed (indicates order had delivered imagery, must have been accepted first)
* canceled (indicates provider was unable to collect/deliver tasked imagery)

State machine intent:
Received -> accepted or rejected.
Accepted -> completed or cancel.

Providers may support these statuses.  Possibly these are all included as extensions rather than the core.

* scheduled (indicates order has been scheduled)
* tasked (indicates tasking commands have been issued to the satellite/constellation)
* processing (indicates some sort of processing has taken place, such as data was downlinked, processed or delivered)
* reserved (action needed by customer prior to acceptance, such as payment)
* held (order held for manual review)


### Enumerated reason codes

Examples (needs elaboration).  This is intended to be provider extensible.  Not sure how to do that.

* invalid_geometry (invalid should be renamed, means that a valid geometry failed business rules)
* competition (e.g., failed tasking auction)
* cloud_cover (imagery rejected for cloud coverage)
* partial_delivery (indicates a file was processed and placed in catalog, used with processing)

