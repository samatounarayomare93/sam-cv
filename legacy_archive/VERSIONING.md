# Versioning Policy

Project Chronos uses semantic versioning:

- `MAJOR` for incompatible changes
- `MINOR` for backward-compatible new features
- `PATCH` for backward-compatible bug fixes

## Tag format

Use tags in the form:

- `v1.0.0`
- `v1.1.0`
- `v1.1.1`

## Release rules

- Create a tag only after the test suite passes locally.
- Use `vX.Y.Z` tags only.
- Keep each release focused on one user-visible set of changes.
- Update the changelog before tagging if the release includes notable fixes.

## Recommended bump examples

- Bug fix only: `v1.0.1`
- New non-breaking capability: `v1.1.0`
- Breaking workflow or API change: `v2.0.0`

## Notes

- The release workflow publishes a zip archive for each version tag.
- GitHub auto-generates release notes for tagged releases.
