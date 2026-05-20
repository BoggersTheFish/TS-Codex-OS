"""File-based project ingestion for TS-Codex-OS."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .graph import add_edge, add_node, create_project_graph
from .types import TSEdge, TSNode, TSProjectGraph


IGNORE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".pytest_cache", "htmlcov"}
TEXT_SUFFIXES = {".md", ".txt", ".rst", ".toml", ".json", ".py"}
MAX_TEXT_BYTES = 200_000
MAX_ARTIFACT_BYTES = 1_000_000


def ingest_repo(path: str) -> TSProjectGraph:
    root = Path(path).resolve()
    graph = create_project_graph(root.name)
    files = list(_scan_files(root))
    rels = [str(file.relative_to(root)) for file in files]
    text_index = _read_text_index(root, files)
    graph.metadata.update(
        {
            "root_path": str(root),
            "file_count": len(files),
            "files": rels,
            "important_files": _important_files(rels),
            "text_index": text_index,
        }
    )

    add_node(
        graph,
        TSNode(
            node_id="repo",
            kind="repo",
            title=root.name,
            status="observed",
            stability=0.7,
            metadata={"path": str(root), "file_count": len(files)},
        ),
    )
    _add_surface_nodes(graph, root, rels)
    _add_package_nodes(graph, root, files)
    return graph


def _scan_files(root: Path) -> Iterable[Path]:
    for file in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in file.relative_to(root).parts):
            continue
        if not file.is_file():
            continue
        if "artifacts" in file.relative_to(root).parts and file.stat().st_size > MAX_ARTIFACT_BYTES:
            continue
        yield file


def _read_text_index(root: Path, files: Iterable[Path]) -> dict:
    text_index = {}
    for file in files:
        rel = str(file.relative_to(root))
        if file.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if file.stat().st_size > MAX_TEXT_BYTES:
            continue
        try:
            text_index[rel] = file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
    return text_index


def _important_files(rels: list[str]) -> dict:
    rel_set = set(rels)
    return {
        "readme": "README.md" in rel_set,
        "release_notes": "RELEASE_NOTES.md" in rel_set,
        "pyproject": "pyproject.toml" in rel_set,
        "requirements": "requirements.txt" in rel_set,
        "license": "LICENSE" in rel_set,
        "tests": any(rel.startswith("tests/") for rel in rels),
        "docs": any(rel.startswith("docs/") for rel in rels),
        "scripts": any(rel.startswith("scripts/") for rel in rels),
        "artifacts": any(rel.startswith("artifacts/") for rel in rels),
        "release_receipt": any(rel.endswith("release_receipt.json") for rel in rels),
        "trace_contract": any("trace" in rel.lower() for rel in rels),
    }


def _add_surface_nodes(graph: TSProjectGraph, root: Path, rels: list[str]) -> None:
    important = graph.metadata["important_files"]
    if important["readme"]:
        _node_and_contains(graph, "docs:readme", "docs", "README.md", "README.md")
    if important["release_notes"]:
        _node_and_contains(graph, "release:notes", "release", "Release notes", "RELEASE_NOTES.md")
    if important["license"]:
        _node_and_contains(graph, "license", "license", "LICENSE", "LICENSE")
    for name in ("tests", "docs", "scripts", "artifacts"):
        if important[name]:
            _node_and_contains(graph, name, name, name, name)
    if important["artifacts"] and important["release_notes"]:
        add_edge(graph, TSEdge("artifacts", "release:notes", "supports", 0.7, {}))
    if important["tests"]:
        for node in ["repo"]:
            add_edge(graph, TSEdge("tests", node, "verifies", 0.8, {}))
    if important["docs"]:
        add_edge(graph, TSEdge("docs", "repo", "explains", 0.7, {}))


def _node_and_contains(graph: TSProjectGraph, node_id: str, kind: str, title: str, path: str) -> None:
    add_node(
        graph,
        TSNode(node_id=node_id, kind=kind, title=title, status="observed", stability=0.75, metadata={"path": path}),
    )
    add_edge(graph, TSEdge("repo", node_id, "contains", 1.0, {}))


def _add_package_nodes(graph: TSProjectGraph, root: Path, files: list[Path]) -> None:
    package_dirs = sorted(
        {
            str(file.parent.relative_to(root))
            for file in files
            if file.suffix == ".py"
            and "__init__.py" in {child.name for child in file.parent.glob("__init__.py")}
            and not str(file.relative_to(root)).startswith(("tests/", "scripts/"))
        }
    )
    for package in package_dirs:
        node_id = f"package:{package.replace('/', '.')}"
        add_node(
            graph,
            TSNode(
                node_id=node_id,
                kind="package",
                title=package,
                status="observed",
                stability=0.72,
                metadata={"path": package},
            ),
        )
        add_edge(graph, TSEdge("repo", node_id, "contains", 1.0, {}))
        if any(edge.source == "tests" for edge in graph.edges):
            add_edge(graph, TSEdge("tests", node_id, "verifies", 0.8, {}))
        if any(edge.source == "docs" for edge in graph.edges):
            add_edge(graph, TSEdge("docs", node_id, "explains", 0.5, {}))

