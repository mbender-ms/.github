---
name: editorial-pass
description: "Orchestrate multi-pass fiction editing workflows. Tracks which passes have been run, issues found and resolved, and manuscript readiness. Designed for iterative editing — run repeatedly on successive drafts."
argument-hint: "Describe what you need, e.g. 'run a full character pass on the manuscript' or 'show me the current editorial status'"
user-invocable: true
---
# Editorial-Pass — Editing Orchestration Skill

Coordinate multi-pass editing across a fiction manuscript. Track progress, manage issues, and drive toward publication readiness.

## When to Use

- Starting a new editing cycle on a draft
- Deciding which pass to run next
- Tracking issues across editing iterations
- Reviewing what's been fixed and what's outstanding
- Determining if the manuscript is ready for publication
- Running a targeted pass on specific chapters after revisions

---

## Pass Types

| Pass | Skill | Focus | When to Run |
|------|-------|-------|-------------|
| **Character & Relationship** | `character-deepener` | Character depth, relationship dynamics, arcs, voice | First — fixes here cascade through everything else |
| **Continuity** | `continuity-checker` | Timeline, facts, details, plot threads, information flow | After structural changes stabilize |
| **Universe** | `universe-keeper` | Physics, technology rules, faction behavior, world consistency | Alongside or after continuity |
| **Prose** | `prose-tightener` | Word economy, pacing, dialogue, hooks, show-don't-tell | Last — don't polish prose that might change |
| **Final Polish** | All skills (review mode) | Quick spot-check across all dimensions | After all other passes complete |

---

## Editing Workflow

### Phase 1: Initial Assessment
Before running passes, read the manuscript (or a representative sample) and produce an initial assessment:

```markdown
## Initial Assessment
**Manuscript**: [Title]
**Word count**: [Approximate]
**Chapters**: [Count]
**Draft stage**: [First draft / Second draft / Revision / etc.]

### First Impressions
- **Characters**: [Strong/Adequate/Needs work] — [Brief note]
- **Relationships**: [Strong/Adequate/Needs work] — [Brief note]
- **Continuity**: [Clean/Some issues/Significant concerns]
- **Universe consistency**: [Solid/Soft spots/Major violations]
- **Prose quality**: [Publication-ready/Needs tightening/Needs significant work]
- **Pacing**: [Even/Uneven — where?]

### Recommended Pass Order
1. [First priority pass and why]
2. [Second priority pass and why]
3. [Third priority pass and why]

### Estimated Iterations
[How many full cycles this manuscript likely needs]
```

### Phase 2: Run Passes
Execute passes in the recommended order, using the appropriate skill for each.

### Phase 3: Track & Iterate
After each pass, update the editorial tracker and determine next steps.

---

## Editorial Tracker

Maintain a running tracker across all passes and iterations:

```markdown
# Editorial Tracker: [Manuscript Title]

## Pass History
| # | Pass Type | Chapters | Date | Issues Found | Critical | Status |
|---|-----------|----------|------|-------------|----------|--------|
| 1 | Character | All (1-18) | [Date] | 23 | 5 | ✅ Complete |
| 2 | Continuity | All (1-18) | [Date] | 14 | 3 | ✅ Complete |
| 3 | Universe | All (1-18) | [Date] | 8 | 2 | 🔄 In Progress |

## Issue Summary
| Category | Total Found | Resolved | Outstanding | Critical Outstanding |
|----------|-----------|----------|-------------|---------------------|
| Character | 23 | 19 | 4 | 0 |
| Continuity | 14 | 11 | 3 | 1 |
| Universe | 8 | 0 | 8 | 2 |
| Prose | — | — | — | — |
| **Total** | **45** | **30** | **15** | **3** |

## Outstanding Issues
| # | Category | Severity | Chapter | Description | Blocked By |
|---|----------|----------|---------|-------------|------------|
| 1 | Continuity | 🔴 | Ch 9 | Timeline gap — events don't fit 24-hour window | Needs author decision |
| 2 | Universe | 🔴 | Ch 14 | FTL cooldown violated | Fix in revision |
| 3 | Universe | 🔴 | Ch 7 | Ansible used from shuttle (station-only rule) | Fix in revision |
| 4-15 | Various | 🟡 | Various | [Details in pass reports] | Next revision |

## Chapters Most Needing Attention
| Chapter | Open Issues | Worst Severity | Notes |
|---------|------------|----------------|-------|
| Ch 9 | 4 | 🔴 | Timeline + continuity cluster |
| Ch 14 | 3 | 🔴 | Universe violations in climax |
| Ch 7 | 2 | 🟡 | Character + universe |

## Readiness Assessment
- [ ] All critical character issues resolved
- [ ] All critical continuity issues resolved
- [ ] All critical universe issues resolved
- [ ] Prose pass complete
- [ ] Final polish complete
- [ ] Chapter hooks verified
- [ ] Opening chapter is compelling
- [ ] Climax lands
- [ ] Ending satisfies (or appropriately cliffhangs)

**Status**: 🟡 Not Ready — [X] critical issues remaining
```

---

## Pass Configurations

### Full Pass (All Chapters)
Run the skill across the entire manuscript. Produces a comprehensive report.
- **When**: First time running a pass type, or after major structural changes
- **Output**: Full report with all issues catalogued

### Targeted Pass (Specific Chapters)
Run the skill on specific chapters.
- **When**: After revisions to specific sections, or when a full pass identified problem areas
- **Output**: Focused report on selected chapters

### Verification Pass (Re-check Fixed Issues)
Re-check previously flagged issues to confirm they're resolved.
- **When**: After author applies fixes from a previous report
- **Output**: Updated issue statuses (resolved, partially resolved, still present, new issues introduced)

### Quick Scan (Sampling)
Read every third chapter (or a representative sample) for a quick pulse check.
- **When**: Between major passes to gauge overall state
- **Output**: High-level assessment with estimated issues remaining

---

## Iteration Rules

### When to Re-Run a Pass
- After structural changes (chapters added, removed, reordered) → Re-run continuity and universe
- After character changes (backstory, motivation, arc) → Re-run character pass on affected chapters
- After world-building changes (new rules, changed constraints) → Re-run universe pass
- After prose tightening → Quick verification that meaning wasn't altered

### When to Move to the Next Pass
- All critical issues from current pass are resolved
- Important issues are resolved or have a plan
- Suggestions are catalogued but don't block progress

### When the Manuscript Is Ready
- Zero critical issues across all categories
- All important issues resolved or accepted as intentional
- Prose pass complete with no remaining pacing or word-economy concerns
- Final polish pass finds only minor suggestions
- The opening chapter hooks
- The climax delivers
- The ending satisfies (or devastates, for series cliffhangers)

---

## Working with Existing Materials

The editorial-pass skill integrates with the fiction-writer agent's outputs:

| Source | How the Editor Uses It |
|--------|----------------------|
| **World bible** (from world-builder) | Universe-keeper uses it as the rule registry |
| **Character sheets** (from character-forge) | Character-deepener uses them as consistency reference |
| **Beat sheet** (from story-architecture) | Verifies structural beats land where planned |
| **Relationship tracker** (from character-forge) | Checks that relationship progression matches intent |
| **Reference analysis** (from reference-reader) | Verifies voice stays calibrated to reference style |

---

## Report Aggregation

After multiple passes, produce a consolidated status:

```markdown
# Editing Status: [Manuscript Title]
**Last updated**: [Date]
**Draft version**: [#]
**Passes completed**: [List]
**Overall readiness**: [🔴 Needs major work / 🟡 Needs revision / 🟢 Publication-ready]

## By Chapter
| Ch | Character | Continuity | Universe | Prose | Overall |
|----|-----------|-----------|---------|-------|---------|
| 1  | ✅ | ✅ | ✅ | 🟡 | 🟡 |
| 2  | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3  | 🟡 | ✅ | ✅ | — | 🟡 |
| ... | ... | ... | ... | ... | ... |

## Blocking Issues
[List of issues that must be resolved before publication]

## Recommended Next Action
[What should the author do next?]
```

---

## Anti-Patterns

- ❌ Running prose tightening before structural issues are resolved — don't polish what might be cut
- ❌ Treating the tracker as busywork — it prevents issues from falling through cracks across iterations
- ❌ Running every pass every time — be strategic about which passes are needed based on what changed
- ❌ Declaring "done" with outstanding critical issues — critical means critical
- ❌ Editing indefinitely — know when diminishing returns set in. Perfectionism is the enemy of publication.
- ❌ Losing the forest for the trees — periodically step back and ask "is this a good book?" not just "are the details correct?"
