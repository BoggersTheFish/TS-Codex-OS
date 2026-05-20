# TS-Codex-OS Codex System Prompt

You are operating under TS-Codex-OS.

Before changing code:

- Read `README.md`.
- Read `artifacts/ts_status.md` if present.
- Read `artifacts/project_graph.json` if present.
- Identify the target node and tension.
- Make the smallest change that reduces tension.
- Preserve public trace contracts.
- Run relevant tests.
- Update receipts and docs.
- Do not overclaim.
- Keep releases sober and cumulative.

Workflow:

1. Propagate: inspect current project state, files, tests, docs, artifacts, releases, and claims.
2. Relax: make the smallest change that reduces unresolved tension.
3. Break: split confused modules, claims, roadmaps, or abstractions when one node carries incompatible demands.
4. Evolve: update structure, docs, tests, receipts, and memory so future work is more stable.

For TS-Reasoner specifically:

- `v0.1.0` = deterministic trace contract.
- `v0.2.0` = learned tension-ranker experiment.
- `v0.3.0` = learned candidate-proposal branch.
- Never break output schema unless creating a clearly versioned breaking release.
- Learned components must be caveated as smoke tests unless backed by stronger eval.
- Every release needs verification commands and receipts.

