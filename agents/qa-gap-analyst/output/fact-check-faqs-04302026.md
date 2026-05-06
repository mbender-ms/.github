# Fact-Check Report: Load Balancer FAQs (load-balancer-faqs.yml)

**Article:** `articles/load-balancer/load-balancer-faqs.yml`
**Live URL:** https://learn.microsoft.com/azure/load-balancer/load-balancer-faqs
**Report date:** April 30, 2026
**Reviewer:** GitHub Copilot (microsoft-fact-checker mode)
**Gap analysis source:** azure-load-balancer-gap-analysis-04302026.csv

---

## Summary

Overall accuracy: **High** for answered questions — confirmed facts are correct. However, multiple questions in the YAML have **empty or truncated answers** in the source file, and the gap analysis reveals several high-traffic Q&A topics not addressed anywhere in the FAQ. The most critical is the UDP idle timeout question, which has a counterintuitive answer many users get wrong.

| Finding | Severity | Type |
|---|---|---|
| UDP idle timeout FAQ — missing or incomplete answer | High | Content gap |
| TLS/SSL termination FAQ — answer truncated in source | High | Incomplete content |
| mTLS FAQ — not present in article | High | Content gap from Q&A |
| Basic LB retirement date (September 30, 2025) | — | Confirmed accurate |
| IP 168.63.129.16 health probe description | — | Confirmed accurate |
| ICMP ping limitation not mentioned | Medium | Content gap |

---

## Finding 1: UDP idle timeout answer missing or incomplete

**Severity:** High — this is one of the most common user questions in the gap analysis: *"How big is Azure Load Balancer UDP idle timeout?"*

### What changed

- **Article:** The question "How big is Azure Load Balancer UDP idle timeout?" does not appear in the FAQ. The idle timeout question shown is mapped to `load-balancer-tcp-idle-timeout`.
- **Official docs:** Explicitly state: **"Idle timeout is not supported for UDP load balancing rules."**
- **Status:** Critical gap — the answer to this question is counterintuitive and widely misunderstood

### Why this matters

Users frequently assume UDP has a configurable idle timeout similar to TCP (4–100 minutes). The official documentation clearly states this is not the case. Without this FAQ entry, users either look for settings that don't exist or incorrectly diagnose UDP connection drops as a timeout issue.

The TCP idle timeout article limitation section states:
> *"Idle timeout is not supported for UDP load balancing rules."*

### Evidence

- **Primary source:** https://learn.microsoft.com/azure/load-balancer/load-balancer-tcp-reset#order-of-precedence
- Limitations excerpt: "Idle timeout is not supported for UDP load balancing rules."
- **TCP idle timeout configurable range:** 4–100 minutes for TCP (Standard); does not apply to UDP
- **Last verified:** April 30, 2026

### Proposed fix

Add a new FAQ question:

```yaml
      - question: |
          What is the idle timeout for UDP load balancing rules?
        answer: |
          Azure Load Balancer doesn't support configurable idle timeout for UDP load balancing rules. 
          The idle timeout setting on load balancing rules applies only to TCP connections. 
          For UDP applications, implement application-level keepalive mechanisms or session management 
          to maintain connections as needed.
          
          For TCP idle timeout configuration, see [Configure TCP reset and idle timeout for Azure Load Balancer](load-balancer-tcp-idle-timeout.md).
```

---

## Finding 2: TLS/SSL termination answer — verify completeness

**Severity:** High — gap analysis shows: *"Having issue with SSL certificate configuration"* and *"mTLS with Azure Load Balancer not working"*

### What changed

- **Article:** The question "Does Azure Load Balancer support TLS/SSL termination?" appears in the YAML source but the answer content was not visible in the attached file (appears truncated)
- **Official docs:** Azure Load Balancer is Layer 4 and does NOT support TLS termination. For TLS offload, use Azure Application Gateway. For TLS passthrough, configure the load balancer TCP listener on port 443 and terminate TLS on backend VMs.
- **Status:** Verify the answer is complete and includes the Application Gateway redirect guidance

### Evidence

- **Primary source:** https://learn.microsoft.com/azure/load-balancer/network-load-balancing-aws-to-azure-how-to
  > *"Azure Load Balancer operates at Layer 4 and does NOT support TLS termination — it only supports TCP, UDP, and TCP_UDP protocols. For TLS termination in Azure, use Azure Application Gateway (Layer 7) which provides SSL/TLS offloading, certificate management, and end-to-end encryption."*
- **Concepts article (concepts.md line 45):** "because the load balancer doesn't interact with the TCP payload nor does it provide TLS offload"
- **Last verified:** April 30, 2026

### Proposed fix (if answer is missing or incomplete)

Ensure the answer reads:

```yaml
      - question: |
          Does Azure Load Balancer support TLS/SSL termination?
        answer: |
          No. Azure Load Balancer is a Layer 4 load balancer and doesn't support TLS/SSL 
          termination or offloading. The load balancer passes TCP traffic transparently 
          to backend virtual machines without inspecting or decrypting the payload.
          
          For TLS termination and SSL offloading, use [Azure Application Gateway](../application-gateway/overview.md), 
          which operates at Layer 7 and provides certificate management and end-to-end encryption options.
          
          For TLS passthrough scenarios (where TLS is terminated on backend VMs), configure 
          a TCP load balancing rule on port 443. The TLS session is established directly 
          between the client and the backend VM, including mutual TLS (mTLS) configurations.
```

---

## Finding 3: mTLS question missing from FAQ

**Severity:** High — top gap analysis question: *"mTLS with Azure Load Balancer not working"*

### What changed

- **Article:** No FAQ entry for mTLS
- **Official docs:** mTLS is not handled by Azure Load Balancer; it must be configured end-to-end between client and backend VM
- **Status:** Content gap — this is a top Q&A question

### Why this matters

mTLS (mutual TLS) requires both client and server to authenticate with certificates. Users incorrectly expect to configure mTLS at the load balancer. Because Azure Load Balancer is Layer 4 and transparent to the TLS payload, mTLS must be configured entirely on the backend VMs. Users find this counterintuitive when comparing to Application Gateway, which does support mTLS.

### Evidence

- **Concepts article:** "Protocol handshakes always occur directly between the client and the backend pool instance"
- **Official overview:** "Because the load balancer doesn't interact with the TCP payload nor does it provide TLS offload"
- **Source:** https://learn.microsoft.com/azure/load-balancer/concepts

### Proposed fix

Add after the TLS/SSL termination question:

```yaml
      - question: |
          Can I configure mutual TLS (mTLS) with Azure Load Balancer?
        answer: |
          Azure Load Balancer doesn't handle TLS, including mutual TLS (mTLS). It operates at 
          Layer 4 and passes TCP traffic transparently without inspecting the payload.
          
          To implement mTLS, configure the client certificate authentication directly on your 
          backend virtual machines. The TLS session, including the mutual authentication 
          handshake, occurs directly between the client and the backend VM.
          
          If you need mTLS termination at the load balancer level, use 
          [Azure Application Gateway](../application-gateway/mutual-authentication-overview.md), 
          which supports mTLS natively.
```

---

## Finding 4: ICMP ping to load balancer not addressed

**Severity:** Medium — gap analysis question: *"Can I ping my load balancer?"* (appears in YAML source, answer may be truncated)

### What changed

- **Article:** Question "Can I ping my load balancer?" appears in YAML source but answer was not visible in the attached content
- **Official docs:** Standard Load Balancer does not respond to ICMP pings. Additionally, Global (cross-region) Load Balancer explicitly states ICMP is not supported.
- **Status:** Verify the answer exists and is complete

### Evidence

- **FAQ verified:** "Can I ping from a backend VM behind a load balancer to a public IP? No, Azure Load Balancer does not support ICMP pings for outbound connectivity."
- **Cross-region limitation (live page):** "ICMP protocol is not supported for global load balancer and ICMP Ping is expected to fail."
- **Source:** https://learn.microsoft.com/azure/load-balancer/cross-region-overview

### Proposed fix (if answer is missing)

```yaml
      - question: |
          Can I ping my load balancer?
        answer: |
          No. Azure Load Balancer doesn't respond to ICMP ping requests. Load Balancer is a 
          Layer 4 service and ICMP is not a supported protocol for testing load balancer 
          frontend connectivity.
          
          To verify load balancer connectivity, use TCP-based tools such as `Test-NetConnection` 
          (PowerShell) or `telnet` to test a port that is configured in a load balancing rule. 
          If you need to verify health probe status, check the 
          [Data path availability metric](load-balancer-standard-diagnostics.md) in Azure Monitor.
          
          If you need to ping from a backend VM to an external IP, associate an 
          Instance-level Public IP to the VM for outbound ICMP.
```

---

## Findings 5–9: Confirmed accurate

The following answered questions were verified:

| FAQ question | Answer status | Source |
|---|---|---|
| What types of Azure Load Balancer exist? | Accurate — describes internal/public LBs | https://learn.microsoft.com/azure/load-balancer/load-balancer-overview |
| Basic LB retirement on September 30, 2025 | Accurate — confirmed retired | https://learn.microsoft.com/azure/load-balancer/skus |
| What is IP 168.63.129.16? | Accurate — Azure infrastructure LB / health probe origin | https://learn.microsoft.com/azure/virtual-network/service-tags-overview |
| Can I use global VNet peering with Basic LB? | Accurate — not supported; Basic LB retired | https://learn.microsoft.com/azure/load-balancer/skus |
| How are inbound NAT rules different from LB rules? | Accurate | https://learn.microsoft.com/azure/load-balancer/components |
| Can I add a VM from the same availability set to different backend pools? | Accurate — NIC-based: no; IP-based: yes | https://learn.microsoft.com/azure/load-balancer/backend-pool-management |
| Can I ping from a backend VM behind a LB to a public IP? | Accurate — No, ICMP not supported; use Instance-level Public IP | https://learn.microsoft.com/azure/load-balancer/load-balancer-faqs |
| What is the maximum data throughput? | Accurate — determined by VM type, not LB | https://learn.microsoft.com/azure/virtual-network/virtual-machine-network-throughput |

---

## Gap analysis opportunities for this article

From the Q&A gap analysis, the following questions should be added as FAQ entries:

| Q&A Question | Priority | Recommended action |
|---|---|---|
| How big is Azure Load Balancer UDP idle timeout? | High | Add FAQ (Finding 1) |
| mTLS with Azure Load Balancer not working | High | Add FAQ (Finding 3) |
| Having issue with SSL certificate configuration | High | Ensure TLS/SSL termination answer is complete (Finding 2) |
| Can I ping my load balancer? | Medium | Ensure answer is complete (Finding 4) |
| Does Azure Load Balancer support TLS/SSL termination? | High | Ensure answer is complete (Finding 2) |
| Can I disable idle timeouts in Azure's iLB? | Medium | Add note: TCP idle timeout minimum is 4 minutes; UDP has no configurable timeout |
| Azure Load Balancer, Time Mismatch issues | Medium | Add note: Load Balancer is stateless at flow level; time mismatch issues relate to VM clock synchronization, not the LB |

---

## References

| Source | URL | Verified |
|---|---|---|
| Azure Load Balancer FAQs (live page) | https://learn.microsoft.com/azure/load-balancer/load-balancer-faqs | April 30, 2026 |
| TCP idle timeout limitations (UDP not supported) | https://learn.microsoft.com/azure/load-balancer/load-balancer-tcp-reset | April 30, 2026 |
| Configure TCP reset and idle timeout | https://learn.microsoft.com/azure/load-balancer/load-balancer-tcp-idle-timeout | April 30, 2026 |
| Azure Load Balancer SKUs (Basic retired) | https://learn.microsoft.com/azure/load-balancer/skus | April 30, 2026 |
| mTLS with Application Gateway | https://learn.microsoft.com/azure/application-gateway/mutual-authentication-overview | April 30, 2026 |
| Global Load Balancer ICMP limitation | https://learn.microsoft.com/azure/load-balancer/cross-region-overview | April 30, 2026 |
| Azure Load Balancer concepts (TLS passthrough) | https://learn.microsoft.com/azure/load-balancer/concepts | April 30, 2026 |
