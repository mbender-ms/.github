# Chunk Scoring Rubric

Use this rubric to assign relevance ratings to each chunk in the inventory table.

## Relevance Ratings

### Γ£à Direct

The chunk **directly answers the query**. It contains the primary procedure, concept, or information the user asked about with no detour.

**Criteria:**
- The section heading matches the query intent (e.g., "Create a virtual network using the Azure portal" for a portal creation query)
- The deployment method matches what was asked (portal steps for a portal query)
- The chunk is a procedural section that the user would execute to complete the task
- The chunk is from the canonical article for the topic (quickstart, how-to, or reference)

**Examples:**
- "## Create a virtual network using the Azure portal" ΓåÆ Γ£à Direct for "how do I create a VNet in the portal"
- "## Configure DNAT rules" ΓåÆ Γ£à Direct for "how do I configure Azure Firewall DNAT rules"

---

### ΓÜá∩╕Å Partial

The chunk is **related but incomplete**. It addresses the topic but is missing critical steps, covers only part of the procedure, or requires other chunks to be actionable.

**Criteria:**
- The chunk is an intro/overview section with no steps
- The chunk covers a prerequisite or follow-up step rather than the main task
- The chunk is from a related article (e.g., "Create, change, or delete a virtual network" for a quickstart query)
- The chunk is cut mid-procedure at a chunk boundary

**Examples:**
- Intro overview paragraph with diagram but no steps ΓåÆ ΓÜá∩╕Å Partial
- "## Prerequisites" section for the target article ΓåÆ ΓÜá∩╕Å Partial
- A chunk that begins "4. Select **IP Addresses** tab..." without the preceding steps ΓåÆ ΓÜá∩╕Å Partial

---

### ≡ƒöÇ Tangential

The chunk is **same topic area but different task or scenario**. The user could conceivably find it useful but it does not answer the query.

**Criteria:**
- Same service, different operation (e.g., "delete a virtual network" returned for "create a virtual network")
- Same operation, different scenario (e.g., "Create a VNet in an Extended Zone" returned for a general VNet creation query)
- A feature variant of the main topic (e.g., "Create a virtual network with encryption" for a basic VNet creation query)
- A related but more advanced service (e.g., Virtual Network Manager for a basic VNet query)

**Examples:**
- "Create a virtual network in an Extended Zone" ΓåÆ ≡ƒöÇ Tangential for basic VNet creation
- "Create a virtual network with encryption" ΓåÆ ≡ƒöÇ Tangential for basic VNet creation
- "Virtual Network Manager instance creation" ΓåÆ ≡ƒöÇ Tangential for basic VNet creation

---

### Γ¥î Noise

The chunk **should not have been returned** for this query. It is a downstream step, wrong deployment method, post-task validation, or unrelated service.

**Criteria:**
- Wrong deployment method (ARM template steps returned for a portal query)
- Post-task steps that only make sense after the primary task is complete (e.g., "Connect to a virtual machine" for "create a virtual network")
- Review/validation sections for a different deployment method (e.g., "Review deployed resources" with CLI/Bicep/Terraform commands)
- A downstream task in a multi-step tutorial (e.g., "Create virtual machines" returned for "create a virtual network")
- An unrelated service article that shares vocabulary with the query

**Examples:**
- "## Review the template" (ARM template review) ΓåÆ Γ¥î Noise for a portal query
- "## Create virtual machines" ΓåÆ Γ¥î Noise for "create a virtual network"
- "## Connect to a virtual machine" ΓåÆ Γ¥î Noise for "create a virtual network"
- "## Review deployed resources" with CLI/PS/Terraform commands ΓåÆ Γ¥î Noise for a portal query

---

## Scoring summary

| Rating | Short description | Actionable for query? | Should have been returned? |
|--------|-------------------|----------------------|---------------------------|
| Γ£à Direct | Directly answers query | Yes | Yes |
| ΓÜá∩╕Å Partial | Related but incomplete | Partially | Borderline |
| ≡ƒöÇ Tangential | Same area, different task | Unlikely | Borderline |
| Γ¥î Noise | Wrong method or downstream step | No | No |

---

## Signal-to-noise calculation

After scoring all chunks, calculate the signal-to-noise ratio:

```
Direct + Partial = Signal
Tangential + Noise = Non-signal

Signal ratio = (Direct + Partial) / Total results ├ù 100
```

**Thresholds:**
- **ΓëÑ 70% signal** ΓÇö Good retrieval quality
- **50ΓÇô69% signal** ΓÇö Moderate quality; structural improvements would help
- **< 50% signal** ΓÇö Poor retrieval quality; significant article or pipeline changes needed

Report the signal ratio in the report's Signal Summary section.
