# Global Copilot Instructions — Michael Bender (@mbender-ms)

These instructions are loaded into **every** Copilot conversation automatically.

## Identity

- **Name**: Michael Bender | **GitHub**: `@mbender-ms` | **Alias**: `mbender`
- **Role**: Content Developer — Azure Networking | **Team**: Azure Core Content
- **ADO**: `msft-skilling` / `Content`

## Core Rules

1. **Delegate before doing** — Route tasks to the correct skill or sub-agent before processing inline. Writing → `doc-writer`, fact-checking → `doc-verifier` / `microsoft-fact-checker` agent, ADO work items → `ado-work-items`, SEO/editorial → `documentor-workflow`, exploration → `Explore` agent.
2. **Never commit to main** — always create a feature branch (`mbender-ms/<service>-<description>-<id>`).
3. **One commit per file** — format: `docs: <imperative verb> <what changed>`. No AB# in commits.
4. **Ask before pushing** — get approval before `git push`.
5. **Sentence casing** for all headings in documentation articles.
6. **Lazy-load** — don't pre-read reference files, source YAMLs, or repo catalogs unless the task requires them.
7. **Efficiency over verbosity** — use direct commands and tools, but never sacrifice research depth or clarity. When in doubt, ask.
8. **Git workflow** — For branch/commit/push/PR tasks, use the `git-workflow` prompt. Prefer `gh` CLI for PR creation.

## Skill Loading

For deeper context on any of these topics, load the `my-workflow` skill (`copilot/skills/my-workflow/SKILL.md`):
- Services table, repo details, PR framework, sub-agent patterns, quick commands

Don't load the full skill unless the task needs it — these global rules cover most interactions.

## Tool strategy and fallback policy

Use the best available tool for speed, quality, and reliability. Do not block progress because a preferred tool is unavailable.

1. **Choose outcome-first tools** — optimize for best result and shortest safe path, not personal preference for a specific CLI.
2. **Install best-of-breed by default** — when a clearly superior tool exists for the task, install and use it rather than defaulting to weaker built-ins.
3. **Verify availability before use** — check whether the preferred external tool exists first (for example, `Get-Command <tool>` in PowerShell).
4. **Timebox installation attempts** — try to install/update preferred tools quickly; if blocked by policy, permissions, network, or excessive delay, then fall back.
5. **Fallback is contingency, not strategy** — use alternatives only when the preferred tool cannot be installed promptly or the user explicitly asks to avoid installs.
6. **Do not stop at missing tools** — either install the preferred tool or continue with the best available equivalent so work always advances.
7. **Be transparent about substitutions** — briefly state which tool was used and why when falling back from the preferred option.

Common examples:
- If `pandoc` is unavailable, install `pandoc`; only use markdown-native conversion if install is blocked.
- If `python` is unavailable, install Python; only use PowerShell/Node automation if install is blocked.
