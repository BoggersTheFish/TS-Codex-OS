#!/usr/bin/env python3
"""Ingest a project into a TS-Codex-OS project graph."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ts_codex_os.ingest import ingest_repo
from ts_codex_os.memory import write_graph
from ts_codex_os.tension import score_project_tension


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest a project into TS-Codex-OS graph JSON.")
    parser.add_argument("--project-path", default=".")
    parser.add_argument("--out", default="artifacts/project_graph.json")
    args = parser.parse_args()
    graph = score_project_tension(ingest_repo(args.project_path))
    write_graph(args.out, graph)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

