---
name: setup-repository
version: 1.0.0
category: Workflow
description: Set up and clone a Microsoft Docs repository. Silently checks authentication and Git config (configuring them if needed), then forks and clones. Works for first-time setup and for cloning additional repositories. Use this skill whenever the user wants to clone a repo, set up their environment, fork a repository, get started with a new doc set, configure Git, or asks about authentication setup - even if they don't mention "setup-repository" explicitly.
argument-hint: "[Learn article URL or repo name]"
---

## Set up and clone a repository

Follow these steps in order. Stop at any step that fails and surface the error.

### Step 1: Check authentication (silent)

The agent needs Azure CLI for ADO work item access and GitHub CLI for forking repos and creating PRs. Check both silently — only surface errors if something is broken.

Run both checks:

```bash
az account show --query user.name -o tsv 2>/dev/null && gh auth status 2>&1 | head -3
```

- If both pass → proceed silently, do not mention auth to the user.
- If `az account show` fails → tell the user:
  > **Azure CLI isn't signed in.** The agent needs this to identify your Microsoft identity for ADO work item access. Run `az login` in a terminal, then try again.
- If `gh auth status` shows "not logged in" → tell the user:
  > **GitHub CLI isn't authenticated.** This is needed to fork repos and create PRs. Run `gh auth login -s user` in a terminal, then try again.

### Step 2: Check and configure Git (silent)

Git identity is needed so commits are attributed correctly and PRs show the right author. Check if it's already set up before configuring.

```bash
git config --global user.email
```

- If a value is returned → Git is already configured, proceed silently.
- If empty → tell the user:
  > **Git isn't configured yet — setting it up now using your GitHub identity.**

  Then run:

  ```bash
  GITHUB_USER=$(gh api user --jq .login) && GITHUB_ID=$(gh api user --jq .id) && git config --global user.name "$GITHUB_USER" && git config --global user.email "${GITHUB_ID}+${GITHUB_USER}@users.noreply.github.com" && git config --global core.longpaths true && git config --global core.editor "code --wait" && echo "✅ Git configured: $GITHUB_USER / ${GITHUB_ID}+${GITHUB_USER}@users.noreply.github.com"
  ```

  Tell the user what was configured and why:
  > ✅ Git configured:
  > - **Name**: `{GITHUB_USER}`
  > - **Email**: `{GITHUB_ID}+{GITHUB_USER}@users.noreply.github.com` (GitHub noreply — keeps your personal email private in commit history)
  > - **Long paths**: enabled (required for deep folder structures on Windows)
  > - **Editor**: VS Code (used for commit messages)

### Step 3: Identify the repository

Microsoft Learn articles are backed by GitHub repos. The user may give a Learn URL (we extract the repo from the page's edit link) or a repo name directly. Most private repos use a `-pr` suffix.

Read VS Code setting `cda.team`.

- If `cda.team` is set, ask:
  > What do you want to clone for the **{cda.team}** team? You can give me a Learn article URL (e.g. `https://learn.microsoft.com/azure/expressroute/...`) or the repo name directly (e.g. `azure-docs-pr`).
- If `cda.team` is empty, keep the existing prompt:
  > What do you want to clone? You can give me a Learn article URL (e.g. `https://learn.microsoft.com/azure/expressroute/...`) or the repo name directly (e.g. `azure-docs-pr`).

**If given a Learn URL:**

Use `web/fetch` to fetch the page. Extract the GitHub edit link from the HTML — look for a pattern like `href="https://github.com/{org}/{repo}/blob/...` or `href="https://github.com/{org}/{repo}/edit/...`. Extract `org` and `repo` from that link.

Convert to the private repo:
- If `repo` already ends in `-pr`, use it as-is
- Otherwise append `-pr` (e.g. `azure-devops-docs` → `azure-devops-docs-pr`)

Verify the private repo exists:
```bash
gh api repos/{org}/{repo-pr} --jq .full_name 2>/dev/null || echo "NOT FOUND"
```

If not found, try without the `-pr` suffix as a fallback, or ask the user to confirm the repo name.

**If given a repo name directly:** Use `MicrosoftDocs` as the org. Use the name as-is.

### Step 4: Check for existing fork and generate commands

The fork-and-clone model lets content developers push to their own copy before creating a PR to the official repo. Check if they already have a fork to avoid unnecessary API calls.

```bash
gh api user/forks --jq '.[] | select(.parent.full_name == "{org}/{repo}") | .full_name' 2>/dev/null | head -1
```

Present the following to the user with explanations, and ask them to confirm before running:

> Here's what I'll do to set up `{org}/{repo}`. Review the steps and confirm when ready:
>
> **Step 1 — Create workspace folder** (skipped if it already exists)
> ```bash
> mkdir -p /c/GitHub && cd /c/GitHub
> ```
>
> **Step 2 — Fork the repo to your GitHub account** (safe to re-run — won't duplicate an existing fork)
> ```bash
> gh repo fork {org}/{repo} --clone=false
> ```
> This gives you a personal copy to push changes to before they go to the main repo.
>
> **Step 3 — Clone your fork locally** (`--filter=blob:none` skips file history blobs for a much faster clone on large repos like `azure-docs-pr`)
> ```bash
> git clone --filter=blob:none https://github.com/$(gh api user --jq .login)/{repo}.git
> ```
>
> **Step 4 — Add the upstream remote** (so you can sync with the official MicrosoftDocs repo)
> ```bash
> cd {repo} && git remote add upstream https://github.com/{org}/{repo}.git
> ```
> After this, `origin` points to your fork and `upstream` points to the official repo.

After confirmation, execute each command and wait for it to complete before running the next.

### Done

Tell the user:
- Repository cloned to: `/c/GitHub/{repo}` ✅
- Remotes: `origin` → their fork, `upstream` → `{org}/{repo}` ✅

They can now start their first session with "@cda".
