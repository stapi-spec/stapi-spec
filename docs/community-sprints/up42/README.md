# Tasking Specification


## About

This is the first draft of a specification aiming to standardize the requirements and user flow for satellite imagery 
tasking, the on-demand acquisition of new images. Even though the exact user flow is an implementation choice, 
the specification provides a common base and defines input and response elements.    
The goal is to have satellite image operators and service providers build tasking ordering systems based on the same 
specification, to ensure well-designed, transferable API behaviour. This is advantageous for users, integrators and 
providers of tasking capabilities. Instead of having to create or adapt to proprietary APIs and formats, it lets them 
integrate community provided tooling, simplifies usage and improves comparability between providers.   
The system could also be applied for different applications and platforms, e.g. ordering of on-demand drone and 
terrestrial imagery acquisitions.

The main challenge for the provider is to determine the feasibility
of acquiring images that meet the user's specifications

The summary of this proposal has been presented and shared in the following [presentation](https://docs.google.com/presentation/d/1fXkPthQdujpEdwXocjLq3m05KksXLIihcuJibgVAXik/edit#slide=id.p).

## Specification Structure

The assumed tasking flow consists of 4 steps 1. search for tasking availability, 2. order confirmation and 3. order 
status. To facilitate this, the specification describes multiple related objects with related input and response 
parameters.

### 1. Search for tasking availability 

Based on the user-defined image requirements for the availability search, the tasking provider returns available 
slots, time windows in which the satellite would be able to capture the image for the desired conditions. Since 
potentially multiple slots and sensors can fullfill the image requirements, the search returns a `SlotCollection` 
object with lists of available slots separated by sensor.

Search query:
```json
    
    {
      "timeWindow": [
        "2022-07-21T17:32:28Z"
      ],
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[...]]],
        "bbox": [...]
      },
      "resolution": "10",
      "price": 1000,
      "imageMode": ["StripMap", "SpotLight"],
      "provider": "AIRBUS",
      "sensor": ["PHR", "SPOT"],
      "priority": 100,
      "satelliteType": ["Optical"],
      "acquisitionConfiguration": {},
      "productionConfiguration": {
        "processingLevel": "SLC",
        "imageFormat": "TIFF"
      }
    }
    
```    


SlotCollection:
```json
  {
    "id": "123456",
    "priority": 100,
    "lifecycle": [ "FEASIBILITY", "ORDER", "DELIVERY" ],
    "provider": "AIRBUS",
    "timestamp": "2017-07-21T17:32:28Z",
    "sensor": "PLEIADES",
    "date": {},
    "geometry": {},
    "dataProduct": {"polarization": "HH", "incidenceAngle": 30},
    "maxPrice": 1000,
    "providerProperties": {"feasibility": 80},
    "slots": [...]
  }
``` 

Slot:
```json
      {
        "id": "123456",
        "spatial": {
            "type": "Polygon",
            "coordinates": [[[...]]],
            "bbox": [...]
          },
        "temporal": [["2021-07-21T17:32:28Z", "2022-07-21T17:32:28Z"]],
        "priority": [0, 100],
        "price": [0, 1000],
        "incidenceAngle": 20,
        "cloudCoverage": 50,
        "providerSpecific": {            
            "feasibility": 80
      }
```

Many existing satellite tasking providers don't require a dedicated feasibility study, but already let the user select
from the available satellite time slots based on their image requirements. However, other providers have a more manual
process, requiring multiple interactions to access and select from the provided slots. In general, sophisticated
orders might also require a dedicated feasibility study. In case the provider does not automatically give the available 
slots, the search response contains details about the triggered feasibility study.

```json
{
    "id": "123456",
    "priority": [
        0,
        100
    ],
    "lifecycle": [
        "FEASIBILITY",
        "ORDER",
        "DELIVERY"
    ],
    "provider": "AIRBUS",
    "timestamp": "2023-01-21T17:32:28Z",
    "sensor": "PLEIADES",
    "date": {},
    "geometry": {},
    "dataProduct": {
        "polarization": "HH",
        "incidenceAngle": 30
    },
    "maxPrice": 1000,
    "providerProperties": {
        "feasibility": 80
    },
    "slots": [
        {
            "id": "123456",
            "spatial": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [...
                        ]
                    ]
                ],
                "bbox": [...
                ]
            },
            "temporal": [
                [
                    "2023-07-21T17:22:28Z",
                    "2023-07-21T17:32:28Z"
                ]
            ],
            "priority": [
                0,
                100
            ],
            "price": [
                0,
                1000
            ],
            "incidenceAngle": 20,
            "cloudCoverage": 50,
            "providerSpecific": {
                "feasibility": 80
            }
        },
        {
            "id": "123458",
            "spatial": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [...
                        ]
                    ]
                ],
                "bbox": [...
                ]
            },
            "temporal": [
                [
                    "2023-07-21T17:32:28Z",
                    "2023-07-21T17:42:28Z"
                ]
            ],
            "priority": [
                0,
                100
            ],
            "price": [
                100,
                1000
            ],
            "incidenceAngle": 21,
            "cloudCoverage": 56,
            "providerSpecific": {
                "feasibility": 85
            }
        }
    ]
}
```

## Next Steps

This is a first draft, to promote discussions and community-driven development of a tasking specification. It
takes into consideration the findings of the initial [Satsummit Tasking Sprint](https://github.com/Element84/sat-tasking-sprint)
and an internal tasking Sprint at UP42. Feedback, contributions and discussions of different solutions are strongly
encouraged, in this repo or the existing Satsummit Tasking
[gitter channel](https://gitter.im/satellite-tasking/community?utm_source=share-link&utm_medium=link&utm_campaign=share-link).
