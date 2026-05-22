# TS-Codex-OS

**Status:** flagship local-first project-control substrate.

**Role in the TS stack:** TS-Codex-OS turns a repository into a local project graph with a tension ledger, planner, memory, verifier suggestions, and release receipts.

**What this repo is:** a local-first control layer for Codex-driven development: it ingests project files, detects release/control tensions, proposes next actions, writes receipts, and keeps project state inspectable.

**What this repo is not:** not an autonomous coding agent, not a replacement for Codex, not an LLM API caller, and not a production project-management platform.

**Start here:** run the demo, inspect the generated artifacts, then read the release notes and receipts.

TS-Codex-OS is a local-first project graph and tension engine for Codex-driven development.

Codex remains the coding executor. TS-Codex-OS is the local knowledge substrate around it: project graph, tension ledger, release verifier, receipt writer, and persistent memory layer.

```text
Codex = hands
TS-Codex-OS = brain, memory, verifier, project graph, and tension engine
```

TS-Codex-OS does not make Codex conscious, autonomous, or magically correct. It gives Codex a persistent project graph, tension ledger, release receipts, and action planner so each coding step is grounded in inspectable project state.

## What It Is

- A standard-library Python package.
- A file-based project ingester.
- A serializable TS project graph.
- A heuristic tension detector.
- A next-action planner.
- A JSON/JSONL memory layer.
- A receipt writer for releases and engineering actions.
- A prompt bundle for TS-guided Codex runs.

## What It Is Not

- Not a replacement for Codex.
- Not an LLM agent framework.
- Not a web service.
- Not a database-backed memory system.
- Not a model trainer.
- Not a claim that TS makes coding automatically correct.

## Install

Run directly from the repo:

```bash
python3 -m ts_codex_os.cli status --project-path .
```

Optional editable install:

```bash
python3 -m pip install -e .
ts-codex-os status --project-path .
```

## Quickstart

```bash
python3 -m ts_codex_os.cli status --project-path .
python3 -m ts_codex_os.cli ingest --project-path . --out artifacts/project_graph.json
python3 -m ts_codex_os.cli plan --project-path . --out artifacts/next_actions.md
python3 scripts/demo_ts_codex_os.py
python3 -m unittest discover
```

The `status` command writes:

- `artifacts/ts_status.md`
- `artifacts/project_graph.json`
- `artifacts/next_actions.md`

## v0.1.0 Release Scope

v0.1.0 is the first public substrate release. It includes local project ingestion, graph serialization, heuristic tension scoring, next-action planning, JSON/JSONL memory helpers, receipt writing, verification command suggestions, CLI commands, prompts, tests, docs, and sample artifacts.

It does not add an agent loop, web API, database dependency, LLM API call, model training system, or autonomous coding layer.

## Docs

- `docs/architecture.md`: graph, ingest, tension, planner, memory, receipts, verifier, and CLI.
- `docs/ts_loop.md`: how Propagate -> Relax -> Break -> Evolve maps to this repo.
- `docs/codex_workflow.md`: how Codex should use prompts and status artifacts.
- `docs/receipts.md`: release and verification receipt behavior.

## Example Workflow

1. Propagate: ingest files, docs, tests, scripts, artifacts, and release notes.
2. Relax: identify the smallest useful change that reduces tension.
3. Break: split confused claims, missing verification, or broad release scope.
4. Evolve: update docs, tests, receipts, and memory so future work is more stable.

## TS Mapping

- Node: stable holder of project state.
- Edge: relation or constraint between project parts.
- Activation: current task focus.
- Tension: unresolved pressure such as missing tests or overclaiming language.
- Stability: ability of the project to hold claims under verification.
- Coherence: graph state that can be inspected without hiding contradictions.
- Attractor: next stable release or project shape.

## Relation To TS-Reasoner-v0

TS-Codex-OS is designed to supervise repositories like `TS-Reasoner-v0`.

Current public ladder:

```text
TS-Reasoner-v0 v0.1.0 = deterministic trace contract
TS-Reasoner-v0 v0.2.0 = learned tension-ranker experiment
TS-Reasoner-v0 v0.3.0 = learned candidate-proposal branch
```

TS-Codex-OS preserves that kind of release framing by checking for trace contracts, caveats, verification receipts, and overbroad claims.

## Roadmap

- v0.1.0: local graph, tension, planner, memory, receipts, prompts.
- v0.2.0: richer project ingestion and safer release receipt templates.
- v0.3.0: optional git-aware release checks.
- v0.4.0: project-specific rule packs.
- v1.0.0: stable TS-Codex workflow substrate for multiple public repos.

## Caveat

This is a local project-memory and release-control substrate. The heuristics are intentionally simple and inspectable. They should guide Codex work, not replace engineering judgment.
