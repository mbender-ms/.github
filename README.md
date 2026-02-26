# .github

Personal GitHub profile repo containing Copilot prompt files, agent definitions, and chat modes for Azure documentation workflows.

## Prompts

| File | Type | Description |
|------|------|-------------|
| `complete-fact-check.prompt.md` | Skill | Fact-check the current article against official Microsoft documentation |
| `complete-fact-checker-internal.prompt.md` | Skill | Fact-check using both public and internal Microsoft resources |
| `complete-freshness-review.prompt.md` | Skill | Full freshness review — update outdated content, fact-check, fix links, and optionally commit + PR |
| `fact-check-and-edit.prompt.md` | Skill | Fact-check and edit the current article in-place, with chat references |
| `microsoft-researcher.prompt.md` | Skill | Research a topic using only official Microsoft documentation and resources |
| `sources-for-fact-checking-publ.md` | Reference | Comprehensive list of public authoritative sources for fact-checking |
| `microsoft-fact-checker.agent.md` | Agent | Microsoft Documentation Fact-Checking agent |

## Usage

These prompt files are automatically available in VS Code via GitHub Copilot when this repo exists under your GitHub account as `.github`.

- **Skills** (`#` prefix): `#complete-fact-check`, `#fact-check-and-edit`, `#microsoft-researcher`, etc.
- **Agents** (`@` prefix): `@microsoft-fact-checker`

## Changelog

### 2026-02-26 — [PR #1](https://github.com/mbender-ms/.github/pull/1)
- Added `ado-work-item-standards.prompt.md` — ADO work item standards per Azure Core Content Standards
- Added `CIA-Analysis.prompt.md` — Agent prompt for Customer Incidents Analysis reports
- Added `Azure-Networking-incident-analysis.md` — Azure Networking incident analysis report
