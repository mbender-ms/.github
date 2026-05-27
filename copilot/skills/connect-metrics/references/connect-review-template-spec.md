<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SAMPLE — Connect Review Data</title>
<style>
:root{--primary:#0078d4;--secondary:#106ebe;--accent:#00a2ed;--success:#107c10;--warning:#ffb900;--danger:#d13438;--text:#323130;--light-bg:#f3f2f1;--white:#fff}
*{box-sizing:border-box;margin:0;padding:0}body{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px;font-family:'Segoe UI',sans-serif;color:var(--text)}
.container{max-width:1400px;margin:0 auto;background:var(--white);border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,0.2);overflow:hidden}
header{background:linear-gradient(135deg,var(--primary),var(--secondary));color:white;padding:30px 40px}header h1{font-size:28px;margin-bottom:8px}header .subtitle{opacity:0.9;font-size:16px}header .meta{margin-top:12px;display:flex;gap:20px;flex-wrap:wrap;font-size:14px;opacity:0.85}
.content{padding:30px 40px}h2{color:var(--primary);margin:30px 0 15px;padding-bottom:8px;border-bottom:2px solid var(--light-bg);font-size:22px}h2:first-child{margin-top:0}
table{width:100%;border-collapse:collapse;margin-bottom:20px;font-size:13px}th{background:var(--primary);color:white;padding:10px 12px;text-align:left;font-weight:600}td{padding:8px 12px;border-bottom:1px solid #eee;vertical-align:top}tr:hover{background:#f8f8f8}
.category-header td{background:linear-gradient(90deg,#e8e8e8,#f5f5f5);font-weight:700;font-size:14px;color:var(--secondary);padding:10px 12px}
a{color:var(--primary);text-decoration:none}a:hover{text-decoration:underline}
.state-closed{background:var(--success);color:white;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600}.state-active{background:var(--accent);color:white;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600}
.badge-uuf{background:var(--warning);color:#333;padding:2px 6px;border-radius:4px;font-size:11px;font-weight:600}
.badge-feature{background:#107c10;color:white;padding:2px 6px;border-radius:4px;font-size:10px;font-weight:600;margin-left:4px}.badge-maint{background:#0078d4;color:white;padding:2px 6px;border-radius:4px;font-size:10px;font-weight:600;margin-left:4px}
.table-wrapper{max-height:600px;overflow-y:auto;border:1px solid #ddd;border-radius:8px;margin-bottom:20px}
.copyable{background:#f8f8f8;border:1px solid #ddd;border-radius:8px;padding:20px;font-family:'Segoe UI',sans-serif;font-size:14px;line-height:1.8;margin-bottom:20px;white-space:pre-line}
.metrics-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-bottom:30px}
.metric-card{background:linear-gradient(135deg,var(--light-bg),var(--white));border-left:4px solid var(--primary);padding:16px;border-radius:8px}
.metric-value{font-size:32px;font-weight:700;color:var(--primary)}.metric-label{font-size:13px;color:#666;margin-top:4px}
footer{text-align:center;padding:20px;font-size:12px;color:#999;border-top:1px solid #eee}
</style></head><body>
<div class="container">
<header><h1>SAMPLE — Connect Review Data</h1><div class="subtitle">Alex Chen | Azure Networking Docs | Content Developer</div><div class="meta"><span>Period: 2025-11-11 to 2026-04-17</span><span>Generated: 4/13/2026</span><span style="background:rgba(255,200,0,0.3);padding:2px 8px;border-radius:4px;">⚠️ FICTIONAL DATA — for template reference only</span></div></header>
<div class="content">

<h2>Key Metrics (copy-friendly)</h2>
<div class="copyable">Items closed: 51
User Stories closed: 39
UUF items resolved: 12 (42% backlog reduction: 19→11)
PRs merged: 48
PRs open: 3
New articles: 7
Updated articles: 189
Lines added: 5,300
Lines removed: 2,800
Images manipulated: 54
PR reviews: 14
Conference PRs (Ignite 2025): 6
Conference PRs (Build 2026): 4

Articles owned:
Virtual WAN: 68 articles (ms.service)
ExpressRoute: 93 articles (ms.service)
VPN Gateway: 142 articles (ms.service)
DNS/Firewall: 47 articles (ms.service, co-owned with Jamie Torres)

Avg Monthly Visitors (Nov 2025 - Mar 2026, Power BI):
Virtual WAN: ~14,200 visitors/month (~22,100 page views/month)
ExpressRoute: ~21,800 visitors/month (~35,400 page views/month)
VPN Gateway: ~31,500 visitors/month (~48,900 page views/month)
DNS/Firewall: ~9,600 visitors/month (~14,300 page views/month)
Total across owned areas: ~77,100 visitors/month (~120,700 page views/month)</div>

<h2>Conference Contributions</h2>
<table style="font-size:13px;table-layout:auto;width:auto;">
<thead><tr>
<th style="text-align:left;padding:6px 10px;">Conference</th>
<th style="text-align:center;padding:6px 8px;">PRs</th>
<th style="text-align:center;padding:6px 8px;">New Articles</th>
<th style="text-align:center;padding:6px 8px;">Updated</th>
<th style="text-align:center;padding:6px 8px;">+Lines</th>
<th style="text-align:center;padding:6px 8px;">-Lines</th>
<th style="text-align:center;padding:6px 8px;">Images</th>
</tr></thead>
<tbody>
<tr><td><strong>Ignite 2025</strong></td><td style="text-align:center;">6</td><td style="text-align:center;">4</td><td style="text-align:center;">28</td><td style="text-align:center;">+1,680</td><td style="text-align:center;">-420</td><td style="text-align:center;">22</td></tr>
<tr style="background:#f3f2f1;"><td><strong>Build 2026</strong></td><td style="text-align:center;">4</td><td style="text-align:center;">1</td><td style="text-align:center;">22</td><td style="text-align:center;">+620</td><td style="text-align:center;">-180</td><td style="text-align:center;">14</td></tr>
<tr style="border-top:2px solid #0078d4;font-weight:700;"><td><strong>Total</strong></td><td style="text-align:center;">10</td><td style="text-align:center;">5</td><td style="text-align:center;">50</td><td style="text-align:center;">+2,300</td><td style="text-align:center;">-600</td><td style="text-align:center;">36</td></tr>
</tbody></table>

<h2>All Work Items (63) — showing sample rows per category</h2>
<div class="table-wrapper"><table>
<thead><tr><th>ID</th><th>Type</th><th>Title</th><th>State</th><th>Closed</th><th>SP</th><th>PRs</th></tr></thead>
<tbody>
<tr class="category-header"><td colspan="7">Virtual WAN (18)</td></tr>
<tr><td>#600101</td><td>User Story</td><td>Virtual WAN | Hub routing GA documentation</td><td><span class="state-closed">Closed</span></td><td>2025-11-18</td><td>5</td><td>#35420, #35421</td></tr>
<tr><td>#600102</td><td>User Story</td><td>Virtual WAN | Secured Virtual Hub integration preview</td><td><span class="state-closed">Closed</span></td><td>2025-11-18</td><td>3</td><td>#35422</td></tr>
<tr><td>#600103</td><td>User Story</td><td>Virtual WAN | NVA in hub preview documentation</td><td><span class="state-closed">Closed</span></td><td>2025-12-05</td><td>3</td><td>#35580</td></tr>
<tr><td>#600104</td><td><span class="badge-uuf">UUF</span></td><td>UUF - Classic VPN migration steps unclear</td><td><span class="state-closed">Closed</span></td><td>2026-01-15</td><td>1</td><td>#36200</td></tr>
<tr><td>#600105</td><td>User Story</td><td>Virtual WAN | BGP peering dashboard documentation</td><td><span class="state-active">Active</span></td><td>—</td><td>2</td><td>—</td></tr>

<tr class="category-header"><td colspan="7">ExpressRoute (22)</td></tr>
<tr><td>#600201</td><td>User Story</td><td>ExpressRoute | FastPath 2.0 GA documentation</td><td><span class="state-closed">Closed</span></td><td>2025-11-18</td><td>3</td><td>#35425</td></tr>
<tr><td>#600202</td><td>User Story</td><td>ExpressRoute | Global Reach zone expansion updates</td><td><span class="state-closed">Closed</span></td><td>2026-01-22</td><td>2</td><td>#36150</td></tr>
<tr><td>#600203</td><td><span class="badge-uuf">UUF</span></td><td>UUF - Outdated circuit provisioning screenshots</td><td><span class="state-closed">Closed</span></td><td>2026-02-20</td><td>1</td><td>#36510</td></tr>
<tr><td>#600204</td><td>User Story</td><td>ExpressRoute | Circuit resiliency monitoring preview</td><td><span class="state-closed">Closed</span></td><td>2026-03-15</td><td>3</td><td>#36780</td></tr>
<tr><td>#600205</td><td><span class="badge-uuf">UUF</span></td><td>UUF - Incorrect BGP ASN guidance causing support tickets</td><td><span class="state-closed">Closed</span></td><td>2026-02-20</td><td>2</td><td>#36510</td></tr>

<tr class="category-header"><td colspan="7">VPN Gateway (15)</td></tr>
<tr><td>#600301</td><td>User Story</td><td>VPN Gateway | Point-to-Site IKEv2 cert automation preview</td><td><span class="state-closed">Closed</span></td><td>2026-03-20</td><td>3</td><td>#36850</td></tr>
<tr><td>#600302</td><td>User Story</td><td>VPN Gateway | Troubleshooting article restructure (top 10)</td><td><span class="state-closed">Closed</span></td><td>2026-03-01</td><td>5</td><td>#36620</td></tr>
<tr><td>#600303</td><td><span class="badge-uuf">UUF</span></td><td>UUF - Broken diagnostic deep links in troubleshooting</td><td><span class="state-closed">Closed</span></td><td>2026-02-20</td><td>1</td><td>#36510</td></tr>
<tr><td>#600304</td><td><span class="badge-uuf">UUF</span></td><td>UUF - IPsec policy reference table missing IKEv2 params</td><td><span class="state-closed">Closed</span></td><td>2026-02-20</td><td>1</td><td>#36510</td></tr>
<tr><td>#600305</td><td>User Story</td><td>VPN Gateway | Active-active metrics dashboard</td><td><span class="state-active">Active</span></td><td>—</td><td>2</td><td>—</td></tr>

<tr class="category-header"><td colspan="7">DNS / Firewall (8)</td></tr>
<tr><td>#600401</td><td>User Story</td><td>DNS | Private Resolver conditional forwarding GA</td><td><span class="state-closed">Closed</span></td><td>2026-03-22</td><td>2</td><td>#36860</td></tr>
<tr><td>#600402</td><td>User Story</td><td>Firewall | Policy analytics preview documentation</td><td><span class="state-closed">Closed</span></td><td>2026-03-22</td><td>2</td><td>#36861</td></tr>
</tbody></table></div>

<h2>Grand Total</h2>
<div class="metrics-grid">
<div class="metric-card"><div class="metric-value">7</div><div class="metric-label">New Articles</div></div>
<div class="metric-card"><div class="metric-value">189</div><div class="metric-label">Updated Articles</div></div>
<div class="metric-card"><div class="metric-value">+5,300</div><div class="metric-label">Lines Added</div></div>
<div class="metric-card"><div class="metric-value">-2,800</div><div class="metric-label">Lines Removed</div></div>
<div class="metric-card"><div class="metric-value">54</div><div class="metric-label">Images</div></div>
</div>

<h2>Executive Summaries (Per Product Area)</h2>

<h3 style="color:#0078d4;border-left:4px solid #0078d4;padding-left:10px;margin-bottom:16px;">Combined Metrics Table</h3>
<table style="font-size:13px;table-layout:auto;width:auto;">
<thead><tr>
<th style="text-align:left;padding:6px 10px;">Metric</th>
<th style="text-align:center;padding:6px 8px;">Virtual WAN</th>
<th style="text-align:center;padding:6px 8px;">ExpressRoute</th>
<th style="text-align:center;padding:6px 8px;">VPN Gateway</th>
<th style="text-align:center;padding:6px 8px;">DNS/Firewall</th>
<th style="text-align:center;padding:6px 8px;background:#106ebe;color:white;">TOTAL</th>
</tr></thead>
<tbody>
<tr style="background:#f3f2f1;"><td><strong>Avg monthly visitors</strong></td><td style="text-align:center;">~14,200</td><td style="text-align:center;">~21,800</td><td style="text-align:center;">~31,500</td><td style="text-align:center;">~9,600</td><td style="text-align:center;font-weight:700;">~77,100</td></tr>
<tr><td><strong>Avg monthly page views</strong></td><td style="text-align:center;">~22,100</td><td style="text-align:center;">~35,400</td><td style="text-align:center;">~48,900</td><td style="text-align:center;">~14,300</td><td style="text-align:center;font-weight:700;">~120,700</td></tr>
<tr style="background:#f3f2f1;"><td><strong>Articles owned</strong></td><td style="text-align:center;">68</td><td style="text-align:center;">93</td><td style="text-align:center;">142</td><td style="text-align:center;">47<sup>1</sup></td><td style="text-align:center;font-weight:700;">350<sup>2</sup></td></tr>
<tr><td><strong>ADO items</strong></td><td style="text-align:center;">18</td><td style="text-align:center;">22</td><td style="text-align:center;">15</td><td style="text-align:center;">8</td><td style="text-align:center;font-weight:700;">63</td></tr>
<tr><td>  Items closed</td><td style="text-align:center;">16</td><td style="text-align:center;">18</td><td style="text-align:center;">12</td><td style="text-align:center;">5</td><td style="text-align:center;font-weight:700;">51</td></tr>
<tr><td>  UUF resolved</td><td style="text-align:center;">3</td><td style="text-align:center;">4</td><td style="text-align:center;">5</td><td style="text-align:center;">0</td><td style="text-align:center;font-weight:700;">12</td></tr>
<tr style="background:#f3f2f1;"><td><strong>PRs</strong></td><td style="text-align:center;">15</td><td style="text-align:center;">18</td><td style="text-align:center;">11</td><td style="text-align:center;">4</td><td style="text-align:center;font-weight:700;">48</td></tr>
<tr><td><strong>New articles</strong></td><td style="text-align:center;">4</td><td style="text-align:center;">2</td><td style="text-align:center;">1</td><td style="text-align:center;">0</td><td style="text-align:center;font-weight:700;">7</td></tr>
<tr style="background:#f3f2f1;"><td><strong>Updated articles</strong></td><td style="text-align:center;">52</td><td style="text-align:center;">71</td><td style="text-align:center;">48</td><td style="text-align:center;">18</td><td style="text-align:center;font-weight:700;">189</td></tr>
<tr><td><strong>Lines added</strong></td><td style="text-align:center;">+1,420</td><td style="text-align:center;">+2,310</td><td style="text-align:center;">+1,180</td><td style="text-align:center;">+390</td><td style="text-align:center;font-weight:700;">+5,300</td></tr>
<tr style="background:#f3f2f1;"><td><strong>Lines removed</strong></td><td style="text-align:center;">-580</td><td style="text-align:center;">-890</td><td style="text-align:center;">-1,120</td><td style="text-align:center;">-210</td><td style="text-align:center;font-weight:700;">-2,800</td></tr>
<tr><td><strong>Ignite 2025 PRs</strong></td><td style="text-align:center;">4</td><td style="text-align:center;">2</td><td style="text-align:center;">0</td><td style="text-align:center;">0</td><td style="text-align:center;font-weight:700;">6</td></tr>
<tr style="background:#f3f2f1;"><td><strong>Build 2026 PRs</strong></td><td style="text-align:center;">0</td><td style="text-align:center;">0</td><td style="text-align:center;">3</td><td style="text-align:center;">1</td><td style="text-align:center;font-weight:700;">4</td></tr>
<tr><td><strong>New features</strong></td><td style="text-align:center;">3</td><td style="text-align:center;">2</td><td style="text-align:center;">1</td><td style="text-align:center;">2</td><td style="text-align:center;font-weight:700;">8</td></tr>
<tr style="background:#f3f2f1;"><td><strong>Features going GA</strong></td><td style="text-align:center;">1</td><td style="text-align:center;">1</td><td style="text-align:center;">0</td><td style="text-align:center;">1</td><td style="text-align:center;font-weight:700;">3</td></tr>
<tr><td><strong>Features in preview</strong></td><td style="text-align:center;">2</td><td style="text-align:center;">1</td><td style="text-align:center;">1</td><td style="text-align:center;">1</td><td style="text-align:center;font-weight:700;">5</td></tr>
</tbody></table>
<p style="font-size:12px;color:#605e5c;margin-top:4px;"><sup>1</sup> DNS/Firewall shared articles, co-owned with Jamie Torres.<br><sup>2</sup> Total includes Virtual WAN (68), ExpressRoute (93), VPN Gateway (142), DNS/Firewall (47).</p>

<div style="margin-bottom:24px;">
<h3 style="color:#0078d4;border-left:4px solid #0078d4;padding-left:10px;">Virtual WAN</h3>
<div class="copyable" style="font-size:14px;line-height:1.7;padding:16px 20px;white-space:pre-wrap;">Virtual WAN was my primary focus this connect period with 18 work items and 15 PRs, aligned with PG's investment in next-generation WAN architecture for enterprise customers. I delivered all Ignite 2025 documentation on schedule for the Virtual WAN 3.0 launch and resolved 3 UUF items improving content for ~8,500 combined monthly readers.

Notable features: Virtual WAN 3.0 hub routing (GA), Secured Virtual Hub integration (preview), NVA in hub (preview), BGP peering dashboard
Notable maintenance: Architecture diagrams refresh (12 articles), UUF batch fixes (3 items), Pricing page restructure, Troubleshooting updates</div>
</div>

<div style="margin-bottom:24px;">
<h3 style="color:#0078d4;border-left:4px solid #0078d4;padding-left:10px;">ExpressRoute</h3>
<div class="copyable" style="font-size:14px;line-height:1.7;padding:16px 20px;white-space:pre-wrap;">ExpressRoute work spanned 22 work items and 18 PRs, supporting PG goals around hybrid connectivity reliability and Global Reach expansion. I documented the new FastPath 2.0 performance tier at GA and updated circuit provisioning guides to reflect the portal redesign.

Notable features: FastPath 2.0 (GA), Global Reach zone expansion, Circuit resiliency monitoring (preview), Managed identity for peering
Notable maintenance: Provisioning workflow screenshots (15 articles), Gateway SKU comparison restructure, Customer-reported peering issues (4 UUF)</div>
</div>

<div style="margin-bottom:24px;">
<h3 style="color:#0078d4;border-left:4px solid #0078d4;padding-left:10px;">VPN Gateway</h3>
<div class="copyable" style="font-size:14px;line-height:1.7;padding:16px 20px;white-space:pre-wrap;">VPN Gateway work focused on simplifying customer troubleshooting and reducing support volume, with 15 work items and 11 PRs. I restructured the top 10 most-visited troubleshooting articles based on CSS feedback, contributing to early signs of reduced repeat support tickets.

Notable features: Point-to-Site IKEv2 certificate automation (preview), Active-active gateway metrics dashboard
Notable maintenance: Troubleshooting article restructure (10 articles, scenario-based with decision trees), IPsec policy reference tables, Certificate renewal guide rewrite, UUF fixes (5 items)</div>
</div>

<div style="margin-bottom:24px;">
<h3 style="color:#0078d4;border-left:4px solid #0078d4;padding-left:10px;">DNS / Firewall (Shared)</h3>
<div class="copyable" style="font-size:14px;line-height:1.7;padding:16px 20px;white-space:pre-wrap;">Contributed to DNS and Firewall documentation with 8 work items and 4 PRs, co-owned with Jamie Torres. Focused on Build 2026 feature launches.

Notable features: DNS Private Resolver conditional forwarding (GA), Firewall policy analytics (preview)
Notable maintenance: FQDN filtering best practices, Network rule collection updates</div>
</div>

<div style="margin-bottom:24px;">
<h3 style="color:#888;border-left:4px solid #888;padding-left:10px;">Team / Admin</h3>
<div class="copyable" style="font-size:14px;line-height:1.7;padding:16px 20px;white-space:pre-wrap;">Participated in 2 UATs (Content Retrieval Risk Detection and Learn Authoring Assistant), completed 14 PR reviews including OOF coverage for 2 teammates, and mentored a new hire (Priya Sharma) during her first 3 months. Created and shared an architecture diagram Visio template adopted by 3 writers across 2 teams.</div>
</div>

</div>
<footer>SAMPLE — Connect Review Data | All content is fictional | Generated for template reference only</footer>
</div></body></html>
