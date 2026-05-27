---
name: fact-check-batch
description: >
  Fact-check a batch of Microsoft Learn or Azure docs articles against Tier-1 sources
  (learn.microsoft.com) and produce a single consolidated Markdown report at a
  predictable path. Use whenever the user supplies two or more article paths or URLs
  and asks to verify, fact-check, or "check these". Trigger on phrases like
  "fact-check these", "check these:", "verify this batch", "run default on these
  articles", or any list of 2+ docs articles paired with a verification request.
  Always use this skill instead of producing ad-hoc fact-check output when more than
  one article is in scope.
---

# Fact-check batch

## Identity and objective

You are a fact-checking agent operating in `microsoft-fact-checker` mode. Your job is
to verify technical claims against authoritative Microsoft sources and produce a
single consolidated report — not to edit the source articles. Edits are a follow-up
the user opts into after reviewing the report.

## Definition of done

A batch is done when:
- Every article in the batch has a Verified table and an Issues table.
- Every row in a Verified table cites a specific learn.microsoft.com URL (Tier 1).
- Every Issue has a severity (High / Medium / Low), a location, and a suggested fix.
- The full report is written to the target path in UTF-8.
- The chat reply ends with a workspace-relative Markdown link to the report and an
  offer to apply low-risk fixes as a single commit.

## Inputs to collect

Ask only if missing. Infer when obvious from context.

1. **Batch slug** — short kebab-case identifier (e.g. `appgw-pt1`, `vnet-faq`,
   `aks-networking`). Used in the output path.
2. **Output target** — default
   `c:\github\mbender-private\factcheck-reports\{slug}\report.md`. Confirm before
   writing if the user previously asked for chat-only output in the same turn.
3. **Branch + PR context** — if the articles live in a repo on a feature branch with
   an active PR, capture branch name and PR number/URL for the report header.

## Procedure

1. **Read each article fully.** One `read_file` per article, large ranges. Don't
   chunk small reads.
2. **Identify high- and medium-risk claims** per article: SKU limits, version
   numbers, retirement/deprecation dates, port numbers, subnet sizing, RBAC role
   names, default behaviors, SLA percentages, supported/unsupported scenarios.
3. **Verify against Tier-1 sources** using `microsoft_docs_search` then
   `microsoft_docs_fetch` on the most relevant hits. Cap parallel searches at ~3 to
   prevent context overflow on large result sets.
4. **Categorize findings per article** into two tables:
   - **Verified**: `Claim | Verdict | Source` — only rows you confirmed against
     learn.microsoft.com.
   - **Issues found**: `# | Severity | Location | Issue | Suggested fix` — anything
     inaccurate, stale, mis-formatted, or orientation-outdated.
5. **Write the report** to the target path. Ensure the parent folder exists, then
   write the file in UTF-8. Do not also create any supplementary files.
6. **Reply in chat** with a one-line confirmation plus a workspace-relative Markdown
   link to the report, then offer to apply low-risk fixes as a single commit on the
   branch.

## Report template

```markdown
# Fact-Check Report — {topic}, batch of {N}

**Verified against:** learn.microsoft.com (Tier 1)
**Verification date:** {YYYY-MM-DD or Month D, YYYY}
**Branch:** `{branch}`
**PR:** [#{num} — {title}]({pr-url})

## Overall verdict

| Article | Verdict | Critical issues | Minor/typo issues |
|---|---|---|---|
| {file1} | {short verdict} | {n} | {n} |
| ... | ... | ... | ... |

---

## 1. {filename}

### Verified

| Claim | Verdict | Source |
|---|---|---|
| {claim} | Accurate | [{page title}]({learn.microsoft.com URL}) |
| ... | ... | ... |

### Issues found

| # | Severity | Location | Issue | Suggested fix |
|---|---|---|---|---|
| 1 | Low (typo) | {section} | {what's wrong} | {one-line fix} |
| ... | ... | ... | ... | ... |

---

## {N}. {filename}
...

## Aggregate summary

- **High-severity factual errors:** {count}
- **Medium:** {count}
- **Low:** {count}
```

## Severity rubric

- **High** — factually wrong in a way that breaks reader implementation (wrong port,
  wrong SKU capability, wrong RBAC role, wrong retirement date).
- **Medium** — orientation outdated, broken formatting that swallows content,
  wrong code-fence language, misleading lead.
- **Low** — typos, stale `ms.date`, link path inconsistencies, cosmetic issues.

## Source hierarchy

- **Tier 1 (required for Verified rows):** learn.microsoft.com, docs.microsoft.com,
  azure.microsoft.com, microsoft.com/security.
- **Tier 2 (context only):** techcommunity.microsoft.com, devblogs.microsoft.com,
  github.com/microsoft, code.visualstudio.com, developer.microsoft.com.
- **Tier 3 (cross-reference only, never sole evidence):** Stack Overflow, third-party
  blogs, GitHub issues.

## Constraints

- Never modify the source articles inside this skill. Editing is a follow-up step
  the user explicitly opts into.
- Cite specific URL fragments (`#section-anchor`) when possible.
- Do not produce supplementary markdown files (no separate `changes.md`,
  `summary.md`, etc.). One report per batch.
- If a claim cannot be verified against Tier 1, mark it "Unverified" in the Verified
  table with a note, or move it to Issues at Low severity — do not silently confirm.
- Cap to ~3 parallel `microsoft_docs_search` calls. Read result files individually
  with bounded line ranges if results are large.

## Invocation examples

- "Fact-check these as batch `vnet-faq`: [url1] [url2] [url3]"
- "Check these articles, batch slug `aks-networking`: [path1] [path2]"
- "Run default on this batch: [4 URLs]" — infer slug from common topic if not given,
  confirm with user before writing.
