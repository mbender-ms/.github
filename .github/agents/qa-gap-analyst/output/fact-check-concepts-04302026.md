# Fact-Check Report: Azure Load Balancer concepts

**Article:** `articles/load-balancer/concepts.md`
**Live URL:** https://learn.microsoft.com/azure/load-balancer/concepts
**Report date:** April 30, 2026
**Reviewer:** GitHub Copilot (microsoft-fact-checker mode)
**Gap analysis source:** azure-load-balancer-gap-analysis-04302026.csv

---

## Summary

Overall accuracy: **High** — core technical claims are correct. Two structural issues and one content gap require fixes.

| Finding | Severity | Type |
|---|---|---|
| H1 does not match frontmatter `title` | Medium | Standards violation |
| Five-tuple list uses bullets instead of numbered list | Low | Standards violation |
| No explanation of session affinity stickiness limitation | Medium | Content gap |
| TLS passthrough claim is accurate | — | Confirmed accurate |
| Layer 4 behavior claims are accurate | — | Confirmed accurate |

---

## Finding 1: H1 does not match frontmatter title

**Severity:** Medium

### What changed

- **Original H1:** `# Azure Load Balancer algorithm`
- **Frontmatter title:** `Azure Load Balancer concepts`
- **Status:** Inaccurate — violates Microsoft Learn authoring standards

### Why this matters

Microsoft Learn authoring standards require the H1 to match the `title` in frontmatter exactly. The current H1 ("Azure Load Balancer algorithm") is narrower than the frontmatter title ("Azure Load Balancer concepts") and doesn't accurately represent the article's scope, which covers session affinity, distribution modes, Layer 4 behavior, and TLS passthrough — not just the algorithm.

### Evidence

- **Standard:** Microsoft Learn Markdown Authoring Standards, "Every article must have exactly one H1 (`#`) matching the `title` in frontmatter"
- **Frontmatter title field (line 2):** `title: Azure Load Balancer concepts`
- **H1 (line 14):** `# Azure Load Balancer algorithm`

### Proposed fix

```diff
- # Azure Load Balancer algorithm
+ # Azure Load Balancer concepts
```

---

## Finding 2: Five-tuple described with bullet points instead of numbered list

**Severity:** Low

### What changed

- **Original:** Bold bullet list (`- **Source IP address**`)
- **Official docs (live):** Numbered list (1–5)
- **Status:** Minor inconsistency with live canonical page formatting

### Why this matters

The live learn.microsoft.com page uses a numbered list for the five-tuple. Using bullets is not wrong but makes the local article drift from the canonical published format.

### Evidence

- **Primary source:** https://learn.microsoft.com/azure/load-balancer/concepts
- Content excerpt: "1. **Source IP address** 2. **Source port** 3. **Destination IP address** 4. **Destination port** 5. **IP protocol number to map flows to available servers**"

### Proposed fix

```diff
-You can also use session affinity [distribution mode](distribution-mode-concepts.md) which uses two-tuple or three-tuple based load balancing.
+The five-tuple includes:
+
+1. **Source IP address**
+2. **Source port**
+3. **Destination IP address**
+4. **Destination port**
+5. **IP protocol number to map flows to available servers**
```

---

## Finding 3: Missing session affinity stickiness limitation (content gap)

**Severity:** Medium — directly addresses gap analysis question: *"Azure Load Balancer: SourceIP Session Persistence Not Working Across Multiple Ports for FTP Passive Mode"*

### What changed

- **Original:** Article states users "can also use session affinity distribution mode which uses two-tuple or three-tuple based load balancing" without caveats
- **Official docs:** Explicitly state session affinity only persists within a single transport session; a new connection from the same source IP gets a new source port and may route to a different backend
- **Status:** Content gap — the article omits a critical behavioral nuance that causes widespread user confusion

### Why this matters

From the gap analysis, session persistence not working is a top support question (e.g., "SourceIP Session Persistence Not Working Across Multiple Ports for FTP Passive Mode", "Session Related issue while using Load Balancer"). The article implies session affinity means "same client always goes to same backend" but this is only true within a single transport session.

Official docs state: *"The algorithm provides stickiness only within a transport session. When the client starts a new session from the same source IP, the source port changes and causes the traffic to go to a different backend instance."*

This is especially critical for FTP passive mode, which uses multiple TCP connections (control + data), each with different source ports — meaning session affinity does not keep both connections on the same backend.

### Evidence

- **Primary source:** https://learn.microsoft.com/azure/load-balancer/distribution-mode-concepts
- Content excerpt: "The algorithm provides stickiness only within a transport session. When the client starts a new session from the same source IP, the source port changes and causes the traffic to go to a different backend instance."
- **Supporting source:** https://learn.microsoft.com/azure/load-balancer/load-balancer-best-practices — "enabling session affinity can cause uneven load distribution"

### Proposed fix

Add a note after the session affinity reference:

```markdown
You can also use session affinity [distribution mode](distribution-mode-concepts.md) which uses two-tuple or three-tuple based load balancing.

> [!NOTE]
> Session affinity provides stickiness only within a single transport session. When a client opens a new connection from the same source IP, the source port changes, and the new connection may route to a different backend instance. Applications that open multiple connections per session, such as FTP passive mode, may not behave as expected with session affinity.
```

---

## Finding 4: TLS passthrough statement — confirmed accurate

**Status:** Accurate

### Verification

The article states: *"because the load balancer doesn't interact with the TCP payload nor does it provide TLS offload, you can build comprehensive encrypted scenarios."*

Official documentation confirms: *"Azure Load Balancer operates at Layer 4 and does NOT support TLS termination — it only supports TCP, UDP, and TCP_UDP protocols. For TLS termination in Azure, use Azure Application Gateway (Layer 7)."*

- **Source:** https://learn.microsoft.com/azure/load-balancer/network-load-balancing-aws-to-azure-how-to
- **Last verified:** April 30, 2026

> [!NOTE]
> While the TLS passthrough claim is accurate, the article does not address the related gap question *"mTLS with Azure Load Balancer not working"* from the Q&A analysis. mTLS is handled end-to-end between client and backend VM; the load balancer is transparent. Consider adding a sentence clarifying that mTLS must be configured on backend VMs, not on the load balancer. See [cross-region-overview fact-check](fact-check-cross-region-overview-04302026.md) and the FAQ article for related TLS/SSL FAQ updates.

---

## Finding 5: Five-tuple hash and Layer 4 claims — confirmed accurate

**Status:** Accurate

The article's description of the five-tuple algorithm, Layer 4 operation, flow symmetry, and source IP preservation all match the current official documentation exactly.

- **Source:** https://learn.microsoft.com/azure/load-balancer/concepts
- **Source:** https://learn.microsoft.com/azure/load-balancer/distribution-mode-concepts
- **Last verified:** April 30, 2026

---

## Gap analysis opportunities for this article

From the Q&A gap analysis, the following questions are partially answered by this article but would benefit from explicit callouts:

| Q&A Question | Gap type | Recommendation |
|---|---|---|
| SourceIP Session Persistence Not Working Across Multiple Ports for FTP Passive Mode | update-article | Add Note per Finding 3 above |
| mTLS with Azure Load Balancer not working | update-article | Add sentence clarifying mTLS is backend-only |
| Having issue with SSL certificate configuration | update-article | Add pointer to Application Gateway for TLS offload |

---

## References

| Source | URL | Verified |
|---|---|---|
| Azure Load Balancer algorithm (concepts) | https://learn.microsoft.com/azure/load-balancer/concepts | April 30, 2026 |
| Azure Load Balancer distribution modes | https://learn.microsoft.com/azure/load-balancer/distribution-mode-concepts | April 30, 2026 |
| Azure Load Balancer best practices | https://learn.microsoft.com/azure/load-balancer/load-balancer-best-practices | April 30, 2026 |
| AWS to Azure Load Balancer migration (TLS comparison) | https://learn.microsoft.com/azure/load-balancer/network-load-balancing-aws-to-azure-how-to | April 30, 2026 |
| Microsoft Learn Markdown Authoring Standards | c:\github\.github\.github\instructions\markdown-authoring.instructions.md | N/A |
