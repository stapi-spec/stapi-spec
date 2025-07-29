[![docs](https://github.com/stapi-spec/stapi-spec/actions/workflows/deploy.yml/badge.svg)](https://github.com/stapi-spec/stapi-spec/actions/workflows/deploy.yml)

# STAPI Specification Repository

This repository contains the official specification for the **Sensor Tasking
API (STAPI)**, a JSON-based web API for discovering and ordering
spatio-temporal data products from remote sensing providers.

## What is STAPI?

STAPI enables users to:
- Discover available **Products** from satellite and airborne data providers
- Request **Opportunities** to understand what data can be collected
- Submit **Orders** for new tasking or archived data processing

The specification is designed to work alongside [STAC](https://stacspec.org/) -
while STAC handles existing data, STAPI handles ordering future data or
processing tasks.

## 🚀 Quick Start

### View the Documentation

Visit the [STAPI documentation site](https://stapi-spec.github.io/stapi-spec/)
to read the full specification.

### Local Development

To run the documentation site locally:

```bash
uv run mkdocs serve
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development instructions.

## 🔗 Related Projects

- [PySTAPI](https://github.com/stapi-spec/pystapi) - Python implementations
  including:
  - STAPI entity model definitions
  - Reference server implementation (stapi-fastapi)
  - Reference client implementation (pystapi-client)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:
- Development setup
- Making changes to the specification
- Submitting pull requests

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE).
