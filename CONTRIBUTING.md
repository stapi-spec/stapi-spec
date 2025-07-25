# Contributing

This document provides instructions for developers working on this project.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js**: Version 18.0 or above. You can download it from
  [nodejs.org](https://nodejs.org/) or use something like Homebrew or your
  system package manager.
- **npm**: Node Package Manager, which comes bundled with Node.js.

## Development

The documentation site is built with Docusaurus and Redoc.

- Docusaurus source files are in the `/docs` directory.
- The OpenAPI specification is located at `/spec/openapi.yaml`.

### Available Scripts

This project includes several scripts to help with development and building the
documentation. All commands should be run from the **root of the repository**.

- **`npm install`**: Installs all necessary dependencies for the project.

- **`npm start`**: Starts the development server. This will first build the API
  documentation from the OpenAPI spec and then launch the Docusaurus site with
  live reload. Use this command for most development work. If you make changes
  to `spec/openapi.yaml`, you will need to restart the server to see them
  reflected in the `api.html` page.

- **`npm run build`**: Creates a production-ready build of the entire site. It
  bundles the Redoc API documentation and the Docusaurus site into the
  `docs/build` directory.

- **`npm run serve`**: Serves the production build locally. Use this to preview
  the final site before deployment.

- **`npm run lint`**: Lints the TypeScript, JavaScript, and Markdown files, and
  validates the OpenAPI specification.

- **`npm run lint:fix`**: Automatically fixes linting issues in TypeScript,
  JavaScript, and Markdown files.

- **`npm run format`**: Automatically formats TypeScript, JavaScript, and
  Markdown files using Prettier.
