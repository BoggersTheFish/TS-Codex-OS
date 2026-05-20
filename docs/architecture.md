# TS-Codex-OS Architecture

TS-Codex-OS is a local-first project substrate for Codex-driven development. It is intentionally small: no agent loop, no web API, no database, and no runtime dependencies outside the Python standard library.

The architecture is built around a simple flow:

```text
project files -> graph -> tension ledger -> planner -> verification suggestions -> receipts -> memory
```

## Graph

The graph is defined in `ts_codex_os/types.py` and managed by `ts_codex_os/graph.py`.

Core graph objects:

- `TSNode`: a stable holder of project state, such as repo, docs, tests, scripts, package modules, artifacts, or release notes.
- `TSEdge`: a relationship between nodes, such as repo contains package, tests verify module, docs explain repo, or artifacts support release.
- `TSProjectGraph`: a serializable project graph with nodes, edges, tensions, and metadata.

The graph is not a database. It is a plain dataclass structure that can be written as JSON for humans and Codex to inspect.

## Ingest

`ts_codex_os/ingest.py` scans a local project path and builds the first graph state.

It detects:

- `README.md`
- `RELEASE_NOTES.md`
- `pyproject.toml`
- `requirements.txt`
- `LICENSE`
- `tests/`
- `docs/`
- `scripts/`
- `artifacts/`
- Python packages with `__init__.py`

It ignores noisy or large local state such as `.git`, `__pycache__`, `.venv`, `node_modules`, and oversized artifacts.

## Tension

`ts_codex_os/tension.py` adds unresolved project pressure to the graph as `TSTension` records.

Examples:

- missing README
- missing license
- missing tests
- missing release notes
- missing docs
- stale artifacts
- unverified release
- overclaiming language
- missing trace contract
- missing caveat for smoke metrics
- missing next step
- too broad scope

Tension detection is heuristic. It flags possible risks; it does not rewrite files or delete claims.

## Planner

`ts_codex_os/planner.py` converts unresolved tensions into practical `TSAction` records.

Actions are ranked by:

```text
expected_tension_delta / max(effort + risk, epsilon)
```

The planner tries to propose the smallest useful next action Codex can execute, such as adding tests, writing a release receipt, adding caveats, documenting a trace contract, or adding missing docs.

## Memory

`ts_codex_os/memory.py` provides plain JSON/JSONL helpers.

Expected memory files:

- `ts_memory/project_events.jsonl`
- `ts_memory/decisions.jsonl`
- `ts_memory/experiments.jsonl`
- `ts_memory/releases.jsonl`
- `ts_memory/tensions.jsonl`

The memory layer is intentionally inspectable. It does not require a database or background service.

## Receipts

`ts_codex_os/receipts.py` creates deterministic `TSReceipt` JSON.

Receipts record:

- project name
- action title
- changed files
- verification commands
- verification result
- remaining tensions
- next actions

Receipts are meant to make release and verification claims auditable.

## Verifier

`ts_codex_os/verifier.py` suggests verification commands based on local files.

Examples:

- `python3 -m unittest discover` when `tests/` exists.
- `python3 -m pip install -e .` when `pyproject.toml` exists.
- `python3 scripts/demo_*.py` for demo scripts.
- optional comments for training scripts, because training may be expensive.

The verifier does not execute commands. CLI and library code only suggest verification by default.

## CLI

`ts_codex_os/cli.py` exposes:

```bash
python3 -m ts_codex_os.cli status --project-path .
python3 -m ts_codex_os.cli ingest --project-path . --out artifacts/project_graph.json
python3 -m ts_codex_os.cli plan --project-path . --out artifacts/next_actions.md
python3 -m ts_codex_os.cli receipt --project-name NAME --action-title TITLE --out artifacts/release_receipt.json
```

The `status` command writes:

- `artifacts/ts_status.md`
- `artifacts/project_graph.json`
- `artifacts/next_actions.md`

These artifacts are the normal handoff files for future Codex runs.

