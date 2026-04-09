from __future__ import annotations

from pathlib import Path

from .models import Evidence, FactInput, Verdict
from .tool_executor import ToolExecutor


class LocalArticleConnector:
    def __init__(self, executor: ToolExecutor) -> None:
        self.executor = executor

    def evaluate(self, fact: FactInput, article_path: Path) -> tuple[Verdict, float, str]:
        def _work() -> tuple[Verdict, float, str]:
            text = article_path.read_text(encoding="utf-8")
            lowered = text.lower()
            fact_text = fact.text.lower().strip()

            if fact_text in lowered:
                return Verdict.PRESENT, 0.95, "Exact fact text found in article body"

            tokens = [t for t in fact_text.split() if len(t) > 3]
            overlap = sum(1 for token in tokens[:8] if token in lowered)
            if overlap >= 2:
                return Verdict.PARTIAL, 0.6, "Partial lexical overlap found; requires human review"
            return Verdict.MISSING, 0.2, "Fact not found in article"

        return self.executor.invoke(
            "fact-checker.local-article.search",
            f"article={article_path.name} fact={fact.id}",
            _work,
        )


class LocalSourceConnector:
    def __init__(self, roots: list[Path], executor: ToolExecutor) -> None:
        self.roots = roots
        self.executor = executor
        self._cache: dict[str, list[Evidence]] = {}

    def find_support(self, fact: FactInput) -> list[Evidence]:
        cache_key = f"{fact.service or 'unknown'}::{fact.text.strip().lower()}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        def _work() -> list[Evidence]:
            matches: list[Evidence] = []
            tokens = [t for t in fact.text.lower().split() if len(t) > 4][:10]
            for root in self.roots:
                if not root.exists():
                    continue
                for path in root.rglob("*.md"):
                    try:
                        text = path.read_text(encoding="utf-8", errors="ignore").lower()
                    except OSError:
                        continue
                    if fact.text.lower() in text:
                        matches.append(Evidence(source=str(path), tier=2, anchor="full-text", confidence=0.9))
                        if len(matches) >= 5:
                            return matches
                        continue
                    overlap = sum(1 for token in tokens if token in text)
                    if overlap >= 3:
                        conf = min(0.8, 0.45 + (overlap * 0.05))
                        matches.append(Evidence(source=str(path), tier=2, anchor="token-overlap", confidence=conf))
                        if len(matches) >= 5:
                            return matches
            return matches

        results = self.executor.invoke(
            "fact-checker.local-source.search",
            f"fact={fact.id} roots={len(self.roots)}",
            _work,
        )
        self._cache[cache_key] = results
        return results
