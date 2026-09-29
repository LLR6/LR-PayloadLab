# Changelog

## 0.2.0 - 2026-09-29

### Added
- Canonical Manifest SHA-256 in receipts and build results.
- Static Manifest inspection with action, path, duration and capability summary.
- CI-published inspection artifact.
- Reproducibility documentation for Manifest-to-artifact provenance.

### Changed
- Receipts use schema v2 and bind execution records to a canonical Manifest fingerprint.

### Safety
- Inspection explicitly reports no network, no arbitrary command execution and no workspace escape.
