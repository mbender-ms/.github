# Repo Recon

**Reverse-engineer any codebase into a complete, verified understanding of what it does, how it works, and why it exists.**

Repo Recon is a Claude skill that crawls repositories or file sets, maps their architecture with Mermaid diagrams, researches similar projects, and produces actionable extraction artifacts — all without fabricating a single claim.

---

## What

Repo Recon takes a GitHub repo, local folder, or uploaded file set and produces:

- An **executive summary** (what / how / why) grounded in the actual code
- **Mermaid diagrams** for dependencies, data flow, request lifecycles, and state machines
- A **component extraction table** scoring each module's portability for reuse in other projects
- A **similar projects comparison** via mandatory web research
- A **compatibility verdict** (go / no-go) when evaluating whether two tools can work together

Every claim references a specific file or web source. If something can't be verified, it's flagged — never invented.

## How

The skill runs in five phases, gated by your request:

| Phase | Name | What happens |
|-------|------|--------------|
| 1 | **Ingest** | Flattens the repo via [Repomix](https://repomix.com) (remote) or file crawl (local). Produces a manifest with file counts, token estimates, and entry points. Large repos get chunked automatically. |
| 2 | **Analyze** | Per-file purpose identification, dependency mapping (Mermaid), workflow extraction, tech stack inventory. Pauses to ask clarifying questions before continuing. |
| 3 | **Research** | Mandatory web search for similar projects, ecosystem health, and claim verification. Produces a comparison table. |
| 4 | **Synthesize** | Final deliverable: executive summary, component extraction table with portability scores, collected diagrams. |
| 5 | **Compatibility** | On-demand only. Analyzes interfaces, integration pathways, and gotchas between two targets. Produces a go / no-go verdict. |

Default is Phases 1–4. You control how far it goes, and you can resume from any completed phase without re-running earlier work.

## Why

Understanding an unfamiliar codebase is one of the most time-consuming tasks in software. Repo Recon exists because:

- **Reading code isn't the bottleneck — building the mental model is.** Repo Recon builds that model for you with verified diagrams and structured summaries.
- **"Can X work with Y?" shouldn't require hours of manual analysis.** The compatibility mode gives you a structured verdict with specific integration steps and risks.
- **Extracting reusable components from a library requires knowing what's coupled and what's clean.** The portability scoring tells you exactly which pieces are worth pulling out.

---

## Installation

Drop the `repo-recon/` folder into your skills directory:

| Platform | Path |
|----------|------|
| Claude.ai | Upload as a user skill via Settings, or place in `/mnt/skills/user/repo-recon/` |
| Claude Code | Place in your project's `.claude/skills/repo-recon/` directory |
| Any skill-compatible agent | Follow that agent's skill installation instructions |

The skill is a single `SKILL.md` file — no dependencies, no scripts, no configuration.

---

## Usage Examples

### Full analysis of a GitHub repo

```
Analyze https://github.com/yamadashy/repomix
```

Runs Phases 1–4. Produces the complete report with diagrams, similar projects, and extraction table.

### Partial analysis — stop after research

```
Analyze https://github.com/supabase/supabase through Phase 3
```

Runs Phases 1–3 only. Useful when you want the research comparison but don't need the full synthesis yet.

### Resume from a prior phase

After running through Phase 3:

```
Continue to Phase 4
```

Picks up from the existing manifest and analysis — no re-ingestion.

### Compatibility check (conversational)

```
Can Repomix work with my Open Brain MCP server?
```

Analyzes both targets through Phase 4, then runs Phase 5 to produce a go/no-go verdict with integration steps.

### Head-to-head compatibility

```
Analyze compatibility https://github.com/yamadashy/repomix against https://github.com/coderamp-labs/gitingest
```

Full dual-ingest, parallel analysis of both repos, then a structured side-by-side comparison with a compatibility verdict.

### Analyze local files

```
Analyze c:\projects\my-tool
```

or

```
Analyze the uploaded files
```

Works with local folders (when running in Claude Code or environments with filesystem access) or uploaded file sets (when running in Claude.ai).

### Quick identification

Just paste a GitHub URL:

```
https://github.com/someone/some-repo
```

The skill triggers automatically and runs a full Phase 1–4 analysis.

---

## Output Examples

### Manifest (Phase 1)

```
## REPO RECON MANIFEST
- **Target:** https://github.com/example/tool
- **Total files:** 47
- **Estimated tokens:** 38,200
- **File types:** .ts (18), .json (8), .md (6), .yml (5), .css (4), ...
- **Entry points identified:** server/index.ts, cli/main.ts
- **Phase completed:** 1
- **Chunking required:** no
```

### Component Extraction Table (Phase 4)

| Component | Files | Purpose | Interfaces (in/out) | External Deps | Portability | Notes |
|-----------|-------|---------|---------------------|---------------|-------------|-------|
| Auth module | auth.ts, middleware.ts | JWT verification | Expects user model, exports `verify()` | jose | High | Self-contained |
| DB layer | db.ts, models.ts | PostgreSQL queries | Exports query functions | pg, drizzle | Medium | Coupled to schema |
| CLI parser | cli/main.ts, cli/commands/ | Argument parsing | Exports `run()` | commander | High | Clean extraction target |

### Compatibility Verdict (Phase 5)

```
## Compatibility Verdict: Repomix + Open Brain MCP

### Signal: 🟢 GO

### Rationale
Repomix outputs markdown/XML that can be ingested as text.
Open Brain accepts text via capture_thought. No shared runtime needed.

### Best integration approach: Data pipeline
### Estimated effort: Low
### Key steps:
1. Run Repomix on target repo
2. Chunk output into thought-sized segments
3. Ingest via capture_thought with topic tagging
```

---

## Large Repo Handling

Repos over ~80K tokens are automatically chunked into three passes:

1. **Skeleton** — README, package manifests, entry points, directory tree. Produces an initial hypothesis.
2. **Core** — Business logic files identified from imports and naming conventions.
3. **Support** — Configs, tests, CI/CD, utilities, remaining files.

After each pass, you're asked whether to continue deeper or if the current understanding is sufficient.

---

## Anti-Hallucination Guarantees

These rules are enforced at every phase:

- Never states a file contains something it hasn't read
- Never invents function names, class names, or API endpoints
- Never claims a dependency exists without seeing it in a manifest file
- Never asserts compatibility without checking actual interfaces
- Flags unverifiable claims with `[UNVERIFIED]` and asks for confirmation
- If web search finds no similar projects, says so — never invents comparisons

---

## Requirements

- **Repomix** (for remote GitHub repos): Runs via `npx repomix` — no global install needed. If unavailable, the skill falls back to manual methods (paste from [repomix.com](https://repomix.com), upload files, or use [gitingest.com](https://gitingest.com)).
- **Web search**: Required for Phase 3. Works automatically in Claude.ai and Claude Code.
- **File system access**: Optional. When available, reports are saved as downloadable markdown files. When unavailable, everything outputs inline in conversation.

---

## License

MIT — use it, modify it, share it.
