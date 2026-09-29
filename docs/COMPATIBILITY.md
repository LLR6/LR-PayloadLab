# Compatibility

## Runtime

- Python: **3.10+**
- CI target: **3.10 / 3.11 / 3.12**
- CLI: `payload-lab`

## Schemas

- Manifest: `lr-payload-lab/v1`
- Receipt: `lr-payload-receipt/v2`
- Inspection: `lr-payload-inspection/v1`

## Policy

Manifest semantics and capability boundaries are compatibility-sensitive.
A new action type requires a documented schema/behavior update and safety review.

Receipt fields may be extended, but existing hash semantics must not change silently.
