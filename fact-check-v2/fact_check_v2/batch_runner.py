from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .chunking import chunk_files
from .engine import run_gap_analysis
from .models import AnalysisResult, FactInput
from .policy import ToolPolicy
from .storage import CacheStore
from .telemetry import ToolCallTracer


def run_chunked_parallel(
    facts: list[FactInput],
    articles: list[Path],
    cache: CacheStore,
    chunk_size: int = 10,
    workers: int = 4,
    source_roots: list[Path] | None = None,
    policy: ToolPolicy | None = None,
    tracer: ToolCallTracer | None = None,
) -> list[AnalysisResult]:
    chunks = chunk_files(articles, chunk_size=chunk_size)

    def _run(chunk: list[Path]) -> AnalysisResult:
        return run_gap_analysis(
            facts,
            chunk,
            cache=cache,
            source_roots=source_roots,
            policy=policy,
            tracer=tracer,
        )

    results: list[AnalysisResult] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_run, chunk) for chunk in chunks]
        for future in as_completed(futures):
            results.append(future.result())
    return results
