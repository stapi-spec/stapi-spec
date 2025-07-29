# Contributing

We welcome contributions to the STAPI specification! This document provides
instructions for developers working on this project.

## What is STAPI?

STAPI (Sensor Tasking API) is a JSON-based web API for discovering and ordering
spatio-temporal data products from remote sensing providers. The specification
enables users to:

- Discover available **Products** from satellite and airborne data providers
- Request **Opportunities** to understand what data can be collected
- Submit **Orders** for new tasking or archived data processing

The specification is designed to work alongside [STAC](https://stacspec.org/) -
while STAC handles existing data, STAPI handles ordering future data or
processing tasks.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python**: Version 3.13 or above (can be installed by `uv`)
- **uv**: The fast Python package and project manager. Install it from
  [astral.sh/uv](https://docs.astral.sh/uv/) or use `pip`

## Development

The documentation site is built with [MkDocs](https://www.mkdocs.org/) and
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

- Documentation source files are in the `/docs` directory
- The OpenAPI specification is located at `/docs/openapi/openapi.yaml`
- MkDocs configuration is in `mkdocs.yml`

### Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/stapi-spec/stapi-spec.git
   cd stapi-spec
   ```

1. Install dependencies using uv:

   ```bash
   uv sync
   ```

### Available Commands

All commands should be run from the root of the repository.

- `uv run mkdocs serve`: Starts the development server with live reload. The
  site will be available at `http://localhost:8000`. Use this command for most
  development work.
- `uv run mkdocs build`: Creates a production-ready build of the entire site in
  the `site/` directory.
- `uv run mkdocs --help`: Shows all available MkDocs commands.

### Making Changes

1. **Documentation Updates**: Edit the Markdown files in the `/docs` directory.
   The navigation structure is defined in `mkdocs.yml`.
1. **API Specification**: The API specification at `/docs/openapi/openapi.yaml`
   is generated via `stapi-fastapi`. Do not update this file manually; make
   `stapi-fastapi` changes as needed for spec updates, regenerate this file,
   and copy the new version into place.
1. **Theme and Configuration**: Site-wide settings, theme configuration, and
   plugins are managed in `mkdocs.yml`.

### Project Structure

```plaintext
stapi-spec/
├── docs/              # Documentation source files
│   ├── spec/          # STAPI specification documents
│   ├── conformances/  # Conformance class definitions
│   └── openapi/       # OpenAPI specification
├── hooks/             # MkDocs hooks
├── mkdocs.yml         # MkDocs configuration
├── pyproject.toml     # Python project configuration
└── uv.lock            # Locked dependencies
```

## Submitting Pull Requests

1. Fork the repository and create a new branch for your changes
1. Install pre-commit with `uv run pre-commit install`
1. Make your changes following the existing style and conventions
1. Test your changes locally using `uv run mkdocs serve`
1. Commit your changes with clear, descriptive messages
1. Push to your fork and submit a pull request

## Related Projects

- [PySTAPI](https://github.com/stapi-spec/pystapi) - Python implementations including:
  - STAPI entity model definitions
  - Reference server implementation (stapi-fastapi)
  - Reference client implementation (pystapi-client)
