"""Deterministic governed-proposal workflow for Laboratory 01.

The AI produces only a candidate proposal. A human decision recorded in a
decision file is the single authority for accepting a proposal. Applying a
proposal that was not explicitly approved, or whose content changed after the
decision was recorded, is a hard workflow error.

Three artefacts carry the protocol, and each has one owner:

* ``boundary-proposal.yaml`` — written by the AI, editable by the student.
* ``boundary-decision.json`` — the recorded human decision, the only authority.
* ``learning-system-boundary.yaml`` — the accepted contract, written by this
  module and never by hand.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import yaml

SCHEMA_VERSION = "1.0"
DECISION_SCHEMA_VERSION = "1.0"
ALLOWED_DECISIONS = ("pending", "approved", "rejected")
REQUIRED_FIELDS = (
    "schema_version",
    "proposal_id",
    "status",
    "personal_domain",
    "intended_learning_outcome",
    "non_goals",
    "governance",
    "usefulness_condition",
    "material_risk",
    "non_ai_baseline",
    "uncertainty",
    "required_evidence",
)

PROPOSAL_FILENAME = "boundary-proposal.yaml"
DECISION_FILENAME = "boundary-decision.json"
ACCEPTED_FILENAME = "learning-system-boundary.yaml"

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class WorkflowError(Exception):
    """Raised when the governed proposal protocol is violated."""


@dataclass(frozen=True)
class Validation:
    proposal_path: Path
    proposal_id: str
    valid: bool
    errors: tuple[str, ...]

    @property
    def decision_path(self) -> Path:
        return self.proposal_path.parent / DECISION_FILENAME


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class _ContractDumper(yaml.SafeDumper):
    """Writes the accepted contract with quotes only where meaning requires them."""

    def increase_indent(self, flow: bool = False, indentless: bool = False):
        # Indent list items under their key, so the contract reads like the proposal.
        return super().increase_indent(flow, False)


def _represent_contract_str(dumper: yaml.SafeDumper, value: str) -> yaml.nodes.ScalarNode:
    implicit_tag = dumper.resolve(yaml.nodes.ScalarNode, value, (True, False))
    style = '"' if implicit_tag != "tag:yaml.org,2002:str" else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", value, style=style)


_ContractDumper.add_representer(str, _represent_contract_str)


def _read_proposal(proposal_path: Path) -> dict:
    try:
        data = yaml.safe_load(proposal_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise WorkflowError(f"Proposal file cannot be read: {exc}") from exc
    except yaml.YAMLError as exc:
        raise WorkflowError(f"Proposal is not valid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise WorkflowError("Proposal root must be a mapping of fields.")
    return data


def _require_string_field(proposal: dict, field: str) -> list[str]:
    value = proposal.get(field)
    if not isinstance(value, str) or not value.strip():
        return [f"{field} must be a non-empty string."]
    return []


def _proposal_sha256(proposal_path: Path) -> str:
    try:
        return hashlib.sha256(proposal_path.read_bytes()).hexdigest()
    except OSError as exc:
        raise WorkflowError(f"Proposal file cannot be read: {exc}") from exc


def validate_proposal(proposal_path: Path) -> Validation:
    errors: list[str] = []

    try:
        proposal = _read_proposal(proposal_path)
    except WorkflowError as exc:
        return Validation(proposal_path, "unknown", False, (str(exc),))

    for field in REQUIRED_FIELDS:
        if field not in proposal:
            errors.append(f"Missing required field: {field}.")

    if errors:
        return Validation(proposal_path, "unknown", False, tuple(errors))

    if proposal.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"Unsupported schema_version. Expected {SCHEMA_VERSION}.")
    proposal_id_value = proposal.get("proposal_id")
    proposal_id = proposal_id_value if isinstance(proposal_id_value, str) else "unknown"
    if not isinstance(proposal_id_value, str) or not SLUG_RE.fullmatch(proposal_id):
        errors.append("proposal_id must be a lowercase slug without spaces.")
    if proposal.get("status") != "proposed":
        errors.append("status must be proposed.")
    governance = proposal.get("governance")
    if not isinstance(governance, dict):
        errors.append("governance must be an object.")
    else:
        for key in ("ai_role", "deterministic_role", "human_role"):
            if not isinstance(governance.get(key), str) or not governance[key].strip():
                errors.append(f"governance.{key} must be a non-empty string.")

    for field in (
        "personal_domain",
        "intended_learning_outcome",
        "usefulness_condition",
        "material_risk",
        "non_ai_baseline",
        "uncertainty",
    ):
        errors.extend(_require_string_field(proposal, field))
    for field in ("non_goals", "required_evidence"):
        values = proposal.get(field)
        if (
            not isinstance(values, list)
            or len(values) < 2
            or any(not isinstance(value, str) or not value.strip() for value in values)
        ):
            errors.append(f"{field} must contain at least two non-empty strings.")

    return Validation(proposal_path, proposal_id, not errors, tuple(errors))


def _canonical_proposal(proposal: dict) -> dict:
    return {key: proposal.get(key) for key in REQUIRED_FIELDS}


def _write_decision(decision_path: Path, decision: dict) -> Path:
    decision_path.write_text(
        json.dumps(decision, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return decision_path


def _read_decision(decision_path: Path) -> dict:
    try:
        decision = json.loads(decision_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkflowError(f"Decision file is missing or invalid: {exc}") from exc
    if not isinstance(decision, dict):
        raise WorkflowError("Decision file must contain a JSON object.")
    if decision.get("schema_version") != DECISION_SCHEMA_VERSION:
        raise WorkflowError(
            f"Decision schema_version must be {DECISION_SCHEMA_VERSION}."
        )
    if decision.get("decision") not in ALLOWED_DECISIONS:
        raise WorkflowError(
            f"decision must be one of {', '.join(ALLOWED_DECISIONS)}."
        )
    if not isinstance(decision.get("proposal_id"), str):
        raise WorkflowError("Decision file must name the proposal_id it decides.")
    proposal_sha256 = decision.get("proposal_sha256")
    if not isinstance(proposal_sha256, str) or not SHA256_RE.fullmatch(proposal_sha256):
        raise WorkflowError("Decision file must contain a valid proposal_sha256.")
    if decision["decision"] != "pending":
        if not isinstance(decision.get("recorded_by"), str) or not decision["recorded_by"].strip():
            raise WorkflowError("A recorded decision must name the human who recorded it.")
        if not isinstance(decision.get("recorded_at"), str) or not decision["recorded_at"].strip():
            raise WorkflowError("A recorded decision must include recorded_at.")
    return decision


def create_decision(validation: Validation, decision_path: Path) -> Path:
    if not validation.valid:
        raise WorkflowError("Cannot create a decision for an invalid proposal.")
    return _write_decision(
        decision_path,
        {
            "schema_version": DECISION_SCHEMA_VERSION,
            "proposal_id": validation.proposal_id,
            "proposal_sha256": _proposal_sha256(validation.proposal_path),
            "decision": "pending",
            "recorded_at": _now(),
        },
    )


def ensure_decision_matches(validation: Validation, decision_path: Path) -> dict:
    decision = _read_decision(decision_path)
    if decision["proposal_id"] != validation.proposal_id:
        raise WorkflowError("Decision references a different proposal_id.")
    if decision["proposal_sha256"] != _proposal_sha256(validation.proposal_path):
        raise WorkflowError("Proposal content changed after the decision was recorded.")
    return decision


def _record_decision(
    decision_path: Path,
    outcome: str,
    *,
    recorded_by: str,
    reason: str | None,
) -> Path:
    if not isinstance(recorded_by, str) or not recorded_by.strip():
        raise WorkflowError("A decision must name the human who recorded it.")

    decision = _read_decision(decision_path)
    if decision["decision"] != "pending":
        raise WorkflowError(
            f"Decision is already recorded as '{decision['decision']}' and cannot be "
            "overwritten. Start a new review to decide again."
        )

    decision["decision"] = outcome
    decision["recorded_by"] = recorded_by.strip()
    decision["recorded_at"] = _now()
    if reason:
        decision["reason"] = reason
    return _write_decision(decision_path, decision)


def record_approval(decision_path: Path, *, recorded_by: str) -> Path:
    """Records an explicit human approval on a pending decision."""
    return _record_decision(decision_path, "approved", recorded_by=recorded_by, reason=None)


def record_rejection(
    decision_path: Path, *, recorded_by: str, reason: str | None = None
) -> Path:
    """Records an explicit human rejection on a pending decision."""
    return _record_decision(decision_path, "rejected", recorded_by=recorded_by, reason=reason)


def _dump_contract(contract: dict) -> str:
    return yaml.dump(
        contract,
        Dumper=_ContractDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=100,
    )


def apply_proposal(proposal_path: Path, decision_path: Path, accepted_path: Path) -> Path:
    validation = validate_proposal(proposal_path)
    if not validation.valid:
        raise WorkflowError(
            "Proposal is invalid and cannot be applied: "
            + "; ".join(validation.errors)
        )

    decision = ensure_decision_matches(validation, decision_path)

    if decision["decision"] != "approved":
        raise WorkflowError(
            "Proposal was not explicitly approved and cannot be applied. "
            "Record an explicit approved decision first."
        )
    proposal_sha256 = _proposal_sha256(proposal_path)

    proposal = _read_proposal(proposal_path)
    contract = _canonical_proposal(proposal)
    contract["status"] = "approved"
    contract["accepted"] = {
        "source_proposal": proposal_path.name,
        "proposal_sha256": proposal_sha256,
        "approved_by": decision.get("recorded_by", "unknown"),
        "approved_at": decision.get("recorded_at", "unknown"),
    }
    if accepted_path.exists():
        try:
            existing = yaml.safe_load(accepted_path.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError):
            existing = None
        if isinstance(existing, dict):
            existing_accepted = existing.get("accepted")
            if isinstance(existing_accepted, dict):
                applied_at = existing_accepted.get("applied_at")
                existing_without_time = dict(existing)
                existing_without_time["accepted"] = dict(existing_accepted)
                existing_without_time["accepted"].pop("applied_at", None)
                if isinstance(applied_at, str) and existing_without_time == contract:
                    return accepted_path
    contract["accepted"]["applied_at"] = _now()
    accepted_path.write_text(_dump_contract(contract), encoding="utf-8")
    return accepted_path
