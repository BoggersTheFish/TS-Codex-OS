"""Plain JSON/JSONL memory helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .types import TSProjectGraph, to_jsonable


MEMORY_FILES = [
    "project_events.jsonl",
    "decisions.jsonl",
    "experiments.jsonl",
    "releases.jsonl",
    "tensions.jsonl",
]


def append_event(path, event) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(to_jsonable(event), sort_keys=True) + "\n")
    return target


def read_events(path) -> list[dict]:
    target = Path(path)
    if not target.exists():
        return []
    events = []
    for line in target.read_text(encoding="utf-8").splitlines():
        if line.strip():
            events.append(json.loads(line))
    return events


def write_graph(path, graph: TSProjectGraph) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(to_jsonable(graph), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def read_graph(path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def ensure_memory_dir(path) -> Path:
    root = Path(path)
    root.mkdir(parents=True, exist_ok=True)
    for name in MEMORY_FILES:
        (root / name).touch(exist_ok=True)
    return root

