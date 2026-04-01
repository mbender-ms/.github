---
name: model-routing-authoring
description: "Route doc-authoring tasks for scenario articles, troubleshooting, and best-practices through phase-based model selection. Use Hybrid Auto behavior: strict verification routing, advisory routing for planning, drafting, and polish."
argument-hint: "Describe doc type and phase, for example: 'plan a troubleshooting article for App Gateway 502', 'draft best practices for Load Balancer probes', or 'verify code snippets in this scenario article'"
user-invocable: true
---

# Model Routing Skill - Doc Authoring (Agent-driven)

Use this skill to route doc-authoring work by phase so Auto mode remains efficient while critical validation remains strict.

## When to use

- Writing or revising scenario, troubleshooting, or best-practices content where phase-based routing improves quality
- Running focused phase work: plan, draft, verify, or polish
- Enforcing strict verification behavior when code or config is present

## When not to use

- New article scaffolding from scratch: delegate to [doc-writer/SKILL.md](../doc-writer/SKILL.md)
- Full factual validation across sources: delegate to [doc-verifier/SKILL.md](../doc-verifier/SKILL.md)
- Editorial SEO/metadata/engagement cleanup: delegate to [documentor-workflow/SKILL.md](../documentor-workflow/SKILL.md)
- Combined fact-check and editorial pass: delegate to [freshness-pass/SKILL.md](../freshness-pass/SKILL.md)

## Relationship to sibling skills

| Task | Primary skill | How this skill helps |
|---|---|---|
| New article creation | `doc-writer` | Apply model routing after structure is scaffolded |
| Fact-check and source verification | `doc-verifier` | Use this skill only for phase handoff and code-verify gating |
| Editorial quality and SEO | `documentor-workflow` | Use this skill for phase ordering, then delegate polish extras |
| Freshness pass | `freshness-pass` | Treat freshness-pass as orchestrator for combined checks |

## Required standards

- Writing style: [copilot/skills/_shared/writing-style.md](../_shared/writing-style.md)
- Formatting rules: [copilot/skills/_shared/formatting-rules.md](../_shared/formatting-rules.md)
- SEO and metadata: [copilot/skills/_shared/seo-and-metadata.md](../_shared/seo-and-metadata.md)
- Source hierarchy: [copilot/skills/_shared/source-hierarchy.md](../_shared/source-hierarchy.md)

## Article type mapping

| Model-routing type | Typical Learn shape | Notes |
|---|---|---|
| Scenario articles | How-to or Tutorial | Goal-oriented flow with decision points |
| Troubleshooting guides | How-to (troubleshooting pattern) | Symptom to diagnosis to fix |
| Best-practices articles | Concept or How-to | Do/Avoid/Why/Example framing |

For base structure templates, use [doc-writer/references/article-templates.md](../doc-writer/references/article-templates.md).

## Core routing policy

Use this preferred model assignment by phase:

1. **Plan / Synthesize / Structure** -> **GPT-5 (preferred, advisory in Auto mode)**
   - Use for outline, decision logic, tradeoffs, narrative structure, requirements extraction.

2. **Draft / Execute / Structured edits** -> **Goldeneye (preferred, advisory in Auto mode)**
   - Use for section drafting against an outline, consistent refactors, template application, disciplined updates.

3. **Verify code/config correctness (when code is involved)** -> **Codex (strict in Auto mode)**
   - Use for validating CLI/PowerShell/Bicep/JSON snippets, multi-file reasoning, and implementation checks.

4. **Polish / Readability / Voice** -> **Claude (preferred, advisory in Auto mode)**
   - Use for final editorial pass, clarity, tone, removing AI voice, and tightening language.

## Auto mode behavior (Hybrid)

- **Strict rule**: In `verify` phase with code/config present, route to Codex first.
- **Advisory rule**: In `plan`, `draft`, and `polish`, prefer mapped models but allow Auto-selected alternatives when they preserve context continuity or produce better outcomes.
- **Fallback rule**: If a named model is unavailable, use the best available model for the same phase role and continue.
- **Transparency rule**: State which model was used for the phase and why if fallback or substitution occurred.

## Task-type playbooks

### A) Scenario articles

**Steps**
1. Plan: GPT-5 preferred (advisory Auto)
2. Draft: Goldeneye preferred (advisory Auto)
3. Verify: Codex strict when code/config exists
4. Polish: Claude preferred (advisory Auto)

**Output requirements**

- Start with a short “What you’ll build / Why” summary
- Include decision points (when to choose option A vs B)
- Keep implementation details concise; link out when possible

### B) Troubleshooting

**Steps**
1. Plan: GPT-5 preferred for symptom taxonomy and diagnostic flow
2. Draft: Goldeneye preferred for cause -> validation -> fix sequence
3. Verify: Codex strict for commands/scripts/config
4. Polish: Claude optional for final tightening

**Output requirements**

- Lead with symptoms and quick checks
- Use clear “If/Then” diagnostics
- Avoid speculation; require validation steps before fixes

### C) Best practices

**Steps**
1. Plan: GPT-5 preferred for recommendation framing
2. Draft: Goldeneye preferred for Do/Avoid/Why/Example structure
3. Verify: Codex strict only when code/config is included
4. Polish: Claude preferred for readability and consistency

**Output requirements**

- Explicit “Do / Don’t” guidance
- Rationale that is brief and actionable
- Examples that are correct and minimal

## Activation instructions for the agent

When the user asks for doc work:

1. Validate scope: confirm this skill is appropriate, else delegate to sibling skill.
2. Identify doc type: scenario, troubleshooting, or best practices.
3. Identify phase: plan, draft, verify, or polish.
4. Apply Hybrid Auto policy:
   - verify with code/config -> strict Codex routing
   - plan/draft/polish -> advisory routing to preferred model
5. Execute only the current phase.
6. Summarize output, model used, and next phase.
7. If additional verification or editorial depth is needed, delegate to `doc-verifier`, `documentor-workflow`, or `freshness-pass`.

## Examples

### Example 1 — Scenario article request
**Input**
"Create a scenario article outline and then draft sections for a secure web app pattern."

**Agent behavior**

- Plan phase: GPT-5 preferred for outline and decisions
- Draft phase: Goldeneye preferred for section drafting
- Verify phase: Codex strict if CLI/Bicep appears
- Polish phase: Claude preferred for final prose

### Example 2 — Troubleshooting request
**Input**
"Add a troubleshooting flow for Application Gateway 502 errors."

**Agent behavior**

- Plan phase: GPT-5 preferred for symptom taxonomy
- Draft phase: Goldeneye preferred for validation/fix sequence
- Verify phase: Codex strict for command/config checks
- Polish phase: optional advisory polish

### Example 3 — Best practices refresh
**Input**
"Update best practices for Load Balancer health probes."

**Agent behavior**

- Plan phase: GPT-5 preferred for recommendation framing
- Draft phase: Goldeneye preferred for structured edits
- Verify phase: Codex strict only if technical snippets are present
- Polish phase: Claude preferred for readability