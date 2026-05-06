# Fact-Check Report: Global Load Balancer (cross-region-overview)

**Article:** `articles/load-balancer/cross-region-overview.md`
**Live URL:** https://learn.microsoft.com/azure/load-balancer/cross-region-overview
**Report date:** April 30, 2026
**Reviewer:** GitHub Copilot (microsoft-fact-checker mode)
**Gap analysis source:** azure-load-balancer-gap-analysis-04302026.csv

---

## Summary

Overall accuracy: **Medium** — most content is accurate but the article is missing two documented limitations from the live page and an SLA section. These gaps are actionable.

| Finding | Severity | Type |
|---|---|---|
| Two limitations missing from live page | High | Content gap / outdated |
| Missing Pricing and SLA section | Medium | Content gap |
| Sweden not a participating region (user confusion) | Low | Documentation gap |
| UDP port 3 limitation phrasing may mislead | Low | Clarity issue |
| All other claims (regions, health probe interval, redundancy) | — | Confirmed accurate |

---

## Finding 1: Two limitations missing from the live page

**Severity:** High

### What changed

The official live page at learn.microsoft.com contains **eight** limitations. The local article only lists **six**.

**Missing limitation #7:**
> "When placing the same NIC(s) behind multiple regional load balancers with global load balancer, the load balancing rules on each regional load balancer with the same frontend port must also be configured to the same backend port."

**Missing limitation #8:**
> "ICMP protocol is not supported for global load balancer and ICMP Ping is expected to fail."

### Why this matters

- Limitation #7 is a backend port consistency requirement that can silently break traffic when multiple regional load balancers share the same backend VMs. Missing this causes hard-to-debug configuration errors.
- Limitation #8 directly addresses a gap analysis question: *"Can I ping my load balancer?"* (from FAQs) and explains why ICMP pings fail to the global load balancer endpoint. Several support tickets in the gap analysis relate to connectivity testing and failover validation that rely on ping behavior.

### Evidence

- **Primary source (live page, fetched April 30, 2026):** https://learn.microsoft.com/azure/load-balancer/cross-region-overview
- Live page limitations section excerpt:
  ```
  - When placing the same NIC(s) behind multiple regional load balancers with global load 
    balancer, the load balancing rules on each regional load balancer with the same frontend 
    port must also be configured to the same backend port.
  - ICMP protocol is not supported for global load balancer and ICMP Ping is expected to fail.
  ```

### Proposed fix

In the `## Limitations of global load balancer` section, add after the existing six bullets:

```markdown
- When placing the same NIC(s) behind multiple regional load balancers with global load balancer, the load balancing rules on each regional load balancer with the same frontend port must also be configured to the same backend port.

- ICMP protocol isn't supported for global load balancer. ICMP pings to a global load balancer frontend IP are expected to fail.
```

---

## Finding 2: Missing Pricing and SLA section

**Severity:** Medium

### What changed

- **Article:** No pricing or SLA information
- **Live page:** Includes "Pricing and SLA" section: *"Global load balancer shares the [SLA](https://azure.microsoft.com/support/legal/sla/load-balancer/v1_0/) of standard load balancer."*

### Why this matters

Users evaluating global load balancer need to know the SLA commitment. The Standard Load Balancer SLA is 99.99%, which applies to the global tier as well.

### Evidence

- **Primary source:** https://learn.microsoft.com/azure/load-balancer/cross-region-overview
- Live page excerpt: "Global load balancer shares the SLA of standard load balancer."
- **SLA URL:** https://azure.microsoft.com/support/legal/sla/load-balancer/v1_0/

### Proposed fix

Add before `## Next steps` (or at end of article):

```markdown
## Pricing and SLA

Global load balancer shares the [SLA](https://azure.microsoft.com/support/legal/sla/load-balancer/v1_0/) of Standard Load Balancer. For pricing information, see [Load Balancer pricing](https://azure.microsoft.com/pricing/details/load-balancer/).
```

---

## Finding 3: Sweden not listed as participating region

**Severity:** Low — documentation gap creating user confusion, not an error in the article

### Status

The article is **accurate** in not listing Sweden as a participating or home region — Sweden Central and Sweden South are not in the official participating regions list. However, the gap analysis shows customer questions ("What is Cross-region loadbalancer in Sweden?") indicate confusion about whether the service is available for Swedish workloads.

### Clarification

Backend regional load balancers can be deployed **in any publicly available Azure region**, including Sweden Central and Sweden South. The article already includes the NOTE: *"The backend regional load balancers can be deployed in any publicly available Azure Region and isn't limited to just participating regions."*

The regional LB in Sweden can be added to a global load balancer; traffic from Swedish users would be routed to the closest **participating region** (likely UK South or North Europe), then to Sweden via the Microsoft backbone.

### Evidence

- **Primary source:** https://learn.microsoft.com/azure/load-balancer/cross-region-overview
- Participating regions list confirmed: does not include Sweden Central or Sweden South as of April 30, 2026.

### Proposed fix

Strengthen the existing NOTE to clarify Sweden specifically:

```markdown
> [!NOTE]
> The backend regional load balancers can be deployed in any publicly available Azure region, including regions not in the participating regions list (such as Sweden Central). Traffic from users near those regions is routed through the closest participating region and then forwarded to the backend via the Microsoft global network backbone.
```

---

## Finding 4: UDP port 3 limitation phrasing may mislead

**Severity:** Low

### What changed

- **Article:** "UDP traffic on port 3 isn't supported on global load balancer"
- **Live page:** Identical wording
- **Status:** Accurate, but potentially confusing — users may read this as "all other UDP ports work fine"

### Why this matters

The gap analysis contains: *"Cross-region Load Balancer appears to drop UDP traffic?"* The limitation wording implies only port 3 is restricted. In practice, UDP health probing has additional constraints and UDP traffic behavior should be verified carefully. The article doesn't explain *why* port 3 is restricted or whether UDP generally works as expected.

### Evidence

- **Primary source:** https://learn.microsoft.com/azure/load-balancer/cross-region-overview
- **TCP/UDP support:** https://learn.microsoft.com/azure/load-balancer/load-balancer-overview

### Proposed fix

Optionally expand the limitation with a brief note:

```markdown
- UDP traffic on port 3 isn't supported on global load balancer. For other UDP ports, behavior depends on the backend regional load balancer configuration and health probe setup.
```

---

## Findings 5–9: Confirmed accurate

The following claims were verified against the live page (April 30, 2026):

| Claim | Status | Source |
|---|---|---|
| Health probe checks every 5 seconds | Accurate | https://learn.microsoft.com/azure/load-balancer/cross-region-overview |
| Home regions list (10 regions including China North 2) | Accurate | Same |
| Participating regions list (22 regions) | Accurate | Same |
| Regional redundancy via geo-proximity algorithm | Accurate | Same |
| Static anycast global IP (IPv4 and IPv6) | Accurate | Same |
| Client IP preservation (Layer-4 pass-through) | Accurate | Same |
| Floating IP operates independently at global vs regional | Accurate | Same |
| Global LB doesn't work with Gateway Load Balancer tier | Accurate | Same |
| Cross-tenant chaining not supported via portal | Accurate | Same |
| Frontend port must match regional LB frontend port (NOTE) | Accurate | Same |

---

## Gap analysis opportunities for this article

From the Q&A gap analysis, the following questions map to this article with specific recommendations:

| Q&A Question | Gap type | Recommendation |
|---|---|---|
| Recommended load balancing strategy for Container Apps with regional failover | update-article | Add note that Container Apps uses its own internal LB; global LB targets regional Standard LB backends, not Container Apps directly |
| Failover of VPN gateway to next region using Traffic Manager/Global Load Balancer | update-article | Add link to Traffic Manager integration guidance; clarify Global LB operates at Layer 4 only |
| Cross-region Load Balancer appears to drop UDP traffic | update-article | Expand Finding 4 above |
| Load balancing internal traffic cross region | add-section | Add explicit statement that internal (private) frontends are not supported (already in limitations, but could be more prominent) |
| Cross-region Load Balancer in Sweden | add-section | Expand NOTE per Finding 3 |

---

## References

| Source | URL | Verified |
|---|---|---|
| Global Load Balancer (live page) | https://learn.microsoft.com/azure/load-balancer/cross-region-overview | April 30, 2026 |
| Standard Load Balancer SLA | https://azure.microsoft.com/support/legal/sla/load-balancer/v1_0/ | April 30, 2026 |
| Load Balancer pricing | https://azure.microsoft.com/pricing/details/load-balancer/ | April 30, 2026 |
| Reliability in Azure Load Balancer | https://learn.microsoft.com/azure/reliability/reliability-load-balancer | April 30, 2026 |
