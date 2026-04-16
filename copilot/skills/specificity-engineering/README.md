# Specificity Engineer

A Copilot skill for designing, auditing, and building agent prompts and skills with the Specificity Engineering framework. It helps you turn vague agent ideas into reviewable specs, audit existing prompts against clear principles, and produce production-ready skill definitions with explicit boundaries and done conditions.

---

## Prerequisites

| Requirement | How to verify |
|-------------|---------------|
| **VS Code** (1.100+) | `code --version` |
| **GitHub Copilot** (agent mode) | Copilot Chat -> mode dropdown -> Agent available |
| **Skill folder access** | This folder exists under `copilot/skills/specificity-engineering/` |

---

## Installation

Copy the `specificity-engineering/` folder to your Copilot skills directory:

```powershell
Copy-Item -Recurse .\specificity-engineering\ "$env:USERPROFILE\.copilot\skills\specificity-engineering"
```

Restart VS Code.

### Folder structure

```text
specificity-engineering/
├── README.md
├── SKILL.md
├── specificity-diagram.jsx
└── specificity-engineering-guide.md
```

---

## What this skill does

This skill applies the Specificity Engineering framework to agent prompts and skills. It is built for cases where a prompt needs more than general prompt polish and instead needs explicit scope, intent, boundaries, tool guidance, failure handling, and a real definition of done.

The skill supports three operating modes and infers the correct mode from the user's first message.

| Mode | When it runs | Output |
|------|--------------|--------|
| **Mode A - Skill Audit** | User pastes an existing skill, prompt, or spec | Structured audit with ratings, findings, and prioritized fixes |
| **Mode B - Guided Build** | User describes a new skill loosely or incompletely | Interview-driven SPEC.md-style skill draft |
| **Mode C - Fast Build** | User says "fast build" or provides a detailed scoped idea | Immediate draft with inline open questions where needed |

---

## Included files

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition and operating instructions for audit, guided build, and fast build workflows |
| `specificity-engineering-guide.md` | Practitioner guide that explains the framework, four-layer hierarchy, and seven principles |
| `specificity-diagram.jsx` | Interactive visual that illustrates the four layers and before/after examples |
| `README.md` | Package overview, installation, and usage guidance |

---

## Usage

Open **GitHub Copilot Chat** in agent mode.

### Audit an existing skill or prompt

> Paste an existing skill file or prompt directly into chat.

The skill will:
1. Evaluate the content against the seven principles
2. Produce an audit table with ratings and findings
3. Rank the highest-impact fixes
4. Ask whether you want a revised version generated

### Build a new skill with guided questions

> "Help me write a skill that reviews PR descriptions for missing context"

The skill will:
1. Ask one question at a time
2. Gather scope, tools, done conditions, failure modes, and reviewer context
3. Produce a complete structured skill spec when it has enough signal

### Fast-build from a detailed idea

> "Fast build: create a skill that audits prompt assets for missing negative examples and weak done conditions"

The skill will:
1. Draft the full spec immediately
2. Insert `[OPEN QUESTION: ...]` placeholders where details are missing
3. List remaining open questions for follow-up

---

## Audit framework

The audit mode evaluates a submitted skill or prompt against these seven principles:

1. Define outcome and definition of done
2. Operate at the right altitude
3. Minimal viable context only
4. Encode intent, not just instructions
5. Curate tools aggressively
6. Negative examples are essential
7. Pass the human test

This keeps reviews focused on behavior and reliability instead of generic prompt advice.

---

## When to use this skill

Use this skill when:
- You want to audit an existing skill for gaps in scope, boundaries, and stopping conditions
- You need to build a new skill from a rough idea without over-specifying it too early
- You want a prompt or skill spec that is reviewable without redoing the work manually
- You need explicit tool guidance, escalation boundaries, and negative examples

Use another skill when:
- You need to write Azure documentation content rather than design the agent that writes it
- You need fact-checking, editorial review, or freshness review on an article itself
- You already have a finished skill and only need a small one-off file edit

---

## Source foundations

The framework is grounded in practitioner guidance from:
- Anthropic prompt and context engineering guidance
- Nate B. Jones on intent and specification engineering
- Simon Willison on practical agent and prompt design

Use `specificity-engineering-guide.md` when you want the theory and examples behind the skill behavior.

---

## Notes

- The skill name is `specificity-engineer`, while the package folder is `specificity-engineering/`.
- The skill is designed to minimize prompt bloat. Longer prompts are not treated as better prompts.
- Negative examples and done conditions are first-class requirements, not optional polish.
