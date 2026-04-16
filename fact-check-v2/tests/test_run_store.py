import tempfile
import unittest
from pathlib import Path

from fact_check_v2.models import ProposalDecision, RunState
from fact_check_v2.storage import RunStore


class RunStoreTests(unittest.TestCase):
    def test_transition_happy_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "runs.db"
            store = RunStore(db)
            run_id = "run-1"
            store.create_run(
                run_id,
                {
                    "scope": "docs/load-balancer",
                    "facts_path": "facts.json",
                    "articles_path": "docs",
                    "analysis_path": "out/analysis.json",
                    "report_path": "out/report.md",
                    "proposals_path": "out/proposals.json",
                    "trace_path": "out/trace.jsonl",
                    "notes": "seed",
                },
                state=RunState.REVIEW_READY,
            )

            store.transition(run_id, RunState.APPROVED)
            store.transition(run_id, RunState.APPLYING)
            store.transition(run_id, RunState.FINALIZED)
            run = store.get_run(run_id)
            self.assertEqual(run["state"], RunState.FINALIZED.value)
            del store

    def test_invalid_transition_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "runs.db"
            store = RunStore(db)
            run_id = "run-2"
            store.create_run(
                run_id,
                {
                    "scope": "docs/load-balancer",
                    "facts_path": "facts.json",
                    "articles_path": "docs",
                    "analysis_path": "out/analysis.json",
                    "report_path": "out/report.md",
                    "proposals_path": "out/proposals.json",
                    "trace_path": "out/trace.jsonl",
                    "notes": "seed",
                },
                state=RunState.REVIEW_READY,
            )

            with self.assertRaises(ValueError):
                store.transition(run_id, RunState.FINALIZED)
            del store

    def test_seed_and_update_decisions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "runs.db"
            store = RunStore(db)
            run_id = "run-3"
            store.create_run(
                run_id,
                {
                    "scope": "docs/load-balancer",
                    "facts_path": "facts.json",
                    "articles_path": "docs",
                    "analysis_path": "out/analysis.json",
                    "report_path": "out/report.md",
                    "proposals_path": "out/proposals.json",
                    "trace_path": "out/trace.jsonl",
                    "notes": "seed",
                },
                state=RunState.REVIEW_READY,
            )
            store.seed_proposals(run_id, ["P-1", "P-2"])
            decisions = store.get_decisions(run_id)
            self.assertEqual(decisions["P-1"], ProposalDecision.PROPOSED)

            store.upsert_proposal_decision(run_id, "P-1", ProposalDecision.ACCEPTED, "looks good")
            decisions = store.get_decisions(run_id)
            self.assertEqual(decisions["P-1"], ProposalDecision.ACCEPTED)
            del store


if __name__ == "__main__":
    unittest.main()
