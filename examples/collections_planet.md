# Opportunities

1. Request opportunities
** some required entities (product_id, datetime, geometry) could be on the top-level
** others will fit into constraints and will be parsed 
2. Receive opportunities (Order-likes)
3. Select opportunities and send unchanged to /order


Two different scenarios:

## Flexible
We'll validate the request and make sure it's compatible with the product constraints.  
This could also include feasibility checks. There aren't several imaging windows, 
so we'll just return the Order-like search argument as an opportunity in case 
it's valid and feasible.

```
POST /opportunities
{
  "product_id": "PL-QA:Flexible",
  "datetime": "2024-04-01T00:00:00Z/2024-04-07T00:00:00Z", 
  "geometry": {
    "type": "Point",
    "coordinates": [...]
  },
  "constraints": {
      // cql2 here but no constraints given
  }
}
```
returns
```
[{
  "product_id": "PL-QA:Flexible",
  "datetime": "2024-04-01T00:00:00Z/2024-04-07T00:00:00Z", 
  "geometry": {
    "type": "Point",
    "coordinates": [...]
  },
  "constraints": {
    
  }
}]
```

## Assured
Again we validate that the request is valid and feasible.
We'll identify (probably multiple) imaging windows and create an opportunity for each one,
taking the provided order-like search as a basis for each but adapting the time to a specific
point in time instead of the provided range and adding an internal ID to refer back to the
opportunity.

```
POST /opportunities
{
  "product_id": "PL-QA:Flexible",
  "datetime": "2024-04-01T00:00:00Z/2024-04-07T00:00:00Z", 
  "geometry": {
    "type": "Point",
    "coordinates": [...]
  },
  "constraints": {
    
  }
}
```
returns
```
[
{
  "product_id": "PL-QA:Assured",
  "datetime": "2024-04-01T00:00:00Z/2024-04-01T00:01:00Z", 
  "geometry": {
    "type": "Point",
    "coordinates": [...]
  },
  "constraints": {
    'imaging_window_id': '1234'
  }
},
{
  "product_id": "PL-QA:Assured",
  "datetime": "2024-04-02T00:00:00Z/2024-04-02T00:01:00Z", 
  "geometry": {
    "type": "Point",
    "coordinates": [...]
  },
  "constraints": {
    'imaging_window_id': '1235'
  }
}
]
```


