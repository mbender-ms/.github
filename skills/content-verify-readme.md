# Content Verification Skill Suite

A three-skill system for verifying AI-generated documentation against the Microsoft Writing Style Guide and a 30-rule AI anti-pattern checklist. Designed for the `mbender-ms/.github` agent fleet.

---

## Skills overview

| Skill | Job | Input | Output |
|---|---|---|---|
| `content-verification` | Runs the 30-rule anti-pattern pass on one article | Single `.md` file | Structured YAML change log |
| `verification-reporter` | Formats a change log into a Markdown PR report | YAML change log | Markdown report file |
| `content-verification-batch` | Orchestrates verification across a folder of articles | Folder path | Per-article reports + batch summary + draft PRs |

The skills are designed to compose — `content-verification-batch` calls the other two as subagents. Each skill can also be invoked independently.

---

## Directory structure

```
mbender-ms/.github/
└── skills/
    ├── content-verification/
    │   ├── SKILL.md
    │   └── references/
    │       └── ai-writing-antipatterns.csv
    ├── verification-reporter/
    │   └── SKILL.md
    └── content-verification-batch/
        └── SKILL.md
```

---

## The anti-pattern checklist

`ai-writing-antipatterns.csv` is the shared reference for all three skills. It contains 30 rules grounded in the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/) and AI writing pattern research from Ethan Mollick, Simon Willison, Chip Huyen, and Nate B. Jones.

**CSV columns:** `id, anti_pattern, category, description, agent_instruction, bad_example, good_example, source_basis`

The `agent_instruction` column is the operative field — it contains the specific directive the agent executes during a verification pass.

**Priority tiers:**

| Tier | Rows | Anti-patterns | When to apply |
|---|---|---|---|
| 1 — High | 1, 2, 3, 7, 16, 19 | Sycophantic openers, throat-clearing, banned word list, passive agent omission, hollow CTAs, landscape openers | Always |
| 2 — Medium | 5, 9, 12, 13, 15, 17, 20, 22 | Em-dash overuse, listicle brain, second-person inconsistency, buzzword stacking, summary restatement, please-note overuse, redundant pairs, qualification stacking | 200+ word articles |
| 3 — Low | All remaining | Vague intensifiers, false balance, generic examples, nested parentheticals, capitalization, title case, apology filler, nominalization | Formal/published content |

---

## Usage

### Single article — manual

In Copilot Chat or Copilot CLI:

```
Run a content verification pass on /articles/azure-networking/design-guide.md
```

The agent loads `content-verification`, runs the 30-rule pass, then calls `verification-reporter` to produce a Markdown report.

### Single article — generate PR report

```
Verify /articles/azure-networking/design-guide.md and create a PR report
```

Output: `verification-report-design-guide-[YYYY-MM-DD].md` written to the article's directory.

### Folder — batch run via /fleet

Requires GitHub Copilot CLI with `/fleet` support.

```
/fleet verify content in /articles/azure-load-balancer
```

Or for background execution with automatic draft PR creation:

```
/delegate /fleet verify content in /articles/azure-load-balancer
```

**What happens:**
1. Skill discovers all eligible `.md` files in the folder
2. Chunks into batches of max 9 articles
3. Dispatches one `/fleet` call per batch — subagents run in parallel within each batch
4. Each subagent runs `content-verification` + `verification-reporter` on its article
5. Creates one draft PR per batch (max 9 articles per PR)
6. Creates a standalone summary PR with scoreboard and pattern trends

### Severity-filtered pass

To run only high-priority checks (faster, lower token cost):

```
/fleet verify content in /articles/azure-load-balancer severity:high
```

Or high and medium only:

```
/fleet verify content in /articles/azure-load-balancer severity:high,medium
```

### Dry run — discover articles without verifying

```
verify content in /articles/azure-load-balancer dry_run:true
```

Returns the article list and batch plan without executing any verification.

---

## Output reference

### Per-article report

**Location:** `[article-directory]/verification-reports/[YYYY-MM-DD]/[article-slug]-report.md`

**Contents:**
- Summary table: findings by severity
- Findings grouped by severity tier (High → Medium → Low)
- Each finding: pattern name, "what this signals" (plain language), findings table with line numbers and suggested revisions
- Bulk patterns (5+ instances): representative examples table + full locations table

### Batch summary report

**Location:** `[scanned-folder]/verification-reports/[YYYY-MM-DD]/batch-summary.md`

**Contents:**
- Scoreboard: all articles sorted by total findings
- Pattern trends: anti-patterns appearing in 3+ articles (runs < 50) or 5+ articles (runs ≥ 50)
- Interpretation note: what the dominant patterns suggest about the authoring workflow
- Not run log: articles that failed with error messages

### Draft PRs

| PR | Branch | Contains |
|---|---|---|
| Batch PR (one per batch) | `verification/[YYYY-MM-DD]-batch-[N]` | Article reports for that batch (max 9) |
| Summary PR (always standalone) | `verification/[YYYY-MM-DD]-summary` | `batch-summary.md` only |

---

## Report reading guide

Reports are written for content developers who are deep SMEs in Microsoft documentation authoring. Each finding includes a **"What this signals"** field — a plain-language description of the reader experience, not a rule citation.

**How to use a report in PR review:**

1. Check the summary table first — High findings are the priority
2. For bulk patterns, review the "All locations" table to understand scope before editing
3. "Consider changing to" suggestions are starting points — your voice and judgment override the checklist
4. Accept, modify, or reject each finding. The report does not write back to the article

---

## `copilot-instructions.md` integration

Add this block to `.github/copilot-instructions.md`:

```markdown
## Content verification gate

All documentation drafts, release notes, how-to articles, and procedure guides
require a content verification pass before delivery.

Skills:
- skills/content-verification/ — runs the 30-rule AI anti-pattern pass (single article)
- skills/verification-reporter/ — formats findings as a Markdown PR report
- skills/content-verification-batch/ — orchestrates batch runs across folders via /fleet

When to invoke:
- After any agent finishes drafting or editing a documentation file
- When asked to "check for AI patterns", "make this sound more human", or "run a style pass"
- When a folder path is provided with a verify/audit/check instruction
- Before delivering any written artifact longer than 200 words

When not to invoke:
- Code comments, commit messages, log output, UI label strings
- Content inside code blocks or callout syntax ([!NOTE], [!TIP], [!IMPORTANT])
```

---

## Runtime requirements

| Feature | Runtime |
|---|---|
| Single article verification | Copilot Chat, Copilot CLI, VS Code Agent Mode |
| PR report generation | Copilot CLI, VS Code Agent Mode |
| Batch `/fleet` run | Copilot CLI only |
| Background `/delegate` run | Copilot CLI only |

---

## Source references

| Source | Link |
|---|---|
| Microsoft Writing Style Guide | [https://learn.microsoft.com/en-us/style-guide/welcome/](https://learn.microsoft.com/en-us/style-guide/welcome/) |
| Ethan Mollick — AI tell signals | [https://www.oneusefulthing.org/](https://www.oneusefulthing.org/) |
| Simon Willison — LLM word frequency | [https://simonwillison.net/](https://simonwillison.net/) |
| Chip Huyen — AI Engineering | [https://huyenchip.com/](https://huyenchip.com/) |
| Nate B. Jones — substance-first writing | [https://www.natebjones.com/](https://www.natebjones.com/) |
| GitHub Copilot CLI /fleet docs | [https://docs.github.com/en/copilot/how-tos/copilot-cli/speed-up-task-completion](https://docs.github.com/en/copilot/how-tos/copilot-cli/speed-up-task-completion) |