---
name: QandA-search
description: >-
  Look up the Microsoft Q&A tag slug and tag ID for an Azure service, then
  optionally run the Q&A scraper to harvest community questions. Use as a
  building block in agents that need real customer Q&A signal as a source.
argument-hint: "Provide the Azure service name — e.g., 'Azure Load Balancer'"
user-invocable: true
---

# Q&A Search Skill

Look up the Microsoft Q&A tag for an Azure service and return the tag slug, tag ID, and tag URL.
Optionally invoke the scraper to collect raw community questions.

## When to use

- As a building block inside an agent that needs Q&A signal as one of its sources
- Quick lookup of a service tag slug and ID before running a scraper manually
- Verifying the correct tag URL for a service before scraping

## Tag lookup

1. Open `skills/QandA-search/references/qa-tag-index.md`.
2. Find the row matching the requested service.
3. Return:
   - **Tag slug** (e.g., `azure-load-balancer`)
   - **Tag ID** (e.g., `230`)
   - **Tag URL**: `https://learn.microsoft.com/en-us/answers/tags/{tag_id}/{tag_slug}`

If the service is not in the index, instruct the user to find the tag by browsing:
`https://learn.microsoft.com/en-us/answers/tags/`
and extracting the ID and slug from the URL.

## Optional: run the scraper

When the calling agent or user also wants harvested questions, pass the tag slug and tag ID
to the Q&A scraper. This skill does not bundle the scraper itself — use the
`qa-customer-signal` skill or `qa-gap-analyst` agent for the full pipeline.

## Reference files

- `skills/QandA-search/references/qa-tag-index.md` — service-to-tag lookup table
