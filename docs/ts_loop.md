# TS Loop In This Repo

TS-Codex-OS uses the Thinking System loop as an engineering control loop:

```text
Propagate -> Relax -> Break -> Evolve
```

The loop is implemented as local project inspection, graph update, tension scoring, next-action planning, receipts, and memory.

## Propagate

Propagate means inspect the current project state before editing.

In this repo, propagation includes:

- scanning files with `ingest_repo`
- detecting docs, tests, scripts, artifacts, packages, and release notes
- reading lightweight text surfaces such as README and docs
- building a `TSProjectGraph`
- preserving observed evidence in graph metadata

The goal is to make the current project state visible before choosing an action.

## Relax

Relax means make the smallest change that reduces unresolved tension.

Examples:

- add missing tests
- add release notes
- add a caveat around smoke-test metrics
- write a release receipt
- document a trace contract
- add a focused docs page instead of a broad rewrite

The planner ranks actions by expected tension reduction against effort and risk. It should bias toward small, verifiable changes.

## Break

Break means split a confused or overloaded node when it is carrying incompatible demands.

Examples:

- split release notes from README
- split architecture docs from workflow docs
- split receipts from generated artifacts
- split learned-component claims from benchmark claims
- split "candidate proposal" from "reasoning generation"

Breaking is not destruction. It is a way to reduce hidden coupling.

## Evolve

Evolve means update the structure so future work is more stable.

In TS-Codex-OS, evolution means:

- write receipts after verification
- update memory JSONL files
- regenerate `artifacts/project_graph.json`
- keep `artifacts/ts_status.md` current
- keep release wording sober
- preserve public contracts across internal changes

The desired attractor is a project state where claims, tests, artifacts, and release notes all point to the same stable story.

