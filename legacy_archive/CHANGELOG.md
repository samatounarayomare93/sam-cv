# Changelog

All notable changes to this project should be recorded here.

## [Unreleased]

### Added
- CI quality gate with unit tests and coverage enforcement.
- Tag-based release workflow with packaged archives.
- Branch protection checklist for GitHub repository settings.

### Changed
- Improved launcher and compatibility shims for legacy imports.
- Hardened workflow behavior for missing secrets and test-only environments.

### Fixed
- Race condition in rate limiting.
- Telegram polling conflict from duplicate instances.
- Email validation false positive on valid `example.com` addresses.
- LinkedIn nudge generation and task persistence compatibility.

## Release Template

When preparing a release, copy the relevant entries from `[Unreleased]` into a dated release section, for example:

## [v1.0.0] - 2026-04-17

### Added
- Feature summary here.

### Changed
- Behavior summary here.

### Fixed
- Bug summary here.
