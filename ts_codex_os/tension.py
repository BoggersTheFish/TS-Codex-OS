"""Heuristic project tension scoring."""

from __future__ import annotations

import re

from .types import TSProjectGraph, TSTension


OVERCLAIM_PHRASES = [
    "proves general reasoning",
    "solves reasoning",
    "agi",
    "guaranteed",
    "fully autonomous",
    "beats all",
    "consciousness",
    "universal truth",
]


def score_project_tension(graph: TSProjectGraph) -> TSProjectGraph:
    graph.tensions = []
    important = graph.metadata.get("important_files", {})
    texts = graph.metadata.get("text_index", {})
    claim_texts = [
        text
        for path, text in texts.items()
        if path == "README.md"
        or path == "RELEASE_NOTES.md"
        or path.startswith("docs/")
        or path.startswith("prompts/")
    ]
    combined = "\n".join(claim_texts).lower()

    def add(kind: str, severity: float, description: str, evidence: list[str], relaxation: str, node_id: str = "repo") -> None:
        graph.tensions.append(
            TSTension(
                tension_id=f"tension:{len(graph.tensions) + 1}:{kind}",
                node_id=node_id,
                kind=kind,
                severity=severity,
                description=description,
                evidence=evidence,
                suggested_relaxation=relaxation,
            )
        )

    if not important.get("readme"):
        add("missing_readme", 0.8, "Project has no README.md.", ["README.md not found"], "Add a sober project README.")
    if not important.get("license"):
        add("missing_license", 0.5, "Project has no explicit LICENSE file.", ["LICENSE not found"], "Add an explicit license file.")
    if not important.get("tests"):
        add("missing_tests", 0.75, "Project has no tests directory.", ["tests/ not found"], "Add focused unittest coverage.")
    if not important.get("release_notes"):
        add("missing_release_notes", 0.45, "Project has no RELEASE_NOTES.md.", ["RELEASE_NOTES.md not found"], "Add release notes before public tags.")
    if not important.get("docs") and any(node.kind == "package" for node in graph.nodes):
        add("missing_docs", 0.35, "Code exists without docs directory.", ["docs/ not found"], "Add docs for project workflow and contracts.")
    if important.get("artifacts") and not important.get("release_receipt"):
        add("stale_artifacts", 0.3, "Artifacts exist without an explicit release receipt.", ["artifacts/ present"], "Write a release receipt for generated artifacts.", "artifacts")
    if important.get("release_notes") and not important.get("release_receipt"):
        add("unverified_release", 0.55, "Release notes exist without a release receipt.", ["RELEASE_NOTES.md present"], "Add verification commands and a release receipt.", "release:notes")
    if not important.get("trace_contract") and "trace" not in combined:
        add("no_trace_contract", 0.35, "Project does not describe a trace or output contract.", ["no trace wording found"], "Document the public output or trace contract.")
    if "roadmap" not in combined and "next" not in combined:
        add("missing_next_step", 0.25, "Project does not state a next step or roadmap.", ["no roadmap/next wording found"], "Add a narrow next-step section.")
    if _has_smoke_metric_without_caveat(combined):
        add("no_caveat_for_smoke_metrics", 0.65, "Smoke-test metrics appear without an explicit caveat.", ["metric-like 1.0 found"], "Add caveat that toy/smoke metrics are not robust benchmark claims.")
    for phrase in OVERCLAIM_PHRASES:
        if _contains_phrase(combined, phrase):
            add(
                "overclaiming_language",
                0.7,
                f"Potential overclaiming phrase detected: {phrase}",
                [phrase],
                "Rewrite as a bounded, source-backed claim or add caveat.",
            )
    if _has_broad_scope_overclaim(combined):
        add("too_broad_scope", 0.45, "Scope language may be broader than v0 substrate claims.", ["broad scope wording"], "Narrow the release claim to local graph/tension/receipt substrate.")

    _update_node_stability(graph)
    return graph


def _contains_phrase(text: str, phrase: str) -> bool:
    pattern = r"\b" + re.escape(phrase).replace(r"\ ", r"\s+") + r"\b"
    return re.search(pattern, text) is not None


def _has_smoke_metric_without_caveat(text: str) -> bool:
    has_metric = "1.0000" in text or " 1.0" in text or ": 1.0" in text
    has_learned = "learned" in text
    has_caveat = "caveat" in text or "smoke test" in text or "toy" in text or "not benchmark" in text
    return has_metric and has_learned and not has_caveat


def _has_broad_scope_overclaim(text: str) -> bool:
    if "replace codex" in text and "not a replacement for codex" not in text:
        return True
    if "full llm" in text and "not a full llm" not in text and "not full llm" not in text:
        return True
    return False


def _update_node_stability(graph: TSProjectGraph) -> None:
    if not graph.tensions:
        return
    pressure = {}
    for tension in graph.tensions:
        pressure[tension.node_id] = pressure.get(tension.node_id, 0.0) + tension.severity
    updated = []
    for node in graph.nodes:
        p = pressure.get(node.node_id, 0.0)
        updated.append(
            type(node)(
                node_id=node.node_id,
                kind=node.kind,
                title=node.title,
                status=node.status,
                stability=round(max(0.0, node.stability - min(0.5, p / 4)), 4),
                metadata=node.metadata,
            )
        )
    graph.nodes = updated
