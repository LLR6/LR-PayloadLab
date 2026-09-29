# Known Failure Modes

- Manifest references a path outside the workspace.
  - Validation/path containment must reject before write.
- Resource request exceeds caps.
  - Validation rejects the Manifest.
- Receipt exists but does not match the intended Manifest.
  - Compare canonical Manifest SHA-256.
- Rollback target changed after execution.
  - Do not overwrite newer state blindly.
- Generated artifact is confused with another experiment.
  - Verify artifact SHA and Manifest SHA together.
- A proposed action requires capabilities outside the project boundary.
  - Reject the action type rather than weakening containment.
