from __future__ import annotations

import json
import hashlib
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


REQUIRED_STATE_FIELDS = [
    "admissibility_score",
    "capacity_margin",
    "authority_valid",
    "constraint_continuity",
]


def canonical_hash(payload: Dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def refuse(reason: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    receipt_core = {
        "receipt_class": "execution_boundary_decision",
        "decision": "REFUSE",
        "reason": reason,
        "transition_id": payload.get("transition_id", "UNKNOWN"),
        "governing_basis_id": payload.get("governing_basis_id", "UNKNOWN"),
        "side_effect_allowed": False,
        "input_hash": canonical_hash(payload),
        "boundary": {
            "decision_before_effect": True,
            "fail_closed": True,
            "receipt_proves": "boundary_decision_not_just_outcome"
        }
    }
    receipt_core["receipt_hash"] = canonical_hash(receipt_core)
    return receipt_core


def evaluate(payload: Dict[str, Any]) -> Dict[str, Any]:
    state = payload.get("state")
    if not isinstance(state, dict):
        return refuse("MISSING_STATE", payload)

    for field in REQUIRED_STATE_FIELDS:
        if field not in state:
            return refuse(f"MISSING_STATE_FIELD:{field}", payload)

    admissibility_ok = state["admissibility_score"] >= 0
    capacity_ok = state["capacity_margin"] >= 0
    authority_ok = state["authority_valid"] is True
    constraints_ok = state["constraint_continuity"] == "VALID"

    proof = {
        "admissibility_ok": admissibility_ok,
        "capacity_ok": capacity_ok,
        "authority_ok": authority_ok,
        "constraints_ok": constraints_ok,
    }

    decision = "EXECUTE" if all(proof.values()) else "REFUSE"
    reason = "ADMISSIBLE" if decision == "EXECUTE" else "BOUNDARY_CONDITIONS_FAILED"

    receipt_core = {
        "receipt_class": "execution_boundary_decision",
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "transition_id": payload["transition_id"],
        "governing_basis_id": payload["governing_basis_id"],
        "decision": decision,
        "reason": reason,
        "proof": proof,
        "state_hash": canonical_hash(state),
        "action_hash": canonical_hash(payload.get("action", {})),
        "input_hash": canonical_hash(payload),
        "side_effect_allowed": decision == "EXECUTE",
        "boundary": {
            "decision_before_effect": True,
            "fail_closed": True,
            "receipt_proves": "boundary_decision_not_just_outcome"
        }
    }

    receipt_core["receipt_hash"] = canonical_hash(receipt_core)
    return receipt_core


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python runner.py demo/valid_case.json")
        return 2

    input_path = Path(sys.argv[1])
    payload = json.loads(input_path.read_text())
    receipt = evaluate(payload)

    # --- EFFECT CONTROL (REAL PROOF) ---
    EFFECT_FILE = "effect_result.txt"

    if receipt["decision"] == "EXECUTE":
        with open(EFFECT_FILE, "w") as f:
            f.write("EXECUTED: consequence allowed and bound\n")
        print("EFFECT: file created -> effect_result.txt")

    elif receipt["decision"] == "REFUSE":
        if os.path.exists(EFFECT_FILE):
            os.remove(EFFECT_FILE)
        print("EFFECT: no file created (refused)")

    # --- SAVE RECEIPT ---
    out_dir = Path("receipts")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / f"{payload.get('transition_id', 'unknown')}_receipt.json"
    out_path.write_text(json.dumps(receipt, indent=2))

    print(json.dumps({
        "decision": receipt["decision"],
        "reason": receipt["reason"],
        "side_effect_allowed": receipt["side_effect_allowed"],
        "receipt_path": str(out_path),
        "receipt_hash": receipt["receipt_hash"]
    }, indent=2))

    return 0 if receipt["decision"] == "EXECUTE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
