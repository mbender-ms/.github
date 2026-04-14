---
mode: agent
description: "Check out a release branch locally, refresh it if it already exists, and optionally create a working branch for edits"
tools:
  - execute/runInTerminal
  - execute/getTerminalOutput
  - read/readFile
  - search/textSearch
  - search/fileSearch
  - todo
---

# Release branch workflow

Check out a named release branch locally from the target repo, refresh it if it already exists, and optionally create a separate working branch for edits.

---

## Inputs

| Input | Required | Default | Example |
|-------|----------|---------|---------|
| **Release branch name** | Yes | None | `release-preview-avnm-vwan` |
| **Repository** | No | `azure-docs-pr` | `azure-docs-pr`, `azure-docs-rest-apis` |
| **Next action after checkout** | No | Ask the user | `stop`, `create working branch` |
| **Working branch details** | No | Infer or ask if needed | `load-balancer`, `freshness-review`, `554195` |

Default to the `azure-docs-pr` repo when no repo is specified.

Resolve common repo aliases before matching a workspace folder:

| Alias | Target repo |
|-------|-------------|
| `docs-pr` | `azure-docs-pr` |
| `azure-docs-pr` | `azure-docs-pr` |
| `rest-apis` | `azure-docs-rest-apis` |
| `docs-rest-apis` | `azure-docs-rest-apis` |
| `azure-docs-rest-apis` | `azure-docs-rest-apis` |
| `github` | `.github` |
| `.github` | `.github` |
| `ai` | `AI` |
| `AI` | `AI` |

Recognize natural-language triggers such as `release branch <name>`, `create release branch <name>`, `create rb <name>`, and repo-qualified forms like `create release branch <name> <repo>` where `<repo>` can be a full repo name or one of the aliases above.

---

## Workflow steps

Execute steps in order. Stop at confirmation gates when required.

### Step 0 — Resolve the target repo and check current state

If the user does not specify a repo, target `azure-docs-pr`.

If the user specifies a repo, first resolve any alias to its canonical repo name, then switch to that repo before running Git commands.

Use the workspace folder that matches the repo name. If the repo name is ambiguous or not present in the workspace, ask the user to confirm the target path before proceeding.

```bash
cd <target-repo-path>
git branch --show-current
git status --porcelain
git remote -v
```

Use these checks to determine:
- whether the prompt is operating in the correct repo
- whether the working tree is clean enough to switch branches
- whether `upstream` exists and should be treated as the authoritative remote
- whether `origin` is the only available fallback remote

### Step 1 — Handle a dirty working tree (**confirmation gate**)

If `git status --porcelain` shows changes, do not switch branches automatically.

Ask the user how to proceed:
- stash changes
- commit changes first
- stop here

Do not continue until the user chooses one of those options.

### Step 2 — Resolve and verify the remote release branch

Prefer `upstream` when it exists. Otherwise use `origin`.

```bash
git ls-remote --heads <remote> <release-branch-name>
git fetch <remote> <release-branch-name>
```

If the remote branch is not found:
- tell the user the branch was not found on `<remote>`
- include the target repo name in the message
- offer to list matching remote `release-*` branches if helpful
- stop unless the user gives a different branch name

### Step 3 — Reuse or create the local release branch

Check whether the local branch already exists:

```bash
git show-ref --verify --quiet refs/heads/<release-branch-name>
```

If the local branch already exists:

```bash
git checkout <release-branch-name>
git branch --set-upstream-to=<remote>/<release-branch-name> <release-branch-name>
git pull --ff-only <remote> <release-branch-name>
```

If the local branch does not exist:

```bash
git checkout --track <remote>/<release-branch-name>
```

After checkout, confirm the result:

```bash
git branch -vv
```

### Step 4 — Ask what to do next (**confirmation gate**)

After the release branch is active locally in the target repo, ask the user which path to take:
- stop after creating the local tracking branch
- create a separate working branch for edits

If the user wants to stop, confirm success and end the workflow.

### Step 5 — Create a working branch for edits (optional)

If the user chooses a working branch, create it from the checked-out release branch.

Use the existing branch naming convention:

```bash
git checkout -b mbender-ms/<service>-<description>-<id>
```

- Omit `<id>` if no work item ID is provided.
- Infer the service and description when reliable.
- Ask the user for the missing parts when they cannot be inferred safely.

After creation, confirm that the new working branch is based on the release branch in the target repo and remind the user that any PR should target the release branch, not `main`, unless they say otherwise.

---

## Expected behavior

- Do not assume the release branch is already present locally.
- Default to `azure-docs-pr` when the repo is omitted.
- Accept repo aliases and normalize them before choosing a workspace folder.
- Do not commit, push, or create a PR as part of this workflow.
- Do not silently switch branches when the working tree is dirty.
- Prefer a separate working branch for edits instead of committing directly on the release branch.

---

## Error handling

| Error | Action |
|-------|--------|
| Repo not specified | Use `azure-docs-pr` |
| Repo alias provided | Resolve it to the canonical repo name before changing directories |
| Repo name not found in workspace | Ask the user to confirm the repo or path before proceeding |
| No `upstream` remote | Fall back to `origin` and say so |
| Release branch not found remotely | Report that it was not found and offer to list matching `release-*` branches |
| Local branch exists but pull cannot fast-forward | Stop and tell the user the local branch has diverged from the remote |
| Dirty working tree | Ask whether to stash, commit, or stop |
| Working branch details missing | Ask for the missing values before creating the working branch |