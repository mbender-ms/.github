---
name: refine-pr
displayName: Refine PR description
version: 1.0.0
category: Workflow
user-invocable: true
description: Enhance a PR description with gold-standard staged article links, per-commit change sections, and validated bookmark anchors. Use when the user says "add staged articles", "refine the PR", "enhance the PR description", "yes" after being offered staged links, or wants a polished PR with staging URLs for every changed section. Also trigger when the baseline create-PR workflow completes and the agent suggests refining — always load this skill before adding staged articles or per-commit sections to a PR.
argument-hint: "[PR number]"
relevant-lesson-tags: [pr-description, staged-articles, refine-pr, create-pr]
---

## Refine PR — gold-standard enhancement

This skill transforms a baseline PR description into a gold-standard format. What it adds depends on the PR type:

- **Docs PR** (only .md/.yml files): Staged article links with `?view=` and `#bookmark`, per-commit change sections with inline staging links
- **Code PR** (.ts/.js/.py etc.): Per-commit change sections with what/why detail, test results summary
- **Mixed PR** (docs + code): Both staging links (for articles) and test details (for code)

**Architecture:** Refinement skill — runs AFTER PR creation when the PR number is available. The baseline create-PR workflow produces a GOOD PR. This skill makes it GREAT.

**Reference:** See `skills/refine-pr/references/gold-standard-example.md` for the target format.

---

### Phase 1: Gather context

1. Get PR number — from conversation context or ask user
2. `pull_request_read` — get existing PR body, title, head branch
3. `git log --oneline origin/main..HEAD` — get all commits on the branch
4. `git log --format="%H %s" origin/main..HEAD` — get commit SHAs and messages for per-commit sections
5. Determine PR type from changed files:
   - All `.md`/`.yml`/`.yaml` → **docs** (add staged articles, skip Testing)
   - All `.ts`/`.js`/`.py`/`.cs` etc. → **code** (add Testing, skip staged articles)
   - Mix of both → **mixed** (add staged articles for .md files, add Testing for code)

### Phase 2: Analyze changes per commit

For each commit (group logically — feedback rounds can be combined):

6. `git show --stat {sha}` — get files changed in this commit
7. For each changed file (staging links apply to `.md` files only):
   - `head -10 {file}` — extract `title:` from YAML frontmatter (for Staged articles link text)
   - `grep -n "^## \|^### \|^#### " {file}` — get all headings in current file
   - `git diff {sha}~1..{sha} -- {file}` — identify which headings were added/modified
   - Build staging URL: `https://review.learn.microsoft.com/en-us/{url-path}?view={view}&branch=pr-en-us-{PR}#{bookmark}`

### Phase 3: Validate and resolve URLs (docs/mixed PRs only)

8. For each staging URL:
   - Convert heading to bookmark: lowercase, spaces → hyphens, remove special chars
   - Verify bookmark exists in current file headings (not the diff — the actual file)
   - Resolve URL path: check if repo folder path matches staging URL path (OPS can remap)
   - Add `?view={product-view}` param if the docset requires it

9. Determine `view` param:
   - Check `docfx.json` or `breadcrumb/toc.yml` in the repo for the moniker/view value
   - If unclear, check an existing live article from the same folder
   - Common values: `azuresql`, `sql-server-ver16`, `azure-devops-rest-7.1`

### Phase 4: Build gold-standard body

10. Construct the enhanced PR body. Include sections based on PR type:

**Docs PR:**
```markdown
## Summary
{Preserve from original PR body}

## Staged articles
1. [Article H1 Title](https://review.learn.microsoft.com/en-us/{path}?view={view}&branch=pr-en-us-{PR}#{bookmark})

## Changes

### Commit 1: {commit message} ({file count} files, +{additions}/-{deletions})

**1. {relative/path/to/file.md}**
- Added [{Heading text}]({staging-url}#{bookmark}) section with {brief description}
- Updated [{Heading text}]({staging-url}#{bookmark}) with {what changed}

---

## Related work items
{Preserve from original PR body — AB# links}

{RAI notice — preserve verbatim}
```

**Code PR:**
```markdown
## Summary
{Preserve from original PR body}

## Changes

### Commit 1: {commit message} ({file count} files, +{additions}/-{deletions})

**1. {relative/path/to/file.ts}**
- {What changed and why}

---

## Testing
{Test results or verification steps}

## Related work items
{Preserve from original PR body — AB# links}

{RAI notice — preserve verbatim}
```

**Mixed PR:** Use code PR structure, but add `## Staged articles` for any changed `.md` files and include staging links in their change bullets.

### Phase 5: Update PR and WI

11. Show the enhanced body to user for review
12. After confirmation → `update_pull_request` with the full enhanced body
13. `wit_get_work_item` → update `## PR info` section with all staged article links → `wit_update_work_item` (format: "markdown")

---

### Format rules

- **Staged articles** (docs/mixed only): One entry per changed article. Link text = article H1 title from frontmatter. URL includes `?view=` and `#bookmark` to the most relevant heading changed.
- **Per-commit sections**: Group commits logically. Feedback rounds can be labeled "Edits based on feedback".
- **Per-file bullets**: One bullet per distinct change. For docs PRs, EVERY bullet includes a staging link with bookmark anchor. For code PRs, describe what changed and why.
- **Bookmark validation** (docs only): Run `grep` on the actual file to get real headings. Convert to bookmarks. Never guess.
- **URL path verification** (docs only): Staging URL path may differ from repo path. Verify by checking an existing live article from the same folder.
- **Testing** (code/mixed only): Include test results or verification steps. Not needed for docs-only PRs.
- **Preserve original sections**: Summary, Related work items, and RAI notice from the original body must be preserved verbatim.
- **Section order**: Docs: Summary → Staged articles → Changes → Related work items → RAI. Code: Summary → Changes → Testing → Related work items → RAI.

---

### Save-again enhancement

When the user pushes more commits to a branch with an existing refined PR:

1. `pull_request_read` — get current body
2. Parse existing commit sections from the body
3. Identify NEW commits not yet in the body
4. Build new commit sections for the new commits only
5. APPEND new commit sections before the `---` separator (don't overwrite existing ones)
6. Re-validate ALL staging links (headings may have changed across commits)
7. Regenerate Staged articles section (may have new files)
8. `update_pull_request` with the merged body

---

### Edge cases

- **Single-file PR**: Skip per-commit structure if there's only 1 commit with 1 file. Use simplified format.
- **Non-article files**: Files like `toc.yml`, `zone-pivot-groups.yml`, or includes — mention them but don't build staging links.
- **Repo path ≠ URL path**: Always verify. Common remaps: `help-content/` → `/help/`, `docs/` → root path.
- **Multiple docsets in one repo**: Check which `docfx.json` covers the changed files to determine the correct `view` param.
- **PR with 50+ files**: Summarize by folder/area instead of per-file bullets. Link to the most important sections only.
