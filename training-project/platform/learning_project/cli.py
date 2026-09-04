"""Command line for the Laboratory 01 governed-proposal workflow.

Three commands map one to one onto the governed-proposal protocol, and one
command verifies the workstation:

* ``validate`` — check a candidate proposal; it changes nothing.
* ``decide``   — record the explicit human approval or rejection.
* ``apply``    — turn an approved proposal into the accepted contract.
* ``doctor``   — write a normalized workstation capability report.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .doctor import collect_environment_report
from .workflow import (
    ACCEPTED_FILENAME,
    DECISION_FILENAME,
    WorkflowError,
    apply_proposal,
    create_decision,
    ensure_decision_matches,
    record_approval,
    record_rejection,
    validate_proposal,
)


def _sibling(proposal_path: Path, explicit: Path | None, filename: str) -> Path:
    return explicit if explicit is not None else proposal_path.parent / filename


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="learning-project",
        description="Govern an AI proposal with an explicit human decision.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    validate = commands.add_parser("validate", help="Validate a candidate proposal.")
    validate.add_argument("proposal", type=Path)

    decide = commands.add_parser("decide", help="Record the human decision on a proposal.")
    decide.add_argument("proposal", type=Path)
    outcome = decide.add_mutually_exclusive_group(required=True)
    outcome.add_argument("--approve", action="store_true", help="Approve the proposal.")
    outcome.add_argument("--reject", action="store_true", help="Reject the proposal.")
    decide.add_argument("--by", required=True, help="Name of the human who decides.")
    decide.add_argument("--reason", help="Why the proposal was rejected.")
    decide.add_argument("--decision", type=Path, help=f"Decision file (default: {DECISION_FILENAME}).")

    apply_command = commands.add_parser("apply", help="Apply an approved proposal.")
    apply_command.add_argument("proposal", type=Path)
    apply_command.add_argument("--decision", type=Path, help=f"Decision file (default: {DECISION_FILENAME}).")
    apply_command.add_argument("--output", type=Path, help=f"Accepted contract (default: {ACCEPTED_FILENAME}).")

    doctor = commands.add_parser("doctor", help="Verify Laboratory 01 workstation capabilities.")
    doctor.add_argument(
        "--output",
        type=Path,
        default=Path("environment-report.json"),
        help="Machine-readable capability report (default: environment-report.json).",
    )

    return parser


def _run_validate(args: argparse.Namespace) -> int:
    validation = validate_proposal(args.proposal)
    if not validation.valid:
        print(f"Proposal {args.proposal} is not valid:", file=sys.stderr)
        for error in validation.errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"Proposal {validation.proposal_id} is valid.")
    return 0


def _run_decide(args: argparse.Namespace) -> int:
    validation = validate_proposal(args.proposal)
    if not validation.valid:
        raise WorkflowError(
            "Proposal is invalid and cannot be decided: " + "; ".join(validation.errors)
        )

    decision_path = _sibling(args.proposal, args.decision, DECISION_FILENAME)
    if not decision_path.exists():
        create_decision(validation, decision_path)
    else:
        ensure_decision_matches(validation, decision_path)

    if args.approve:
        record_approval(decision_path, recorded_by=args.by)
        print(f"Approved {validation.proposal_id} as {args.by}.")
    else:
        record_rejection(decision_path, recorded_by=args.by, reason=args.reason)
        print(f"Rejected {validation.proposal_id} as {args.by}.")
    return 0


def _run_apply(args: argparse.Namespace) -> int:
    decision_path = _sibling(args.proposal, args.decision, DECISION_FILENAME)
    accepted_path = _sibling(args.proposal, args.output, ACCEPTED_FILENAME)
    apply_proposal(args.proposal, decision_path, accepted_path)
    print(f"Wrote the accepted contract to {accepted_path}.")
    return 0


def _run_doctor(args: argparse.Namespace) -> int:
    report = collect_environment_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote the environment report to {args.output}.")
    return 0 if report["preflight"] == "green" else 1


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    handlers = {
        "validate": _run_validate,
        "decide": _run_decide,
        "apply": _run_apply,
        "doctor": _run_doctor,
    }
    try:
        return handlers[args.command](args)
    except WorkflowError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
