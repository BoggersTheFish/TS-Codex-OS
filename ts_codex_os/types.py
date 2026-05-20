"""Shared dataclasses for TS-Codex-OS."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Dict, List


def to_jsonable(value: Any) -> Any:
    """Convert dataclasses, lists, and dicts into JSON-safe values."""
    if is_dataclass(value):
        return {key: to_jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    return value


@dataclass(frozen=True)
class TSNode:
    node_id: str
    kind: str
    title: str
    status: str
    stability: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TSEdge:
    source: str
    target: str
    kind: str
    weight: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TSTension:
    tension_id: str
    node_id: str
    kind: str
    severity: float
    description: str
    evidence: List[str] = field(default_factory=list)
    suggested_relaxation: str = ""


@dataclass
class TSProjectGraph:
    project_name: str
    nodes: List[TSNode] = field(default_factory=list)
    edges: List[TSEdge] = field(default_factory=list)
    tensions: List[TSTension] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TSAction:
    action_id: str
    title: str
    target_node_id: str
    expected_tension_delta: float
    effort: float
    risk: float
    rationale: str
    verification: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class TSReceipt:
    receipt_id: str
    project_name: str
    action_title: str
    changed_files: List[str]
    verification_commands: List[str]
    verification_result: str
    remaining_tensions: List[str]
    next_actions: List[str]

