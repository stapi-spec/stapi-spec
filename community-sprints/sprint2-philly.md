# Satellite Tasking Sprint #2, March 2023

Notes for second tasking sprint for advancing a specification for tasking
of satellite remote sensing data.

## When and Where

- When: March 27-28, 2023
- Where: [Element 84](https://element84.com/), Philadelphia, PA

## Objectives

- Create an initial tasking metadata spec (STAC Extension?)
- Create draft API, with OpenAPI
- Determine how to support provider & sensor specific parameters
- Create a working POC/MVP that demonstrates the basic capabilities of the Tasking API
- Understand and document the future functionality roadmap
- Promote adoption 

## Guiding Principles

- Leverage existing standards
- Focus on tasking for end users, push complexity to providers
- Identify a small stable core
- Build implementations
- Release early, release often

## Agenda

### March 28, 2023 

```
0800-0900 - Meet and Greet Opener (Coffee & Light Breakfast) - Kitchen/Istanbul Room 
0900-0930 - Introductions and Recap - Istanbul Room 
0930-1000 - Lightning Talks 6 x 5 mins - Istanbul Room 
1015-1145 – Spec Discussion - Istanbul Room 
1145-1200 - Breakout Objectives and Level Setting - Istanbul Room 
1200-1330 - Working Lunch - Kitchen & Breakout Rooms 
1330-1630 - Implementation Breakouts - Sydney, Madrid & Nairobi 
1630-1700 - Action Item Generation / Debrief - Istanbul Room 
1700-1900 - Happy Hour* - Yard Brewing* 
```

(*offsite at Yard Brewing, 500 Spring Garden Street; 9-minute walk down the street) 


### March 29, 2023 

```
0800-0900 - Coffee/Light Breakfast - Kitchen/Istanbul Room 
0900-1200 - Implementation Breakouts - Sydney, Madrid & Nairobi 
1200-1330 - Working Lunch - Progress Updates/Demonstrations - Istanbul 
1330-1600 - Implementation Breakouts - Sydney, Madrid & Nairobi 
1600-1630 - Implementation Demonstrations - Istanbul                            
1630-1700 - Action Item Generation / Debrief - Istanbul 
```

## Lighting Talks

- Joe Reed @ Albedo
- Derek Daczewitz @ BlackSky - BlackSky tasking
- Andris Jaunzemis @ Capella - Capella Tasking
- Alex Robin @ GeoRobotix - OGC Connected Systems
- Nicolas Neubauer @ Planet - Planet Tasking
- Andy Fink-Miller @ Umbra - Canopy API
- Dylan Bartels @ Up42 - Internal tasking sprint


## Attendees

- Albedo
- AWS
- BlackSky
- Capella
- Element 84
- EOI
- Microsoft
- Planet
- SkyFi
- SparkGeo
- Umbra
- Up42


## Workstreams

In Sprint #1 we outlined how a user would interact with a tasking API. First, they would make
an initial request describing the area being tasked and optional parameters such as date limits,
maximum cloud cover or viewing angle, sensor specific collection modes. This is a
**feasibility request** and the API responds with a potential list of acquisitions that can
fullfull that request.

For this sprint we will split into 4 workstreams:

- Feasibility response: The specific required and optional metadata fields APIs should return
- API: Endpoints, parameters, and response schemas (including errors)
- Back-end Demo: a server that provides an API and dynamic responses based on publicly available 
satallite data
- Tasking UI Demo: a proof of concept front-end illustrating how a user interacts with a tasking API
to make a feasibility request, evaluate responses and place an order.


### Feasibility Response

In Sprint #1 while we decided that a feasibility response should be GeoJSON we stopped short 
of saying it should be a STAC Item. However, there is clearly a lot of overlap between a 
metadata record showing what could be collected vs what has already been collected.

To generate a concrete example, we will explore how a feasibility response would be STAC Item.
Aligning to the STAC Item spec would allow use of some of the STAC ecosystem, such as PySTAC,
methods for validating responses, and an existing process for defining schemas.

Issues:
- Can a basic feasibility response be a compliant STAC Item?  As Items require at least one
asset, would an `order` asset with a link be sufficient?
- Create a new repo from the [stac-extensions template](https://github.com/stac-extensions/template),
to make a stac-extension detailing additional required and optional fields an API should return
- What is the returned geometry?  If AOI can be 100% covered is this just the same geometry as the AOI?, or bigger representing the larger area that can be imaged (which would presumably cost more?)
- Is overlap percentage (voerage) something that should be returned?
- Is there any overlap of STAC Catalogs/Collections with needs in a tasking API?
- Each type of "product" (e.g., multi-spectal, sar, stereoscopic, video) needs to define it's own set of
metadata. Do the existing STAC extensions cover these? Does it make sense to use them in responses?  How is
a product defined?  Compare with the STAC Collection spec.
- Is the [STAC Order extension](https://github.com/stac-extensions/order)
sufficient for ordering future data collects?


### API

The API workstream will explore the requirements of a tasking API as well as explore
overlap and synergies with existing API standards.

Issues
- Is a feasibility request the same as a STAC search request? What are the differences?
- Providers should advertise their capabiltiies as a set of products (for lack of better term)
that define which parameters can be used when making a tasking request. In OGC API there are 
queryables which could be used here to define products.
- Can a tasking API be built on top of (as an extension) to the
[OGC Connected Systems API ](https://github.com/opengeospatial/connected-systems)?
- Can a tasking API be built on top of (as an extension) to OGC Features API,
or on a STAC API (e.g., via a new /task endpoint). 
- What is the response when a request cannot be fulfulled at all?  Error or empty list?
- Both a feasibility request and an order should be able to be asynchronous. Define responses.
- Should a user have the option of providing a prioritized list of orders (i.e., 1st choice, 2nd choice),
so that if an initial order cannot be fulfilled then task the second one.


### Back-end Demo

This workstream is the creation of a working tasking API with some dynamic content. Using ongoing, 
regularly collected public data sources (landsat, sentinel), future data collects can be modeled
through an API. Not only is this useful for demonstrating how a tasking API would work, it can also be
helpful to get information on future public satellite data, such as to coordinate with commercial collects.

Issues
- Using stac-fastapi, the back-end group will create the simplest possible API to respond to
feasibility requests and orders. The use of stac-fastapi along with Pydantic will enable automatic
creation of OpenAPI docs. Coordinate with the API group.
- Develop logic to predict future collects from 1 or more Landsats (Landsat-8 or 9) and/or Sentinel-2
- Stretch goal: Return predictions of future cloud cover based on historical data
(this might require STAC API aggregations)


### UI Demo

The UI demo workstream will create an front-end that will use the back-end API to make simple requests
and visualize the responses in a web map. The user should be able to compare and evaluate all the responses
in order to make a selection, and then order 1 or more selections.

Issues
- Create a UI to make a spatial and temporal request to a backend and displays the
responses as vectors on a web map.
- The UI should enable the user to make an informed choice based on multiple options that may have
different tradeoffs (e.g., price, total coverage, view angle). Demonstrate how the UI can
help the users compare the tradeoffs.
