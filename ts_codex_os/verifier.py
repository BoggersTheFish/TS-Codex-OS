"""Verification command suggestions.

This module only suggests commands. It does not execute them.
"""

from __future__ import annotations

from pathlib import Path


def suggest_verification_commands(project_path: str) -> list[str]:
    root = Path(project_path)
    commands = []
    if (root / "tests").exists():
        commands.append("python3 -m unittest discover")
    if (root / "pyproject.toml").exists():
        commands.append("python3 -m pip install -e .")
    for script in sorted((root / "scripts").glob("demo*.py")) if (root / "scripts").exists() else []:
        commands.append(f"python3 {script.relative_to(root)}")
    for script in sorted((root / "scripts").glob("train*.py")) if (root / "scripts").exists() else []:
        commands.append(f"# optional/explicit: python3 {script.relative_to(root)}")
    return commands

