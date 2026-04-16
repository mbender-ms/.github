# Specificity Engineering: A Practitioner's Guide to Building Better Agent Prompts

> **What this is.** A hands-on guide for anyone building Copilot skills or agent prompts who wants to move from "it kind of works" to "it reliably works." Read it once to understand the framework. Use the skill file alongside it to apply it.

---

## What Is Specificity Engineering?

Specificity engineering is the discipline of scoping agents to narrow, well-defined tasks with enough precision that their output can be reviewed without re-doing the work manually. It is not a collection of prompt tips — it is a design philosophy for agent systems.

The term comes from Michael Bender's practice of delegating to agents and reviewing rather than executing manually. The underlying principle is simple: the agent's job is to produce reviewable output, and your job is to define "reviewable" precisely enough that the agent can meet the bar without guessing.

A well-engineered agent prompt is not the longest prompt. It is the minimal prompt that fully specifies expected behavior, encodes the agent's intent, and leaves no ambiguity about what "done" looks like.

---

## Why This Matters

Most agent prompt failures trace to one of five root causes:

1. The agent doesn't know when to stop (missing definition of done).
2. The agent has too much or too little context (context engineering failure).
3. The agent knows what to do but not why, so it improvises at edge cases (missing intent).
4. The agent has never been shown what failure looks like (no negative examples).
5. The instructions are either too rigid (brittle) or too vague (unactionable).

Specificity engineering addresses all five systematically.

---

## The Four-Layer Hierarchy

These are four compounding disciplines. You cannot skip layers — each one assumes the previous is solid. The interactive diagram in this package lets you explore each layer with before/after examples drawn from a real fact-checking skill.

```
Layer 4 │ SPECIFICITY ENGINEERING  ← complete spec: done conditions,
        │                            boundaries, negative examples
        │
Layer 3 │ INTENT ENGINEERING       ← the why: governing principles
        │                            for edge cases
        │
Layer 2 │ CONTEXT ENGINEERING      ← everything in the window: role,
        │                            tools, memory, retrieved content
        │
Layer 1 │ PROMPT CRAFT             ← the words you write: task,
                                     output format, basic constraints
```

**Prompt Craft** is where most people start — and stop. A well-crafted prompt specifies the task and the expected output format clearly. It is necessary but not sufficient.

**Context Engineering** is the set of strategies for curating what enters the model's context window: role, tools, source hierarchy, injected content, memory. The model can only work with what it sees. Most reliability problems are context problems.

**Intent Engineering** encodes the *why* behind the instructions — the governing principles that let an agent reason about situations the instructions don't explicitly cover. Without intent, the agent improvises at every edge case. With intent, it applies a principle.

**Specificity Engineering** is the complete specification: definition of done, decision boundaries, tool failure handling, negative examples, and evaluation criteria. This is the layer that closes the gap between "it sometimes works" and "it reliably works."

---

## The Seven Principles

These principles apply within the Specificity Engineering layer (Layer 4). They are the checklist against which any skill or agent prompt can be evaluated.

**Principle 1 — Define the outcome AND the definition of done.** A prompt that describes what to produce but not when to stop produces unreliable agents. The definition of done should be an agent stopping condition: "complete when X, pause and escalate if Y."

**Principle 2 — Operate at the right altitude.** There is a Goldilocks zone between two common failure modes. Too brittle: hardcoded logic that breaks when inputs vary slightly (`"if the user asks about X, always respond with Y, unless Z, then do W..."`). Too vague: instructions that assume shared context (`"be helpful and accurate"`). Right altitude: specific enough to guide behavior, flexible enough to let the agent apply heuristics to novel situations (`"when verifying claims against documentation, flag discrepancies with the source URL and confidence level — escalate if you can't find a matching source"`).

**Principle 3 — Minimal viable context only.** More context is not better context past a threshold. Every token the agent reads depletes its attention budget. Context rot is real: as context length increases, recall accuracy decreases across all models. Include only what the agent needs. Exclude everything it doesn't.

**Principle 4 — Encode intent, not just instructions.** Instructions tell the agent what to do. Intent tells the agent what it is optimizing for and what principle governs tradeoffs. An agent with only instructions will fail at the boundary of those instructions. An agent with intent will reason through it.

**Principle 5 — Curate tools aggressively.** If you cannot definitively say which tool the agent should use in a given situation, the agent cannot either. Overlapping tool definitions produce ambiguous decision points at exactly the moment the task is most complex. Every tool must justify its existence. Every tool needs guidance on when *not* to use it.

**Principle 6 — Negative examples are as important as positive ones.** Most prompts only show the agent what to do. The agent's failure modes live in the unspecified space — the cases the prompt didn't address. Negative examples define the failure boundary. Without them, the unspecified space is where the agent goes wrong.

**Principle 7 — The human test.** Show the prompt to a colleague who hasn't seen it. If they are confused, the agent will be too. If they understand the task, output, and constraints clearly, the prompt is likely at the right altitude.

---

## How to Use the `specificity-engineer` Skill

The skill has three modes. It infers which mode to use from your first message — you do not need to specify.

---

### Mode A — Skill Audit

**Use when:** You have an existing skill or system prompt and want structured feedback.

**How to invoke:** Paste the skill file or prompt into the chat. The skill will evaluate it against all seven principles, produce an audit table with ratings and findings, and offer to apply all fixes and produce a revised version.

**Example invocation:**

```
[paste skill content]
```

The agent reads the content, runs the audit automatically, and produces:

```
AUDIT TABLE
Principle                      | Rating     | Finding
------------------------------|------------|----------------------------------
1. Definition of Done         | ❌ Missing | No stopping condition defined...
2. Right Altitude             | ✅ Strong  | Source hierarchy well-specified...
3. Minimal Viable Context     | ⚠️ Gap    | Three sections could move to assets...
4. Intent Encoded             | ⚠️ Gap    | Instructions present, but no why...
5. Tool Guidance              | ✅ Strong  | Tools named with when-to-use...
6. Negative Examples          | ❌ Missing | No failure modes defined...
7. Human Test                 | ✅ Strong  | A colleague could follow this...

PRIORITY FIXES
1. [highest impact gap + exact fix]
2. [next gap + exact fix]
...
```

It then asks: *"Do you want me to apply all recommendations and produce a revised version?"*

---

### Mode B — Guided Build

**Use when:** You want to build a new skill but haven't fully defined it yet.

**How to invoke:** Describe what you want the agent to do in one or two sentences. The skill will interview you, one question at a time, and produce a complete SPEC.md when it has enough information.

**Example invocation:**

> "I want to build a skill that reviews pull request descriptions and flags missing context."

The skill will ask:

> "What tools, data sources, or external services does this agent depend on?"

Then:

> "How will you know the agent succeeded? Describe the output format and any stopping condition."

Then:

> "What are the most important failure modes to prevent? What should this agent never do?"

After five questions (compressing if your answers cover multiple questions), it produces a complete SPEC.md with all sections filled.

---

### Mode C — Fast Build

**Use when:** You have a clear, detailed idea and want output immediately.

**How to invoke:** Say "fast build" followed by a detailed description of the skill, including what it does, what tools it uses, what done looks like, and what it should never do.

**Example invocation:**

> "Fast build: a skill that monitors Azure service health RSS feeds, summarizes incidents affecting our subscribed services, and posts a daily digest to a Slack channel. It should use the Azure status RSS feed and Slack MCP. Done means a digest was posted. It should never post if there are no incidents."

The skill builds the complete SPEC.md immediately, inserting `[OPEN QUESTION: ...]` placeholders for any section it cannot fill from the description. All open questions appear at the bottom of the spec. Answer them in one reply and the spec is updated.

---

## Further Learning

These are the primary sources behind this framework. All are practitioner-focused — written by people who build with AI systems, not commentators.

### Anthropic

The primary technical reference for context and prompt engineering with Claude models.

- **[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)** — the source for context rot, attention budget, tool curation, and the "right altitude" concept. Start here.
- **[Prompting Best Practices: Claude 4.x](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)** — model-specific guidance including negative examples, structured outputs, and agentic coding patterns.
- **[Prompt Engineering Overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)** — the canonical reference for foundational techniques.
- **[Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)** — working code examples for tool use, agents, RAG, and multimodal patterns.

### Nate B. Jones

Frameworks and workflows for deploying AI at scale. The intent engineering and specification engineering concepts in this guide draw directly from his work.

- **[Substack: natesnewsletter.substack.com](https://natesnewsletter.substack.com/)** — the primary channel for his frameworks. The "Age of Intent Engineering" and "State of Prompt Engineering" issues are directly relevant.
- **[Prompt Kits: promptkit.natebjones.com](https://promptkit.natebjones.com/)** — structured exercises for building context documents, specification files, intent frameworks, and eval harnesses. The Specification Engineering prompt kit is a practical companion to this guide.
- **[YouTube: @NateBJones](https://www.youtube.com/@NateBJones)** — daily AI strategy and implementation. His token management and context window episodes are particularly relevant.

### Simon Willison

Hands-on AI engineering and agentic coding patterns. The most transparent practitioner publishing in this space.

- **[Blog: simonwillison.net](https://simonwillison.net/)** — builds in public with detailed write-ups on what works and what doesn't. Search "agents" and "prompt engineering" for directly relevant posts.
- **[Substack: simonw.substack.com](https://simonw.substack.com/)** — curated highlights from his blog and projects.

### Chip Huyen

The definitive textbook for AI engineering as a discipline. Relevant for anyone who wants to go deeper on evaluation, RAG, and production systems.

- **[AI Engineering (O'Reilly)](https://www.oreilly.com/library/view/ai-engineering/9781098166298/)** — the reference book for this field. Chapters on evaluation and context management are directly applicable.
- **[GitHub Resources: chiphuyen/aie-book](https://github.com/chiphuyen/aie-book)** — code and resources from the book.

---

## Quick Reference Card

Cut this out and keep it accessible when building or reviewing any skill.

```
FOUR LAYERS (build in order, don't skip)
  1. Prompt Craft        — task + output format
  2. Context Engineering — role, tools, injected content
  3. Intent Engineering  — the why, for edge cases
  4. Specificity Eng.    — done conditions, boundaries, negative examples

SEVEN PRINCIPLES (use as audit checklist)
  1. Define outcome + definition of done
  2. Right altitude (not brittle, not vague)
  3. Minimal viable context only
  4. Encode intent, not just instructions
  5. Curate tools aggressively
  6. Negative examples are essential
  7. The human test

RIGHT ALTITUDE — three examples:
  ✗ Too brittle: "If X, do Y, unless Z, then W..."
  ✗ Too vague:   "Be helpful and accurate."
  ✓ Right:       "When verifying claims, flag discrepancies
                  with source URL and confidence level.
                  Escalate if no matching source found."

DEFINITION OF DONE (must be an agent stopping condition):
  ✗ Human checklist
  ✓ "Complete when every claim is classified.
     Pause if >20% are Unverifiable."
```

---

*Built on Anthropic, Nate B. Jones, and Simon Willison practitioner frameworks. See `specificity-engineer.SKILL.md` to apply this framework directly in your Copilot agent workflows.*
