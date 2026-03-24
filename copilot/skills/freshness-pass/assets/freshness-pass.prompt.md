---
mode: agent
description: "Run a comprehensive freshness pass on the currently open article — full fact-check against public docs and APIs, comprehensive editorial review, SEO audit, markdown auto-fix, content suggestions, and MS Style Guide checks"
tools:
  - microsoft-learn-mcp-server/microsoft_docs_search
  - microsoft-learn-mcp-server/microsoft_docs_fetch
  - microsoft-learn-mcp-server/microsoft_code_sample_search
  - web/fetch
  - web/githubRepo
  - read/readFile
  - read/problems
  - search/codebase
  - search/fileSearch
  - search/textSearch
  - search/usages
  - edit/editFiles
  - edit/createFile
  - execute/runInTerminal
  - execute/getTerminalOutput
  - todo
---

# Freshness Pass — Single Article

Run a comprehensive freshness pass on the currently open article. This combines a full fact-check against public documentation and APIs with a complete editorial review covering SEO, markdown formatting, content engagement, and Microsoft Style Guide compliance.

All corrections are applied directly to the file. A per-edit summary with source citations is presented in chat.

---

## Authority hierarchy

Use sources in this priority order:

1. **Tier 1 (Primary)**: learn.microsoft.com, azure.microsoft.com — product docs, features, limits, pricing
2. **Tier 2 (Secondary)**: techcommunity.microsoft.com, devblogs.microsoft.com, github.com/Azure, github.com/MicrosoftDocs — announcements, API specs, SDKs, samples
3. **Tier 3 (Cross-reference)**: developer.microsoft.com, code.visualstudio.com, MS Q&A (verified MS employees only) — platform docs, edge cases

> Higher tier always wins. REST API specs on GitHub are ground truth for API parameters and schemas.

---

## Phase A — Fact-check

### Step A1: Read and extract claims

Read the currently open article. Extract every technical claim:

- Product/service names and descriptions
- Feature capabilities, limitations, and prerequisites
- Version numbers, API references, CLI commands
- Configuration values, default settings, quotas
- Code examples and syntax
- URLs and link targets

### Step A2: Verify claims against public sources

For each extracted claim:

1. Search `microsoft_docs_search` for the topic on learn.microsoft.com
2. Use `microsoft_docs_fetch` to retrieve full documentation pages when needed
3. Use `microsoft_code_sample_search` for code examples
4. Use `web/fetch` for API specs, SDK repos, and REST API definitions
5. Use `web/githubRepo` for GitHub repository content (azure-rest-api-specs, SDK repos)
6. Check for deprecation notices, retirement announcements, and version changes
7. Validate code examples using `read/problems` where applicable

### Step A3: Classify each claim

| Icon | Status | Action |
|------|--------|--------|
| ✅ | Accurate | No change needed |
| ⚠️ | Partially accurate | Edit with correction |
| ❌ | Inaccurate | Edit + cite source |
| 🕐 | Outdated | Update + cite source |
| ❓ | Unverifiable | Flag in summary — do not remove from article |
| 🔗 | Broken link | Fix URL or flag if replacement unknown |

### Step A4: Scan for freshness issues

- **ms.date**: Note the current value — it will be updated after edits
- **Deprecated/retired services**: Flag any services that have been sunset
- **Old version numbers**: Flag versions that are no longer current
- **Broken/redirected links**: Fetch all absolute URLs and flag errors or redirects
- **Outdated UI references**: Flag references to old Azure portal UI that has changed

---

## Phase B — Editorial pass

### Step B1: Comprehensive editorial review

1. **Frontmatter completeness** — Verify all required fields present: `title`, `description`, `ms.date`, `ms.topic`, `ms.service`, `ms.custom` (with customer intent), `author`, `ms.author`
2. **Title validation** — 30–65 characters, title case, primary keyword near beginning, unique from H1 and description, no gerunds at start
3. **Description validation** — 120–165 characters, primary keyword at beginning, includes CTA (Learn how to..., Find out..., Discover...), unique from title and H1, active voice
4. **Customer intent** — Verify `ms.custom: customer-intent="As a <role>, I want <what> so that <why>"` is present and accurate
5. **Passive voice scan** — Identify passive voice and rewrite to active voice using "you" to address readers
6. **Procedure validation** — Verify procedures have ≤ 10 steps, each begins with an imperative verb, one action per step
7. **Sensitive identifier scan** — Check for real GUIDs, secrets, subscription IDs, tenant IDs, client secrets — replace with approved placeholders from the sensitive identifiers reference

### Step B2: SEO audit

1. **Title** — 30–65 chars, title case, primary keyword, unique from H1/description, no gerunds, spell out abbreviations
2. **Description** — 120–165 chars, CTA, keyword at beginning, unique, active voice, compelling copy
3. **H1** — Sentence case (NOT title case), primary keyword, no gerunds, exactly one per article, differs from title
4. **Intro paragraph** — Primary keyword in first or second sentence, 2–3 sentences, establishes scope and audience, aligns with customer intent
5. **Subheadings (H2+)** — Sentence case (NOT title case), secondary keywords where natural, no gerunds, no trailing periods. Preserve standard headings: Prerequisites, Related content, Next steps, Clean up resources, Overview
6. **Image alt text** — 40–150 chars, prefix with "Screenshot of..." or "Diagram of...", descriptive, keywords where natural
7. **Internal linking** — Relative paths for same docset, descriptive anchor text (no "click here" or "learn more"), 3–5 related content links, 1–3 actionable next steps

### Step B3: Auto-fix markdown

Systematically fix formatting issues:

1. **Heading hierarchy** — No skipped levels (H1 → H2 → H3), single H1
2. **Blank lines** — Ensure blank lines before and after headings, code blocks, lists, and alerts
3. **List formatting** — Consistent markers, proper nesting, blank lines between top-level items
4. **Code fence identifiers** — Use `azurecli` not `bash` for Azure CLI, `azurepowershell` not `powershell` for Azure PowerShell, `kusto` for KQL
5. **Alert syntax** — Standard format: `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!CAUTION]`, `> [!WARNING]`
6. **Table formatting** — Consistent columns, proper alignment, header row present
7. **Trailing whitespace** — Remove trailing spaces on all lines
8. **File ending** — Ensure file ends with a single newline

### Step B4: Content suggestions

Analyze for engagement improvements:

1. **Bounce rate** — Does the intro hook the reader? Does it align with what search results promise? Are there visual elements (diagrams, screenshots) to break up text?
2. **Click-through rate** — Are links placed within the first half of the article? Is anchor text verb-first and actionable ("Deploy to Azure" not "Learn more")? Are CTAs clear?
3. **Copy-try-scroll rate** — Are code samples complete and runnable? Are procedures scannable with clear headings every 2–3 paragraphs? Do complex procedures have screenshots?
4. **Dwell rate** — Is content depth appropriate for the article type? Are abstract concepts illustrated with examples? Are comparisons presented in tables?
5. **Exit rate** — Is there a "Next steps" section with 1–3 actionable links? Is there "Related content" with 3–5 links? Does the article use progressive disclosure via internal linking?

### Step B5: MS Style Guide checks

1. **Voice and tone** — Warm, relaxed, crisp, ready to lend a hand. Natural and conversational.
2. **Contractions** — Use "you'll", "it's", "don't" — not "You will", "it is", "do not"
3. **Sentence-style capitalization** — All H2+ headings capitalize only the first word and proper nouns
4. **Procedures** — Imperative verbs ("Select", "Enter", "Open"), one action per step, max 7 steps per section, intro ends with colon
5. **Active voice** — "The function processes the message" not "The message is processed by the function"
6. **Brief writing** — Short paragraphs (2–4 sentences), short sentences (under 25 words), every sentence earns its place
7. **Word choices** — Simple everyday words, avoid jargon without context, link to definitions on first use
8. **Oxford comma** — Always: "VMs, storage, and networking"
9. **Audience** — Write for experienced professionals new to this specific feature. Don't over-explain fundamentals.

---

## Phase C — Consolidation

### Step C1: Apply all corrections

For every issue found in Phases A and B:

- Make corrections directly in the current file
- Preserve the article's existing tone, style, and structure
- Update `ms.date` to today's date (MM/DD/YYYY format)
- Fix broken links with current URLs
- Update version numbers, CLI commands, and code samples to current versions
- Correct deprecated feature references with current alternatives
- Do NOT add HTML comments or reference markers into the article

### Step C2: Present summary in chat

After ALL edits are complete, present a single summary. For each change:

---

**Edit N: [brief description]**
- **Line(s)**: [approximate line number(s)]
- **What changed**: [original text] → [new text]
- **Why**: [brief explanation]
- **Type**: [Fact: Outdated | Inaccurate | Broken Link] or [Editorial: SEO | Style | Markdown | Metadata | Engagement | Sensitivity]
- **Source(s)**: [Title](URL) — for fact-check edits only

---

End with:
- **Phase A summary**: Total fact-check findings by classification (✅ ⚠️ ❌ 🕐 ❓ 🔗)
- **Phase B summary**: Total editorial findings by severity (Critical / Important / Suggestion)
- **Edit totals**: Count by type (outdated, inaccurate, broken link, SEO, style, markdown, metadata, engagement, sensitivity)
- Reminder to review via **Source Control** (Ctrl+Shift+G) or `git diff`

### Step C3: Offer git workflow

Ask if the user wants to commit the changes. If yes:

1. Create a new branch: `freshness/[article-name]-MMDDYYYY`
2. Commit with message: `freshness: [article-name] — fact-check + editorial pass`
3. Push the branch
4. Open a pull request with the freshness review summary

---

## Quality checklist

Before finishing, confirm ALL of these:

### Fact-check quality
- [ ] All technical claims verified against at least one Tier 1 source
- [ ] Every fact-check correction includes a source citation with URL
- [ ] Code examples validated
- [ ] Version/deprecation status confirmed for all mentioned services
- [ ] Broken links fixed or flagged
- [ ] Unverifiable claims flagged but not removed

### Editorial quality
- [ ] `ms.date` updated to today's date
- [ ] Title: 30–65 chars, title case, primary keyword
- [ ] Description: 120–165 chars, CTA, keyword at beginning, unique
- [ ] H1: sentence case, differs from title
- [ ] Customer intent present in `ms.custom`
- [ ] Heading hierarchy correct (no skipped levels, single H1)
- [ ] All H2+ headings use sentence-style capitalization
- [ ] Code fence identifiers correct (`azurecli`, `azurepowershell`)
- [ ] Alert syntax uses standard format
- [ ] No trailing whitespace
- [ ] Sensitive identifiers replaced with approved placeholders
- [ ] Passive voice eliminated or justified
- [ ] Procedures use imperative verbs, ≤ 10 steps each
- [ ] Writing follows MS Style Guide (contractions, active voice, Oxford comma)
- [ ] Engagement improvements suggested (intro hooks, CTAs, next steps)
