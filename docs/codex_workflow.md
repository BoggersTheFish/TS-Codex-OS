# Codex Workflow With TS-Codex-OS

TS-Codex-OS is designed to guide Codex work without replacing Codex.

Codex remains the executor. TS-Codex-OS provides project state, tension, memory, verification suggestions, and receipts.

## Before Editing

For a future Codex run, start with:

1. Read `README.md`.
2. Read `prompts/CODEX_SYSTEM_PROMPT.md`.
3. Read `artifacts/ts_status.md` if present.
4. Read `artifacts/project_graph.json` if present.
5. Identify the target node.
6. Identify the active tension.
7. Choose the smallest useful relaxation.

## During Editing

Codex should:

- keep edits scoped to the target tension
- preserve public trace contracts
- avoid unrelated rewrites
- update docs when public behavior changes
- add receipts when release or verification claims change
- avoid overclaiming
- keep learned-component language caveated unless stronger eval exists

## After Editing

Codex should run or report verification:

```bash
python3 -m unittest discover
python3 scripts/demo_ts_codex_os.py
python3 -m ts_codex_os.cli status --project-path .
```

The exact commands depend on the repo. `ts_codex_os.verifier.suggest_verification_commands` can suggest commands, but it does not execute them.

## Handoff Artifacts

The normal handoff artifacts are:

- `artifacts/ts_status.md`
- `artifacts/project_graph.json`
- `artifacts/next_actions.md`
- `artifacts/release_receipt.json`

These files let Codex and humans resume work from the same graph state.

## TS-Reasoner Example

For TS-Reasoner-v0, the current framing is:

```text
v0.1.0 = deterministic trace contract
v0.2.0 = learned tension-ranker experiment
v0.3.0 = learned candidate-proposal branch
```

Codex should not break that public ladder without an explicitly versioned breaking release.

