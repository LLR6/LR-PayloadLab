# Engineering Decisions

## D1 — Capability allowlist

Only explicitly implemented benign actions are accepted. Unknown action types fail validation.

## D2 — Static inspection before execution

A Manifest can be summarized without running it, including paths, action types, declared active time and capabilities.

## D3 — Workspace confinement

Path-based actions resolve beneath a caller-provided workspace and reject traversal outside it.

## D4 — Receipts bind to the Manifest

Canonical Manifest SHA-256 links a run receipt or build result back to the exact experiment definition.

## D5 — Safety boundaries are testable

CI includes a rejected network-action fixture so out-of-scope capabilities cannot silently become accepted.
