
## Overview
This document explains the structure of a STAT Product.

STAT Product objects are represented in JSON format and are very flexible. Any JSON object that contains all the required fields is a valid STAT Product. A Product object contains a minimal set of required properties to be valid and can be extended through the use of constraints and parameters.

# Product Spec

| Element         | Type                                             | Description                                                  |
| --------------- | ------------------------------------------------ | ------------------------------------------------------------ |
| type            | string                                           | **REQUIRED.** Must be set to `Product` to be a valid Product. |
| id              | string                                           | **REQUIRED.** Identifier for the Product that is unique across the provider. |
| title           | string                                           | A short descriptive one-line title for the Product.       |
| description     | string                                           | **REQUIRED.** Detailed multi-line description to fully explain the Collection. [CommonMark 0.29](http://commonmark.org/) syntax MAY be used for rich text representation. |
| keywords        | \[string]                                        | List of keywords describing the Product.                  |
| license         | string                                           | **REQUIRED.** Collection's license(s), either a SPDX [License identifier](https://spdx.org/licenses/), `various` if multiple licenses apply or `proprietary` for all other cases. |
| providers       | \[[Provider Object](#provider-object)]           | A list of providers, which may include all organizations capturing or processing the data or the hosting provider. Providers should be listed in chronological order with the most recent provider being the last element of the list. |                |
| links           | \[[Link Object](#link-object)]                   | **REQUIRED.** A list of references to other documents.       |
| constraints | Map<string, [Constraints Object](#constraints-object)> | User supplied constraints on a tasking request |
| parameters | [Parameters Object](#parameters-object) | User supplied parameters that don't constrain tasking (e.g., output format) |


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
| rel        | string | **REQUIRED.** Relationship between the current document and the linked document. See chapter "[Relation types](#relation-types)" for more information. |
| type       | string | [Media type](../catalog-spec/catalog-spec.md#media-types) of the referenced entity. |
| title      | string | A human readable title to be used in rendered displays of the link. |

For a full discussion of the situations where relative and absolute links are recommended see the
['Use of links'](../best-practices.md#use-of-links) section of the STAC best practices.

### Constraints Object

Constraints are limitations imposed by the user and the data provider as to what data is desired, and what data is available. In addition to space, time, and product limitations, constraints filter the needs of the user and capacity of the provider through an API negotiation. Constraints build off STAC extensions and modify them in order to support ranges of values.

Users of the Tasking API Should follow STAC Extension naming conventions when adding constraints.

A Constraints Object is a definitions for fine-grained information, see the [JSON Schema Object](#json-schema-object) section for more.

It is recommended to use [JSON Schema draft-07](https://json-schema.org/specification-links.html#draft-7)
to align with the JSON Schemas provided by STAC. Empty schemas are not allowed.

For an introduction to JSON Schema, see "[Learn JSON Schema](https://json-schema.org/learn/)".

### Parameters Object

Parameters are objects which do not affect the Tasking process, but are nevertheless useful. For example, a user may wish to select a preferred output format or a data provider may provide additional metadata about a product.

A Constraints Object is a definitions for fine-grained information, see the [JSON Schema Object](#json-schema-object) section for more.

It is recommended to use [JSON Schema draft-07](https://json-schema.org/specification-links.html#draft-7)
to align with the JSON Schemas provided by STAC. Empty schemas are not allowed.

For an introduction to JSON Schema, see "[Learn JSON Schema](https://json-schema.org/learn/)".

### Range Object

For summaries that would normally consist of a lot of continuous values, statistics can be added instead.
By default, only ranges with a minimum and a maximum value can be specified.
Ranges can be specified for [ordinal](https://en.wikipedia.org/wiki/Level_of_measurement#Ordinal_scale) values only,
which means they need to have a rank order.
Therefore, ranges can only be specified for numbers and some special types of strings. Examples: grades (A to F), dates or times.
Implementors are free to add other derived statistical values to the object, for example `mean` or `stddev`.

| Field Name | Type           | Description |
| ---------- | -------------- | ----------- |
| minimum    | number\|string | **REQUIRED.** Minimum value. |
| maximum    | number\|string | **REQUIRED.** Maximum value. |

### Properties Object

Providers should include metadata fields that are relevant for users of STAC, but it is recommended to select only those necessary for search. Where possible metadata fields should be mapped to the STAC Common Metadata and widely used extensions, to enable cross-catalog search on known fields.

STAC Common Metadata - A list of fields commonly used throughout all domains. These optional fields are included for STAC Items by default.
Extensions - Additional fields that are more specific, such as EO, View.
Custom Extensions - It is generally allowed to add custom fields but it is recommended to add multiple fields for related values instead of a nested object, e.g., two fields view:azimuth and view:off_nadir instead of a field view with an object value containing the two fields. The convention (as used within Extensions) is for related fields to use a common prefix on the field names to group them, e.g. view. A nested data structure should only be used when the data itself is nested, as with eo:bands.
