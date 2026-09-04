import json
import tempfile
import unittest
from pathlib import Path

from learning_project.workflow import (
    WorkflowError,
    apply_proposal,
    create_decision,
    record_approval,
    validate_proposal,
)


VALID_PROPOSAL = {
    "schema_version": "1.0",
    "proposal_id": "lab01-boundary-distributed-systems",
    "status": "proposed",
    "personal_domain": "distributed systems",
    "intended_learning_outcome": "Explain how replicated services preserve availability.",
    "non_goals": [
        "Building a production cluster",
        "Changing canonical notes without human approval",
    ],
    "governance": {
        "ai_role": "Propose a bounded system description.",
        "deterministic_role": "Validate, record the decision, and apply only approved content.",
        "human_role": "Review meaning and explicitly approve or reject it.",
    },
    "usefulness_condition": "The system links an answer to preserved source evidence.",
    "material_risk": "Generated relations may overstate what a source supports.",
    "non_ai_baseline": "Search curated Markdown notes by exact keywords.",
    "uncertainty": "The initial relation vocabulary may not cover every domain concept.",
    "required_evidence": [
        "A passing deterministic validation result",
        "A recorded human decision bound to the proposal digest",
    ],
}


class GovernedProposalWorkflowTests(unittest.TestCase):
    def _write_valid_proposal(self, root: Path) -> Path:
        proposal_path = root / "boundary-proposal.yaml"
        proposal_path.write_text(
            json.dumps(VALID_PROPOSAL, indent=2) + "\n",
            encoding="utf-8",
        )
        return proposal_path

    def test_pending_decision_cannot_be_applied(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            proposal_path = root / "boundary-proposal.yaml"
            decision_path = root / "boundary-decision.json"
            accepted_path = root / "learning-system-boundary.yaml"
            proposal_path.write_text(
                json.dumps(VALID_PROPOSAL, indent=2) + "\n",
                encoding="utf-8",
            )

            validation = validate_proposal(proposal_path)
            create_decision(validation, decision_path)

            with self.assertRaisesRegex(WorkflowError, "explicitly approved"):
                apply_proposal(proposal_path, decision_path, accepted_path)

            self.assertFalse(accepted_path.exists())

    def test_approved_decision_creates_accepted_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            proposal_path = root / "boundary-proposal.yaml"
            decision_path = root / "boundary-decision.json"
            accepted_path = root / "learning-system-boundary.yaml"
            proposal_path.write_text(
                "schema_version: \"1.0\"\n"
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
                "  - A recorded human decision bound to the proposal digest\n",
                encoding="utf-8",
            )

            validation = validate_proposal(proposal_path)
            self.assertTrue(validation.valid, validation.errors)
            create_decision(validation, decision_path)
            record_approval(decision_path, recorded_by="student-01")

            apply_proposal(proposal_path, decision_path, accepted_path)

            accepted = accepted_path.read_text(encoding="utf-8")
            self.assertIn("proposal_id: lab01-boundary-distributed-systems", accepted)
            self.assertIn("schema_version: \"1.0\"", accepted)

    def test_approval_is_bound_to_the_exact_proposal_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            proposal_path = self._write_valid_proposal(root)
            decision_path = root / "boundary-decision.json"
            accepted_path = root / "learning-system-boundary.yaml"
            validation = validate_proposal(proposal_path)
            create_decision(validation, decision_path)
            record_approval(decision_path, recorded_by="student-01")

            changed = dict(VALID_PROPOSAL)
            changed["material_risk"] = "This content was changed after approval."
            proposal_path.write_text(json.dumps(changed, indent=2) + "\n", encoding="utf-8")

            with self.assertRaisesRegex(WorkflowError, "changed after the decision"):
                apply_proposal(proposal_path, decision_path, accepted_path)

            self.assertFalse(accepted_path.exists())

    def test_incomplete_forged_decision_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            proposal_path = self._write_valid_proposal(root)
            decision_path = root / "boundary-decision.json"
            accepted_path = root / "learning-system-boundary.yaml"
            decision_path.write_text(
                json.dumps(
                    {
                        "proposal_id": VALID_PROPOSAL["proposal_id"],
                        "decision": "approved",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(WorkflowError, "schema_version"):
                apply_proposal(proposal_path, decision_path, accepted_path)

            self.assertFalse(accepted_path.exists())

    def test_reapplying_the_same_approved_proposal_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            proposal_path = self._write_valid_proposal(root)
            decision_path = root / "boundary-decision.json"
            accepted_path = root / "learning-system-boundary.yaml"
            validation = validate_proposal(proposal_path)
            create_decision(validation, decision_path)
            record_approval(decision_path, recorded_by="student-01")

            apply_proposal(proposal_path, decision_path, accepted_path)
            first = accepted_path.read_bytes()
            apply_proposal(proposal_path, decision_path, accepted_path)

            self.assertEqual(accepted_path.read_bytes(), first)

    def test_proposal_requires_proposed_status_and_two_string_non_goals(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            proposal_path = self._write_valid_proposal(root)
            invalid = dict(VALID_PROPOSAL)
            invalid["status"] = "approved"
            invalid["non_goals"] = [None]
            invalid["governance"] = {
                "ai_role": "Propose content.",
                "human_role": "Approve or reject content.",
            }
            invalid["required_evidence"] = [None]
            proposal_path.write_text(json.dumps(invalid) + "\n", encoding="utf-8")

            validation = validate_proposal(proposal_path)

            self.assertFalse(validation.valid)
            self.assertIn("status must be proposed.", validation.errors)
            self.assertIn(
                "non_goals must contain at least two non-empty strings.",
                validation.errors,
            )
            self.assertIn(
                "governance.deterministic_role must be a non-empty string.",
                validation.errors,
            )
            self.assertIn(
                "required_evidence must contain at least two non-empty strings.",
                validation.errors,
            )


if __name__ == "__main__":
    unittest.main()
