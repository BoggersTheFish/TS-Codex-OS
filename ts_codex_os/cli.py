"""Command-line interface for TS-Codex-OS."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .graph import summarize_graph
from .ingest import ingest_repo
from .memory import write_graph
from .planner import propose_next_actions
from .receipts import create_receipt, write_receipt
from .tension import score_project_tension
from .types import TSAction, TSProjectGraph, to_jsonable
from .verifier import suggest_verification_commands


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="TS-Codex-OS local project graph and tension CLI.")
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="Ingest, score, plan, and write status artifacts.")
    status.add_argument("--project-path", default=".")

    ingest = sub.add_parser("ingest", help="Ingest a project and write graph JSON.")
    ingest.add_argument("--project-path", default=".")
    ingest.add_argument("--out", default="artifacts/project_graph.json")

    plan = sub.add_parser("plan", help="Write next actions markdown.")
    plan.add_argument("--project-path", default=".")
    plan.add_argument("--out", default="artifacts/next_actions.md")

    receipt = sub.add_parser("receipt", help="Create a deterministic receipt JSON.")
    receipt.add_argument("--project-name", required=True)
    receipt.add_argument("--action-title", required=True)
    receipt.add_argument("--out", default="artifacts/release_receipt.json")

    args = parser.parse_args(argv)
    if args.command == "status":
        return _status(args.project_path)
    if args.command == "ingest":
        graph = score_project_tension(ingest_repo(args.project_path))
        write_graph(args.out, graph)
        print(f"Wrote {args.out}")
        return 0
    if args.command == "plan":
        graph = score_project_tension(ingest_repo(args.project_path))
        actions = propose_next_actions(graph)
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(render_actions(actions), encoding="utf-8")
        print(f"Wrote {args.out}")
        return 0
    if args.command == "receipt":
        receipt_obj = create_receipt(
            args.project_name,
            args.action_title,
            changed_files=[],
            verification_commands=[],
            verification_result="not run",
            remaining_tensions=[],
            next_actions=[],
        )
        write_receipt(receipt_obj, args.out)
        print(f"Wrote {args.out}")
        return 0
    return 2


def _status(project_path: str) -> int:
    root = Path(project_path).resolve()
    artifacts = root / "artifacts"
    artifacts.mkdir(exist_ok=True)
    graph = score_project_tension(ingest_repo(str(root)))
    actions = propose_next_actions(graph)
    commands = suggest_verification_commands(str(root))
    write_graph(artifacts / "project_graph.json", graph)
    (artifacts / "ts_status.md").write_text(render_status(graph, commands), encoding="utf-8")
    (artifacts / "next_actions.md").write_text(render_actions(actions), encoding="utf-8")
    print(f"Project: {graph.project_name}")
    print(f"Tensions: {len(graph.tensions)}")
    print(f"Next actions: {len(actions)}")
    print(f"Wrote {artifacts / 'ts_status.md'}")
    return 0


def render_status(graph: TSProjectGraph, commands: list[str]) -> str:
    summary = summarize_graph(graph)
    lines = [
        "# TS-Codex-OS Status",
        "",
        f"Project: {graph.project_name}",
        "",
        "## Graph Summary",
        "",
        "```json",
        json.dumps(summary, indent=2, sort_keys=True),
        "```",
        "",
        "## Tensions",
        "",
    ]
    if graph.tensions:
        for tension in graph.tensions:
            lines.append(f"- `{tension.kind}` severity `{tension.severity}` on `{tension.node_id}`: {tension.description}")
    else:
        lines.append("- No unresolved tensions detected by v0 heuristics.")
    lines.extend(["", "## Suggested Verification", ""])
    if commands:
        lines.extend(f"- `{command}`" for command in commands)
    else:
        lines.append("- No verification commands detected.")
    lines.append("")
    return "\n".join(lines)


def render_actions(actions: list[TSAction]) -> str:
    lines = ["# TS-Codex-OS Next Actions", ""]
    if not actions:
        lines.append("No next actions proposed by v0 heuristics.")
        return "\n".join(lines) + "\n"
    for action in actions:
        lines.extend(
            [
                f"## {action.title}",
                "",
                f"- action_id: `{action.action_id}`",
                f"- target_node_id: `{action.target_node_id}`",
                f"- expected_tension_delta: `{action.expected_tension_delta}`",
                f"- effort: `{action.effort}`",
                f"- risk: `{action.risk}`",
                f"- rationale: {action.rationale}",
                "- verification:",
            ]
        )
        lines.extend(f"  - `{command}`" for command in action.verification)
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())

