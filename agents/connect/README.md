# Connect Impact Agent

A self-contained GitHub Copilot agent that generates two Microsoft Connect artifacts for any review period:

- **`slides-artifact.md`** — content for your Microsoft Impact Summary PowerPoint
- **`connect-artifact.md`** — content for the Microsoft Connect tool form

The agent gathers impact data from four sources (personal notes, Microsoft 365 via WorkIQ, Azure DevOps, and GitHub PRs), organizes it under the three org impact categories, and writes both artifacts in one pass.

---

## Prerequisites

| Requirement | Notes |
| --- | --- |
| VS Code | Latest stable |
| GitHub Copilot extension | Agent mode enabled |
| ADO MCP server | Required — used for work item queries |
| GitHub MCP server | Required — used for PR search |
| WorkIQ MCP server | Optional — used for M365 Teams/meeting data; agent skips gracefully if unavailable |
| `.github` repo cloned locally | This package must be in your VS Code workspace |

---

## Quick start

1. **Clone this repo** and open the `.github` folder as a VS Code workspace folder.

2. **Update `config/variables.yaml`** with your personal values for the current Connect period:
   - Connect period dates
   - Path to your personal notes document
   - GitHub username and target repo
   - ADO query URLs

3. **Update the three reference files** (see [Annual maintenance](#annual-maintenance)) if this is a new fiscal year.

4. Open `agents/connect-writer.agent.md` in VS Code.

5. Open the Copilot chat panel, switch to **Agent mode**, select the `connect-writer` agent, and start a new conversation.

6. At the pre-flight prompt, verify the three reference files are current, then type **"ready"**.

7. Answer the 8 setup questions in the batch prompt (accept defaults or provide your own values).

8. Wait for the agent to gather data and write the artifacts. Both files will appear in `agents/connect/output/` (or your custom output path).

---

## Annual maintenance

Each Connect period, update two things:

### 1. `config/variables.yaml`

| Field | What to update |
| --- | --- |
| `connectPeriodStart` | New period start date (`YYYY-MM-DD`) |
| `connectPeriodEnd` | New period end date (`YYYY-MM-DD`) |
| `personalNotesPath` | Path to your notes for the new period |
| `exampleDocumentPath` | Path to a prior Connect doc (optional) |
| `adoUserStoriesQuery` | Updated ADO query URL for the new period |

### 2. Reference files (when the org updates them)

Verify and update these files if the org has changed the definitions or templates:

| File | What changes |
| --- | --- |
| `references/impact-categories.md` | If org impact category names or descriptions changed |
| `references/slide-template.md` | If the Impact Summary PowerPoint slide structure changed |
| `references/smart-goal-examples.md` | Each fiscal year — new uber goal titles and examples |

The agent shows a pre-flight prompt at every run to remind you to do this check.

---

## Artifact conversion — ingesting binary input files

The agent can auto-detect and convert binary input files specified in `exampleDocumentPath`:

| Format | Behavior |
| --- | --- |
| `.md`, `.txt` | Read directly — no conversion needed |
| `.pdf`, `.docx`, `.pptx` | Agent attempts conversion using the artifact-conversion skill |
| Conversion fails | Agent skips style reference and notes the gap in the completion summary |

**Recommendation:** For the most reliable experience, convert your prior Connect document to `.md` yourself and save it locally before running. Update `exampleDocumentPath` in `variables.yaml` to point to the `.md` file.

**Templates (slide deck, connect form):** Store and maintain these as `.md` files in the `references/` folder. The agent never reads binary `.pptx` or `.docx` templates — only the markdown equivalents here. When the PowerPoint template changes, update `references/slide-template.md` directly.

---

## Output files

Both output files are written to `{outputFolder}` (default: `agents/connect/output/`).

| File | Contents |
| --- | --- |
| `slides-artifact.md` | Populated table-format content for each slide section: Content Areas, Changes & Challenges, Quality, Peers & Partners, Continuous Improvement, Security, Diversity & Inclusion |
| `connect-artifact.md` | Full narrative for the Connect tool: past results (under 3 categories), optional stretch activities, optional setbacks, and 3 sections of SMART goals for the next period |

> [!IMPORTANT]
> The `output/` folder is listed in `.gitignore` in this package. Your personal Connect drafts will never be accidentally committed to a shared repo. If you redirect output to a path outside this repo, manage that location's privacy yourself.

---

## File structure

| File | Purpose |
| --- | --- |
| `agents/connect-writer.agent.md` | Main agent definition — the file you run in VS Code agent mode (lives at `agents/` root for VS Code discovery) |
| `README.md` | This file — setup, usage, and reference guide |
| `.gitignore` | Prevents `output/` from being committed to the shared repo |
| `config/variables.yaml` | All personal config: dates, paths, GitHub username, ADO query URLs |
| `instructions/data-gathering.instructions.md` | Five-step pipeline for collecting impact data from personal notes, M365, ADO, and GitHub |
| `instructions/organization-rules.instructions.md` | Rules for assigning impact items to the three impact categories and ordering them |
| `instructions/writing-guidelines.instructions.md` | Style and framing rules: big rocks, impact-first, measurable outcomes, collaborative tone |
| `references/impact-categories.md` | Definitions of the three org impact categories — **update each fiscal year** |
| `references/connect-template.md` | Mirrors the Connect tool form structure — **update if Microsoft changes the form** |
| `references/slide-template.md` | Mirrors the Impact Summary PowerPoint sections — **update if the slide deck changes** |
| `references/smart-goal-examples.md` | Uber goal titles and SMART goal examples — **update each fiscal year** |
| `output/` | Default output folder (gitignored) — `slides-artifact.md` and `connect-artifact.md` written here |

---

## Sharing with teammates

This package is designed to be shared. Teammates:

1. Clone the `.github` repo (or copy the `agents/connect/` folder into their own `.github` repo).
2. Update `config/variables.yaml` with their own values — all `PLACEHOLDER` fields.
3. Verify the three annual reference files are current for the current fiscal year.
4. Run the agent per the Quick start steps above.

The `.gitignore` ensures no personal data (output artifacts or personal file paths) are accidentally committed to a shared repo.

---

## Troubleshooting

| Problem | Solution |
| --- | --- |
| WorkIQ MCP unavailable | Agent skips Source 2 (M365 data) automatically and notes the gap in the completion summary. Output is still generated from remaining sources. |
| ADO query returns 403 or no results | Update `adoUserStoriesQuery` in `config/variables.yaml` with a fresh query URL. Verify you're signed into the correct ADO organization. |
| Binary file conversion fails | Agent skips the style reference and continues. For best results, pre-convert your example doc to `.md`. |
| Path errors on personal notes | Use an absolute path for `personalNotesPath` in `variables.yaml`. On Windows, use double backslashes: `C:\\Users\\you\\notes.md`. |
| Agent says "PLACEHOLDER" in questions | Update `config/variables.yaml` — one or more required fields have not been filled in. |
| Artifacts not appearing in output folder | Verify VS Code workspace root includes the `.github` folder. The `agents/connect/output/` path is relative to the workspace root. |
