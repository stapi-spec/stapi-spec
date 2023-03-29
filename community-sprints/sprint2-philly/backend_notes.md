# Backend Notes

## Day 1

* Layers
  * API - implements API. Sends requests to a backend layer
  * Bakend Layer
    * Implements a protocol defined by the API.
    * Accepts token and search request object
    * Returns Item Collection
* Backends
  * Sentinel
  * Umbra
  * ...
* Authorization
  * Backends accept a token.
  * The frontend could get a token for

Temp Backend Issues List

* Define pystac search-like request type
* Define pystac ItemCollection-like response type
* Implement Sentinel backend with defined search and ItemCollection-like response types

Uncertain
* Define Options Request and Implement Options API
* Implement options request with Sentinel backend
*
