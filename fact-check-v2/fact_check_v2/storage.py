from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import ProposalDecision, RunState

from .models import Evidence, FactResult


class CacheStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with closing(sqlite3.connect(self.db_path)) as conn:
            with conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS claim_cache (
                        claim_key TEXT PRIMARY KEY,
                        result_json TEXT NOT NULL
                    )
                    """
                )

    def get(self, claim_key: str) -> FactResult | None:
        with closing(sqlite3.connect(self.db_path)) as conn:
            row = conn.execute(
                "SELECT result_json FROM claim_cache WHERE claim_key = ?",
                (claim_key,),
            ).fetchone()
        if not row:
            return None
        return FactResult.model_validate(json.loads(row[0]))

    def set(self, claim_key: str, result: FactResult) -> None:
        payload = json.dumps(result.model_dump(mode="json"))
        with closing(sqlite3.connect(self.db_path)) as conn:
            with conn:
                conn.execute(
                    """
                    INSERT INTO claim_cache (claim_key, result_json) VALUES (?, ?)
                    ON CONFLICT(claim_key) DO UPDATE SET result_json=excluded.result_json
                    """,
                    (claim_key, payload),
                )


class RunStore:
    ALLOWED_TRANSITIONS: dict[RunState, set[RunState]] = {
        RunState.QUEUED: {RunState.RUNNING, RunState.ABORTED},
        RunState.RUNNING: {RunState.REVIEW_READY, RunState.ABORTED},
        RunState.REVIEW_READY: {RunState.REVISION_REQUESTED, RunState.APPROVED, RunState.ABORTED},
        RunState.REVISION_REQUESTED: {RunState.QUEUED, RunState.ABORTED},
        RunState.APPROVED: {RunState.APPLYING, RunState.ABORTED},
        RunState.APPLYING: {RunState.FINALIZED, RunState.ABORTED},
        RunState.FINALIZED: set(),
        RunState.ABORTED: set(),
    }

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS runs (
                        run_id TEXT PRIMARY KEY,
                        state TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        scope TEXT NOT NULL,
                        facts_path TEXT NOT NULL,
                        articles_path TEXT NOT NULL,
                        analysis_path TEXT NOT NULL,
                        report_path TEXT NOT NULL,
                        proposals_path TEXT NOT NULL,
                        trace_path TEXT,
                        notes TEXT
                    )
                    """
                )
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS proposal_decisions (
                        run_id TEXT NOT NULL,
                        proposal_id TEXT NOT NULL,
                        decision TEXT NOT NULL,
                        review_note TEXT,
                        decided_at TEXT NOT NULL,
                        PRIMARY KEY (run_id, proposal_id),
                        FOREIGN KEY (run_id) REFERENCES runs(run_id)
                    )
                    """
                )

    def create_run(self, run_id: str, metadata: dict[str, str], state: RunState = RunState.REVIEW_READY) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    """
                    INSERT INTO runs (
                        run_id, state, created_at, updated_at, scope,
                        facts_path, articles_path, analysis_path, report_path,
                        proposals_path, trace_path, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        state.value,
                        now,
                        now,
                        metadata["scope"],
                        metadata["facts_path"],
                        metadata["articles_path"],
                        metadata["analysis_path"],
                        metadata["report_path"],
                        metadata["proposals_path"],
                        metadata.get("trace_path"),
                        metadata.get("notes"),
                    ),
                )

    def get_run(self, run_id: str) -> dict[str, Any]:
        with closing(self._connect()) as conn:
            row = conn.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        if not row:
            raise KeyError(f"Run not found: {run_id}")
        return dict(row)

    def transition(self, run_id: str, new_state: RunState, note: str | None = None) -> None:
        run = self.get_run(run_id)
        current = RunState(run["state"])
        if new_state not in self.ALLOWED_TRANSITIONS[current]:
            raise ValueError(f"Invalid state transition: {current.value} -> {new_state.value}")

        now = datetime.now(timezone.utc).isoformat()
        new_note = note if note is not None else run.get("notes")
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    "UPDATE runs SET state = ?, updated_at = ?, notes = ? WHERE run_id = ?",
                    (new_state.value, now, new_note, run_id),
                )

    def upsert_proposal_decision(
        self,
        run_id: str,
        proposal_id: str,
        decision: ProposalDecision,
        review_note: str | None = None,
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    """
                    INSERT INTO proposal_decisions (run_id, proposal_id, decision, review_note, decided_at)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(run_id, proposal_id) DO UPDATE SET
                        decision = excluded.decision,
                        review_note = excluded.review_note,
                        decided_at = excluded.decided_at
                    """,
                    (run_id, proposal_id, decision.value, review_note, now),
                )

    def seed_proposals(self, run_id: str, proposal_ids: list[str]) -> None:
        for proposal_id in proposal_ids:
            self.upsert_proposal_decision(run_id, proposal_id, ProposalDecision.PROPOSED)

    def get_decisions(self, run_id: str) -> dict[str, ProposalDecision]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                "SELECT proposal_id, decision FROM proposal_decisions WHERE run_id = ?",
                (run_id,),
            ).fetchall()
        return {row["proposal_id"]: ProposalDecision(row["decision"]) for row in rows}


def claim_key(text: str, service: str | None, article_path: str | None = None) -> str:
    normalized = " ".join(text.strip().lower().split())
    svc = (service or "unknown").strip().lower()
    article = (article_path or "any").strip().lower()
    return f"{svc}::{normalized}::{article}"
