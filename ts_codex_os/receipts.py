"""Release/action receipt helpers."""

from __future__ import annotations

import json
from pathlib import Path

from .types import TSReceipt, to_jsonable


def create_receipt(
    project_name,
    action_title,
    changed_files,
    verification_commands,
    verification_result,
    remaining_tensions,
    next_actions,
) -> TSReceipt:
    safe_id = f"receipt:{project_name}:{action_title}".lower().replace(" ", "_")
    return TSReceipt(
        receipt_id=safe_id,
        project_name=project_name,
        action_title=action_title,
        changed_files=list(changed_files),
        verification_commands=list(verification_commands),
        verification_result=verification_result,
        remaining_tensions=list(remaining_tensions),
        next_actions=list(next_actions),
    )


def write_receipt(receipt: TSReceipt, path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(to_jsonable(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target

