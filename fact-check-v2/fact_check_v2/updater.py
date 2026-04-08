from __future__ import annotations

import json
from pathlib import Path

from .models import AnalysisResult, ProposalDecision, RiskLevel, UpdateProposal, Verdict


def build_proposals(analysis: AnalysisResult) -> list[UpdateProposal]:
    proposals: list[UpdateProposal] = []
    idx = 1
    for result in analysis.results:
        if result.verdict in {Verdict.PRESENT}:
            continue
        proposals.append(
            UpdateProposal(
                id=f"P-{idx}",
                article_path=result.article_path,
                fact_id=result.fact_id,
                current_excerpt="[excerpt unavailable in MVP]",
                proposed_text=f"Update section with verified fact: {result.fact_id}",
                rationale=result.notes,
                risk=RiskLevel.MEDIUM if result.verdict == Verdict.PARTIAL else RiskLevel.HIGH,
                evidence=result.evidence,
            )
        )
        idx += 1
    return proposals


def save_proposals(proposals: list[UpdateProposal], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [p.model_dump(mode="json") for p in proposals]
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_proposals(path: Path) -> list[UpdateProposal]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [UpdateProposal.model_validate(item) for item in data]


def filter_proposals_by_status(proposals: list[UpdateProposal], statuses: set[ProposalDecision]) -> list[UpdateProposal]:
    return [proposal for proposal in proposals if proposal.status in statuses]


def apply_proposals(proposals: list[UpdateProposal], mode: str, proposal_id: str | None, min_risk: str | None) -> list[str]:
    applied: list[str] = []
    for proposal in proposals:
        if mode == "individual" and proposal.id != proposal_id:
            continue
        if mode == "bulk" and min_risk is not None:
            order = {"low": 1, "medium": 2, "high": 3}
            if order[proposal.risk.value] < order[min_risk]:
                continue
        path = Path(proposal.article_path)
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        update_line = f"\n\n[FACT-CHECK-V2] {proposal.proposed_text}\n"
        path.write_text(original + update_line, encoding="utf-8")
        applied.append(proposal.id)
    return applied


def apply_accepted_proposals(proposals: list[UpdateProposal], min_risk: str | None = None) -> list[str]:
    accepted = filter_proposals_by_status(proposals, {ProposalDecision.ACCEPTED})
    return apply_proposals(accepted, mode="bulk", proposal_id=None, min_risk=min_risk)
