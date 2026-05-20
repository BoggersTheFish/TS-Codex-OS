# Release Notes

## v0.1.0

TS-Codex-OS v0.1.0 is the first local-first project substrate release for Codex-driven development under the Thinking System workflow.

Release scope:

- File-based project ingestion.
- Serializable project graph with nodes and edges.
- Heuristic tension ledger.
- Practical next-action planner.
- JSON/JSONL memory helpers.
- Release and verification receipts.
- Verification command suggestions.
- CLI commands for status, ingest, plan, and receipt generation.
- Prompt templates for TS-guided Codex runs.

This release does not replace Codex. It does not add an agent loop, web API, database, model trainer, or external dependency. It is a standard-library local project graph, tension ledger, planner, memory, verifier, and receipt system.

Verification for v0.1.0:

```bash
python3 -m unittest discover
python3 scripts/demo_ts_codex_os.py
python3 -m ts_codex_os.cli status --project-path .
python3 -c "from ts_codex_os.cli import main; print(callable(main))"
```

Known limits:

- Ingestion is file-based and heuristic.
- Tension scoring is conservative and pattern-based.
- Verification commands are suggested, not executed by library code.
- Memory is plain JSON/JSONL, not a database.

