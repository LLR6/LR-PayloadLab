# LR-PayloadLab Architecture

```text
Manifest JSON
    ↓
schema + policy validation
    ↓
static inspection
    ↓
canonical Manifest SHA-256
    ↓
plan / bounded run / build
    ↓
receipt + artifact hashes
    ↓
rollback / cleanup
```

## Trust boundaries

Allowed behavior is represented by a small explicit action set. A Manifest cannot request arbitrary commands or network operations.

Paths are resolved beneath a caller-provided workspace and rejected if they escape it.

## Provenance

Receipts and build metadata carry the canonical Manifest fingerprint. Generated artifacts have independent SHA-256 values.

## Non-goals

- malware generation;
- persistence;
- remote callbacks;
- evasion;
- credential access;
- arbitrary shell execution.
