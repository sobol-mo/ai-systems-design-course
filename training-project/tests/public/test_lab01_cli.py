import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from learning_project.cli import main


PROPOSAL_TEXT = (
    'schema_version: "1.0"\n'
    "proposal_id: lab01-boundary-distributed-systems\n"
    "status: proposed\n"
    "personal_domain: distributed systems\n"
    "intended_learning_outcome: Explain how replicated services preserve availability.\n"
    "non_goals:\n"
    "  - Building a production cluster\n"
    "  - Changing canonical notes without human approval\n"
    "governance:\n"
    "  ai_role: Propose a bounded system description.\n"
    "  deterministic_role: Validate, record the decision, and apply only approved content.\n"
    "  human_role: Review meaning and explicitly approve or reject it.\n"
    "usefulness_condition: The system links an answer to preserved source evidence.\n"
    "material_risk: Generated relations may overstate what a source supports.\n"
    "non_ai_baseline: Search curated Markdown notes by exact keywords.\n"
    "uncertainty: The initial relation vocabulary may not cover every domain concept.\n"
    "required_evidence:\n"
    "  - A passing deterministic validation result\n"
    "  - A recorded human decision bound to the proposal digest\n"
)


def run_cli(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


class Lab01CommandLineTests(unittest.TestCase):
    def setUp(self) -> None:
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        self.root = Path(self._temp.name)
        self.proposal_path = self.root / "boundary-proposal.yaml"
        self.decision_path = self.root / "boundary-decision.json"
        self.accepted_path = self.root / "learning-system-boundary.yaml"
        self.proposal_path.write_text(PROPOSAL_TEXT, encoding="utf-8")

    def test_validate_accepts_a_well_formed_proposal(self) -> None:
        code, out, _ = run_cli(["validate", str(self.proposal_path)])

        self.assertEqual(code, 0)
        self.assertIn("lab01-boundary-distributed-systems", out)

    def test_validate_reports_every_error_of_an_invalid_proposal(self) -> None:
        self.proposal_path.write_text("proposal_id: Not A Slug\n", encoding="utf-8")

        code, _, err = run_cli(["validate", str(self.proposal_path)])

        self.assertEqual(code, 1)
        self.assertIn("schema_version", err)

    def test_apply_refuses_a_proposal_that_was_never_decided(self) -> None:
        code, _, err = run_cli(["apply", str(self.proposal_path)])

        self.assertEqual(code, 1)
        self.assertIn("Decision file is missing", err)
        self.assertFalse(self.accepted_path.exists())

    def test_apply_refuses_a_rejected_proposal(self) -> None:
        run_cli(["decide", str(self.proposal_path), "--reject", "--by", "student-01"])

        code, _, err = run_cli(["apply", str(self.proposal_path)])

        self.assertEqual(code, 1)
        self.assertIn("explicitly approved", err)
        self.assertFalse(self.accepted_path.exists())

    def test_approved_proposal_becomes_the_accepted_contract(self) -> None:
        decide_code, _, _ = run_cli(
            ["decide", str(self.proposal_path), "--approve", "--by", "student-01"]
        )
        apply_code, _, _ = run_cli(["apply", str(self.proposal_path)])

        self.assertEqual(decide_code, 0)
        self.assertEqual(apply_code, 0)
        decision = json.loads(self.decision_path.read_text(encoding="utf-8"))
        self.assertEqual(decision["decision"], "approved")
        self.assertEqual(decision["recorded_by"], "student-01")
        accepted = self.accepted_path.read_text(encoding="utf-8")
        self.assertIn("status: approved", accepted)
        self.assertIn("approved_by: student-01", accepted)

    def test_a_recorded_decision_cannot_be_silently_overwritten(self) -> None:
        run_cli(["decide", str(self.proposal_path), "--reject", "--by", "student-01"])

        code, _, err = run_cli(
            ["decide", str(self.proposal_path), "--approve", "--by", "student-01"]
        )

        self.assertEqual(code, 1)
        self.assertIn("already recorded", err)

    def test_decide_refuses_a_pending_decision_for_a_different_proposal(self) -> None:
        first_code, _, _ = run_cli(
            ["decide", str(self.proposal_path), "--reject", "--by", "student-01"]
        )
        self.assertEqual(first_code, 0)
        decision = json.loads(self.decision_path.read_text(encoding="utf-8"))
        decision["decision"] = "pending"
        decision.pop("recorded_by")
        self.decision_path.write_text(json.dumps(decision) + "\n", encoding="utf-8")
        self.proposal_path.write_text(
            PROPOSAL_TEXT.replace(
                "lab01-boundary-distributed-systems",
                "lab01-boundary-operating-systems",
            ),
            encoding="utf-8",
        )

        code, _, err = run_cli(
            ["decide", str(self.proposal_path), "--approve", "--by", "student-01"]
        )

        self.assertEqual(code, 1)
        self.assertIn("different proposal_id", err)
        unchanged = json.loads(self.decision_path.read_text(encoding="utf-8"))
        self.assertEqual(unchanged["decision"], "pending")


if __name__ == "__main__":
    unittest.main()
