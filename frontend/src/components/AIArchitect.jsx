import { useEffect, useMemo, useState } from "react";
import { askAIArchitect } from "../services/aiArchitect";
import "./AIArchitect.css";

const SUGGESTED_QUESTIONS = [
  "What should I refactor first?",
  "Why is the highest-impact module risky?",
  "Which modules have the highest blast radius?",
  "How can I reduce coupling?",
];

function cleanText(value) {
  return String(value ?? "")
    .replace(/<br\s*\/?\s*>/gi, " ")
    .replace(/\*\*/g, "")
    .replace(/\s{2,}/g, " ")
    .trim();
}

function severityClass(severity) {
  const value = String(severity || "medium").toLowerCase();
  if (value.includes("critical")) return "critical";
  if (value.includes("high")) return "high";
  return "medium";
}

function RiskCard({ risk, index }) {
  const severity = severityClass(risk.severity);
  return (
    <article className={`ai-risk-card ${severity}`}>
      <div className="ai-risk-top">
        <span className="ai-risk-number">{String(index + 1).padStart(2, "0")}</span>
        <span className={`ai-severity ${severity}`}>{risk.severity || "Medium"}</span>
      </div>
      <h4>{cleanText(risk.title) || "Architectural risk"}</h4>
      {risk.evidence && <p><strong>Evidence</strong>{cleanText(risk.evidence)}</p>}
      {risk.why_it_matters && <p><strong>Why it matters</strong>{cleanText(risk.why_it_matters)}</p>}
      {risk.recommended_action && <div className="ai-action"><span>→</span>{cleanText(risk.recommended_action)}</div>}
    </article>
  );
}

function ListPanel({ icon, title, items = [], wide = false }) {
  return (
    <article className={`ai-panel ai-list-panel ${wide ? "wide" : ""}`}>
      <div className="ai-section-title"><span>{icon}</span><h3>{title}</h3></div>
      {items.length ? <ul>{items.map((item, index) => <li key={`${item}-${index}`}>{cleanText(item)}</li>)}</ul> : <div className="ai-empty-copy">No items were identified for this section.</div>}
    </article>
  );
}

function AssessmentView({ assessment }) {
  return (
    <div className="ai-assessment-grid">
      <article className="ai-executive-card">
        <div className="ai-section-title"><span>◈</span><h3>Executive Assessment</h3></div>
        <p>{cleanText(assessment.executive_assessment)}</p>
      </article>

      <div className="ai-two-column">
        <article className="ai-panel ai-risks-panel">
          <div className="ai-section-title"><span>⚠</span><h3>Top Architectural Risks</h3><em>{assessment.top_risks?.length || 0}</em></div>
          <div className="ai-risk-list">
            {(assessment.top_risks || []).map((risk, index) => <RiskCard key={`${risk.title}-${index}`} risk={risk} index={index} />)}
            {!assessment.top_risks?.length && <div className="ai-empty-copy">No high-confidence architectural risks were returned from the available evidence.</div>}
          </div>
        </article>

        <article className="ai-panel">
          <div className="ai-section-title"><span>↗</span><h3>Recommended Refactoring Order</h3></div>
          <div className="ai-phase-list">
            {(assessment.refactoring_order || []).map((phase, index) => (
              <div className="ai-phase" key={`${phase.title}-${index}`}>
                <span className="ai-phase-number">{index + 1}</span>
                <div><small>{cleanText(phase.phase) || `Phase ${index + 1}`}</small><h4>{cleanText(phase.title)}</h4><p>{cleanText(phase.action)}</p></div>
              </div>
            ))}
          </div>
        </article>
      </div>

      <div className="ai-two-column">
        <ListPanel icon="⚡" title="Quick Wins" items={assessment.quick_wins} />
        <ListPanel icon="◇" title="Structural Changes" items={assessment.structural_changes} />
      </div>
      <ListPanel icon="⌕" title="What Should Be Investigated Manually Before a Risky Refactor" items={assessment.manual_investigation} wide />
    </div>
  );
}

export default function AIArchitect({ projectId, projectName }) {
  const storageKey = useMemo(() => `forgeiq:ai-conversation:${projectId}`, [projectId]);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [assessment, setAssessment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [collapsed, setCollapsed] = useState(false);
  const [error, setError] = useState("");
  const [focus, setFocus] = useState(null);

  useEffect(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || "[]");
      if (Array.isArray(saved)) setMessages(saved.slice(-8));
    } catch { setMessages([]); }
    setAssessment(null);
    setQuestion("");
    setError("");
    setCollapsed(false);
  }, [storageKey]);

  useEffect(() => {
    if (messages.length) localStorage.setItem(storageKey, JSON.stringify(messages.slice(-8)));
    else localStorage.removeItem(storageKey);
  }, [messages, storageKey]);

  useEffect(() => {
    const handleFocus = (event) => {
      const detail = event.detail || {};
      if (!detail.target) return;
      setFocus(detail);
      setQuestion(detail.question || "Explain this ForgeIQ finding and tell me how to address it safely.");
      setError("");
      setCollapsed(false);
      window.setTimeout(() => document.querySelector(".ai-architect-shell")?.scrollIntoView({ behavior: "smooth", block: "start" }), 0);
    };
    window.addEventListener("forgeiq:ai-focus", handleFocus);
    return () => window.removeEventListener("forgeiq:ai-focus", handleFocus);
  }, []);

  const ask = async (value = question) => {
    const prompt = value.trim();
    if (!prompt || !projectId || loading) return;
    const priorHistory = messages.slice(-8);
    try {
      setLoading(true);
      setError("");
      const data = await askAIArchitect(projectId, prompt, priorHistory, focus);
      setAssessment(data.assessment || null);
      setMessages((prev) => [
        ...prev,
        { role: "user", content: prompt },
        { role: "assistant", content: data.assessment?.executive_assessment || "ForgeIQ returned an assessment." },
      ].slice(-8));
      setQuestion("");
    } catch (err) {
      setError(err.message || "AI Architect request failed.");
    } finally {
      setLoading(false);
    }
  };

  const submit = (event) => { event.preventDefault(); ask(); };
  const clearConversation = () => {
    setMessages([]);
    setAssessment(null);
    setQuestion("");
    setError("");
    setFocus(null);
  };

  return (
    <section className={`ai-architect-shell ${collapsed ? "is-collapsed" : ""}`}>
      <div className="ai-architect-header">
        <div>
          <div className="ai-eyebrow"><span className="ai-pulse" /> AI ARCHITECT</div>
          <h2>Talk to your codebase.</h2>
          <p>Ask ForgeIQ about <strong>{projectName || "this project"}</strong>'s architecture, risks, dependencies, and refactoring strategy.</p>
        </div>
        <div className="ai-header-actions">
          <div className="ai-model-badge"><span /> GEMINI POWERED</div>
          <button className="ai-collapse-btn" type="button" onClick={() => setCollapsed((v) => !v)}>
            {collapsed ? "Expand" : "Collapse"} <span>{collapsed ? "↗" : "−"}</span>
          </button>
        </div>
      </div>

      {collapsed ? (
        <div className="ai-collapsed-bar">
          <div><span className="ai-answer-dot" /> {messages.length ? `${Math.ceil(messages.length / 2)} conversation turn(s)` : "No conversation yet"}</div>
          <button type="button" onClick={() => setCollapsed(false)}>Open AI Architect <span>↗</span></button>
        </div>
      ) : (
        <>
          {messages.length > 0 && (
            <div className="ai-conversation-bar">
              <div><span className="ai-answer-dot" /> CONVERSATION ACTIVE</div>
              <button type="button" onClick={clearConversation}>Clear conversation</button>
            </div>
          )}

          {focus && (
            <div className="ai-focus-context">
              <span>✦</span> Focused on <strong>{focus.title || focus.target}</strong>
              <span>·</span> {focus.target}
              <button type="button" onClick={() => setFocus(null)}>Clear focus</button>
            </div>
          )}

          <form className="ai-question-form" onSubmit={submit}>
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => { if ((e.metaKey || e.ctrlKey) && e.key === "Enter") submit(e); }}
              placeholder={messages.length ? "Ask a follow-up about the assessment..." : "Ask a question about this project's architecture..."}
              rows={3}
              disabled={loading}
            />
            <div className="ai-form-footer">
              <span>ForgeIQ analysis is the source of truth · ⌘/Ctrl + Enter to ask</span>
              <button type="submit" disabled={!question.trim() || loading}>
                {loading ? <><span className="ai-button-spinner" /> Thinking...</> : <>Ask ForgeIQ <span>→</span></>}
              </button>
            </div>
          </form>

          {!assessment && !loading && !error && (
            <div className="ai-suggestions">
              <span className="ai-suggestions-label">TRY ASKING</span>
              <div className="ai-suggestion-grid">
                {SUGGESTED_QUESTIONS.map((item) => <button key={item} type="button" onClick={() => { setQuestion(item); ask(item); }}>{item}<span>↗</span></button>)}
              </div>
            </div>
          )}

          {loading && <div className="ai-thinking-card"><div className="ai-thinking-orb">✦</div><div><strong>ForgeIQ is reasoning over your architecture...</strong><p>Combining dependency structure, impact analysis, health metrics, and engineering priorities.</p></div></div>}
          {error && !loading && <div className="ai-error"><span>!</span><div><strong>AI Architect couldn't answer</strong><p>{error}</p></div></div>}

          {assessment && !loading && (
            <div className="ai-answer-area">
              <div className="ai-answer-bar"><div><span className="ai-answer-dot" /> ARCHITECT'S ASSESSMENT</div><button type="button" onClick={() => { setAssessment(null); setError(""); }}>New question</button></div>
              <AssessmentView assessment={assessment} />
            </div>
          )}
        </>
      )}
    </section>
  );
}
