from __future__ import annotations

from pathlib import Path

from .models import Evidence, FactInput, FactResult, Verdict


def analyze_fact_in_article(fact: FactInput, article_path: Path) -> FactResult:
    text = article_path.read_text(encoding="utf-8")
    lowered = text.lower()
    fact_text = fact.text.lower().strip()

    if fact_text in lowered:
        verdict = Verdict.PRESENT
        confidence = 0.95
        notes = "Exact fact text found in article body"
    elif any(token in lowered for token in fact_text.split()[:3]):
        verdict = Verdict.PARTIAL
        confidence = 0.6
        notes = "Partial lexical overlap found; requires human review"
    else:
        verdict = Verdict.MISSING
        confidence = 0.2
        notes = "Fact not found in article"

    evidence = [
        Evidence(
            source=str(article_path),
            tier=1,
            anchor="article-body",
            confidence=confidence,
        )
    ]

    return FactResult(
        fact_id=fact.id,
        verdict=verdict,
        confidence=confidence,
        article_path=str(article_path),
        evidence=evidence,
        notes=notes,
    )
