"""Small serializable project graph helpers."""

from __future__ import annotations

from collections import Counter
from typing import Optional

from .types import TSEdge, TSNode, TSProjectGraph


def create_project_graph(project_name: str) -> TSProjectGraph:
    return TSProjectGraph(
        project_name=project_name,
        metadata={"schema": "ts-codex-os.project_graph.v0", "version": "0.1.0"},
    )


def add_node(graph: TSProjectGraph, node: TSNode) -> TSProjectGraph:
    existing = {item.node_id: index for index, item in enumerate(graph.nodes)}
    if node.node_id in existing:
        graph.nodes[existing[node.node_id]] = node
    else:
        graph.nodes.append(node)
    return graph


def add_edge(graph: TSProjectGraph, edge: TSEdge) -> TSProjectGraph:
    key = (edge.source, edge.target, edge.kind)
    existing = {(item.source, item.target, item.kind) for item in graph.edges}
    if key not in existing:
        graph.edges.append(edge)
    return graph


def find_node(graph: TSProjectGraph, node_id: str) -> Optional[TSNode]:
    return next((node for node in graph.nodes if node.node_id == node_id), None)


def summarize_graph(graph: TSProjectGraph) -> dict:
    node_kinds = Counter(node.kind for node in graph.nodes)
    edge_kinds = Counter(edge.kind for edge in graph.edges)
    tension_kinds = Counter(tension.kind for tension in graph.tensions)
    mean_stability = 0.0
    if graph.nodes:
        mean_stability = round(sum(node.stability for node in graph.nodes) / len(graph.nodes), 4)
    total_tension = round(sum(tension.severity for tension in graph.tensions), 4)
    return {
        "project_name": graph.project_name,
        "node_count": len(graph.nodes),
        "edge_count": len(graph.edges),
        "tension_count": len(graph.tensions),
        "node_kinds": dict(sorted(node_kinds.items())),
        "edge_kinds": dict(sorted(edge_kinds.items())),
        "tension_kinds": dict(sorted(tension_kinds.items())),
        "mean_stability": mean_stability,
        "total_tension": total_tension,
    }

