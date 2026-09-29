# Contributing

LR-PayloadLab accepts improvements that make bounded experiments more observable, reproducible, or easier to verify.

## Before adding an action

A new action must:

1. be clearly benign;
2. be statically inspectable;
3. have an explicit resource/path cap;
4. produce an auditable receipt;
5. have rollback or cleanup semantics when it creates artifacts;
6. remain local-only;
7. include tests for boundary enforcement.

Run:

```bash
python -m pip install -e .
python -m unittest discover -s tests
payload-lab inspect examples/telemetry-demo.json
```

Do not submit features for stealth, evasion, persistence, credential access, exploitation, or remote control.
