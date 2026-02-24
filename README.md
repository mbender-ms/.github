# .github

Personal GitHub profile repo containing Copilot prompt files, agent definitions, and chat modes for Azure documentation workflows.

## Prompts

| File | Type | Description |
|------|------|-------------|
| `freshness-review.prompt.md` | Skill | Review current article for outdated content |
| `save-and-pr.prompt.md` | Skill | Commit changes, push branch, and create PR |
| `new-article.prompt.md` | Skill | Scaffold a new Azure docs article from a template |
| `work-item-status.prompt.md` | Skill | Check ADO work item progress and completion status |
| `complete-fact-check.prompt.md` | Skill | Full fact-check with standalone report file |
| `fact-check-and-edit.prompt.md` | Skill | Fact-check with in-place edits and chat references |
| `microsoft-researcher.prompt.md` | Skill | Research using only official Microsoft docs |
| `content-developer.agent.md` | Agent | Content Developer workflow agent (v6.0.3) |
| `microsoft-fact-checker.agent.md` | Agent | Microsoft Documentation Fact-Checking agent |
| `content-developer-beta.chatmode.md` | Chat Mode | Azure Documentation Workflow chat mode |

## Usage

These prompt files are automatically available in VS Code via GitHub Copilot when this repo exists under your GitHub account as `.github`.

- **Skills** (`#` prefix): `#freshness-review`, `#fact-check-and-edit`, `#microsoft-researcher`, etc.
- **Agents** (`@` prefix): `@content-developer`, `@microsoft-fact-checker`
- **Chat Modes**: Select from the chat mode picker in Copilot Chat
