# Tasking API (WIP)

The Tasking API is a specification designed to standardize the process of tasking satellites for image capture. By defining a common language and set of API calls, it enables satellite data providers, users, and marketplaces to work seamlessly together. The API facilitates feasibility or opportunity assessments, allowing users to input criteria like area, time range, and acceptable cloud cover percentage. The satellite data provider can then return a series of intervals in which image capture is possible.

## Audience

The Tasking API is designed for a wide range of industry participants, including:

- **Data providers**: This specification allows providers to build APIs with a clear, industry-reviewed standard, reducing development effort and facilitating collaboration.
- **Data users**: End-users can task satellites more easily across multiple providers, thanks to a shared API language and ecosystem of tools.
-**Data marketplaces**: By establishing standard API calls and expected metadata, this specification enables marketplaces to bring together diverse providers and offer a consistent experience for users.

## Benefits

Adopting the Satellite Tasking API Specification provides several key benefits:

- **Industry Standardization**: Establishing a shared language for satellite tasking streamlines communication and collaboration between industry members, fostering innovation and interoperability.
- **Ecosystem Growth**: A common API language allows for the development of new tools and services that benefit users, expanding the market and making satellite tasking more accessible.
- **Marketplace Integration**: Standard API calls and metadata expectations enable the creation of satellite data marketplaces, offering a cohesive experience for users and providers alike.

## Relationship to STAC

The Satellite Tasking API Specification will be developed to closely integrate with the SpatioTemporal Asset Catalog (STAC) standard. This ensures compatibility and consistency between satellite data cataloging and tasking, further promoting industry-wide collaboration.

# Endpoints

`/products` GET

Lists products available.

`/products/{product_id}/opportunities` POST

Post an object containing a `Search`. Get an object with a  refined `Search`.

`/products/{product_id}/order` POST

Post an object containing a `Search`. Get confirmation and ID.

`/products/{product_id}/order/{order_id}/status` GET

Gets status ID.

# Models

## Search
The Search contains a "filter" property that is either modeled after CQL 2 queries, or can itself be CQL 2 similar to the STAC [filter extension](https://github.com/stac-api-extensions/filter) and OGC API - Features Part 3.

It is used both as a request and a response to the `/products/{product_id}/opportunities` endpoint.