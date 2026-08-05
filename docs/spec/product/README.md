# STAPI Product Spec

This document defines a Product and explains its specification and structure.

A STAPI Product is remote sensing data or derived insights with spatio-temporal
components that can deliver value to the user. A non-exhaustive list of
examples includes:

- Electro-optical (EO) images
- Synthetic Aperture Radar (SAR) images
- Hyperspectral images
- Mosaic images
- Feature (immobile) detection
- Object (movable) detection
- Change detection

Some Providers may offer only data or analytic Products while some may offer
both. The Product specification is flexible enough to offer queryables at the
level of the product offering. For example, a ship (object) detection Product
may only specify queryables like location, datetime, and minimum ship length.
The specific data products -- SAR, EO, or otherwise can be left as an
implementation detail to the analytic Product Provider.

STAPI Product objects are represented in JSON format and are very flexible. Any
JSON object that contains all the required fields is a valid STAPI Product. A
`Product` object contains a minimal set of required properties to be valid and
can be extended through the use of Queryables and Order Parameters.

## Product Collection

In addition to the fields common to every [Collection
Object](../collection/README.md), a Product Collection has the following
fields.

| Element | Type | Description |
| ------- | ---- | ----------- |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. **Must** be set to `ProductCollection`. |
| products | [[Product Object](#product-object)] | **REQUIRED** List of `Product` offered in the application. |

## Product Object

| Element | Type | Description |
| ------- | ---- | ----------- |
| type | string | **REQUIRED.** Must be set to `Collection` to be a valid Product. |
| stapi_type | string | **REQUIRED.** Type of the STAPI Object. MUST be set to `Product`. |
| stapi_version | string | **REQUIRED.** The STAPI version the Product implements. |
| id | string | **REQUIRED.** Identifier for the Product that is unique across the provider. |
| conformsTo | \[string\] | Conformance classes that apply to the product specifically. |
| title | string | A short descriptive one-line title for the Product. |
| description | string | **REQUIRED.** Detailed multi-line description to fully explain the Collection. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation. |
| keywords | \[string\] | List of keywords describing the Product. |
| license | string | **REQUIRED.** Collection's license(s), either a SPDX [License identifier](https://spdx.org/licenses/), `various` if multiple licenses apply or `proprietary` for all other cases. |
| providers | \[[Provider Object](#provider-object)\] | A list of providers, which may include all organizations capturing or processing the data or the hosting provider. Providers should be listed in chronological order with the most recent provider being the last element of the list. |
| links | \[[Link Object](../link/README.md)\] | **REQUIRED.** A list of references to other documents. See [Product Links](#product-links). |

Additional properties are allowed to be placed in the top-level object,
comparable to how STAC Collections work.  STAC Collection fields can be reused,
including fields defined in STAC Collection extensions.

### Product Links

Each link in the links array must be a [Link Object](../link/README.md).

| rel type | Description |
| ---------- | ----------- |
| `queryables` | Links to the `GET /products/{productId}/queryables` endpoint. |
| `order-parameters` | Links to the `GET /products/{productId}/order-parameters` endpoint. |
| `conformance` | Links to the `GET /products/{productId}/conformance` endpoint. |

### Provider Object

The object provides information about a provider.  A provider is any of the
organizations that captures or processes the content of the Collection and
therefore influences the data offered by this Collection.  May also include
information about the final storage provider hosting the data.

| Field Name | Type | Description |
| ---------- | ---- | ----------- |
| name | string | **REQUIRED.** The name of the organization or the individual. |
| description | string | Multi-line description to add further provider information such as processing details for processors and producers, hosting details for hosts or basic contact information. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation. |
| roles | \[string\] | Roles of the provider. Any of `licensor`, `producer`, `processor`, or `host` |
| url | string | Homepage on which the provider describes the dataset and publishes contact information. |

**roles**: The provider's role(s) can be one or more of the following elements:

- *licensor*: The organization that is licensing the dataset under the license
  specified in the Collection's `license` field.
- *producer*: The producer of the data is the provider that initially captured
  and processed the source data, e.g. ESA for Sentinel-2 data.
- *processor*: A processor is any provider who processed data to a derived
  product.
- *host*: The host is the actual provider offering the data on their storage.
  There should be no more than one host, specified as last element of the list.

## Queryables

Queryables define the `Opportunity` and `Order` properties that can be used in
CQL2 JSON filter statements to constrain the intended search results.

The concept of `Queryables` is meant to align with the [STAC API Filter
Extension
Specification](https://github.com/stac-api-extensions/filter?tab=readme-ov-file#queryables),
which uses queryables to define searchable properties of STAC Items, as well as
the [OGC Features API Part
3](https://developer.ogc.org/api/features/part3.html#operation/getQueryables)
equivalent term.

For example, one `queryable` might be `eo:cloud_cover` which allows users to
filter Opportunities to only results with `eo:cloud_cover` within a certain
range.

The queryables must be exposed as a separate endpoint that is provided at
`GET /products/{productId}/queryables`. The response body is a JSON Schema
definition, as described in [Schema Documents](#schema-documents).

A queryable listed in the schema's `required` array indicates that a filter
predicate constraining that queryable must be supplied in any Opportunity or
Order request for the Product. Marking one or more queryables as required
thereby makes the otherwise-optional `filter` field of the [Search Parameters
Object](../search-parameters/README.md) effectively required for that Product.

[Example queryables document](./examples/ProductConstraintsUmbra_umbra_spotlight.json)

## Order Parameters

Order Parameters define Product options that can be used when creating an
Order.  These are different than Product Queryables, in that they do not
constrain (filter) the desired results, but rather define general properties of
an entire order. For example, an order parameter might define what file format
to use for delivery, what cloud service provider the order will be delivered
in, or what location to deliver to.

The parameters must be exposed as a separate endpoint that is provided at
`GET /products/{productId}/order-parameters`. The response body is a JSON
Schema definition, as described in [Schema Documents](#schema-documents).

Use of Order Parameters when placing an Order is described in the [Order
Request Object](../order/README.md#order-request-object).

[Example order parameters document](./examples/ProductOrderParametersUmbra_umbra_spotlight.json)

## Schema Documents

Both the queryables and the order parameters endpoints return a schema
document, and the same rules apply to each.

The response body is a JSON Schema definition.  Empty schemas are not allowed.
It is recommended to use [JSON Schema
draft-07](https://json-schema.org/specification-links.html#draft-7).  For an
introduction to JSON Schema, see [Learn JSON
Schema](https://json-schema.org/learn/getting-started-step-by-step).

### Schema Documents Best Practices

There are many Tasking queryables and order parameters that cannot be
represented by JSON Schema. For these, strongly consider documenting the
queryable or parameter in the `"description"` property of the relevant
queryable or parameter or use the `"links"` attribute to link the user out to
documentation that describes additional queryables or parameters.
