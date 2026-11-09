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

2. **Run analysis**: Review the changed passages against the Microsoft Writing Style Guide using the PR URL, author, title, and file contents as context. Record each actionable suggestion with its file, line, original text, proposed replacement, and rationale.

3. **Write suggestions (REQUIRED)**: Produce a complete proposed replacement for each finding while preserving its technical meaning. Save the structured suggestions document to a user-confirmed location. Do not leave rewrite placeholders or incomplete recommendations.

4. **Present results**: Tell the user the file location, suggestion count, and remind them to evaluate in context

### Key gates
- Ground each finding in a specific passage and writing-style rule.
- Complete every proposed rewrite before presenting results.

### Edge cases
- **PR has no `.md` files changed**: Tell the user "No markdown files found in this PR — style review only applies to documentation files."
- **Zero suggestions returned**: Tell the user the PR looks clean — no style issues detected.
- **Review file write fails**: Surface the error and offer to display suggestions directly in chat instead.

**Scope:** Suggest edits for review; do not modify the pull request without the user's approval.
