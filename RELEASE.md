# Release Process

This document describes the process for releasing new versions of the STAPI
specification.

## Versioning

STAPI follows [Semantic Versioning](https://semver.org/):

- **Major** version for incompatible API changes
- **Minor** version for backwards-compatible functionality additions
- **Patch** version for backwards-compatible bug fixes

## Release Steps

To release a new version of the STAPI specification:

1. **Prepare the Release**

   - Ensure all changes for the release are merged to `main`
   - Review the changes since the last release
   - Update any version references in the documentation if needed

1. **Create a GitHub Release**

   - Go to the [Releases page](https://github.com/stapi-spec/stapi-spec/releases)
   - Click "Draft a new release"
   - Create a new tag following semantic versioning (e.g., `v0.2.0`)
   - Set the release title (e.g., "STAPI v0.2.0")
   - Write release notes describing the changes
   - Publish the release

1. **Automated Deployment**

   The GitHub Actions workflow will automatically:

   - Deploy the new version to the documentation site
   - Update the `stable` alias to point to the new version
   - Keep the `dev` version for ongoing development

## Documentation Versions

After a release, the documentation will be available at:

- **Specific version**: `https://stapi-spec.github.io/stapi-spec/v0.2.0/`
- **Latest stable**: `https://stapi-spec.github.io/stapi-spec/stable/`
- **Development**: `https://stapi-spec.github.io/stapi-spec/dev/`
- **Latest** (alias for dev): `https://stapi-spec.github.io/stapi-spec/latest/`

## Version Management

The documentation uses [mike](https://github.com/jimporter/mike) for version management:

- Every push to `main` updates the `dev` and `latest` versions
- Publishing a release updates that version and the `stable` alias
- Old versions remain accessible at their specific URLs

## Pre-release Versions

For pre-release versions (alpha, beta, rc):

- Use appropriate version tags (e.g., `v1.0.0-beta.1`)
- Mark as "pre-release" when creating the GitHub release
- These will be deployed at their version URL but won't update the `stable` alias
- Pre-releases are useful for testing and preview purposes

## Troubleshooting

If you need to manually manage versions (not recommended):

```bash
# List all versions
uv run mike list

# Deploy a specific version (requires push permissions)
uv run mike deploy --push --update-aliases VERSION ALIAS

# Delete a version (use with caution)
uv run mike delete --push VERSION
```

**Note**: Manual version management should only be done in exceptional
circumstances. Normal releases should always go through the GitHub release
process.
