---
name: learn-screenshot-alt-text
description: Writes Microsoft Learn-compliant screenshot alt text. Use when creating or updating screenshot descriptions for documentation, PRs, or accessibility fixes.
---

# Skill: Write Screenshot Alt Text for Microsoft Learn

## Purpose
Generate high-quality, Learn-compliant alt text for screenshots used in Microsoft Learn documentation. Ensure accessibility, consistency, and alignment with contributor guide expectations.

---

## When to Use
Use this skill when:
- adding or updating screenshots in documentation
- fixing accessibility issues flagged in PR review or authoring tools
- replacing generic screenshot alt text
- creating new screenshot descriptions from surrounding procedural steps

---

## Inputs
- Screenshot or screenshot description
- Surrounding content
- Product or UI surface
- Scenario or task being documented

---

## Output
Concise alt text that:
- describes the purpose of the screenshot
- captures the user-relevant state or outcome
- starts with screenshot wording
- ends with a period

---

## Purpose-based alt text pattern

Alt text should describe what the screenshot **shows the learner** (the action, outcome, or state), not just what appears visually.

- **Preferred pattern**: `Screenshot that shows [action/outcome the learner cares about].`
- **Example**: `Screenshot that shows the Networking settings pane in Azure portal with inbound security rules configured.`

## Guidelines

- **Be concise and task-relevant**: Include only the UI state, action, error, or outcome that matters to the procedure.
- **End with a period**.
- **Avoid generic alt text** like "Screenshot of the Azure portal," "Configuration screen," or "Settings page."
- **Don't inventory the full UI** or repeat surrounding procedure text unless it's essential for clarity.

## Examples of good alt text

- Screenshot that shows the Network Manager configuration page with security admin rules listed.
- Screenshot that shows an error message indicating invalid IP range.
- Screenshot that shows the save confirmation after deploying changes.

## Examples to avoid

- ❌ Azure portal screenshot
- ❌ Configuration dialog box
- ❌ Settings and options displayed (too vague)

---

## Output Instructions
- Return only the alt text unless the user asks for explanation.
- Prefer the minimum wording needed to preserve meaning.
- Optimize for clarity, accessibility, and retrieval.