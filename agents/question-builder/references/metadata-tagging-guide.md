# Metadata Tagging Guide

This file is the authoritative contract for populating the final Question Builder CSV.

## Authoritative field definitions

| Field | Required | Description | Values |
|---|---|---|---|
| **Question** | Yes | The question as a customer would phrase it. | Free text |
| **Source** | Yes | Where the question came from. | - **AI system**: Questions from Copilot, Ask Learn, or other telemetry. <br>- **Community**: From Q&A, forums, support channels, or other customer-facing sources. <br>- **Patterns/Insights**: Derived from customer question patterns or aggregated insights. <br>- **Content dev**: From your own expertise or content gap analysis. <br>- **Product team**: Flagged by the product team - new features, edge cases, blind spots. |
| **Type** | Yes | The question type. | - **Conceptual**: What something is, how it works, or why it matters. <br>- **Procedural**: How to accomplish a task step by step. <br>- **Troubleshooting**: Diagnosing or fixing a problem. <br>- **Decision-making**: Choosing between options or approaches. <br>- **Fact-finding**: Looking up a specific detail, limit, or configuration value. <br>- **Coding**: Writing, modifying, or understanding code. |
| **Confidence** | Yes | How closely the question maps to known customer demand. | - **High**: Direct customer question or strong telemetry signal. <br>- **Medium**: Derived from customer patterns or multiple signals. Questions generated from customer pattern data are medium because they're grounded in real data but a few steps removed from direct customer input.<br>- **Low**: Content dev or product-driven exploratory question. <br><br> The goal of confidence indicators is context, not precision. Don't overthink it - consistency matters more than accuracy. |
| **Notes** | No | Why you added this question, known assumptions, or relevant context. | Free text |

## Pilot tagging guidance

- Canonical customer questions spreadsheet: `Source = AI system`, `Confidence = High`
- Fan-out variants from high-signal canonical questions: `Source = AI system`, `Confidence = High`

These questions are derived, not strictly verbatim, but grounded in strong telemetry signals.

## Type inference

Apply the first matching rule in order.

| Pattern (case-insensitive) | Type |
|---|---|
| `error` · `fail` · `broken` · `not working` · `issue` · `timeout` · `refused` · `cannot connect` · `500` · `502` · `503` · `504` · `denied` | Troubleshooting |
| `how do I` · `how to` · `steps to` · `configure` · `set up` · `create` · `deploy` · `migrate` · `enable` · `install` · `add` · `remove` · `update` · `change` | Procedural |
| `should I` · `which` · `compare` · `vs` · `versus` · `difference between` · `best practice` · `recommend` · `choose` · `when to use` | Decision-making |
| `what is the limit` · `what is the maximum` · `how many` · `what are the` · `pricing` · `cost` · `SLA` · `quota` · `region` · `availability` | Fact-finding |
| `code` · `script` · `command` · `CLI` · `PowerShell` · `Bicep` · `Terraform` · `ARM template` · `SDK` · `API call` · `example` · `sample` | Coding |
| `what is` · `explain` · `overview` · `how does` · `why does` · `architecture` · `concept` · `understand` | Conceptual |
| no match | Conceptual |

## Source assignment

Source is assigned by workflow, not inferred from the words in the question.

| Workflow | Source |
|---|---|
| Single article | Content dev |
| Multiple articles | Content dev |
| Microsoft Q&A | Community |
| Canonical CSV | AI system |
| Customer issue spec | Patterns/Insights |
| GitHub Issues | Community |
| WorkIQ M365 internal discussion | Product team |
| WorkIQ M365 documents or derived data | AI system |
| Ask Learn telemetry via canonical CSV | AI system |

## Confidence assignment

| Case | Confidence |
|---|---|
| Canonical CSV or Ask Learn telemetry import | High |
| Fan-out variants from high-signal canonical questions | High |
| Microsoft Q&A with `group_count >= 3` | High |
| Microsoft Q&A with `group_count < 3` | Medium |
| Customer issue spec | Medium |
| GitHub Issues | Medium |
| WorkIQ M365 | Medium |
| Single article or multiple articles | Low |
| Fan-out from non-canonical sources | One step lower than the source row, minimum Low |

## Deduplication

1. Normalize text to lowercase and collapse repeated spaces.
2. Compare questions using token-sort ratio.
3. Treat scores `>= 80%` as duplicates.

Conflict rules:

- **Fresh mode**: keep the row with higher confidence. If tied, keep source priority in this order: `AI system`, `Community`, `Patterns/Insights`, `Product team`, `Content dev`.
- **Append mode**: keep the existing CSV row and discard the duplicate incoming row.