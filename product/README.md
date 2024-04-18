
## Overview
This document explains the structure of a STAT Product.

STAT Product objects are represented in JSON format and are very flexible. Any JSON object that contains all the required fields is a valid STAT Product. A Product object contains a minimal set of required properties to be valid and can be extended through the use of constraints and parameters.

# Product Spec

| Element         | Type                                             | Description                                                  |
| --------------- | ------------------------------------------------ | ------------------------------------------------------------ |
| type            | string                                           | **REQUIRED.** Must be set to `Collection` to be a valid Product. |
| id              | string                                           | **REQUIRED.** Identifier for the Product that is unique across the provider. |
| conformsTo      | \[string\]                                       | Conformance classes that apply to the product specifically. |
| title           | string                                           | A short descriptive one-line title for the Product.       |
| description     | string                                           | **REQUIRED.** Detailed multi-line description to fully explain the Collection. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation. |
| keywords        | \[string]                                        | List of keywords describing the Product.                  |
| license         | string                                           | Collection's license(s), either a SPDX [License identifier](https://spdx.org/licenses/), `other` for all other cases. |
| providers       | \[[Provider Object](#provider-object)]           | A list of providers, which may include all organizations capturing or processing the data or the hosting provider. Providers should be listed in chronological order with the most recent provider being the last element of the list. |                |
| links           | \[[Link Object](#link-object)]                   | **REQUIRED.** A list of references to other documents.       |
| parameters      | JSON Schema                                      | JSON Schema that defines the Opportunity and Order properties that can be used in cql2json filter statements. |


### Provider Object

The object provides information about a provider.
A provider is any of the organizations that captures or processes the content of the Collection
and therefore influences the data offered by this Collection.
May also include information about the final storage provider hosting the data.

| Field Name  | Type      | Description                                                  |
| ----------- | --------- | ------------------------------------------------------------ |
| name        | string    | **REQUIRED.** The name of the organization or the individual. |
| description | string    | Multi-line description to add further provider information such as processing details for processors and producers, hosting details for hosts or basic contact information. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation. |
| roles       | \[string] | Role of the provider. Set to `producer` or `reseller`. |
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
| rel        | string | **REQUIRED.** Relationship between the current document and the linked document. See chapter "[Relation types](#relation-types)" for more information. |
| type       | string | [Media type](../catalog-spec/catalog-spec.md#media-types) of the referenced entity. |
| title      | string | A human readable title to be used in rendered displays of the link. |

For a full discussion of the situations where relative and absolute links are recommended see the
['Use of links'](../best-practices.md#use-of-links) section of the STAC best practices.

### Parameters Object

Parameters are fields that can be filtered on in Opportunity and Order requests to reduce the results set. For example, a `parameter` might be `eo:cloud_cover` which allows users to filter Opportunities to only results with `eo:cloud_cover` within a certain range. 

A Parameters Object is a definitions for fine-grained information, see the [JSON Schema Object](#json-schema-object) section for more.

It is recommended to use [JSON Schema draft-07](https://json-schema.org/specification-links.html#draft-7)
to align with the JSON Schemas provided by STAC. Empty schemas are not allowed.

For an introduction to JSON Schema, see "[Learn JSON Schema](https://json-schema.org/learn/)".

#### Parameters Best Practices

There are many Tasking constraints that cannot be represented by JSON Schema. For these constraints, strongly consider documenting the constraint in the `"description"` property of the relevant constraint or use the `"links"` attribute to link the user out to documentation that describes additional constraints.

TODO: Example
TODO: Documented link type for client libraries to be able to find and surface to users
