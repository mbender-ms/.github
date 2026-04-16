from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .connectors import LocalArticleConnector, LocalSourceConnector
from .models import AnalysisResult, Evidence, FactInput, FactResult, Verdict
from .policy import ToolPolicy
from .storage import CacheStore, claim_key
from .telemetry import ToolCallTracer
from .tool_executor import ToolExecutor


def load_facts(path: Path) -> list[FactInput]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [FactInput.model_validate(item) for item in data]


def list_articles(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(path.rglob("*.md"))


def run_gap_analysis(
    facts: list[FactInput],
    articles: list[Path],
    cache: CacheStore | None = None,
    source_roots: list[Path] | None = None,
    policy: ToolPolicy | None = None,
    tracer: ToolCallTracer | None = None,
) -> AnalysisResult:
    executor = ToolExecutor(policy=policy, tracer=tracer)
    article_connector = LocalArticleConnector(executor)
    source_connector = LocalSourceConnector(source_roots or [], executor)

    results = []
    for article in articles:
        for fact in facts:
            key = claim_key(fact.text, fact.service, article_path=str(article))
            cached = cache.get(key) if cache else None
            if cached:
                result = cached.model_copy(update={"notes": "Cache hit reused article-level verdict"})
            else:
                verdict, confidence, notes = article_connector.evaluate(fact, article)
                evidence: list[Evidence] = [
                    Evidence(source=str(article), tier=1, anchor="article-body", confidence=confidence)
                ]
                source_evidence = source_connector.find_support(fact)
                evidence.extend(source_evidence)

                if verdict == Verdict.MISSING and not source_evidence:
                    verdict = Verdict.UNVERIFIABLE
                    notes = "No support found in article or configured source roots"

                result = FactResult(
                    fact_id=fact.id,
                    verdict=verdict,
                    confidence=confidence,
                    article_path=str(article),
                    evidence=evidence,
                    notes=notes,
                )
                if cache:
                    cache.set(key, result)
            results.append(result)

    return AnalysisResult(
        generated_at=datetime.now(timezone.utc),
        facts_total=len(facts),
        article_count=len(articles),
        results=results,
    )
