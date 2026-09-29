# Benchmarks and Reproducibility Checks

PayloadLab intentionally avoids offensive performance benchmarks. The important checks are boundedness and reproducibility.

## Static inspection

```bash
payload-lab inspect examples/telemetry-demo.json
```

Verifies and reports:

- Manifest SHA-256;
- action types;
- workspace paths;
- declared active duration;
- allowed actions;
- no network capability;
- no arbitrary command execution;
- no workspace escape.

## Receipt / artifact provenance

Plan and run receipts bind to a canonical Manifest SHA-256. Generated artifacts also expose SHA-256 so an experiment can retain both input-definition and output fingerprints.

## CI

CI runs unit tests and publishes a manifest-inspection artifact for independent review.
