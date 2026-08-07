import { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = "http://127.0.0.1:8001/api";
const today = () => new Date().toISOString().slice(0, 10);

async function request(path, options = {}) {
  const response = await fetch(`${API}${path}`, options);
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail || "The agent could not complete that step.");
  return payload;
}

function App() {
  const [transcript, setTranscript] = useState("");
  const [transactions, setTransactions] = useState([]);
  const [ledger, setLedger] = useState([]);
  const [audit, setAudit] = useState([]);
  const [warnings, setWarnings] = useState([]);
  const [recording, setRecording] = useState(false);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("Ready for a voice note.");
  const recorderRef = useRef(null);
  const chunksRef = useRef([]);

  const loadLedger = async () => {
    const data = await request("/ledger");
    setLedger(data.expenses);
  };
  useEffect(() => { loadLedger().catch(() => setNotice("Ledger is unavailable. Is the API running?")); }, []);

  const createProposal = async (text) => {
    if (!text.trim()) return;
    setBusy(true); setNotice("Agent is extracting and validating your proposal…");
    try {
      const data = await request("/propose", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ transcript: text }) });
      setTranscript(data.transcript); setTransactions(data.transactions); setWarnings(data.warnings || []); setAudit(data.audit || []);
      setNotice(data.transactions.length ? "Proposal ready — review before saving." : "I need a clearer amount or expense description.");
    } catch (error) { setNotice(error.message); }
    finally { setBusy(false); }
  };

  const toggleRecording = async () => {
    if (recording) { recorderRef.current.stop(); return; }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];
      recorder.ondataavailable = (event) => chunksRef.current.push(event.data);
      recorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        setRecording(false); setBusy(true); setNotice("Sarvam is translating your voice note to English…");
        try {
          const blob = new Blob(chunksRef.current, { type: recorder.mimeType || "audio/webm" });
          const form = new FormData(); form.append("audio", blob, "expense-note.webm");
          const result = await request("/transcribe", { method: "POST", body: form });
          setTranscript(result.transcript); await createProposal(result.transcript);
        } catch (error) { setNotice(error.message); }
        finally { setBusy(false); }
      };
      recorder.start(); recorderRef.current = recorder; setRecording(true); setNotice("Listening… say an amount and what it was for.");
    } catch { setNotice("Microphone access was not granted."); }
  };

  const updateTransaction = (index, field, value) => setTransactions((current) => current.map((item, itemIndex) => itemIndex === index ? { ...item, [field]: field === "amount" ? Number(value) : value } : item));
  const removeTransaction = (index) => setTransactions((current) => current.filter((_, itemIndex) => itemIndex !== index));
  const addTransaction = () => setTransactions((current) => [...current, { id: Date.now(), amount: 0, description: "", category: "uncategorized", spent_on: today() }]);

  const approve = async () => {
    if (!transactions.length || transactions.some((item) => !item.amount || !item.description)) { setNotice("Each entry needs an amount and description before approval."); return; }
    setBusy(true);
    try {
      const result = await request("/approve", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ transactions }) });
      setTransactions([]); setWarnings([]); setNotice(`${result.saved} approved entr${result.saved === 1 ? "y" : "ies"} saved to your ledger.`); await loadLedger();
    } catch (error) { setNotice(error.message); }
    finally { setBusy(false); }
  };

  return <main>
    <header className="topbar"><div className="brand"><span className="mark">◉</span><span>VOICE LEDGER</span></div></header>
    <section className="hero"><p className="eyebrow">A controlled voice workflow</p><h1>Speak it. <em>Review it.</em> Save it.</h1><p>Voice becomes a structured, traceable ledger proposal—not an automatic write.</p></section>
    <section className="workspace">
      <article className="card capture"><div className="card-label">01 / CAPTURE</div><h2>What did you spend?</h2><p className="muted">Speak naturally in English, Hindi, Tamil, or a mix. Sarvam translates it before extraction.</p><button className={`record ${recording ? "is-recording" : ""}`} onClick={toggleRecording} disabled={busy}><span>{recording ? "■" : "●"}</span>{recording ? "Stop recording" : "Record voice note"}</button><div className="or">or paste a transcript</div><textarea value={transcript} onChange={(event) => setTranscript(event.target.value)} placeholder="I paid 450 for lunch and 120 for auto yesterday." /><button className="text-button" disabled={busy || !transcript.trim()} onClick={() => createProposal(transcript)}>Extract proposal <span>→</span></button><p className="notice">{busy ? "Working…" : notice}</p></article>
      <article className="card review"><div className="card-label">02 / HUMAN APPROVAL</div><div className="review-head"><div><h2>Proposed entries</h2><p className="muted">Edit anything. Nothing reaches the ledger until you approve.</p></div><button className="add" onClick={addTransaction}>+ Add</button></div>
        {warnings.map((warning) => <p className="warning" key={warning}>! {warning}</p>)}
        <div className="entries">{transactions.length ? transactions.map((item, index) => <div className="entry" key={item.id || index}><input className="amount" type="number" min="0" value={item.amount} onChange={(e) => updateTransaction(index, "amount", e.target.value)} /><input value={item.description} onChange={(e) => updateTransaction(index, "description", e.target.value)} placeholder="What was it for?" /><select value={item.category} onChange={(e) => updateTransaction(index, "category", e.target.value)}><option>food</option><option>transport</option><option>subscriptions</option><option>shopping</option><option>utilities</option><option>health</option><option>entertainment</option><option>work</option><option>uncategorized</option></select><input type="date" value={item.spent_on} onChange={(e) => updateTransaction(index, "spent_on", e.target.value)} /><button className="remove" onClick={() => removeTransaction(index)} aria-label="Remove entry">×</button></div>) : <div className="empty">Your reviewed proposal will appear here.</div>}</div>
        <button className="approve" disabled={busy || !transactions.length} onClick={approve}>Approve & save <span>→</span></button>
        {audit.length > 0 && <details><summary>Run inspector</summary><div className="audit">{audit.map((step) => <span key={step}>{step}</span>)}</div></details>}
      </article>
      <aside className="side"><article className="card ledger"><div className="card-label">03 / APPROVED LEDGER</div><h2>Recent activity</h2>{ledger.length ? <>{ledger.map((item) => <div className="ledger-row" key={item.id}><div><b>{item.description}</b><small>{item.category} · {item.spent_on}</small></div><strong>₹{Number(item.amount).toLocaleString("en-IN")}</strong></div>)}<div className="total"><span>Total shown</span><b>₹{ledger.reduce((sum, item) => sum + Number(item.amount), 0).toLocaleString("en-IN")}</b></div></> : <div className="empty">Approved entries will live here.</div>}</article>
      <article className="trace"><span className="pulse" /> <div><b>Trace-ready</b><p>Each LLM extraction is sent to Langfuse when its keys are configured.</p></div></article></aside>
    </section>
  </main>;
}

createRoot(document.getElementById("root")).render(<App />);
