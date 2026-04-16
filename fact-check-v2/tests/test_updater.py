from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from fact_check_v2.models import Evidence, ProposalDecision, RiskLevel, UpdateProposal
from fact_check_v2.updater import apply_accepted_proposals, filter_proposals_by_status


class UpdaterTests(unittest.TestCase):
    def _proposal(
        self,
        proposal_id: str,
        article_path: Path,
        status: ProposalDecision,
        risk: RiskLevel,
    ) -> UpdateProposal:
        return UpdateProposal(
            id=proposal_id,
            article_path=str(article_path),
            fact_id="F-1",
            current_excerpt="old",
            proposed_text=f"new text {proposal_id}",
            rationale="test rationale",
            risk=risk,
            evidence=[
                Evidence(
                    source="https://example.com",
                    tier=1,
                    anchor="sample-anchor",
                    confidence=0.9,
                )
            ],
            status=status,
        )

    def test_filter_proposals_by_status(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            article = Path(td) / "article.md"
            article.write_text("content", encoding="utf-8")

            proposals = [
                self._proposal("P-1", article, ProposalDecision.ACCEPTED, RiskLevel.MEDIUM),
                self._proposal("P-2", article, ProposalDecision.REJECTED, RiskLevel.HIGH),
            ]

            accepted = filter_proposals_by_status(proposals, {ProposalDecision.ACCEPTED})
            self.assertEqual([p.id for p in accepted], ["P-1"])

    def test_apply_accepted_proposals_only(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            article = Path(td) / "article.md"
            article.write_text("base", encoding="utf-8")

            proposals = [
                self._proposal("P-1", article, ProposalDecision.ACCEPTED, RiskLevel.MEDIUM),
                self._proposal("P-2", article, ProposalDecision.REJECTED, RiskLevel.HIGH),
            ]

            applied = apply_accepted_proposals(proposals)
            self.assertEqual(applied, ["P-1"])
            content = article.read_text(encoding="utf-8")
            self.assertIn("new text P-1", content)
            self.assertNotIn("new text P-2", content)

    def test_apply_accepted_proposals_respects_min_risk(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            article = Path(td) / "article.md"
            article.write_text("base", encoding="utf-8")

            proposals = [
                self._proposal("P-1", article, ProposalDecision.ACCEPTED, RiskLevel.MEDIUM),
                self._proposal("P-2", article, ProposalDecision.ACCEPTED, RiskLevel.HIGH),
            ]

            applied = apply_accepted_proposals(proposals, min_risk="high")
            self.assertEqual(applied, ["P-2"])
            content = article.read_text(encoding="utf-8")
            self.assertIn("new text P-2", content)
            self.assertNotIn("new text P-1", content)


if __name__ == "__main__":
    unittest.main()
