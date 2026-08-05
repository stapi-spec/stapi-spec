#!/usr/bin/env python3
"""Keep spec/openapi.yaml honest.

``spec/openapi.yaml`` is hand-maintained, so nothing regenerates it and nothing
else checks it. This script does two things:

1. validates ``spec/openapi.yaml`` as an OpenAPI document, and
2. validates the JSON examples under ``docs/`` against the component schema
   each one is an example of, so the examples and the schemas cannot drift
   apart silently.

Examples are matched to schemas by file name (see ``EXAMPLE_SCHEMAS``). The
queryables and order-parameters examples are not instances of a component
schema -- they are themselves JSON Schema documents -- so they are checked for
being valid, non-empty schemas instead, as required by the Product spec.

Run with ``uv run python scripts/check_spec.py``.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft7Validator, Draft202012Validator
from openapi_spec_validator import validate as validate_openapi
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError
from referencing import Registry
from referencing.jsonschema import DRAFT202012

ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "spec" / "openapi.yaml"
DOCS = ROOT / "docs"

SPEC_URI = "urn:stapi-openapi"

#: file name (without suffix) -> component schema name.
#: Patterns are matched against the file stem, in order, and the first match
#: wins. Any example not matched here is reported as unmapped.
EXAMPLE_SCHEMAS: tuple[tuple[str, str], ...] = (
    (r"^landingpage$", "RootResponse"),
    (r"^OpportunitySearchRecordCollection$", "OpportunitySearchRecordCollection"),
    (r"^OpportunitySearchStatusCollection$", "OpportunitySearchStatusCollection"),
    (r"^OpportunitySearchRecord", "OpportunitySearchRecord"),
    (r"^OpportunityRequest", "OpportunityRequest"),
    (r"^OpportunityResponse", "OpportunityCollection"),
    (r"^OpportunityCollectionResponse", "OpportunityCollection"),
    (r"^OrderStatusCollection$", "OrderStatusCollection"),
    (r"^OrderCollection$", "OrderCollection"),
    (r"^Order$", "Order"),
    (r"^ProductCollection", "ProductCollection"),
)

#: examples that are JSON Schema documents rather than instances of a
#: component schema
SCHEMA_DOCUMENT_STEMS = (
    r"^ProductConstraints",
    r"^ProductOrderParameters",
)

#: examples whose containing directory names the schema, when the file name
#: does not
DIRECTORY_SCHEMAS = {"OrderStatus": "OrderStatus"}


def load_spec() -> dict[str, Any]:
    return yaml.safe_load(SPEC_PATH.read_text())


def schema_for(path: Path) -> str | None:
    stem = path.stem
    if path.parent.name in DIRECTORY_SCHEMAS:
        return DIRECTORY_SCHEMAS[path.parent.name]
    for pattern, name in EXAMPLE_SCHEMAS:
        if re.search(pattern, stem):
            return name
    return None


def is_schema_document(path: Path) -> bool:
    return any(re.search(p, path.stem) for p in SCHEMA_DOCUMENT_STEMS)


def main() -> int:
    errors: list[str] = []

    spec = load_spec()

    # 1. the OpenAPI document itself
    try:
        validate_openapi(spec)
    except OpenAPIValidationError as exc:
        errors.append(f"{SPEC_PATH.relative_to(ROOT)}: {exc}")
    else:
        print(f"ok   {SPEC_PATH.relative_to(ROOT)} is a valid OpenAPI document")

    components = spec["components"]["schemas"]
    registry = Registry().with_resource(
        SPEC_URI,
        DRAFT202012.create_resource(spec),
    )

    validators = {
        name: Draft202012Validator(
            {"$ref": f"{SPEC_URI}#/components/schemas/{name}"},
            registry=registry,
        )
        for name in components
    }

    checked = 0
    unmapped: list[Path] = []

    for path in sorted(DOCS.rglob("*.json")):
        rel = path.relative_to(ROOT)
        instance = json.loads(path.read_text())

        if is_schema_document(path):
            try:
                Draft7Validator.check_schema(instance)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{rel}: not a valid JSON Schema: {exc}")
                continue
            if not instance:
                errors.append(f"{rel}: empty schemas are not allowed")
                continue
            checked += 1
            print(f"ok   {rel} is a valid, non-empty JSON Schema document")
            continue

        name = schema_for(path)
        if name is None:
            unmapped.append(rel)
            continue
        if name not in validators:
            errors.append(f"{rel}: no component schema named {name!r}")
            continue

        found = sorted(
            validators[name].iter_errors(instance),
            key=lambda e: list(e.absolute_path),
        )
        if found:
            for err in found[:5]:
                loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
                errors.append(f"{rel} [{name}] at {loc}: {err.message}")
        else:
            checked += 1
            print(f"ok   {rel} validates against {name}")

    if unmapped:
        for rel in unmapped:
            errors.append(
                f"{rel}: no component schema mapped for this example; add it "
                "to EXAMPLE_SCHEMAS or SCHEMA_DOCUMENT_STEMS in "
                "scripts/check_spec.py"
            )

    print()
    if errors:
        print(f"FAILED: {len(errors)} problem(s)", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"PASSED: OpenAPI document valid, {checked} examples checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
