# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

none

### Changed

- Create-order endpoint now pluralized to `/product/{productId}/orders`
- Order Statuses retrieval endpoint now plural (`/statuses`)
- Product Parameters renamed to Constraints
- Product Constraints renamed (again) to Queryables to align with OGC Features API terminology
- Opportunities search and Order creation parameters `datetime` and `geometry` removed in favor of using existing
  support in CQL2 for datetime comparison and spatial intersects operations.
  

### Deprecated

none

### Removed

none

### Fixed

none

### Security

none
