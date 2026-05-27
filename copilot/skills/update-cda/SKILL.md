---
name: update-cda
version: 1.0.0
category: Utility
user-invocable: true
description: "Update the CDA agent file and skills to the latest server version while preserving local customizations. Compares sections between your installed file and the latest bundled version, applies template updates, and keeps any custom content you've added. Use when the user says: 'update my agent', 'update cda', 'check for updates', 'my agent is outdated', 'refresh my agent', 'sync cda', '/update-cda'."
argument-hint: "check | apply | diff"
---

## Update CDA agent and skills

This skill updates the CDA agent file (`cda.agent.md`) and bundled skills to the latest version shipped with CDA Cortex, while preserving any customizations the user has made.

### How it works

The extension writes the latest assembled templates to `~/.copilot/cda/latest/` on every activation. This skill compares the user's installed files against those latest templates.

### Workflow

1. **Read installed agent file** from VS Code prompts directory:
   - **Windows:** `%APPDATA%/Code/User/prompts/cda.agent.md`
   - **macOS:** `~/Library/Application Support/Code/User/prompts/cda.agent.md`
   - **Linux:** `~/.config/Code/User/prompts/cda.agent.md`

2. **Read latest template** from `~/.copilot/cda/latest/agents/cda.agent.md`

3. **Compare section by section** — split both files by `## ` headings, diff each section:
   - Section exists in both and is IDENTICAL → skip (no change needed)
   - Section exists in both and DIFFERS → show diff, ask user: keep theirs, take update, or merge
   - Section exists only in latest → new section added in update, offer to insert
   - Section exists only in installed → user customization, ALWAYS preserve

4. **Apply approved changes** — write the merged content back to the installed file

5. **Repeat for skills** — compare each skill in `~/.copilot/cda/latest/skills/` against installed skills in the VS Code prompts directory

### Commands

- **`check`** (default) — show what would change without applying
- **`apply`** — apply all non-conflicting updates automatically, prompt for conflicts
- **`diff`** — show full diff between installed and latest

### Important notes

- NEVER delete user customizations — sections, comments, or content the user added
- The `# Installed by CDA Cortex` marker in frontmatter identifies CDA-managed files
- If no installed file exists, this is a fresh install — tell the user to run the setup wizard
- Version comparison uses the `# Version:` comment in frontmatter
- After updating, confirm what changed and what was preserved
