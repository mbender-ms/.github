---
name: uat-feedback
displayName: UAT feedback
version: 1.0.0
category: Testing
hidden: false
description: Capture structured UAT (User Acceptance Testing) feedback into a per-tester monthly markdown file, optionally filing a GitHub issue after investigation. Use ONLY when the user explicitly says "UAT feedback", "file UAT bug", "UAT testing note", "UAT observation", or "UAT agent issue". Do NOT trigger on generic phrases like "file a bug" or "this doesn't work" — those should route to the CDA bug-reporting tool (mcp_cda_report_bug) instead.
argument-hint: 'brief description of the UAT feedback (e.g., "create-pr skipped style fixes")'
relevant-lesson-tags: [uat, feedback, testing, cda-extension]
user-invocable: true
disable-model-invocation: false
---

# UAT Feedback Skill

Capture structured tester feedback during CDA UAT (User Acceptance Testing). Each entry is appended to a monthly markdown file in `~/.copilot/cda/uat/` and can optionally be filed as a GitHub issue against `duongau/cda-extension`.

**Invocation:**
- `/uat-feedback create-pr skipped style fixes` — Start a new feedback entry
- `/uat-feedback` — Start a guided conversation
- Natural-language triggers (must include the word "UAT"): "UAT feedback", "file UAT bug", "UAT testing note", "UAT observation", "UAT agent issue"

**Important — Do NOT collide with `mcp_cda_report_bug`:**

The CDA MCP server has a separate `mcp_cda_report_bug` tool that files Bug work items against the **cda-cortex ADO project** for general bug reporting. This skill is different: it captures **UAT-only** feedback into a local markdown file and optionally files **GitHub issues** against `duongau/cda-extension`.

To avoid confusion, this skill **only triggers on phrases that explicitly include "UAT"**. Generic phrases like *"file a bug"*, *"this doesn't work"*, or *"observation"* should route to `mcp_cda_report_bug` instead.

**Investigate before logging:**

Even with the UAT keyword, investigate the issue first by asking clarifying questions and gathering context. Only log a UAT entry once the issue is well-understood and the user explicitly confirms.

---

## Step 1: Restate and confirm

When triggered, restate what the user reported in your own words and ask for confirmation:

> "It sounds like {summary}. Want me to capture this as UAT feedback?"

If the user says no or pivots, stop. Don't log anything.

If yes, continue.

## Step 2: Investigate

Probe for missing detail. Skip questions the user already answered.

1. **What were you doing?** — Which skill, command, or workflow was active?
2. **What did you expect?** — The intended behavior.
3. **What actually happened?** — The observed behavior.
4. **Steps to reproduce** — Minimal sequence to trigger the issue (bugs only).
5. **Severity** — Critical / High / Medium / Low (bugs only).
6. **Related skill or feature** — e.g., `create-pr`, `session-summary`, sidebar, MCP server.

For agent behavior issues, also ask:
- Was the agent's response wrong, off-topic, or misleading?
- Does the user have a chat exchange ID or timestamp to reference?

For UX observations, ask:
- What did you expect the UI to do?
- Is this a friction point or a missing affordance?

## Step 3: Categorize

Pick one of the fixed categories. If ambiguous, ask the user to choose.

- **Bugs** — Something broken or incorrect
- **Feature requests** — New capability the user wants
- **UX observations** — Friction, confusion, missing affordances
- **Testing notes** — General observations during UAT (not a bug or request)
- **Agent behavior issues** — Agent gave wrong, misleading, or off-topic responses

## Step 4: Auto-capture metadata

Gather these without asking the user:

- **Timestamp**: Current ISO datetime (e.g., `2026-05-04T10:30:00`)
- **Extension version**: Read from `~/.vscode/extensions/cda-extension-*/package.json` (or use the version visible in the CDA sidebar). If unsure, ask once: *"What CDA extension version are you on?"*
- **Tester alias**: Read `cda.alias` from VS Code settings. Falls back to `cda.userName` or "unknown".

## Step 5: Ask about GitHub issue filing

> "File this as a GitHub issue in `duongau/cda-extension`?"

If **yes**:
- Build a clear title (e.g., `[UAT] {category}: {short description}`)
- Build a body using the same structured format as the entry below
- Add labels based on category:
  - Bugs → `bug`, `uat`
  - Feature requests → `enhancement`, `uat`
  - UX observations → `ux`, `uat`
  - Testing notes → `uat`
  - Agent behavior issues → `agent-behavior`, `uat`
- Call `mcp_github_create_issue` with `owner: "duongau"`, `repo: "cda-extension"`, the title, body, and labels
- Capture the returned issue number and URL

If **no**, set the GitHub issue field to `Not filed`.

## Step 6: Append to the monthly file

### File location and naming

`~/.copilot/cda/uat/uat-feedback-{alias}-{YYYY-MM}.md`

- One file per tester per calendar month (monthly rollover)
- Create the directory if it doesn't exist
- If the file doesn't exist for the current month, create it with this header:

  ```markdown
  # UAT Feedback — {alias} — {YYYY-MM}

  Tester: {alias}
  Period: {YYYY-MM}

  ---
  ```

### Entry schema

Append to the end of the file:

```markdown
## {timestamp} — {category}: {short title}

- **Extension version**: {version}
- **Related skill/feature**: {skill name or "n/a"}
- **Severity**: {Critical/High/Medium/Low — bugs only, omit otherwise}
- **GitHub issue**: [#{N}]({url}) or "Not filed"

### Description

{What the user reported, refined after the investigation in Step 2.}

### Steps to reproduce

1. {step}
2. {step}

### Expected vs. actual

- **Expected**: {expected behavior}
- **Actual**: {actual behavior}

---
```

Omit empty sections. For non-bugs, the "Steps to reproduce" and "Severity" lines can be removed.

## Step 7: Confirm

After writing the entry, tell the user:

> ✅ UAT feedback logged to `~/.copilot/cda/uat/uat-feedback-{alias}-{YYYY-MM}.md`
> {If filed} 🐛 GitHub issue: [#{N}]({url})
> {If not filed} 📝 Not filed as GitHub issue.
>
> Want to log another, or are we done?

---

## Important rules

- **Investigate before logging.** Never silently capture chat content as feedback. Always restate, confirm, and probe.
- **One entry per issue.** If the user reports two distinct problems, run the flow twice.
- **Don't aggregate.** This skill writes individual entries only. The user (or their agent) can aggregate across testers separately.
- **Hidden post-UAT.** Currently `hidden: false` so the skill is visible during the testing phase. After UAT concludes, flip the frontmatter to `hidden: true` and bump the version — the extension's `cda.uatMode` setting (default `true`) will keep it visible for users who opt into UAT mode, while regular users see it disappear from the sidebar. The skill remains invocable by the model either way.
- **Use `mcp_github_create_issue`** for GitHub filing — never `gh` CLI or other tools.
- **Always include the extension version** — the team needs it to triage which build the issue applies to.
