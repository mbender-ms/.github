---
name: learn-screenshot-alt-text-lint
description: Lints and fixes screenshot alt text for Microsoft Learn content. Use when reviewing image alt text, accessibility issues, PR feedback, or bulk cleanup of screenshot descriptions.
---

# Skill: Lint Screenshot Alt Text for Microsoft Learn

## Purpose
Review screenshot alt text for Microsoft Learn documentation, identify violations, and either:
1. return a concise lint report, or
2. rewrite the alt text so it is compliant.

This skill is for screenshot alt text only. It should not be used for diagrams, charts, icons, logos, or decorative images unless the user explicitly asks to adapt the workflow.

---

## When to Use
Use this skill when the user asks to:
- review screenshot alt text
- lint or audit alt text
- fix accessibility issues
- clean up screenshot descriptions
- enforce Learn-compliant screenshot alt text
- bulk-review multiple screenshot alt text entries
- rewrite weak or generic screenshot alt text

---

## Inputs
The user may provide:
- one alt text string
- several alt text strings
- screenshot markdown/image blocks
- surrounding procedural text
- PR diff content
- a file containing screenshot references and alt text

If surrounding content is available, use it to determine the screenshot's actual purpose.

---

## Required Output Modes

### Mode 1: Lint report
Use this mode when the user asks to review, lint, audit, or evaluate.

For each alt text entry, return:
- Original
- Status: Pass or Fail
- Issues
- Suggested fix

### Mode 2: Rewrite
Use this mode when the user asks to fix, rewrite, tighten, or improve.

Return only the improved alt text unless the user asks for commentary.

### Mode 3: Batch summary
Use this mode when the user provides multiple entries and asks for a summary.

Return:
- total reviewed
- passed
- failed
- common issue categories
- corrected results

---

## What to look for

When reviewing alt text, check that it:
- Describes the **purpose or outcome** shown, not just the visual appearance
- Is concise and task-relevant
- Ends with a period
- Avoids generic patterns like "Screenshot of the Azure portal"
- Doesn't inventory every UI element

## Common issues to fix

| Issue | Fix |
|-------|-----|
| Generic alt text ("Screenshot of the portal") | Rewrite to show what the learner sees: "Screenshot that shows the inbound security rules configured in Network Manager." |
| Too verbose or inventories UI | Trim to only what's needed for the procedure. |
| Missing the action or outcome | Add context: what is the user doing or what result are they seeing? |
| No period at the end | Add period. |
| Appearance-based instead of purpose-based | Shift focus to the learner's task: "Configuration screen" → "Screenshot that shows the completed Network Manager configuration." |

## When summarizing multiple issues

- List the 2–3 most common patterns found
- Provide corrected versions of representative examples
- Explain the pattern so the author can apply it to remaining instances

### Rule 4: Include product or surface when needed
When helpful for clarity, include the product or surface, such as:
- Azure portal
- Visual Studio Code
- terminal
- Microsoft Entra admin center

Fail if the missing product makes the alt text ambiguous.

### Rule 5: Include embedded text only when essential
If the screenshot contains critical text that matters to the user outcome, include it briefly or ensure the surrounding content already states it.

Fail if:
- the screenshot contains an important error or key label that is omitted
- the alt text depends on text in the image that is not available elsewhere

### Rule 6: Keep it concise
Target:
- one sentence
- concise and unambiguous
- generally 40 to 150 characters when possible

Fail if:
- too short to be meaningful
- excessively long
- packed with unnecessary detail

### Rule 7: End with a period
Pass if the alt text ends with a period.

### Rule 8: Avoid redundancy
Fail if the alt text:
- repeats the surrounding step almost word-for-word
- repeats captions without adding value
- uses placeholder/generic wording only

### Rule 9: Reject weak patterns
Treat these as failures unless the surrounding context makes them acceptable:
- Screenshot of the Azure portal.
- Screenshot of a page.
- Configuration screen.
- Settings page.
- Screenshot showing options.
- Image of ...
- Picture of ...

---

## Decision Logic

### Pass
The alt text:
- starts with "Screenshot that shows" or equivalent screenshot wording
- explains the reason the screenshot exists
- includes the key task-relevant state or outcome
- is concise
- ends with a period

### Fail
The alt text:
- is generic
- focuses on appearance instead of purpose
- omits the important state
- is too short or too long
- repeats surrounding text without adding value
- does not clearly help a non-visual reader complete or understand the step

---

## Rewrite Strategy
When rewriting:
1. Identify the screenshot's purpose from surrounding content.
2. Identify the one thing the learner needs to notice.
3. Write a single sentence using this pattern:

`Screenshot that shows [product or UI] with [key state, action, or outcome].`

4. Keep only the task-relevant detail.
5. End with a period.

Do not preserve bad phrasing just because it appears in the original.

---

## Preferred Output Examples

### Example: Fail
Original:
Connector-SVR Properties window.

Status:
Fail

Issues:
- Does not explain why the screenshot matters
- Does not identify the relevant state
- Too generic

Suggested fix:
Screenshot that shows the Connector-SVR Properties window with the Delegation tab selected.

### Example: Fail
Original:
Screenshot of the Azure portal.

Status:
Fail

Issues:
- Too generic
- No task-relevant state
- Does not explain purpose

Suggested fix:
Screenshot that shows the Azure portal Virtual machines page with contoso-vm selected.

### Example: Pass
Original:
Screenshot that shows the deployment status marked as Succeeded in the Azure portal.

Status:
Pass

Issues:
- None

Suggested fix:
No change needed.

---

## Batch Review Format
When reviewing multiple entries, use this structure:

### Summary
- Reviewed: X
- Passed: X
- Failed: X

### Common issues
- Too generic
- Missing task-relevant state
- Missing product context
- Too short
- Redundant with surrounding text

### Results
#### 1
Original: ...
Status: Pass/Fail
Issues: ...
Suggested fix: ...

#### 2
Original: ...
Status: Pass/Fail
Issues: ...
Suggested fix: ...

---

## Strict Output Instructions
- If the user asks to lint, provide a lint report.
- If the user asks to fix, return corrected alt text.
- If the user asks to bulk-review, provide both summary and corrected results.
- Be direct.
- Do not add unnecessary explanation unless requested.