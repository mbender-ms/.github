import { useState } from "react";

const layers = [
  {
    id: 0,
    name: "Prompt Craft",
    subtitle: "The foundation",
    icon: "✍",
    accentHex: "#38BDF8",
    accentBg: "rgba(56,189,248,0.08)",
    accentBorder: "rgba(56,189,248,0.35)",
    what: "The words you write. A clear task description, the expected output format, and basic constraints. This is where most people start — and stop.",
    adds: "Clarity of task and output. The agent knows what to produce and what shape to produce it in.",
    before: {
      label: "Before — Vague request",
      content: `"Can you help me fact-check this article?"`
    },
    after: {
      label: "After — Prompt-crafted",
      content: `"Fact-check this Azure documentation article.\nFor each technical claim, return:\n  • The claim text\n  • Status: accurate / inaccurate / outdated\n  • Recommended fix (if status is not accurate)"`
    }
  },
  {
    id: 1,
    name: "Context Engineering",
    subtitle: "Everything in the window",
    icon: "⚙",
    accentHex: "#A78BFA",
    accentBg: "rgba(167,139,250,0.08)",
    accentBorder: "rgba(167,139,250,0.35)",
    what: "Everything else the agent sees: role definition, tools available, memory, retrieved content, source hierarchy. The full operating environment, not just the instruction.",
    adds: "The agent knows WHO it is, WHAT it can use, and WHAT to prioritize — before it reads a single word of the task.",
    before: {
      label: "Before — No context",
      content: `Agent receives only the user message.\n\nNo role. No tools. No source hierarchy.\nIt has to guess what "authoritative" means\nand improvise when sources conflict.`
    },
    after: {
      label: "After — Context-engineered",
      content: `Role: "You are a technical documentation\n  verifier for Microsoft Azure content."\n\nTools: microsoft_docs_search,\n  microsoft_docs_fetch, grep_search\n\nSource hierarchy:\n  Tier 1: learn.microsoft.com (governs)\n  Tier 2: techcommunity.microsoft.com\n\nInjected: [article content to verify]`
    }
  },
  {
    id: 2,
    name: "Intent Engineering",
    subtitle: "The why behind the what",
    icon: "🎯",
    accentHex: "#FBBF24",
    accentBg: "rgba(251,191,36,0.08)",
    accentBorder: "rgba(251,191,36,0.35)",
    what: "The governing principles that let the agent reason about situations the instructions don't explicitly cover. Intent answers the question: what should this agent optimize for?",
    adds: "The agent can handle edge cases and novel situations by applying the principle — not by improvising.",
    before: {
      label: "Before — Instructions only",
      content: `"Search learn.microsoft.com. If the claim\nmatches, mark ✅. If it contradicts, mark ❌."\n\n→ What if Tier 2 contradicts Tier 1?\n→ What if no source is found?\n→ Should it delete unverifiable claims?\n\nNo principle to apply. Agent improvises.`
    },
    after: {
      label: "After — Intent-engineered",
      content: `"The goal is to protect documentation\naccuracy. Flag rather than remove —\na flagged claim can be resolved by a\nhuman author; a silently deleted claim\ncannot.\n\nWhen sources conflict, Tier 1 governs.\nWhen no source is found, mark\nUnverifiable — do not correct, do not\ndelete."`
    }
  },
  {
    id: 3,
    name: "Specificity Engineering",
    subtitle: "The complete spec",
    icon: "⬡",
    accentHex: "#34D399",
    accentBg: "rgba(52,211,153,0.08)",
    accentBorder: "rgba(52,211,153,0.35)",
    what: "The full specification: definition of done, decision boundaries, negative examples, tool failure handling, and evaluation criteria. This is the gap between 'it sometimes works' and 'it reliably works.'",
    adds: "Reliability. The agent stops at the right time, fails gracefully, and doesn't improvise in the unspecified space.",
    before: {
      label: "Before — Missing the spec",
      content: `Good prompt + context + intent. But:\n\n✗ When does the agent stop?\n✗ What if microsoft_docs_fetch fails?\n✗ What should it NEVER do, even if\n  it seems reasonable in context?\n✗ How do you score output quality?\n\nThe agent improvises at every edge case.`
    },
    after: {
      label: "After — Fully specified",
      content: `Done when: every claim classified, >20%\nUnverifiable triggers pause + report.\n\nNegative examples:\n  ✗ Never mark Inaccurate from a snippet\n  ✗ Never remove Unverifiable claims\n\nTool failure: fall back to snippets,\n  note reduced confidence in report.\n\nEval: every correction must cite a URL.`
    }
  }
];

const principles = [
  { n: 1, name: "Define outcome + definition of done" },
  { n: 2, name: "Operate at the right altitude" },
  { n: 3, name: "Minimal viable context only" },
  { n: 4, name: "Encode intent, not just instructions" },
  { n: 5, name: "Curate tools aggressively" },
  { n: 6, name: "Negative examples are essential" },
  { n: 7, name: "The human test" },
];

export default function SpecificityDiagram() {
  const [active, setActive] = useState(0);
  const [tab, setTab] = useState("layers");
  const layer = layers[active];

  return (
    <div style={{
      fontFamily: "'IBM Plex Sans', -apple-system, system-ui, sans-serif",
      background: "#0D1117",
      minHeight: "100vh",
      padding: "2rem 1.5rem",
      color: "#E6EDF3"
    }}>
      <div style={{ maxWidth: "1080px", margin: "0 auto" }}>

        {/* Header */}
        <div style={{ marginBottom: "2rem" }}>
          <div style={{ fontSize: "0.7rem", letterSpacing: "0.18em", color: "#7D8590", textTransform: "uppercase", marginBottom: "0.4rem" }}>
            Specificity Engineering Framework
          </div>
          <h1 style={{ fontSize: "1.7rem", fontWeight: "700", color: "#E6EDF3", margin: "0 0 0.4rem" }}>
            From Prompt to Production
          </h1>
          <p style={{ color: "#7D8590", margin: 0, fontSize: "0.9rem" }}>
            Four disciplines that compound. Each layer builds on the last.
          </p>
        </div>

        {/* Tab bar */}
        <div style={{ display: "flex", gap: "0.5rem", marginBottom: "1.75rem" }}>
          {[
            { id: "layers", label: "Architecture + Before/After" },
            { id: "principles", label: "7 Principles" }
          ].map(t => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              style={{
                padding: "0.45rem 1rem",
                borderRadius: "6px",
                border: tab === t.id ? "1px solid #30363D" : "1px solid transparent",
                background: tab === t.id ? "#161B22" : "transparent",
                color: tab === t.id ? "#E6EDF3" : "#7D8590",
                cursor: "pointer",
                fontSize: "0.85rem",
                fontWeight: tab === t.id ? "500" : "400"
              }}
            >
              {t.label}
            </button>
          ))}
        </div>

        {tab === "layers" && (
          <div style={{ display: "grid", gridTemplateColumns: "minmax(240px, 340px) 1fr", gap: "1.5rem", alignItems: "start" }}>

            {/* Left: Architecture Stack */}
            <div>
              <div style={{ fontSize: "0.65rem", letterSpacing: "0.14em", color: "#7D8590", textTransform: "uppercase", marginBottom: "0.75rem" }}>
                Layered Architecture
              </div>

              <div style={{ fontSize: "0.7rem", color: "#7D8590", textAlign: "center", marginBottom: "0.5rem" }}>
                ▲ more powerful
              </div>

              {[...layers].reverse().map((l) => (
                <div key={l.id}>
                  <div
                    onClick={() => setActive(l.id)}
                    style={{
                      cursor: "pointer",
                      padding: "0.9rem 1rem",
                      borderRadius: "8px",
                      border: `1px solid ${active === l.id ? l.accentBorder : "#21262D"}`,
                      background: active === l.id ? l.accentBg : "#161B22",
                      transition: "all 0.15s",
                      display: "flex",
                      alignItems: "center",
                      gap: "0.75rem",
                      borderLeft: `${active === l.id ? "3px" : "1px"} solid ${active === l.id ? l.accentHex : "#21262D"}`,
                    }}
                  >
                    <div style={{
                      width: "32px",
                      height: "32px",
                      borderRadius: "8px",
                      background: active === l.id ? l.accentHex : "#21262D",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: "1rem",
                      flexShrink: 0
                    }}>
                      {l.icon}
                    </div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{
                        fontSize: "0.85rem",
                        fontWeight: "600",
                        color: active === l.id ? l.accentHex : "#C9D1D9"
                      }}>
                        {l.id + 1}. {l.name}
                      </div>
                      <div style={{ fontSize: "0.72rem", color: "#7D8590" }}>
                        {l.subtitle}
                      </div>
                    </div>
                  </div>
                  {l.id > 0 && (
                    <div style={{ textAlign: "center", color: "#3D444D", fontSize: "0.8rem", margin: "0.15rem 0" }}>
                      │
                    </div>
                  )}
                </div>
              ))}

              <div style={{ fontSize: "0.7rem", color: "#7D8590", textAlign: "center", marginTop: "0.5rem" }}>
                ▼ start here
              </div>

              {/* Progress */}
              <div style={{ marginTop: "1.25rem", padding: "1rem", background: "#161B22", borderRadius: "8px", border: "1px solid #21262D" }}>
                <div style={{ fontSize: "0.65rem", color: "#7D8590", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "0.6rem" }}>
                  Progress
                </div>
                <div style={{ display: "flex", gap: "0.35rem" }}>
                  {layers.map(l => (
                    <div
                      key={l.id}
                      onClick={() => setActive(l.id)}
                      title={l.name}
                      style={{
                        flex: 1,
                        height: "5px",
                        borderRadius: "3px",
                        background: active >= l.id ? l.accentHex : "#21262D",
                        cursor: "pointer",
                        transition: "background 0.2s"
                      }}
                    />
                  ))}
                </div>
                <div style={{ fontSize: "0.8rem", color: "#E6EDF3", marginTop: "0.65rem", fontWeight: "500" }}>
                  {active === 0 && "Foundation — keep building ↑"}
                  {active === 1 && "Layer 2 of 4 — good start ↑"}
                  {active === 2 && "Layer 3 of 4 — almost there ↑"}
                  {active === 3 && "✓ Full specification achieved"}
                </div>
              </div>
            </div>

            {/* Right: Detail Panel */}
            <div>
              <div style={{ fontSize: "0.65rem", letterSpacing: "0.14em", color: "#7D8590", textTransform: "uppercase", marginBottom: "0.75rem" }}>
                Layer {layer.id + 1} — {layer.name}
              </div>

              {/* What it is */}
              <div style={{
                padding: "1.1rem",
                background: "#161B22",
                borderRadius: "8px",
                border: "1px solid #21262D",
                marginBottom: "0.75rem"
              }}>
                <div style={{ fontSize: "0.65rem", color: "#7D8590", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "0.5rem" }}>
                  What it is
                </div>
                <p style={{ margin: 0, color: "#C9D1D9", fontSize: "0.875rem", lineHeight: "1.65" }}>
                  {layer.what}
                </p>
              </div>

              {/* What it adds */}
              <div style={{
                padding: "1.1rem",
                background: "#161B22",
                borderRadius: "8px",
                border: "1px solid #21262D",
                borderLeft: `3px solid ${layer.accentHex}`,
                marginBottom: "1.1rem"
              }}>
                <div style={{ fontSize: "0.65rem", color: "#7D8590", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "0.5rem" }}>
                  What it adds
                </div>
                <p style={{ margin: 0, color: "#E6EDF3", fontSize: "0.875rem", lineHeight: "1.65", fontWeight: "500" }}>
                  {layer.adds}
                </p>
              </div>

              {/* Before / After */}
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem", marginBottom: "1rem" }}>
                <div style={{
                  padding: "1rem",
                  background: "#161B22",
                  borderRadius: "8px",
                  border: "1px solid rgba(248,81,73,0.3)",
                }}>
                  <div style={{ fontSize: "0.65rem", color: "#F85149", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "0.65rem", display: "flex", alignItems: "center", gap: "0.35rem" }}>
                    <span style={{ fontSize: "0.75rem" }}>✕</span> {layer.before.label}
                  </div>
                  <pre style={{
                    margin: 0,
                    fontSize: "0.74rem",
                    color: "#8B949E",
                    whiteSpace: "pre-wrap",
                    fontFamily: "'IBM Plex Mono', 'Fira Code', monospace",
                    lineHeight: "1.65"
                  }}>
                    {layer.before.content}
                  </pre>
                </div>
                <div style={{
                  padding: "1rem",
                  background: "#161B22",
                  borderRadius: "8px",
                  border: "1px solid rgba(52,211,153,0.25)",
                }}>
                  <div style={{ fontSize: "0.65rem", color: "#3FB950", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "0.65rem", display: "flex", alignItems: "center", gap: "0.35rem" }}>
                    <span style={{ fontSize: "0.75rem" }}>✓</span> {layer.after.label}
                  </div>
                  <pre style={{
                    margin: 0,
                    fontSize: "0.74rem",
                    color: "#C9D1D9",
                    whiteSpace: "pre-wrap",
                    fontFamily: "'IBM Plex Mono', 'Fira Code', monospace",
                    lineHeight: "1.65"
                  }}>
                    {layer.after.content}
                  </pre>
                </div>
              </div>

              {/* Navigation */}
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <button
                  onClick={() => setActive(Math.max(0, active - 1))}
                  disabled={active === 0}
                  style={{
                    padding: "0.5rem 1.1rem",
                    background: "#21262D",
                    color: active === 0 ? "#3D444D" : "#C9D1D9",
                    border: "1px solid #30363D",
                    borderRadius: "6px",
                    cursor: active === 0 ? "default" : "pointer",
                    fontSize: "0.85rem",
                    opacity: active === 0 ? 0.4 : 1
                  }}
                >
                  ← Previous
                </button>
                <button
                  onClick={() => setActive(Math.min(3, active + 1))}
                  disabled={active === 3}
                  style={{
                    padding: "0.5rem 1.1rem",
                    background: active === 3 ? "#21262D" : layer.accentHex,
                    color: active === 3 ? "#3D444D" : "#0D1117",
                    border: "none",
                    borderRadius: "6px",
                    cursor: active === 3 ? "default" : "pointer",
                    fontSize: "0.85rem",
                    fontWeight: "600",
                    opacity: active === 3 ? 0.4 : 1
                  }}
                >
                  {active === 3 ? "Complete ✓" : "Next layer →"}
                </button>
              </div>
            </div>
          </div>
        )}

        {tab === "principles" && (
          <div>
            <div style={{ fontSize: "0.65rem", letterSpacing: "0.14em", color: "#7D8590", textTransform: "uppercase", marginBottom: "1rem" }}>
              The 7 Principles of Specificity Engineering
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "0.75rem" }}>
              {principles.map((p, i) => {
                const accent = ["#38BDF8","#A78BFA","#FBBF24","#34D399","#FB7185","#F97316","#818CF8"][i];
                return (
                  <div key={p.n} style={{
                    padding: "1.1rem",
                    background: "#161B22",
                    borderRadius: "8px",
                    border: "1px solid #21262D",
                    borderLeft: `3px solid ${accent}`,
                    display: "flex",
                    gap: "0.75rem",
                    alignItems: "flex-start"
                  }}>
                    <div style={{
                      width: "26px",
                      height: "26px",
                      borderRadius: "50%",
                      background: accent,
                      color: "#0D1117",
                      fontWeight: "700",
                      fontSize: "0.8rem",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0
                    }}>
                      {p.n}
                    </div>
                    <div style={{ fontSize: "0.875rem", color: "#C9D1D9", lineHeight: "1.5", fontWeight: "500", paddingTop: "0.15rem" }}>
                      {p.name}
                    </div>
                  </div>
                );
              })}
            </div>

            <div style={{ marginTop: "2rem", padding: "1.25rem", background: "#161B22", borderRadius: "8px", border: "1px solid #21262D" }}>
              <div style={{ fontSize: "0.65rem", color: "#7D8590", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: "0.75rem" }}>
                How the layers map to the principles
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "0.75rem" }}>
                {layers.map(l => (
                  <div key={l.id} style={{ textAlign: "center" }}>
                    <div style={{
                      fontSize: "0.75rem",
                      fontWeight: "600",
                      color: l.accentHex,
                      marginBottom: "0.5rem",
                      paddingBottom: "0.5rem",
                      borderBottom: `1px solid ${l.accentBorder}`
                    }}>
                      {l.name}
                    </div>
                    <div style={{ fontSize: "0.72rem", color: "#7D8590", lineHeight: "1.6" }}>
                      {l.id === 0 && "Principles 2, 7"}
                      {l.id === 1 && "Principles 3, 5"}
                      {l.id === 2 && "Principle 4"}
                      {l.id === 3 && "Principles 1, 6, + all refined"}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div style={{ marginTop: "2.5rem", paddingTop: "1.25rem", borderTop: "1px solid #21262D", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ fontSize: "0.75rem", color: "#7D8590" }}>
            Based on Anthropic context engineering + Nate B. Jones intent engineering frameworks
          </div>
          <div style={{ fontSize: "0.75rem", color: "#7D8590" }}>
            specificity-engineer skill · v1.0
          </div>
        </div>

      </div>
    </div>
  );
}
