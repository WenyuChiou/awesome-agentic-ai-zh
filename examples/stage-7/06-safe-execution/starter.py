"""Offline approval, checkpoint, resume, and idempotency example.

The "side effect" is only a JSON ledger entry. No network request is made.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
WAITING = "waiting_for_approval"
COMPLETED = "completed"
CANCELLED = "cancelled"
VALID_STATUSES = {WAITING, COMPLETED, CANCELLED}
KEY_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,100}$")


class StateError(ValueError):
    """Raised when saved state cannot be trusted enough to resume."""


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise StateError(f"cannot read trusted JSON state: {path.name}") from error


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def _validate_action(action: str) -> str:
    if not isinstance(action, str):
        raise StateError("action must be text")
    cleaned = action.strip()
    if not cleaned or len(cleaned) > 200:
        raise StateError("action must contain 1-200 visible characters")
    return cleaned


def _validate_key(idempotency_key: str) -> str:
    if not isinstance(idempotency_key, str):
        raise StateError("idempotency key must be text")
    if not KEY_PATTERN.fullmatch(idempotency_key):
        raise StateError(
            "idempotency key must be 1-100 letters, numbers, dots, colons, dashes, or underscores"
        )
    return idempotency_key


def _validate_state(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise StateError("checkpoint must be a JSON object")
    required = {
        "schema_version",
        "task_id",
        "action",
        "idempotency_key",
        "status",
        "checkpoint",
        "approval",
    }
    if set(payload) != required:
        raise StateError("checkpoint fields do not match the current schema")
    if payload["schema_version"] != SCHEMA_VERSION:
        raise StateError("checkpoint schema version is not supported")
    _validate_action(payload["action"])
    _validate_key(payload["idempotency_key"])
    if payload["task_id"] != payload["idempotency_key"]:
        raise StateError("task ID and idempotency key do not match")
    if payload["status"] not in VALID_STATUSES:
        raise StateError("checkpoint has an unknown status")
    if type(payload["checkpoint"]) is not int or payload["checkpoint"] < 1:
        raise StateError("checkpoint number must be a positive integer")
    if payload["approval"] not in {None, "approved", "rejected"}:
        raise StateError("checkpoint has an unknown approval decision")
    expected_approval = {
        WAITING: None,
        COMPLETED: "approved",
        CANCELLED: "rejected",
    }[payload["status"]]
    if payload["approval"] != expected_approval:
        raise StateError("checkpoint status and approval decision do not agree")
    return payload


def _load_ledger(path: Path) -> dict[str, list[dict[str, str]]]:
    if not path.exists():
        return {"executed": []}
    payload = _read_json(path)
    if not isinstance(payload, dict) or set(payload) != {"executed"}:
        raise StateError("ledger fields do not match the current schema")
    records = payload["executed"]
    if not isinstance(records, list):
        raise StateError("ledger records must be a list")
    seen_keys: set[str] = set()
    for record in records:
        if not isinstance(record, dict) or set(record) != {"idempotency_key", "action"}:
            raise StateError("ledger contains an invalid record")
        key = _validate_key(record["idempotency_key"])
        _validate_action(record["action"])
        if key in seen_keys:
            raise StateError("ledger contains a duplicate idempotency key")
        seen_keys.add(key)
    return payload


def start_workflow(state_path: Path, *, action: str, idempotency_key: str) -> dict[str, Any]:
    """Create a checkpoint and pause before the fake side effect."""

    action = _validate_action(action)
    idempotency_key = _validate_key(idempotency_key)
    if state_path.exists():
        state = _validate_state(_read_json(state_path))
        if state["action"] != action or state["idempotency_key"] != idempotency_key:
            raise StateError("existing checkpoint belongs to a different task")
        return state

    state = {
        "schema_version": SCHEMA_VERSION,
        "task_id": idempotency_key,
        "action": action,
        "idempotency_key": idempotency_key,
        "status": WAITING,
        "checkpoint": 1,
        "approval": None,
    }
    _atomic_write_json(state_path, state)
    return state


def resume_workflow(
    state_path: Path,
    ledger_path: Path,
    *,
    decision: str,
) -> dict[str, Any]:
    """Resume one paused task and execute the fake side effect at most once."""

    if decision not in {"approve", "reject"}:
        raise StateError("decision must be approve or reject")
    if not state_path.exists():
        raise StateError("checkpoint does not exist")

    state = _validate_state(_read_json(state_path))
    ledger = _load_ledger(ledger_path)
    key = state["idempotency_key"]
    matching = [record for record in ledger["executed"] if record["idempotency_key"] == key]
    if matching and matching[0]["action"] != state["action"]:
        raise StateError("idempotency key was already used for a different action")

    # The ledger records the outside action. Reconcile it before trusting a
    # terminal checkpoint or accepting a late reject decision.
    if state["status"] == COMPLETED:
        if not matching:
            raise StateError("completed checkpoint is missing its ledger record")
        return state
    if state["status"] == CANCELLED:
        if matching:
            raise StateError("cancelled checkpoint conflicts with an existing ledger record")
        return state
    if state["status"] != WAITING:
        raise StateError("workflow is not waiting for approval")

    if matching:
        state["approval"] = "approved"
        state["status"] = COMPLETED
        state["checkpoint"] += 1
        _atomic_write_json(state_path, state)
        return state

    if decision == "reject":
        state["approval"] = "rejected"
        state["status"] = CANCELLED
        state["checkpoint"] += 1
        _atomic_write_json(state_path, state)
        return state

    if not matching:
        ledger["executed"].append({"idempotency_key": key, "action": state["action"]})
        # Write the ledger before marking the checkpoint complete. If the process
        # stops between these writes, the next resume sees the key and does not
        # repeat the side effect.
        _atomic_write_json(ledger_path, ledger)

    state["approval"] = "approved"
    state["status"] = COMPLETED
    state["checkpoint"] += 1
    _atomic_write_json(state_path, state)
    return state


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--state",
        type=Path,
        default=Path(".cache/safe-execution-state.json"),
        help="checkpoint file (default: .cache/safe-execution-state.json)",
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path(".cache/safe-execution-ledger.json"),
        help="fake side-effect ledger (default: .cache/safe-execution-ledger.json)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    start = subparsers.add_parser("start", help="create a checkpoint and pause")
    start.add_argument("--action", required=True)
    start.add_argument("--key", required=True)
    resume = subparsers.add_parser("resume", help="approve or reject the paused task")
    resume.add_argument("--decision", choices=("approve", "reject"), required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "start":
            state = start_workflow(
                args.state,
                action=args.action,
                idempotency_key=args.key,
            )
        else:
            state = resume_workflow(
                args.state,
                args.ledger,
                decision=args.decision,
            )
    except StateError as error:
        print(f"STOPPED: {error}")
        return 1
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
