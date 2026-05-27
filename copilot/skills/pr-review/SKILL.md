---
name: pr-review
version: 1.0.0
displayName: PR Review
category: Review
description: Review a pull request for Microsoft Writing Style Guide compliance. Use when the user says "review this PR", "check PR #N", "run a style review", "style check", "how does this PR look?", "check for style issues", or shares a PR URL and asks for feedback. Also trigger when the user mentions reviewing another author's documentation changes for quality before approving.
argument-hint: "[PR URL or PR number]"
relevant-lesson-tags: [pr-review, style-guide, microsoft-writing-style, editorial]
---

## PR review workflow

When user asks to review a PR, this skill runs a systematic style analysis on changed markdown files and produces a structured suggestions document.

### Steps

1. **Fetch files**: Get changed `.md` files via `pull_request_read` (`method: "get_files"`), then read each file's content via `get_file_contents` (`ref: "refs/pull/{pr_number}/head"`)

2. **Run analysis**: Call `generate_pr_review` with the file contents, PR URL, author, and title

3. **Process rewrites (REQUIRED)**: The style engine flags some violations (passive voice, dangling modifiers) but can't deterministically produce the corrected text — it leaves `[AGENT: Rewrite this line — {hint}]` markers that you must resolve. Delivering a review file with unresolved markers looks broken to the user and makes the review unusable. For EACH item in `suggestions_needing_rewrite`:
   - Read the `original_text` and `hint` from the response
   - Write a corrected version based on the hint (e.g., passive → active voice)
   - Use `replace_string_in_file` on the review file to replace the `[AGENT: ...]` marker + original text with your corrected version

4. **Present results**: Tell the user the file location, suggestion count, and remind them to evaluate in context

### Key gates
- `generate_pr_review` required for style analysis
- ALL `[AGENT: ...]` rewrite markers must be processed before presenting results — if the file still has markers, the review is incomplete

### Edge cases
- **PR has no `.md` files changed**: Tell the user "No markdown files found in this PR — style review only applies to documentation files."
- **Zero suggestions returned**: Tell the user the PR looks clean — no style issues detected.
- **Review file write fails**: Surface the error and offer to display suggestions directly in chat instead.

**Need details?** → `get_workflow_example workflow_type='pr-review'`
