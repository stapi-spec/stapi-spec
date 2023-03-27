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


## Topics


### Feasibility Response spec

The goal of this group is to flesh out the basics of a via README files (see how stac-spec and stac-api-spec are documented in their repos)....basically tables of parameters and descriptions as well as descriptions of the overall process (user stories would be good here).

Asynchronous Feasibility Request -> Status Checks -> Result -> User selection -> Ordering -> Deliverable

Questions:
How aligned with STAC is this API?  Can responses actually be (minimal) STAC records?  Is tasking just a STAC API extension?
If a returned geometry is required, what is the returned geometry?  If AOI can be 100% covered is this just the same geometry as the AOI, or bigger representing the larger area that can be imaged (which would presumably cost more?)
As a user how can I specify minimum % overlap (think this was discussed in Sprint 1)
Not feasible responses: Is this an error or an empty FeatureCollection?


### Products Spec

A concept that came up last sprint was that of Products. How are products defined in the API, are they like STAC Collections that provide a set of `queryables` that can then be used as different user parameters when making a Feasibility Request?

This group will help define Product-level metadata spec.  They seem similar to STAC Collections in that they can provide some of the same metadata, but does geometry make sense? The extent over which a Product can be ordered?


### API Spec


Feasibility Request

Is this just a STAC query?  
Is the response valid STAC ?

What would a tasking extension look like to a STAC Item?

Ordering extension

Error response for nothing feasible


Tasking Products

Are they like Collections


### Implementations

#### Backend Demo

An example backend could use existing satellites that have publicly available data (Landsat, Sentinel) since we already know the future paths of these instruments we can construct responses to a Feasibility Request and send back a response based on using existing STAC catalogs and a priori knowledge of the revisit times.  Ideally the backend incorporates both Sentinel-2 and Landsat
Estimating expected cloud cover (and thus probability of collect) would be an added bonus


#### UI Demo

Using a tasking API develop a simple interface for a user to able to select AOI (maybe not just bounding box?) and desired timerange and make a request.  Visualize responses using footprints and returned metadata. This seems like pretty much the same as a STAC Viewer…but we are looking at fundamentally different data - a selection of (never perfect) choices rather than what is already available. A user should be able to visually sort by different criteria - datetime, resolution, estimated cloud cover (probability of collect?), % overlap with AOI, cost, etc.