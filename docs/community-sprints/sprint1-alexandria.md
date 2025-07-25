# Satellite Tasking Sprint 2022 Notes

- [When and Where](#when-and-where)
- [Sprint Goals](#sprint-goals)
- [Guiding Principles](#guiding-principles)
- [Agenda](#agenda)
- [Lighting Talks](#lighting-talks)
- [Topic: Spatial Parameters](#topic-spatial-parameters)
  - [Reference Questions](#reference-questions)
  - [Notes](#notes)
  - [Key Takeaways/Conclusion, Single Slide Summary](#key-takeawaysconclusion-single-slide-summary)
  - [Recap Notes](#recap-notes)
  - [Actions Items](#actions-items)
- [Topic: Temporal Parameters](#topic-temporal-parameters)
  - [Reference Questions](#reference-questions-1)
  - [Notes](#notes-1)
  - [Key Takeaways/Conclusion, Single Slide Summary](#key-takeawaysconclusion-single-slide-summary-1)
  - [Recap Notes](#recap-notes-1)
  - [Actions Items](#actions-items-1)
- [Topic: Additional Parameters](#topic-additional-parameters)
  - [Reference Questions](#reference-questions-2)
  - [Notes](#notes-2)
  - [Product / Asset Definition](#product--asset-definition)
  - [Request Info](#request-info)
  - [Request Example](#request-example)
  - [Response Info](#response-info)
  - [Key Takeaways/Conclusion, Single Slide Summary](#key-takeawaysconclusion-single-slide-summary-2)
  - [Actions Items](#actions-items-2)
- [Topic: Feasibility & Fulfillment](#topic-feasibility--fulfillment)
  - [Reference Questions](#reference-questions-3)
  - [Key Takeaways/Conclusion, Single Slide Summary](#key-takeawaysconclusion-single-slide-summary-3)
  - [Actions Items](#actions-items-3)
  - [Notes](#notes-3)
- [Session 2 Potential Breakout Topics](#session-2-potential-breakout-topics)
- [Topic: OpenAPI Doc](#topic-openapi-doc)
  - [Key Takeaways/Conclusion, Single Slide Summary](#key-takeawaysconclusion-single-slide-summary-4)
  - [Actions Items](#actions-items-4)
- [Topic: Contracts and Exclusivity, Multi Agency Uplifts, Holdbacks](#topic-contracts-and-exclusivity-multi-agency-uplifts-holdbacks)
  - [Key Takeaways/Conclusion, Single Slide Summary](#key-takeawaysconclusion-single-slide-summary-5)
  - [Actions Items:](#actions-items-5)
  - [Notes:](#notes-4)
- [Topic: Products/Platforms/Sensors - Coherent Image Pairs](#topic-productsplatformssensors---coherent-image-pairs)
  - [Reference Questions](#reference-questions-4)
  - [Key Takeaways/Conclusion, Single Slide Summary](#key-takeawaysconclusion-single-slide-summary-6)
  - [Actions Items](#actions-items-6)
  - [Notes](#notes-5)
- [Topic: Status](#topic-status)
  - [Notes](#notes-6)

## When and Where

- When: September 27, 2022
- Where: [Element 84](https://element84.com/) HQ, Alexandria, VA

## Sprint Goals

- Promote discussion & identify requirements
- Agree on basic API operation
  - Feasibility request through ordering
- Get to a minimal core set of parameters
  - Spatial, temporal, other?
- Determine how to support provider & sensor specific parameters
  - Mechanism for including additional parameters
- Create OpenAPI doc
  - Publish an initial OpenAPI doc
- Get buy-in from participants!

## Guiding Principles

- Leverage existing standards
- Identify a small stable core
- Start building implementations
- Release early, release often

## Agenda

- 0800-0900 - Meet and Greet Opener
- 0900-0930 - Introductions
- 0930-1030 - Lightning Talks
- 1030-1100 - Breakout Objectives and Level Setting
- 1100-1230 - Breakout Session 1
- 1230-1400 - Working Lunch - Breakout Review/Consolidation
- 1400-1600 - Breakout Session 2
- 1600-1630 - Breakout Review/Consolidation
- 1630-1700 - Action Item Generation / Debrief
- 1700-1900 - Happy Hour! (Emmy Squared Pizza)

## Lighting Talks

1. [Alex Herz - Orbit
    Logic](https://docs.google.com/presentation/d/1cSXL9wLFu3Z606xkOXAyxj2pogGkBc_F/edit?usp=sharing&ouid=111811177138429531773&rtpof=true&sd=true)
2. [Joe Reed -
    Hydrosat](https://docs.google.com/presentation/d/1YKJfZ6shxygNxaBC8OIXdscZ66rh4T2_/edit?usp=sharing&ouid=111811177138429531773&rtpof=true&sd=true)
3. [Scott Simmons -
    OGC](https://portal.ogc.org/files/?artifact_id=102351)
4. [Drew Botts -
    OpenSensorHub](https://docs.google.com/presentation/d/1EjYcp1SyleQS76vNNnRr_1JBkDZjWtM7P48Kk3tmCzI/edit?usp=sharing)
5. [Derek Daczewitz - Black
    Sky](https://docs.google.com/presentation/d/1EnOY7tipfXzS9Mx-gOWo1E8HWoZOJinx2lP8zUsxtaA/edit?usp=sharing)
6. [Luis Veci -
    SkyWatch](https://docs.google.com/presentation/d/1TEt5L5jhLMe8K1QG_WEkNXVfZWOH_cYq/edit?usp=sharing&ouid=111811177138429531773&rtpof=true&sd=true)
7. [Paulo de Figueiredo Cruz -
    SkyWatch](https://docs.google.com/presentation/d/1aXJfP28Y91Bv6YG7ttpUPJIaVvWWSuz8/edit?usp=sharing&ouid=111811177138429531773&rtpof=true&sd=true)
8. [Marc Horowitz -
    SkyFi](https://docs.google.com/presentation/d/1KcbEaqUPNty4uxCd8GfOycZ2dIqeWve0/edit?usp=sharing&ouid=111811177138429531773&rtpof=true&sd=true)
9. [Dylan Bartels -
    Up42](https://docs.google.com/presentation/d/16Dw1NEz8nY-KAEfa9K5u53nMw27SNnPD7_DJ1E9navQ/edit?usp=sharing)
10. [Eric Cote -
    Ursa](https://drive.google.com/file/d/1C4Gb-HnnZ10NRzqct7QfDBc_fboEKWcd/view?usp=sharing)

## Topic: Spatial Parameters

- **Attendees**: James Banting, Kevin Rioles, Warren Strong,
    Mark Perillo, David Raleigh, Marc Horowitz, Tom Kunicki
- **Location**: King and Columbus

### Reference Questions

1. How do we specify AOIs?
   1. a. Geojson Feature
2. How do you handle a requested AOI vs actual AOI?
   1. Keep it simple, Geojson. If AOI does not meet feasibility, return nothing
   2. Actual AOI is final product
3. How do we handle if the AOI will be partially obscured?
   1. Let the customer decide or determine criteria
    for delivery internally
4. Do we need prioritized concentric AOIs?

### Notes

- Current implementations use point mostly to search
  - Customers usually provide polygons for their AOI's
- Customers typically want all imagery within an area (CONTAINS)
- Specified parameters for collect determine actual AOI. Center point vs target within AOI
- 3 stages for requested AOI vs Actual AOI
  - Customer request, feasibility AOI, Actual Capture AOI
  - Use JSON-LD for Chain of Custody
- Feasibility vs fulfillment
- Customer AOI is ideal, feasibility API will return probable collects for the actual AOI
  - Imaging modes, scan angles, ...
- How do we task on a moving platform like vehicle Lidar?
  - 2.5 D?
- Burden of altitude is on producer

### Key Takeaways/Conclusion, Single Slide Summary

KISS

- Use Geojson (use standard winding order)
- Acknowledge the spatial bias. Community will need to define other dimensions (OGC work)
  - How are other dimensions integrated into the spatial format
- Customer request vs. Feasibility vs. Fulfillment
- Chain of Custody - use a linked format
- Constrain geometry to 2 dimensions
- The minimum spatial query type should be an INTERSECT

### Recap Notes

- Limit GEOJSON by POST payload restrictions

### Actions Items

None

## Topic: Temporal Parameters

- **Attendees**: Phil Varner, Lauryn Gutowski, Scott Simmons,
    Winston Tri, Drew Botts, Mike Panos, Chris Brown
- **Location**: The Driveway

### Reference Questions

1. How do we specify datetime intervals?
2. Are there standard re-coverage requests? (3,
    7, 14 days?)
3. Do we need guaranteed return timeframes if the
    scene was not sufficient to meet the request?
4. Do we allow backwards facing datetime
    intervals?
5. Is this just a regular order?

### Notes

- Two types of temporal considerations:
  - Actual collect time
  - When products can be delivered
- How different is querying the past (archive) vs future (tasking)?
  - Providers seem to separate the two
  - What does the entity look like for a feasibility/tasking request
  - request may be for products processed to a
    higher level (ARD, analytics), not just \"raw\" images (practically,
    all provided data is processed to some degree)

- How far do we abstract the actual tasking from the request?
  - Tell the satellite to go here and do this thing
  - vs
  - An expression of desires - this is what I want,
    is it possible?
- local solar time vs. UTC

Desirability of Time - How do you express order of preferences -- Monday
is great, Tuesday is not so great
- Maybe better feasibility responses make this unnecessary?
- **Feasibility responses are tractable for
providers**, with high levels of certainty
  - obviously, clouds happen
- Clients can do (possibly multiple) requests and
sort based on their own multi-dimensional criteria

What does feasibility mean?

- Where is the satellite going to be, what else
    is being done
- Not just parameters in the satellite world -
    tasking necessity

Recurrences

- Temporal aspects - what does \"every day\", week,
mean?
- Should be able to specify
  - recurrence interval
  - recurrence start / end range
  - Minimum time between collects
  - Time of day options

- See [OGC SPS EO Extension 7.1.2.8 TimeSeries Class](https://drive.google.com/file/d/1Utkw6_e4WhA0mXXlD02X9LcaiPavBQDW/view?usp=sharing)

How does feasibility matter for time of day? This likely changes over
time -- the farther into the future usually has fewer conflicting
bookings, but also move uncertainty about position, continued existence
of specific satellite, etc.

Expose information to clients in feasibility responses so that they can
make decisions about what is most important to them for a collect.

### Key Takeaways/Conclusion, Single Slide Summary

None

### Recap Notes

- Do we have any approach for long standing recurrence requests?

### Actions Items

None

## Topic: Additional Parameters

- **Attendees**: Dan Pilone, Derek Daczewitz, Joe Reed, Victor
    Madrigal, Eric Cote, Paulo Cruz, Krasen Georgiev
- **Location**: Main Area

### Reference Questions

1. Are there any other common parameters that
    should be considered?
2. How does an individual provider expose
    additional parameters?
3. Are parameters fixed or mutable?
4. What is the set of parameters that need to be
    exposed to allow different types of users to request the quality of
    data they require?

### Notes

- Query params really form the basis for all of this

- Topics to discuss:

  - Provenance
  - Who am I?
  - Tasking priority - does this tie into pricing?
  - Order Management
  - Product selection capability

- Handling things like Coherent pairs really isn't
"two" requests - I need both for a successful tasking request

- Archive is a subset of tasking, not the other way
around.

  - Get scene X is directly comparable between
    catalog & tasking
  - Status updates are tasking related
  - Repeat information - e.g. stereo pair every
    week. What's the status of having the
    first of the pair but not the second yet?

- Order management is "unknown" - retry capabilities,
etc. bids vs. asks - biggest problem so far

- Are analytics just another example of ordering?

  - Increased # of params based on instrument /
    product / analytic?

- User experience level
  - may have someone saying I need "image over here
    @ this resolution" - analytics is an example of this: "I want to
    know how many vehicles are in this parking lot"
  - Collection requirements may be much deeper

- Could API users define their own "products"?
E.g. bands xyz from product M

### Product / Asset Definition

- Can we leverage STAC here? **There are extensions but no current definition
of a "product" in STAC.**

- Default "product" == single collection

### Request Info

- Common properties
- Spatial (seperate group)
- Temporal Info
  - Max delivery latency - (e.g. < 24hrs)
  - Observation time (e.g. now -> until I cancel)
- Priority & Pricing info
- Product selection(s) - e.g. ("Stereo pairs", SLC, etc.)
  - Common Collection Type (e.g. SAR specific) Specific information
  - Provider + Product specific attributes defined in extension
- Resolution info
  - SAR extension (e.g. slant range, etc.)
- Priority information: collect if you can vs. will pay more to get
- Recurring info +
- Products are unique to a data provider BUT

### Request Example

Header Info:

 Provider specific authentication information

**spatial_aoi:** bbox(1,2,3,4)

**temporal_info:**

 max_delivery_latency: 24hrs

 observation_time: UNTIL_CANCELLED

**pricing_info:**

priority: CAPELLA_TIER_1 \| ICEYE_BACKGROUND_TASK \|
EGEOS_EMERGENCY_TASKING \| EGEOS_RAPID_DELIVERY

optimize_for: PRICE, LATENCY, SUCCESSFUL_COLLECT, EARLIEST_COLLECT, etc.

???

**customer_info:**

```
customer_reference_id: asdf1234

provenance_type: NONE | BLOCKCHAIN_LEDGER | HASH

end_user_information(?) { self | "end_user_name, address, etc." }
```

**delivery_info:**

```
destination_info { s3_bucket_id, credentials, etc. }

Status_update_info { webhook info }
```

**products:**

 capella_sar_fancy_image:

sar_imaging_mode: CAPELLA_SPOTLIGHT \| CAPELLA_STRIPMAP \|
ICEYE_STRIPMAP_VV

sar_collect_param2: xyz

sar_output_format: ...

capella:denali_spot: 1234

 Optical_image: *\<- is this a separate product?*

optical_mode: STEREO

optical_stereo_convergance_angle: ...

minimal_resolution: ...?

 vnir_thermal_1km:

thermal_something: asdf

thermal_ouptut_format: COG

Metadata_output_format: STAC_CATALOG

hydrosat:custom : MODE_2

 hyper_something:

hyper_band_selection: 1,2,7,22

...

### Response Info

Feasibility info?

### Key Takeaways/Conclusion, Single Slide Summary

None

### Actions Items

None

## Topic: Feasibility & Fulfillment

- **Attendees**: Trevor Skaggs, Ben Tuttle, Dylan Bartels,
    Chris Holmes, Luis Veci, Alex Herz, Payton Barnwell
- **Location**: The Batcave

### Reference Questions

1. How are prices returned? Ranges?
2. Is price an input to the Feasibility Request?
3. What happens when/if a request cannot be
    filled? Are there options for allowing a possibly later delivery for
    a discount?
4. What does an auction based model look like?
5. Do we consider the probability of delivery as
    part of the pricing model?

### Key Takeaways/Conclusion, Single Slide Summary

- Need to put information in customers hands.
Return all the options, let them make the call based on all options,
instead of a black box.
- Feasibility needs to do Area in addition to
point, and that may not be millisecond response. We want to always
assume an area (which for some people can be a point)
- Feasibility should have a time limit for how long
it's valid for.
- Importance of push responses, like if you get
bumped after we said we collect.
  - Give new option, maybe all free
- Stable ID for feasibility request, allow a
provider to push to customer if something has changed for their original
feasibility.
- Show 'technically feasible', but likely as a
default off parameters. 'Commercially feasible'.
- Show responses of what parameters they could
change to 'get' a certain collect.
- Response on 'order deadline' - certain 'last
call' time.
- Order is valid for X amount of time - how
long is this feasibility thing I gave to you.

### Actions Items

None

### Notes

- Enter an order in the system and filters down to
satellites that have that capability
- Looking at ones that can be actually on the site.
- Shows the opportunities
- Request specifies what to both filter and sort by,
amongst the various request parameters supported
- Provides feedback based on when user wants image
back - how likely is that. EO we look for statistical weather,
competition from higher priorities in the system, other efficiencies.
You said you want in a week, but we can get it in ten days.
- Everyone wants 'overhead constraints', but own.
- Doing own orbit propagation, we know where the
satellites are.
- That's the easy part.
- Albedo - our satellites in the future will be low
enough to not predict.
- But we could get your ephemeris prediction (yes,
we'll provide an API for that).
- Can I get it by my deadline.
- Self-serve feasibility for users lets them push a
button and get it. It says ten days instead of 7 - maybe I'll loosen my
constraints, elevation.
- Instaed of wait for operator to get back we can
get back self service.
  - But operator has to expose their availability
    stack.
  - Yes, but this is for an internal system where
    you control the satellite.
  - If I have this ordering system people can run
    self-service feasibility. Don't have to tell what orders block
    feasibility, but not what those are.
- Feasibility - they get a yes or know, and
estimated response time. Estimate you'll get this in ten. Open up to
ten, and they can fulfill that order.
  - Is there percentage confidence tied to that.
    Priority - DoD calls and you don't get a picture, orders might come
    in. Some kind of confidence interval.
- Formulas for feasibility - based on experience we
get it faster or slower.
- Put in a feasibility request - put in a window.
- Price may be an input into feasibility request.
- Price as equivalent to priority. Higher price into
higher priority.
- How many tiers of priority should there be? Some
have 100.
  - Seen 256 levels of priority. We just use 100
  - Say in spec, use 1 to 100
  - Make priority dynamic.
  - Have to have convention, make a provider match.
  - Could provider say 'I have complete
    availability', or I've only got it in.
  - Is priority in your contract?
  - Not just priority in your contract.
  - Have customer who wants collection 3 times a
    week with 12 hour intervals at least. Need them to be successful.
- Priority is often dictated by contract signed.
Your login id gives you your priority, range from 70-85, have to work
within their priority. Have user-id based restrictions based on what
they can do.
  - Within urgent there's relative priorities
    within that deck.
  - Customer wants their deck in their tier.
    Relative priority in their tier. Low priority customer, but high
    priority within a customer.
  - Can only achieve this with a high priority
    customer.
- Like an idea is reply back - here's all the
options available. These ones require this priority and this price, this
is when it'll be cloudy. Give all information to need. Don't 'guess' on
request.
  - Downside is if a provider can't commit to
    intervals request the person is making then it can
    go.
  - If provider can't do it then it should
    go.
- Dynamic pricing, based on availability and competition. Something not seen before.
  - Not quite, more like 'I can take that shot for you'.
- 'True Collection Availability' is all that matters. -\> "Available to Order"
- Provider may not want to show everything
available, you may always have top customer
in.
  - I'm only worried about these collections, this
    category of collection.
  - I'm going to show anything.
  - Let the consumer decide 'I'll take this, I'll
    take that'.
  - If it comes that way the customer can choose.
    Let know what can choose from.
- Model of 'lock-in' - some time an airline
overbooks. Flip side is theatre seating - I buy my seat, but first come
first served, but flat pricing.
- One more 'I'd like this thing, but a discount for
you to lock off'.
  - Already have option - have it anytime in the
    next two weeks.
  - Cases where it's only valuable if it meets
    constraints, but I'm fine to be bumped.
  - Another option - I don't care when you collect it for me and deliver to me.
    What if they say 'over next two weeks and collect for someone else'.
  - Feasibility could include archive - image in location from the past.
  - Provider side needs to query archive.

- Auction model
  - Investors want you to sign contracts for revenue stability.
  - Long term it's great, but beginning.
  - Supporting one off contracts is a nightmare on the backend.

- Disaster response work
  - Always looking for high resolution thermal data.
  - Need it right now, but have no money to get you.
  - Hopefully get a fund for $1000 over the year.
  - Submit google form to a guy and he'll hook it up.
  - Marketplace will never be there without
    auction model. Still got to prioritize when NGA calls.
  - Lots of rooms for bad actors. If only a few
    images then I can outprice and you won't have possibility.
  - If I see a competitor mapping a place, just
    make it so they can't place it.
  - Think state of california should be spending $1m a year on this.
  - AIS tech has 2 satellites.
  - Have organizational id present, plus
    non-profit flag. Let companies set aside stuff for non-profits.
    Haven't given this group enough access, let's let this group.

- Priority on the back-end.
  - Plus discount mechanism.

- I still submit same request. Each provider decides
how they want to handle the request.
  - Provider should know what you're requesting
    and why, that you have a burning field and people in it. A 'context'
    field?
  - Hard to trust that, could introduce bad
    actor.
  - Should have an organization ID, to set context
    for the 'context' field.
  - Include all this in feasibility. No individual
    is going to look at this data. Needs to be an algorithm
    incorporating the data into the response.
- If we're taking 2000 requests per day we can't
have an individual look at it.
  - Don't assume no one does, people do bespoke
    tasking filtering.
  - Long term we want to get there, but don't want
    to rule out that particular need.
- Another break out on what to capture about an
organization. How much an org is paying, if they're a non-profit. Just
because it's cheap it's not useful to get in 2 weeks.
  - Still here the key is to get the information
    about what's available.
  - High resolution thermal is only useful for a
    couple days. But imagery is useful for week after, to do the
    disaster recovery.
  - Provider to tell you 'you definitely can't get
    it' vs 'do x,y,z (pay money, verify you are a nonprofit)' then you
    can get it.
- Back to 'true collection availability'
  - For highest resolution the footprint size matters.
    Big image could take months to map all of LA.
  - Feasibility has to be more than points. Has to do
    full areas. Can be multiple images. Tell me everything you want.
    Complicated ones we may need to get back to you in 5 minutes (or days to
    do analysis).
  - Isn't that ok?

- Canceling tasking, if you get feasibility from one provider you want to cancel the other.
  - Need to understand cancellation policies.

- Is there cost related to feasibility?
  - Can I just squat it?
  - To hit the API you need to be an authenticated
    customer, and if they are jamming you then you can remove.
  - Build this with presumption that this will be
    trusted.

- Always will be issues where part of things broke.
(order couldn't be fulfilled due to rare outage of some kind)
- Status / webhooks - let
- For people who want priority need to optionally submit priority.
- Lock-in should also be optional. Or is business
logic on the backend.
- Push business logic to where it should.
Feasibility should same in and same out.
  - Could as a business decide first person to
    take it gets it.
  - With push thing you can remember what they
    asked for, your order wasn't available yesterday, but it's available
    today.
- Feasibility request has a stable ID, and perhaps if it updates you can tell someone something changed.
- Difference between STAC and tasking API - when you place order you know you're going to get.
- Two paradigms
  - I submit price / priority, what meets that
  - I submit what I need, I'll give you price / priority.
- Ability to respond back with "if you loosened
  these constraints/parameters, I'll be able to better meet your
  needs"
- A thing we didn't discuss is, if processing spec
  is part of the tasking request (ARD, etc.) how that plays into the
  price/feasibility response (maybe that's super straightforward, but we
  didn't discuss it)

- Response discussion

## Session 2 Potential Breakout Topics

- OpenAPI Doc
- Standardizing Error Codes
- Status Tracking/Callbacks
- Chain of Custody/Confirmation
- Tiers of Priority
- Products/Platforms/Sensors - Coherent Image Pairs
- Contracts and Exclusivity, Multi Agency Uplifts, Holdbacks
- Spatial Follow-on (if needed)
- Temporal Follow-on (if needed)
- Feasibility & Fulfillment Follow-on (if needed)
- Additional Parameters (if needed)



## Topic: OpenAPI Doc

- **Attendees**: Phil Varner, Mark Perillo,
    Winston Tri, Chris Brown, Warren Strong
- **Location**: Main Area
- **Reference Questions:**


### Key Takeaways/Conclusion, Single Slide Summary
- There is a difference between the \"ordering of products in the
    future\" and \"tasking a satellite\" -- leaning towards the
    declarative approach of \"I want data with these constraints\"
    rather than the imperative approach \"make this satellite do this
    thing at this time\".

Multi-stage process:

1. Client: Here are my constraints
2. Server: Here are your available options
3. Client: I want this option
4. Server: That option will be delivered to you in the future
5. time goes by...
6. Server: Here is the result of your order

### Actions Items

1. Work on OpenAPI spec



## Topic: Contracts and Exclusivity, Multi Agency Uplifts, Holdbacks

- **Attendees**: Trevor Skaggs
- **Location**: The Batcave
- **Reference Questions:**
  - Is exclusivity universal across all organizations?

### Key Takeaways/Conclusion, Single Slide Summary

### Actions Items:

### Notes:

1. There is currently automatic exclusivity, in some instances there is
    automatic non-exclusivity.
2. Is the full tile exclusive or just the AOI?
3. How long are the terms of exclusivity? Do we have infinite
    exclusivity? How does the pricing scale?
4. Include Exclusive Flag, default to No
5. Include Exclusive End Date, default to 30 days
6. Added a Exclusive Price to Feasbility Response.
7. Is exclusivity separate from priority?
8. Exclusivity has no effect on priority, would just limit the total
    number of responses to a feasibility request.

## Topic: Products/Platforms/Sensors - Coherent Image Pairs

- **Attendees**: Dan Pilone
- **Location**: King & Columbus

### Reference Questions
### Key Takeaways/Conclusion, Single Slide Summary
### Actions Items
### Notes

## Topic: Status

- Attendees: James Banting

### Notes

- Commonalities for states of order
  - Order Placement
  - In progress
  - Delivery
- Enhanced products are still a manual task
  - Tri-stereo
- Callbacks would be nice to have but majority of interaction is still polling
  - We need to alert the customer to the status of the order
- Keeping and presenting a status history is useful
- Core states
  1. Order Placement
  2. Order Received
  3. Feasibility Review
  4. Cancelled
  5. Accepted
  6. Predicted
  7. Scheduled
  8. Scheudled (when)
  9. Captured
  10. Failed
  11. Processing
  12. Delivered
  13. Finished
- More detailed Statuses
