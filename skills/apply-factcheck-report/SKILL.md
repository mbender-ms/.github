---
name: apply-factcheck-report
description: >
  Apply suggested fixes from a fact-check report produced by the fact-check-batch
  skill. Use when the user says "apply changes from report", "apply the fixes",
  "apply low-risk fixes from {path}", "apply fact-check report at {path}", or
  hands off a fact-check report path with instructions to edit articles.
  Defaults to Low-severity-only as a single commit, never pushes. Always use this
  skill — never manually parse a fact-check report and edit articles ad-hoc.
---

# Apply fact-check report

## Identity and objective

You are an applier, not a re-verifier. The report is the source of truth. Read it,
apply mechanical fixes per its "Suggested fix" column, and stop. Do not re-verify
claims against learn.microsoft.com — that already happened upstream.

## Definition of done

A run is done when:
- Every in-scope (matching severity filter) Issue row was either applied or
  explicitly skipped with a reason.
- All edits land in one staged commit on the report's named branch.
- The chat reply lists Applied / Skipped / Needs-review with file links.
- Nothing was pushed. The user pushes themselves.

## Inputs to collect

Ask only if missing.

1. **Report path** — required. Read it first; everything else can be inferred.
2. **Severity filter** — default `Low`. Accept `Low`, `Low+Medium`, or `All`.
3. **Branch** — read from the report header. If the current branch differs, stop
   and ask before switching.
4. **Article root** — infer from the report's per-article filenames + the active
   workspace folders. Confirm if ambiguous.

## Procedure

1. **Read the report** in full (`read_file`, large range). Parse each article
   section's Issues table.
2. **Classify each in-scope row** as:
   - **Apply** — mechanical, unambiguous text replacement (typo, unclosed
     backtick, wrong code-fence language, link path swap, stray character).
   - **Needs-review** — orientation rewrites, section reordering, anything where
     "Suggested fix" describes intent rather than exact replacement text.
   - **Skip** — out of severity scope, or already applied.
3. **Verify branch**: confirm the report's branch matches the current checkout
   for the target repo. If not, stop and ask.
4. **Apply edits** per article using `multi_replace_string_in_file`:
   - Group all edits for one article into one call.
   - Each `oldString` must include 3-5 lines of surrounding context per repo
     convention.
   - Read the article first if you don't already have the exact context.
5. **Stage and commit** with `git add` + `git commit` (no push):
   - Message: `Fact-check fixes from {report-folder} ({severity})`
   - Example: `Fact-check fixes from appgw-pt1 (Low)`
6. **Reply in chat** with three sections:
   - **Applied** — file + brief description of each change, as Markdown links.
   - **Needs-review** — items skipped because they require judgment, with the
     report row reference so the user can address them manually.
   - **Skipped** — out-of-scope items (briefly).
7. End with the commit SHA and a reminder that nothing was pushed.

## Mechanical-fix heuristics

Apply automatically:
- Typos with exact "from → to" in the Suggested fix.
- Missing/extra characters (closing backticks, stray asterisks, double spaces).
- Code-fence language label swaps (`azurecli-interactive` → `azurepowershell`).
- Link path swaps where both old and new paths are quoted in the fix.
- `ms.date` updates if the report explicitly lists the new date.

Send to Needs-review:
- "Reorder", "lead with", "demote", "refresh orientation", "rewrite section".
- Any fix that requires choosing between multiple valid replacements.
- Any fix touching code samples beyond a single token.

## Constraints

- Never modify articles outside the report's scope.
- Never auto-apply High severity — even if requested. Always list as
  Needs-review and ask.
- Never push. Never force-push. Never amend a published commit.
- Do not touch `ms.date` unless the report explicitly says to.
- Do not run linters, formatters, or markdown auto-fixers that touch lines
  outside the report's scope.
- One commit per run. If the user wants multiple commits, they'll say so.

## Invocation examples

- "Apply the fact-check report at `c:\github\mbender-private\factcheck-reports\appgw-pt1\report.md`"
- "Apply changes from report — Low only"
- "Apply Low+Medium fixes from `{path}`"
- "Apply fact-check report" (with report path in editor context or recent chat)
