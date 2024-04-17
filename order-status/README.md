# Overview

This document explains the structure of a STAT **Order Status** request. Operation returns a list/array of statuses that have affected an order.  The most recent status code is the current status of the order.


Endpoint: GET /order/{id}/status

## Order Status Request

List operation only in specced API.

## Order Status Response

Array of:

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| timestamp  | datetime | Timestamp for the order status (required) |
| status_code | string | Enumerated status code (required) |
| reason_code | string | Enumerated reason code for why the status was set (optional) |
| reason_text | string | Textual description for why the status was set (optional) |
| catalog_id | string | Id for affected catalog item (optiona) |

### Enumerated status codes

Providers must support these statuses.

* order_received (indicates order received by provider and it passed format validation.)
* order_accepted (indicates order has been accepted)
* order_rejected (indicates order will not be fulfilled)
* order_complete (indicates order had delivered imagery, must have been accepted first)
* order_canceled (indicates provider was unable to collect/deliver tasked imagery)

Do we need an order_hold (Order has has been placed in manual review state) status?

Providers may support these statuses

* order_scheduled (indicates order has been scheduled)
* order_tasked (indicates tasking commands have been issued to the satellite/constellation)
* order_processing (indicates some sort of processing has taken place, such as data was downlinked, processed or delivered)

### Enumerated reason codes

Examples (needs elaboration).  This is intended to be provider extensible.  Not sure how to do that.

* invalid_geometry (invalid should be renamed, means that a valid geometry failed business rules)
* competition (e.g., failed tasking auction)
* cloud_cover (imagery rejected for cloud coverage)
* partial_delivery (indicates a file was processed and placed in catalog, used with processing)

