"""Next-action planner for reducing project tension."""

from __future__ import annotations

from .types import TSAction, TSProjectGraph


ACTION_BY_TENSION = {
    "missing_readme": ("Add README.md", 0.8, 0.5, 0.1, ["Review README.md"]),
    "missing_license": ("Add LICENSE", 0.5, 0.2, 0.05, ["Confirm license text"]),
    "missing_tests": ("Add focused unittest coverage", 0.75, 0.8, 0.2, ["python3 -m unittest discover"]),
    "missing_release_notes": ("Add release notes", 0.45, 0.4, 0.1, ["Review RELEASE_NOTES.md"]),
    "missing_docs": ("Add project docs", 0.35, 0.6, 0.1, ["Review docs/"]),
    "stale_artifacts": ("Write artifact receipt", 0.3, 0.3, 0.05, ["Review artifacts/release_receipt.json"]),
    "unverified_release": ("Add release receipt with verification", 0.55, 0.4, 0.1, ["python3 -m unittest discover"]),
    "overclaiming_language": ("Add caveat or narrow overclaiming language", 0.7, 0.4, 0.2, ["Review README.md and docs/"]),
    "no_trace_contract": ("Document trace contract", 0.35, 0.5, 0.1, ["Review docs/trace preview"]),
    "no_caveat_for_smoke_metrics": ("Add smoke-test caveat", 0.65, 0.25, 0.05, ["Review release notes"]),
    "missing_next_step": ("Add narrow next-step section", 0.25, 0.25, 0.05, ["Review roadmap wording"]),
    "too_broad_scope": ("Narrow scope statement", 0.45, 0.3, 0.1, ["Review public claims"]),
}


def propose_next_actions(graph: TSProjectGraph, limit: int = 5) -> list[TSAction]:
    actions = []
    seen = set()
    for tension in sorted(graph.tensions, key=lambda item: item.severity, reverse=True):
        if tension.kind in seen:
            continue
        title, delta, effort, risk, verification = ACTION_BY_TENSION.get(
            tension.kind,
            ("Relax unresolved project tension", tension.severity, 0.5, 0.2, ["Review changed files"]),
        )
        seen.add(tension.kind)
        actions.append(
            TSAction(
                action_id=f"action:{len(actions) + 1}:{tension.kind}",
                title=title,
                target_node_id=tension.node_id,
                expected_tension_delta=delta,
                effort=effort,
                risk=risk,
                rationale=tension.suggested_relaxation or tension.description,
                verification=verification,
            )
        )

    actions.extend(_structural_actions(graph, len(actions)))
    actions = sorted(actions, key=_priority, reverse=True)
    return actions[:limit]


def _structural_actions(graph: TSProjectGraph, offset: int) -> list[TSAction]:
    text = "\n".join(graph.metadata.get("text_index", {}).values()).lower()
    actions = []
    if "trace" in text and "trace_preview" not in text:
        actions.append(
            TSAction(
                f"action:{offset + len(actions) + 1}:trace_preview",
                "Add trace preview artifact",
                "docs:readme",
                0.3,
                0.4,
                0.05,
                "Trace contract exists; a preview makes it inspectable.",
                ["Review docs/trace_preview.md"],
            )
        )
    if "learned" in text and "ablation" not in text:
        actions.append(
            TSAction(
                f"action:{offset + len(actions) + 1}:ablation",
                "Add learned-component ablation",
                "repo",
                0.4,
                0.7,
                0.15,
                "Learned components need comparison against baselines.",
                ["Run comparison script", "Review artifacts"],
            )
        )
    if "learned" in text and "fallback" not in text:
        actions.append(
            TSAction(
                f"action:{offset + len(actions) + 1}:fallback",
                "Add safety fallback for learned component",
                "repo",
                0.45,
                0.6,
                0.2,
                "Learned generator/ranker should not remove critical verification paths.",
                ["python3 -m unittest discover"],
            )
        )
    return actions


def _priority(action: TSAction) -> float:
    return action.expected_tension_delta / max(action.effort + action.risk, 1e-6)

