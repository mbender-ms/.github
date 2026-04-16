from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Verdict(str, Enum):
    PRESENT = "present"
    PARTIAL = "partial"
    MISSING = "missing"
    CONTRADICTED = "contradicted"
    UNVERIFIABLE = "unverifiable"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RunState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    REVIEW_READY = "review-ready"
    REVISION_REQUESTED = "revision-requested"
    APPROVED = "approved"
    APPLYING = "applying"
    FINALIZED = "finalized"
    ABORTED = "aborted"


class ProposalDecision(str, Enum):
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    SUPERSEDED = "superseded"


class FactInput(BaseModel):
    id: str
    text: str
    service: Optional[str] = None
    expected_source_tier: Optional[int] = None


class Evidence(BaseModel):
    source: str
    tier: int
    anchor: str
    confidence: float = Field(ge=0.0, le=1.0)


class FactResult(BaseModel):
    fact_id: str
    verdict: Verdict
    confidence: float = Field(ge=0.0, le=1.0)
    article_path: str
    evidence: list[Evidence] = Field(default_factory=list)
    notes: str = ""


class AnalysisResult(BaseModel):
    generated_at: datetime
    facts_total: int
    article_count: int
    results: list[FactResult]


class GradeBreakdown(BaseModel):
    score: int = Field(ge=0, le=100)
    present_ratio: float = Field(ge=0.0, le=1.0)
    contradicted_count: int = 0
    missing_count: int = 0
    unverifiable_count: int = 0


class UpdateProposal(BaseModel):
    id: str
    article_path: str
    fact_id: str
    current_excerpt: str
    proposed_text: str
    rationale: str
    risk: RiskLevel
    evidence: list[Evidence]
    status: ProposalDecision = ProposalDecision.PROPOSED
    selected: bool = False


class ToolCallEvent(BaseModel):
    timestamp: datetime
    correlation_id: str
    tool_name: str
    args_summary: str
    status: str
    latency_ms: int
    message: str = ""
