# Security Policy

LR-PayloadLab is intentionally bounded to benign, local, auditable endpoint-telemetry experiments.

## Security boundaries

The project must not add:

- network callbacks;
- arbitrary command execution;
- persistence;
- credential collection;
- privilege escalation;
- evasion or anti-analysis behavior;
- workspace escape.

If you find a way to bypass a documented path, action, duration, or capability boundary, report it privately.

Use synthetic values and temporary workspaces in reproductions. Do not include real credentials, production endpoints, or private customer data.
