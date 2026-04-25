# Connect: 2025-10-01 - 2026-03-31

## Reflect on the past

### What results did you deliver, and how did you do it?

#### Deliver secure, high-quality content for customers

I closed 109 work items over six months while keeping our Azure Networking docs accurate and useful for customers. The focus was on fixing real customer problems and plugging documentation gaps that were causing support load.

Fixed high-impact customer issues: Closed 37 UUF items (customer feedback items) within 30 days of triage. I prioritized the ones hitting high-traffic articles across Application Gateway, Load Balancer, and Virtual Network. This directly cuts down escalations and helps customers get things done faster.

Made troubleshooting simpler: Updated docs to handle the top 5 problem patterns we see in Application Gateway support tickets. This coincided with the migration of troubleshooting docs to the Supportability repo. Customers can now work through these issues on their own instead of opening tickets through a centralized and focused troubleshooting experience.

Published end-to-end guidance: Develepoed and helped published content showing how to design secure cross-service networks, and Zero Trust asssement patterns. This helps customers understand how services connect together instead of viewing them in isolation.

Kept the pace steady: Handled 109 items across six months (30, 6, 14, 15, 8, 36 by month), which meant sustaining good content quality even when other priorities were pulling in different directions.

Built for reuse: Set up modular content patterns (reusable blocks, standard templates) for Virtual Network Manager and Virtual Network. This cuts down rework and makes updates faster for the team going forward. For customers, it means more consistentency across related articles and easier navigation. Because these patterns were built on best practices and designed for reuse, they'll help us as AI becomes a bigger consumer of our content for our customers. Structured content is easier for AI to understand and use effectively, which means we can get more value out of our docs as AI tools become more prevalent.

#### Continuously improve and innovate

I ran some experiments and built systems to work more efficiently without sacrificing quality.

Tested AI for content work and led team adoption: Used GitHub Copilot, Content Developer Agent, Documentor, Copilot agents, and custom prompts to speed up draft writing, PR reviews, and fact-checking. Identified two approaches that deliver measurable value without over-dependence on AI. Led AI Brown Bags and knowledge-sharing sessions with writers and partners on when and how to use these tools effectively. (Impact: Freed editorial capacity for higher-value work; built team confidence in AI tooling; established practical guidance for responsible AI use in content work.)

Built a fact-checking tool: Made a custom Copilot agent that checks our docs against public Microsoft sources. As AI without proper guardrails can create poor results, I grounded this tool in only our documentation, created a tiered structure within the tool for grading, and ensured all fact-check claims were doubles sourced. In initial tests, I found 4 articles with outdated info before they went live, which matters for security content especially. As it's a part of my general workflow toolset, it continues to help me catch issues and keep our content accurate though I may not be able to attribute specific saves to it.

Made work repeatable: Built patterns for reviews, grouped similar work together, and created standard workflows for common updates. This means less context-switching and more predictable delivery. 

Started Zero Trust groundwork: Working with John Flores from Security Docs team and Allen Sudbring, integrated Zero Trust assessments for Azure Networking into our doc set. With these assessments, we have a central source of security best practices we can use for baselining our content sets. Gives us a head start on future security scenario work and helps ensure our content is aligned with current security thinking.

Adopted a builders mindset around continuous improvement and innovation: I'm always looking for ways to work smarter, not harder. This mindset is crucial for keeping up with the pace of change in our products and customer needs, and it helps ensure that we're always delivering the best possible content for our customers. I dig deeply into the work to understand where the bottlenecks and pain points are, and then I experiment with different approaches to find what works best for myself, our team, and our customers. This approach has allowed me to make meaningful improvements to my processes and our content, and it's something I plan to continue in the future.

#### Work better together with peers and partners

Shipping quality docs requires talking to people who actually know the products. I worked with PMs and engineers throughout to stay accurate and move fast.

Worked with engineering teams: Looped in PM and engineering folks from Application Gateway, Network Security Perimeter, and Virtual Network Manager teams to validate what we shipped. Caught issues early, built better working relationships, and made sure we stayed in sync with what the product team was doing.

Handled feature launches: Coordinated Network Security Perimeter and Application Gateway docs for product launches at Ignite. Dealt with last-minute changes, kept quality up, and hit the schedule. Shows what's possible when you actually talk to the product team.

Kept the review pipeline moving: Handled ongoing GitHub issue and PR reviews across all our services. Unblocked partners and kept docs moving through the approval process without bottlenecks.

Thought across service boundaries: Took on cross-service scenario work and spotlight content beyond my single-service ownership. Connected services in ways customers actually find useful and got teams thinking about the bigger picture.

### Stretch activities
- [STRETCH] Ran a comparison of AI-assisted PR review approaches (including hands-on testing) and pulled together practical guidance for when and how to use these tools going forward.
- [STRETCH] Stepped up on cross-service content and scenario work beyond typical single-service scope to improve how customers navigate multiple networking services together.
- [STRETCH] Built a prototype for Zero Trust content structure to clear the path for future security work and reduce the friction of getting started.

### Reflect on recent setbacks - what did you learn and how did you grow?

The main challenge was balancing urgent operational work (UUF triage, maintenance) with forward-looking stuff (new scenarios, innovation). First attempt was doing multiple complex things in parallel, which created rework and slipped schedules. Shifted to working through things more serially—batching similar work, reusing templates, setting clear review windows. That fixed the flow. Bigger picture: I learned to move from just reacting to work that comes in to actually designing the system around the work. Asked better planning questions upfront, documented processes so they're repeatable, and got better at realistic estimates based on what we actually have capacity for.

### Summary of security impact

Published Zero Trust networking recommendations in partnership with Microsoft Security Docs team. Developed service-specific recommendation pages for Azure DDoS Protection, Azure Firewall, Application Gateway WAF, and Front Door WAF, with added Zero Trust index card for discoverability. (Impact: Customers implementing Zero Trust architectures have authoritative, step-by-step guidance aligned to Microsoft Zero Trust principles; content established as baseline resource for future security scenario work and helps ensure our content is aligned with current security thinking.)

### Diversity & Inclusion Activities

Mentored next generation in STEM: Mentored 35 students on AI, business development, and leadership through a FIRST Robotics Competition team. (Impact: Helping younger generation develop toward STEM careers; building pipeline of future technologists.)

Co-founded non-profit supporting STEM education: Established a non-profit organization supporting STEM education through Robotics in our community. (Impact: Sustained commitment to expanding access to technology careers.)

Built internal employee community: Co-chaired Madison Microsoft FTE community, organizing 3 local events for employee engagement and volunteerism. (Impact: Strengthened local Microsoft employee community interaction and engagement opportunities.)

Extended AI upskilling to non-profits: Worked with Ronald McDonald House of Madison through Microsoft Give Change Agent program to upskill their staff on AI, helping them advance their mission through technology. (Impact: Demonstrates value of our expertise; builds community trust in Microsoft AI initiatives; supports non-profit sector to achieve their goals.)

Deep learning on Agentic workflows: Invested time building tooling and exploring agentic AI patterns for both professional development and community impact. (Impact: Personal skill advancement in emerging AI paradigm; insights applied to team innovation experiments and Give Change volunteer work.)

## Plan for the future

### What are your goals for the upcoming period?

#### Goal 1: Deliver secure, high-quality content for customers

1. By October 2026, increase content discoverability and retrievability for customers: complete TSG migration for remaining top 12 services and optimize content for copilots via Knowledge service integration. Target measurable increase in page views and retrieval rates for troubleshooting content. Measured by TSG migration completion %, content retrievability metrics, and organic traffic.

2. By June 30, 2026, ship the Azure Networking Plan & Design Guide: all 18 articles (hub + 17 capability modules) live on Learn with PM team sign-off through all five phases. This addresses the critical gap where customers struggle to find scenario-based guidance and rely on service-centric how-tos. Measured by articles published, PM confirmations per phase, positive feedback from architects and network admins.

3. By October 2026, cut customer support demand by tackling quality at scale: reduce UUF backlog by 20%, address top 3 CSS issues for priority services, fact-check high-impact content for consistency and freshness, and remediate duplicate/contradictory content in Virtual Network, VPN Gateway, and Load Balancer. Identify content gaps from Microsoft Q&A and MVP channels and close them. Measured by items closed, CSS resolution rate, defect-free page views, and gap-fix count.

#### Goal 2: Continuously improve and innovate

1. By September 2026, build team AI capacity through structured knowledge-sharing: run three focused sessions on AI-assisted workflows, including copilot tools for retrievability and content quality. Document practical guidance on when and how to use these tools. Measured by session attendance, peer adoption in team PRs, and documented workflows in shared resources.

2. By September 2026, integrate Zero-trust Assessment findings into our docs: ensure customers implementing Zero-trust architectures have authoritative guidance aligned to Microsoft security principles. Establish baseline structure for future security-first scenario work. Measured by zero-trust articles published and security-related organic search rate improvement.

3. By November 2026, ship one repeatable workflow for common maintenance updates that cuts end-to-end cycle time by 15% versus today. Use AI-assisted quality checks on 100% of priority troubleshooting updates to reduce first-pass revisions by 25%. Pilot improvements on 269 high-bounce articles (>20%) across Application Gateway and Load Balancer to reduce bounce rate. Measured by workflow adoption, revision queue depth, and bounce rate reduction.

#### Goal 3: Work better together with peers and partners

1. By June 30, 2026, execute the Azure Networking Scenario Design Guide collaboration: complete all five scheduled phases with PM team (India) reviews and confirmations. Align engineering dependencies and manage cross-team handoffs so nothing blocks publish. Measured by phase completion, PM sign-offs, clear tracking of next steps after each review.

2. By September 2026, clear PR review backlog by 20% and tighten handoffs on urgent work (TSG, CSS, fact-checking). Implement scheduled review windows and clear ownership boundaries so partners know what to expect. Measured by review queue depth and partner satisfaction with handoff clarity.

3. By October 2026, run three cross-service collaboration sessions with PMs, engineers, and writers to align on scenario design priorities, CSS resolution strategy, and quality standards. At least five improvements get implemented based on attendee input. Measured by session attendance, documented decisions, and tracked implementations.
