# Receipts

Receipts are the audit trail for TS-Codex-OS.

They make engineering and release claims inspectable by recording what changed, how it was verified, what tension remains, and what should happen next.

## Receipt Shape

`TSReceipt` includes:

- `receipt_id`
- `project_name`
- `action_title`
- `changed_files`
- `verification_commands`
- `verification_result`
- `remaining_tensions`
- `next_actions`

Receipts are written as deterministic, readable JSON.

## Release Receipts

A release receipt should be written when a repo is tagged, published, or prepared for public release.

It should include:

- files changed for the release
- tests and scripts run
- release note updates
- artifact regeneration
- remaining tensions
- next branch or next version

## Verification Receipts

A verification receipt should be written when the important claim is "this was checked."

Examples:

- tests passed
- demo generated expected artifacts
- CLI status regenerated graph and next actions
- packaging import works
- release status no longer reports a specific tension

## What Receipts Do Not Mean

A receipt is not a proof that the software is correct. It is evidence that a specific verification path was run or considered.

For v0.1.0, receipts are simple JSON files. There is no signing, database, or external service.

