# Releasing LR-PayloadLab

## Checklist

1. CI green.
2. Manifest validation and static inspection tests pass.
3. CI inspection artifact explicitly shows bounded capability assumptions.
4. Receipt / Manifest fingerprint tests pass.
5. No new arbitrary command execution, persistence, credential access or uncontrolled networking capability is introduced.
6. Update `CHANGELOG.md`, `pyproject.toml` and `CITATION.cff`.
7. Review `SECURITY.md`, `docs/BENCHMARKS.md` and `docs/ROADMAP.md`.

Release notes should describe defensive telemetry scenarios, not evasive capability.
