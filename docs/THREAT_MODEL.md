# Threat Model

LR-PayloadLab is deliberately constrained to bounded, benign, local endpoint-telemetry experiments. Its most important property is not feature count; it is the **absence of hidden capability**.

## Protected boundaries

The project must preserve all of these:

- no network access;
- no arbitrary command execution;
- no persistence;
- no credential collection;
- no privilege escalation;
- no evasion/anti-analysis behavior;
- no path escape outside the selected workspace.

## Trust boundaries

```text
Manifest JSON (untrusted until validation)
       │
       ▼
 validator / inspector
       │ allowed action set + hard caps
       ▼
 bounded executor
       │
       ├── workspace only
       ├── receipt
       └── rollback plan
```

## Manifest threats

A manifest may attempt:

- absolute paths;
- `..` traversal;
- unsupported action types;
- oversized marker content;
- excessive sleep/CPU duration;
- too many actions.

Validation must reject these before execution.

## Generated artifact threats

A generated research payload must not become a generic execution wrapper.

The generated artifact is expected to:

- embed only a validated Manifest;
- call the same bounded executor;
- preserve Manifest provenance;
- remain inspectable Python source.

## Provenance threats

Receipts without input identity can be confused across experiments.

Mitigations:

- canonical Manifest SHA-256;
- artifact SHA-256;
- inspection report before execution;
- versioned receipt schema.

## Non-goals

This project intentionally does not implement:

- shell command actions;
- sockets or callbacks;
- binary mutation;
- loader behavior;
- process injection;
- credential access;
- stealth/evasion.

A proposal requiring one of these belongs outside LR-PayloadLab.

## Review invariants

Before merging a new action type:

1. Can it be expressed without arbitrary command execution?
2. Can all filesystem effects be constrained to the workspace?
3. Is there a hard resource cap?
4. Can its effects be represented in a receipt?
5. Can it be rolled back or explicitly declared non-reversible?
6. Does `inspect` expose its capability before execution?
