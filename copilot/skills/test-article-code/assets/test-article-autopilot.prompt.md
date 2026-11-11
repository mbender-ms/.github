---
mode: agent
description: 'Test all runnable code in a Learn article end-to-end in autopilot (deletions and cleanup still require approval), then report findings and optionally open a fix PR. Pre-fills the common test-article-code variant.'
---

Test the runnable code in the target article by loading and following the `test-article-code` skill (`copilot/skills/test-article-code/SKILL.md`).

Pre-filled choices for this run:

- **Article:** ${input:article:Path to the article, or leave blank to use the open editor file}
- **Mode:** Autopilot — run all non-destructive commands back-to-back without pausing. **Deletions and cleanup always stop for explicit approval**, even in autopilot.
- **Tab order:** Run every Azure CLI command first; after they pass, ask before starting Azure PowerShell.
- **Prerequisites:** Check current state with me first (auth, tooling, resources) — I may have already done some. Don't re-run steps that are already satisfied.
- **Work item for fixes:** ${input:workitem:ADO work item ID for AB# linking, or leave blank to be asked later}

Follow the skill exactly:

1. Enumerate every code block (follow `[!INCLUDE]` files), grouped by tab.
2. Confirm prerequisites and authentication; map `<placeholders>` to real resource names, generating default names (`resource-group-test###`, `virtual-network-###`, `<resource-type>-###`) when I haven't supplied any, and show me the mapping before creating anything.
3. Run the commands per the mode above, echoing output and verifying results.
4. On any error, stop and report the command, exact error, root cause, and possible solutions.
5. When done, ask before cleaning up, then summarize results and documentation findings.
6. If I approve fixes, apply them end-to-end: feature branch from `upstream/main` → minimal edits → commit (no AB# in commit) → push to fork → draft PR against `MicrosoftDocs:main` with `AB#<id>` in the body → comment the PR link on the work item.
