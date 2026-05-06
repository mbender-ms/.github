---
name: one-pager
description: >
  Write a crisp, structured one-pager for any AI project or initiative. Use this skill whenever Michael
  needs to communicate a project proposal to leadership or stakeholders — including any request for a
  "one-pager", "project summary", "proposal doc", "pitch doc", or "project brief". Also trigger when
  Michael says things like "write up what I'm building", "summarize this project for my boss", or
  "I need to explain this to stakeholders". The output follows a fixed five-section structure: problem,
  solution approach, timeline, success measures, and stakeholders. No buzzwords. Readable in under
  3 minutes.
---

# One-Pager Skill

Produces a focused, single-page project summary for internal stakeholders. Structure is fixed.
Tone is plain and direct. Length is controlled — the goal is a document someone can read in 2–3 minutes.

---

## Inputs to gather before writing

If any of these are missing, ask before writing. Don't guess.

| Input | Why it matters |
|---|---|
| Project name | Title of the doc |
| The core problem | What's broken, slow, or missing today |
| The proposed approach | What you're building and what AI tools are involved |
| Timeline / sprint plan | High-level phases or milestones with rough dates |
| How you'll know it worked | Concrete, measurable outcomes |
| Who's involved or affected | Names or roles of key stakeholders |

---

## Output structure

Use this exact section order. Keep each section to 2–5 sentences or a short list — no more.

---

### [Project Name]

*One sentence. What this project does, in plain language.*

---

#### Problem

What's not working today, and why it matters. Be specific — name the pain, not the category.
Avoid: "lack of visibility", "inefficient processes", "siloed data".
Instead: "We manually track X in a spreadsheet, which takes Y hours and breaks when Z."

---

#### Approach

What you're building and how AI tools help. Focus on what changes, not how cool the tech is.
Name specific tools only if they're already decided. If undecided, describe the capability instead.

Format:
- What the system does (user-facing behavior)
- What AI component does the work (and why it fits this problem)
- What's manual vs. automated

---

#### Timeline

Sprint-style breakdown. Use phases, not Gantt charts.

| Phase | What ships | Target |
|---|---|---|
| 1 | [Deliverable] | [Week or date] |
| 2 | [Deliverable] | [Week or date] |
| … | … | … |

Keep phases to 2–4 items. If the project is longer than 8 weeks, consider whether the one-pager
covers the full scope or just the first major milestone.

---

#### Success Measures

2–4 concrete outcomes. Each should be answerable with a yes/no or a number.

Avoid: "improved efficiency", "better user experience", "faster turnaround".
Instead: "Time to find a part drops from 10 minutes to under 1 minute", "Zero manual spreadsheet
updates after go-live", "80% of inventory queries answered without human lookup".

---

#### Stakeholders

List name + role + relationship to project (owner, reviewer, end user, informed).
Keep it short. If the list exceeds 6 people, it's probably not a one-pager problem anymore.

---

## Style rules

Apply these throughout. They are non-negotiable defaults.

- **No buzzwords.** Flag and replace: leverage, synergy, scalability, paradigm, frictionless,
  streamline, robust, utilize, empower, unlock, transform, harness.
- **Active voice.** "The agent searches the database" not "The database is searched by the agent."
- **Plain nouns.** Call things what they are: "a search tool", "a weekly report", "a lookup table".
- **No filler openers.** Don't start sections with "In today's environment…" or "As AI continues to…"
- **Numbers over adjectives.** "4 hours/week" beats "significant time savings".
- **One page.** If the rendered output is longer than one printed page, cut — don't compress the font.

---

## Quality check before output

Before returning the draft, verify:

- [ ] Each section is present and labeled
- [ ] No section exceeds 5 sentences or 5 list items (timelines excepted)
- [ ] No buzzwords present (run the list above)
- [ ] Success measures are specific and measurable
- [ ] Stakeholders include role context, not just names
- [ ] Problem section names a real, specific pain — not a category

---

## Example: what good looks like

### AI Parts Inventory — Phase 1

*A Python CLI that lets team members search our parts inventory in plain English instead of navigating a spreadsheet.*

**Problem**  
Finding a specific part before build sessions takes 10–15 minutes of spreadsheet hunting. During competition prep, this compounds across the whole team. Parts go "missing" because no one knows they exist.

**Approach**  
Build a SQLite-backed inventory system with a Claude-powered natural language search layer. Members type queries like "M3 bolts, 20mm, stainless" and get matched results. No training required, no spreadsheet skills required. The AI handles query interpretation; the database handles storage and retrieval.

**Timeline**

| Phase | What ships | Target |
|---|---|---|
| 1 | CLI with NL search, SQLite DB | Week 2 |
| 2 | Semantic search via embeddings | Week 4 |
| 3 | Vision-based part identification | Week 6 |
| 4 | React UI, QR scan, check-in/out | Week 8 |

**Success Measures**  
- Part lookup time under 1 minute for 90% of queries  
- Zero spreadsheet updates after Phase 1 go-live  
- All 500+ current parts imported before first use session

**Stakeholders**  

| Name / Role | Involvement |
|---|---|
| Michael B. — Builder | Owner and developer |
| Head Mentor | Reviewer / approver |
| Team Leads (4) | End users, feedback loop |
| Students | End users |
