# Terminology / Ontology

During the tasking sprint 2024, we realize that all providers call the same things slightly differently, but are mostly share the same concepts. Also, we found some confusion about what the ´orders´ and ´products´ refer to in STAT current proposal. 

## Layers
We've found that more or less we all do the same operations at different layers.

- **Business:** the to most level for any company, where we expect our customers to interact with us through. At this level, we all handle business logic operations like order fulfillment logic, archive/tasking discrimination/ retasking, etc. 
- **Constellation:** At this level, we more or less decide which satellite will capture what and when, tessellation/fragmentation for big AOIs happens at this level or above.
- **Satellite:** At this level, we all agree satellites are dumb and this is a "Command" level, we just say a satellite what to capture exactly and when. No logic or intelligence is usually put here apart from low level corrections (like pointing refinement in closed loop in orbit, timing adjustment, etc).

## Main concept per layers

| Layer         | Satellogic   | Umbra   | Planet  | SatVu       | BlackSky | Orbital Sidekick |
| ------------- | ------------ | ------- | ------- | ----------- | -------- | ---------------- |
| Business      | Order        | Order   | Order   | Order       | Order    | Order            |
| Constellation | Tasking Task | Task    | Task    | Task        | Task     | Task requirement |
| Satellite     | Capture      | Collect | Capture | Acquisition | Attempt  | Task             |

Most agreed that an order can spawn multiple tasks, and each task can spawn multiple captures/collects/acquisitions/.

## Open questions?
- What layer is the Tasking API working at?
- If orders are the topmost  `business` layer and the interface to interact with customers, should STAC have an analog order concept too? or even the same one? 
- There is an ´opportunity´ endpoint. What is an opportunity in this context? Is a capture/collect/acquisition/attempt? or is it a generic answer for an order?
- Are opportunities used for optionality, to allow users select which capture to take, or for information to show customers what their order will do.