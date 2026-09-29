# Migration Policy

PayloadLab versioned data currently includes:

- Manifest: `lr-payload-lab/v1`
- Receipt: `lr-payload-receipt/v2`
- Inspection: `lr-payload-inspection/v1`

## Rules

1. Existing action semantics must not change silently.
2. New action types require explicit schema documentation.
3. Existing Manifest hashes must continue to identify the same canonical content.
4. Receipt hash fields must not be repurposed.
5. Old receipts should remain readable after additive report changes.
6. If a Manifest version changes, validation must reject unsupported versions before execution.

## Safety requirement

Migration code must not expand project capabilities. Data-format upgrades are not a reason to introduce networking, arbitrary commands, persistence or evasion behavior.
