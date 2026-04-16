from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import typer

from .chunking import chunk_files
from .batch_runner import run_chunked_parallel
from .engine import list_articles, load_facts, run_gap_analysis
from .models import AnalysisResult, ProposalDecision, RunState
from .policy import ToolPolicy
from .reports import build_markdown_report, grade_analysis
from .storage import CacheStore, RunStore
from .telemetry import ToolCallTracer
from .updater import apply_accepted_proposals, apply_proposals, build_proposals, load_proposals, save_proposals

app = typer.Typer(help="fact-check-v2 local CLI")


def _run_store(cache_db: Path) -> RunStore:
    run_db = cache_db.with_name("runs.db")
    return RunStore(run_db)


def _merge_chunk_results(chunk_results: list[AnalysisResult]) -> AnalysisResult:
    all_results = []
    article_paths: set[str] = set()
    facts_total = 0
    for chunk in chunk_results:
        all_results.extend(chunk.results)
        facts_total = max(facts_total, chunk.facts_total)
        article_paths.update(result.article_path for result in chunk.results)

    return AnalysisResult(
        generated_at=datetime.now(timezone.utc),
        facts_total=facts_total,
        article_count=len(article_paths),
        results=all_results,
    )


@app.command("gap-analyze")
def gap_analyze(
    facts: Path = typer.Option(..., exists=True),
    articles: Path = typer.Option(..., exists=True),
    output: Path = typer.Option(Path("out/analysis.json")),
    cache_db: Path = typer.Option(Path("out/claims.db")),
    source_root: list[Path] | None = typer.Option(None),
    trace: Path | None = typer.Option(None),
    strict_policy: bool = typer.Option(False),
) -> None:
    cache = CacheStore(cache_db)
    fact_items = load_facts(facts)
    article_files = list_articles(articles)
    tracer = ToolCallTracer(trace) if trace else None
    policy = ToolPolicy(strict=strict_policy) if strict_policy else None
    analysis = run_gap_analysis(
        fact_items,
        article_files,
        cache=cache,
        source_roots=source_root,
        policy=policy,
        tracer=tracer,
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(analysis.model_dump(mode="json"), indent=2), encoding="utf-8")
    typer.echo(f"Analysis saved: {output}")


@app.command("report")
def report(
    analysis: Path = typer.Option(..., exists=True),
    output: Path = typer.Option(Path("out/factcheck_report.md")),
) -> None:
    from .models import AnalysisResult

    payload = json.loads(analysis.read_text(encoding="utf-8"))
    parsed = AnalysisResult.model_validate(payload)
    grade = grade_analysis(parsed)
    markdown = build_markdown_report(parsed, grade)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    typer.echo(f"Report saved: {output}")


@app.command("propose-updates")
def propose_updates(
    analysis: Path = typer.Option(..., exists=True),
    output: Path = typer.Option(Path("out/proposals.json")),
) -> None:
    from .models import AnalysisResult

    payload = json.loads(analysis.read_text(encoding="utf-8"))
    parsed = AnalysisResult.model_validate(payload)
    proposals = build_proposals(parsed)
    save_proposals(proposals, output)
    typer.echo(f"Proposals saved: {output} ({len(proposals)} items)")


@app.command("apply-updates")
def apply_updates(
    proposals: Path = typer.Option(..., exists=True),
    mode: str = typer.Option("individual", help="individual|bulk"),
    id: str | None = typer.Option(None, help="Proposal id for individual mode"),
    min_risk: str | None = typer.Option(None, help="low|medium|high for bulk filtering"),
) -> None:
    items = load_proposals(proposals)
    applied = apply_proposals(items, mode=mode, proposal_id=id, min_risk=min_risk)
    typer.echo(f"Applied proposals: {applied}")


@app.command("batch-plan")
def batch_plan(
    articles: Path = typer.Option(..., exists=True),
    chunk_size: int = typer.Option(10, min=8, max=10),
) -> None:
    files = list_articles(articles)
    chunks = chunk_files(files, chunk_size=chunk_size)
    for idx, chunk in enumerate(chunks, start=1):
        typer.echo(f"Chunk {idx}: {len(chunk)} files")
        for path in chunk:
            typer.echo(f"  - {path}")


@app.command("batch-run")
def batch_run(
    facts: Path = typer.Option(..., exists=True),
    articles: Path = typer.Option(..., exists=True),
    output: Path = typer.Option(Path("out/batch_analysis.json")),
    cache_db: Path = typer.Option(Path("out/claims.db")),
    chunk_size: int = typer.Option(10, min=8, max=10),
    workers: int = typer.Option(4, min=1, max=16),
    source_root: list[Path] | None = typer.Option(None),
    trace: Path | None = typer.Option(None),
    strict_policy: bool = typer.Option(False),
) -> None:
    cache = CacheStore(cache_db)
    fact_items = load_facts(facts)
    article_files = list_articles(articles)
    tracer = ToolCallTracer(trace) if trace else None
    policy = ToolPolicy(strict=strict_policy) if strict_policy else None
    chunk_results = run_chunked_parallel(
        fact_items,
        article_files,
        cache=cache,
        chunk_size=chunk_size,
        workers=workers,
        source_roots=source_root,
        policy=policy,
        tracer=tracer,
    )

    payload = [result.model_dump(mode="json") for result in chunk_results]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    typer.echo(f"Batch analysis saved: {output} chunks={len(chunk_results)}")


@app.command("review-folder")
def review_folder(
    facts: Path = typer.Option(..., exists=True),
    articles: Path = typer.Option(..., exists=True),
    analysis_output: Path = typer.Option(Path("out/analysis_review.json")),
    report_output: Path = typer.Option(Path("out/factcheck_review.md")),
    proposals_output: Path = typer.Option(Path("out/proposals_review.json")),
    cache_db: Path = typer.Option(Path("out/claims.db")),
    chunk_size: int = typer.Option(10, min=8, max=10),
    workers: int = typer.Option(4, min=1, max=16),
    source_root: list[Path] | None = typer.Option(None),
    trace: Path | None = typer.Option(None),
    strict_policy: bool = typer.Option(False),
) -> None:
    """Fact-check a folder, create consolidated report/proposals, and wait for approval before apply."""
    cache = CacheStore(cache_db)
    fact_items = load_facts(facts)
    article_files = list_articles(articles)
    tracer = ToolCallTracer(trace) if trace else None
    policy = ToolPolicy(strict=strict_policy) if strict_policy else None

    if len(article_files) > chunk_size:
        chunk_results = run_chunked_parallel(
            fact_items,
            article_files,
            cache=cache,
            chunk_size=chunk_size,
            workers=workers,
            source_roots=source_root,
            policy=policy,
            tracer=tracer,
        )
        analysis = _merge_chunk_results(chunk_results)
    else:
        analysis = run_gap_analysis(
            fact_items,
            article_files,
            cache=cache,
            source_roots=source_root,
            policy=policy,
            tracer=tracer,
        )

    analysis_output.parent.mkdir(parents=True, exist_ok=True)
    analysis_output.write_text(json.dumps(analysis.model_dump(mode="json"), indent=2), encoding="utf-8")

    grade = grade_analysis(analysis)
    markdown = build_markdown_report(analysis, grade)
    report_output.parent.mkdir(parents=True, exist_ok=True)
    report_output.write_text(markdown, encoding="utf-8")

    proposals = build_proposals(analysis)
    save_proposals(proposals, proposals_output)

    run_id = str(uuid.uuid4())
    store = _run_store(cache_db)
    store.create_run(
        run_id,
        {
            "scope": str(articles),
            "facts_path": str(facts),
            "articles_path": str(articles),
            "analysis_path": str(analysis_output),
            "report_path": str(report_output),
            "proposals_path": str(proposals_output),
            "trace_path": str(trace) if trace else "",
            "notes": "Created by review-folder",
        },
        state=RunState.REVIEW_READY,
    )
    store.seed_proposals(run_id, [proposal.id for proposal in proposals])

    typer.echo(f"Review complete: {analysis_output}")
    typer.echo(f"Report ready: {report_output}")
    typer.echo(f"Proposals ready: {proposals_output}")
    typer.echo(f"Run ID: {run_id}")
    typer.echo("Awaiting approval. No file updates were applied.")


@app.command("run-status")
def run_status(
    run_id: str = typer.Option(..., help="Run identifier from review-folder"),
    cache_db: Path = typer.Option(Path("out/claims.db")),
) -> None:
    store = _run_store(cache_db)
    run = store.get_run(run_id)
    decisions = store.get_decisions(run_id)
    summary = {
        "run_id": run_id,
        "state": run["state"],
        "scope": run["scope"],
        "created_at": run["created_at"],
        "updated_at": run["updated_at"],
        "decision_counts": {
            "proposed": sum(1 for value in decisions.values() if value == ProposalDecision.PROPOSED),
            "accepted": sum(1 for value in decisions.values() if value == ProposalDecision.ACCEPTED),
            "rejected": sum(1 for value in decisions.values() if value == ProposalDecision.REJECTED),
            "deferred": sum(1 for value in decisions.values() if value == ProposalDecision.DEFERRED),
            "superseded": sum(1 for value in decisions.values() if value == ProposalDecision.SUPERSEDED),
        },
    }
    typer.echo(json.dumps(summary, indent=2))


@app.command("review-transition")
def review_transition(
    run_id: str = typer.Option(...),
    action: str = typer.Option(..., help="approve|request-revision|abort|queue"),
    note: str | None = typer.Option(None),
    cache_db: Path = typer.Option(Path("out/claims.db")),
) -> None:
    action_to_state = {
        "approve": RunState.APPROVED,
        "request-revision": RunState.REVISION_REQUESTED,
        "abort": RunState.ABORTED,
        "queue": RunState.QUEUED,
    }
    if action not in action_to_state:
        raise typer.BadParameter("action must be one of: approve, request-revision, abort, queue")

    store = _run_store(cache_db)
    store.transition(run_id, action_to_state[action], note=note)
    typer.echo(f"Run {run_id} transitioned to {action_to_state[action].value}")


@app.command("proposal-decision")
def proposal_decision(
    run_id: str = typer.Option(...),
    proposal_id: str = typer.Option(...),
    decision: str = typer.Option(..., help="accepted|rejected|deferred|superseded|proposed"),
    note: str | None = typer.Option(None),
    cache_db: Path = typer.Option(Path("out/claims.db")),
) -> None:
    valid = {status.value: status for status in ProposalDecision}
    if decision not in valid:
        raise typer.BadParameter("invalid decision")
    store = _run_store(cache_db)
    store.upsert_proposal_decision(run_id, proposal_id, valid[decision], note)
    typer.echo(f"Run {run_id} proposal {proposal_id} set to {decision}")


@app.command("apply-approved")
def apply_approved(
    run_id: str = typer.Option(...),
    proposals: Path = typer.Option(..., exists=True),
    min_risk: str | None = typer.Option(None, help="low|medium|high"),
    cache_db: Path = typer.Option(Path("out/claims.db")),
) -> None:
    store = _run_store(cache_db)
    run = store.get_run(run_id)
    if RunState(run["state"]) != RunState.APPROVED:
        raise typer.BadParameter("run must be in approved state before apply")

    proposal_items = load_proposals(proposals)
    decisions = store.get_decisions(run_id)
    for proposal in proposal_items:
        if proposal.id in decisions:
            proposal.status = decisions[proposal.id]

    store.transition(run_id, RunState.APPLYING, note="Applying accepted proposals")
    applied = apply_accepted_proposals(proposal_items, min_risk=min_risk)
    store.transition(run_id, RunState.FINALIZED, note=f"Finalized with {len(applied)} applied proposals")
    typer.echo(f"Applied proposals: {applied}")


@app.command("sandbox-test")
def sandbox_test(
    trace: Path = typer.Option(Path("out/tool_calls.jsonl")),
    strict: bool = typer.Option(True),
) -> None:
    policy = ToolPolicy(strict=strict)
    tracer = ToolCallTracer(trace)

    simulated_calls = [
        ("fact-checker", "run gap analysis", 18),
        ("mcp.learn.search", "query=azure load balancer", 56),
        ("web.fetch", "url=https://example.com", 31),
    ]

    violations = 0
    for tool_name, args_summary, latency in simulated_calls:
        time.sleep(0.01)
        allowed = policy.is_allowed(tool_name)
        status = "ok" if allowed else "blocked"
        message = "allowed by sandbox policy" if allowed else "blocked by sandbox policy"
        tracer.emit(tool_name, args_summary, status, latency, message)
        if not allowed:
            violations += 1

    if strict and violations > 0:
        raise typer.Exit(code=2)
    typer.echo(f"Sandbox test complete. Violations={violations} trace={trace}")


if __name__ == "__main__":
    app()
