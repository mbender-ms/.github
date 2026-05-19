# Build Rebuild Guide

This guide defines the target structure for the `.github` repo after the April 2026 consolidation work.

## Goal

Keep one canonical runtime layout for Copilot customizations and remove ambiguous duplicate paths.

## Canonical layout

```text
.github/
├── agents/
├── instructions/
├── prompts/
├── references/
├── copilot/
│   └── skills/
├── .vscode/
├── README.md
├── copilot-instructions.md
└── sync-prompts.ps1
```

## Keep

- `copilot/skills/` as the source of truth for all active skills
- `prompts/` for standalone prompts
- `agents/` for canonical shared agents
- `instructions/` for workspace instructions
- `references/` for shared reference content
- `.vscode/`, `README.md`, `copilot-instructions.md`, and `sync-prompts.ps1`

## Consolidate

- Keep skill-specific workflow prompt assets inside each skill's `assets/` directory
- Keep standalone reusable prompts in `prompts/`
- Prefer root `agents/` over agent definitions buried inside skill assets
- Keep global rules minimal in `copilot-instructions.md`
- Keep personal and service-specific context in `copilot/skills/my-workflow/`

## Archive

- `.archive/skills-root-20260413/` contains the former top-level `skills/` tree
- `.archive/non-target-20260413/` contains non-target items removed from the live runtime tree during rebuild
- `conflict-log-as.md` is historical merge metadata and has been archived
- `.factcheck_cache/` is optional runtime data, not source-of-truth content, and can be recreated by tooling as needed
- `copilot/skills/docs-screenshot/` was an empty non-target skill folder and has been archived

## Why the root skills tree was archived

- `README.md` documents `copilot/skills/` as the active skill location
- `sync-prompts.ps1` syncs from `copilot/skills/*/assets/` and `prompts/`
- Active skill references point to `copilot/skills/...`
- The archived root tree had drifted and included broken prompt references

## Rebuild sequence

1. Start from the stable baseline in `.oldGithub/.github/` for canonical skill directories that were already working.
2. Keep these canonical baseline directories unless there is a verified newer improvement:
   - `_shared`
   - `ado-work-items`
   - `article-integrity`
   - `azure-quickstart-templates`
   - `doc-writer`
   - `documentor-workflow`
   - `freshness-pass`
   - `my-workflow`
   - `sources`
3. Merge validated current improvements into `copilot/skills/`:
   - `doc-verifier/`
   - `repo-recon/`
   - `specificity-engineering/`
4. Keep the current root directories that are part of the runtime model:
   - `agents/`
   - `instructions/`
   - `prompts/`
   - `references/`
5. Remove or archive any remaining duplicate structures that imply a second canonical skill path.

## Validation checklist

- `copilot-instructions.md` points only to canonical skill paths
- `sync-prompts.ps1` still discovers all prompts and agents that should sync
- No active skill depends on `.archive/skills-root-20260413/`
- `README.md` documents only one active skill tree
- Agent references resolve to `agents/` unless intentionally kept as compatibility stubs

## Current implementation status

- Archived former root `skills/` tree to `.archive/skills-root-20260413/`
- Updated `README.md` to document the canonical runtime layout
- Added this rebuild guide for follow-on manual merge work
- Archived non-target rebuild leftovers to `.archive/non-target-20260413/`
- Removed `conflict-log-as.md` from the live root and archived it
- Removed the live `.factcheck_cache/` directory and archived its existing sample cache state
- Removed the empty `copilot/skills/docs-screenshot/` folder from the live skill tree and archived it
- Live `copilot/skills/` now contains only the canonical keep set plus validated current improvements
