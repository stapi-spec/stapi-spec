
# STAPI Product Spec

This document defines a Product and explains its specification and structure.

A STAPI Product is remote sensing data or derived insights with spatio-temporal components that can deliver value to the user. A non-exhaustive list of examples includes:

- Electro-optical (EO) images
- Synthetic Aperture Radar (SAR) images
- Hyperspectral images
- Mosaic images
- Feature (immobile) detection
- Object (movable) detection
- Change detection

Some Providers may offer only data or analytic Products while some may offer both. The Product specification is flexible enough to offer queryables at the level of the product offering. For example, a ship (object) detection Product may only specify queryables like location, datetime, and minimum ship length. The specific data products -- SAR, EO, or otherwise can be left as an implementation detail to the analytic Product Provider.

STAPI Product objects are represented in JSON format and are very flexible. Any JSON object that contains all the required fields is a valid STAPI Product. A Product object contains a minimal set of required properties to be valid and can be extended through the use of queryables and parameters.

## Product Collection Spec

| Element       | Type    | Description |
| ---- | --- | --- |
| products | [[Product Object](#product-object)] | **REQUIRED** List of `Product` offered in the application. |
| links | [[Link Object](#link-object)] | **REQUIRED** Links for e.g. pagination. |


## Product Object 
| Element         | Type                                             | Description                                                  |
| --------------- | ------------------------------------------------ | ------------------------------------------------------------ |
| type            | string                                           | **REQUIRED.** Must be set to `Product` to be a valid Product. |
| id              | string                                           | **REQUIRED.** Identifier for the Product that is unique across the provider. |
| conformsTo      | \[string\]                                       | Conformance classes that apply to the product specifically. |
| title           | string                                           | A short descriptive one-line title for the Product.       |
| description     | string                                           | **REQUIRED.** Detailed multi-line description to fully explain the Collection. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation. |
| keywords        | \[string]                                        | List of keywords describing the Product.                  |
| license         | string                                           | **REQUIRED.** Collection's license(s), either a SPDX [License identifier](https://spdx.org/licenses/), `various` if multiple licenses apply or `proprietary` for all other cases. |
| providers       | \[[Provider Object](#provider-object)]           | A list of providers, which may include all organizations capturing or processing the data or the hosting provider. Providers should be listed in chronological order with the most recent provider being the last element of the list. |                |
| links           | \[[Link Object](#link-object)]                   | **REQUIRED.** A list of references to other documents.       |

Additional properties are allowed to be placed in the top-level object, comparable to how STAC Collections work. 
STAC Collection fields can be reused, including fields defined in STAC Collection extensions.

### Provider Object

The object provides information about a provider.
A provider is any of the organizations that captures or processes the content of the Collection
and therefore influences the data offered by this Collection.
May also include information about the final storage provider hosting the data.

| Field Name  | Type      | Description                                                  |
| ----------- | --------- | ------------------------------------------------------------ |
| name        | string    | **REQUIRED.** The name of the organization or the individual. |
| description | string    | Multi-line description to add further provider information such as processing details for processors and producers, hosting details for hosts or basic contact information. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation. |
| roles       | \[string] | Role of the provider. Set to `producer` or `reseller`|
| url         | string    | Homepage on which the provider describes the dataset and publishes contact information. |

**roles**: The provider's role(s) can be one or more of the following elements:

- *licensor*: The organization that is licensing the dataset under the license specified in the Collection's `license` field.
- *producer*: The producer of the data is the provider that initially captured and processed the source data, e.g. ESA for Sentinel-2 data.
- *processor*: A processor is any provider who processed data to a derived product.
- *host*: The host is the actual provider offering the data on their storage.
  There should be no more than one host, specified as last element of the list.

### Link Object

This object describes a relationship with another entity. Data providers are advised to be liberal with links.

| Field Name | Type   | Description                                                  |
| ---------- | ------ | ------------------------------------------------------------ |
| href       | string | **REQUIRED.** The actual link in the format of an URL. Relative and absolute links are both allowed. |
| rel        | string | **REQUIRED.** Relationship between the current document and the linked document.  |
| type       | string | Media Type of the referenced entity. |
| title      | string | A human readable title to be used in rendered displays of the link. |

The relation type `queryables` is to be used to link to the `GET /products/{productId}/queryables` endpoint.

The relation type `order-parameters` is to be used to link to the `GET /products/{productId}/order-parameters` endpoint.

## Queryables 

Queryables define the Opportunity and Order properties that can be used in CQL2 JSON filter expressions to
filter the set of results.
For example, a `queryables` might be `eo:cloud_cover` which allows users to filter Opportunities to only results with `eo:cloud_cover` within a certain range. 

The queryables must be exposed as a separate endpoint that is provided at 
`GET /products/{productId}/queryables`.

The response body for parameters is a JSON Schema definition. Empty schemas are not allowed.
It is required to use [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/schema).
This definition should follow the same conventions
defined by the [OGC API - Features - Part 3: Filtering](https://docs.ogc.org/is/19-079r2/19-079r2.html) Requirements Class "Queryables", including:

- The Content-Type of the response should be `application/schema+json`
- The property $schema is `https://json-schema.org/draft/2020-12/schema`
- The property $id is the URI of the resource without query parameters, e.g., `https://stapi.example.com/products/my_product/queryables`
- The type is `object`

#### Queryables Best Practices

There are many Tasking constraints that cannot be represented by JSON Schema. For these constraints, strongly consider documenting the constraint in the `description` property of the relevant constraint or use the `"links"` attribute to link the user out to documentation that describes additional constraints.

TODO: Is this actually the case?
TODO: Example
TODO: Documented link type for client libraries to be able to find and surface to users

## Order Parameters

Order Parameters define the properties that can be used when creating an Order. These are different
than queryables, in that they do not constrain the desired results, but instead are used to specify
desired properties of the entities that fulfill an order. For example, the desired file format (COG vs. NITF)
or cloud object storage location (AWS S3 vs. Microsoft Azure) may be an order parameter.

For example, an order parameter might define what file format or what cloud service provider that
the order will be delivered in.

The parameters must be exposed as a separate endpoint that is provided at 
`GET /products/{productId}/order-parameters`.

The response body for order parameters is a JSON Schema definition.
Empty schemas are not allowed.
It is required to use [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/schema).

#### Order Parameters Best Practices

There are many order parameters that cannot be represented by JSON Schema. For these parameters, strongly consider documenting the constraint in the `"description"` property of the relevant constraint or use the `"links"` attribute to link the user out to documentation that describes additional parameters.

TODO: Example
TODO: Documented link type for client libraries to be able to find and surface to users
