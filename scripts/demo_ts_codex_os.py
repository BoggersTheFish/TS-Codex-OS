#!/usr/bin/env python3
"""Small TS-Codex-OS demo that writes sample artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ts_codex_os.cli import render_actions, render_status
from ts_codex_os.graph import add_edge, add_node, create_project_graph
from ts_codex_os.planner import propose_next_actions
from ts_codex_os.receipts import create_receipt, write_receipt
from ts_codex_os.types import TSEdge, TSNode, TSTension


def main() -> int:
    artifacts = ROOT / "artifacts"
    artifacts.mkdir(exist_ok=True)
    graph = create_project_graph("demo-ts-project")
    add_node(graph, TSNode("repo", "repo", "demo-ts-project", "observed", 0.7, {}))
    add_node(graph, TSNode("docs:readme", "docs", "README.md", "observed", 0.8, {"path": "README.md"}))
    add_edge(graph, TSEdge("repo", "docs:readme", "contains", 1.0, {}))
    graph.tensions.append(
        TSTension(
            tension_id="tension:demo:missing_tests",
            node_id="repo",
            kind="missing_tests",
            severity=0.75,
            description="Demo project has no tests yet.",
            evidence=["tests/ not found"],
            suggested_relaxation="Add focused unittest coverage.",
        )
    )
    actions = propose_next_actions(graph)
    receipt = create_receipt(
        "demo-ts-project",
        "Add focused unittest coverage",
        changed_files=["tests/test_demo.py"],
        verification_commands=["python3 -m unittest discover"],
        verification_result="demo receipt; not run",
        remaining_tensions=[tension.kind for tension in graph.tensions],
        next_actions=[action.title for action in actions[:3]],
    )
    (artifacts / "ts_status.md").write_text(render_status(graph, ["python3 -m unittest discover"]), encoding="utf-8")
    (artifacts / "next_actions.md").write_text(render_actions(actions), encoding="utf-8")
    write_receipt(receipt, artifacts / "release_receipt.json")
    print("TS-Codex-OS demo")
    print(f"Project: {graph.project_name}")
    print(f"Tensions: {len(graph.tensions)}")
    print(f"Top action: {actions[0].title if actions else 'none'}")
    print("Wrote artifacts/ts_status.md, artifacts/next_actions.md, artifacts/release_receipt.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

