from __future__ import annotations

from collections import Counter

from .models import AnalysisResult, GradeBreakdown, Verdict


def grade_analysis(analysis: AnalysisResult) -> GradeBreakdown:
    counts = Counter(r.verdict for r in analysis.results)
    total = max(analysis.facts_total * analysis.article_count, 1)
    present = counts.get(Verdict.PRESENT, 0)
    partial = counts.get(Verdict.PARTIAL, 0)
    missing = counts.get(Verdict.MISSING, 0)
    contradicted = counts.get(Verdict.CONTRADICTED, 0)
    unverifiable = counts.get(Verdict.UNVERIFIABLE, 0)

    score = int(
        max(
            0,
            100
            - (contradicted * 8)
            - (missing * 5)
            - (unverifiable * 4)
            - (partial * 2)
            + (present * 1),
        )
    )

    return GradeBreakdown(
        score=min(score, 100),
        present_ratio=present / total,
        contradicted_count=contradicted,
        missing_count=missing,
        unverifiable_count=unverifiable,
    )


def build_markdown_report(analysis: AnalysisResult, grade: GradeBreakdown) -> str:
    lines = []
    lines.append("# Fact Check Report")
    lines.append("")
    lines.append(f"Generated: {analysis.generated_at.isoformat()}")
    lines.append(f"Articles: {analysis.article_count}")
    lines.append(f"Facts: {analysis.facts_total}")
    lines.append("")
    lines.append("## Grade")
    lines.append(f"- Score: {grade.score}/100")
    lines.append(f"- Present ratio: {grade.present_ratio:.2%}")
    lines.append(f"- Missing: {grade.missing_count}")
    lines.append(f"- Contradicted: {grade.contradicted_count}")
    lines.append(f"- Unverifiable: {grade.unverifiable_count}")
    lines.append("")
    lines.append("## Future updates")
    lines.append("- Recheck facts tied to recently updated services weekly.")
    lines.append("- Prioritize missing/contradicted facts for next editorial sprint.")
    lines.append("")
    lines.append("## Detailed findings")
    for result in analysis.results:
        lines.append(
            f"- {result.article_path} | {result.fact_id} | {result.verdict.value} | {result.confidence:.2f} | {result.notes}"
        )
    return "\n".join(lines)
