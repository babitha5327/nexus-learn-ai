import { useState } from "react";
import CitationChip from "../components/CitationChip";
import GroundingBadge from "../components/GroundingBadge";
import { api, type ChatResponse } from "../services/api";

export default function Tutor() {
  const [q, setQ] = useState("");
  const [res, setRes] = useState<ChatResponse | null>(null);
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const ask = async () => {
    setBusy(true); setErr("");
    try { setRes(await api.chat(q)); } catch (e) { setErr((e as Error).message); } finally { setBusy(false); }
  };
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-extrabold">Source-grounded tutor</h1>
      <div className="flex gap-2">
        <input value={q} onChange={(e) => setQ(e.target.value)} onKeyDown={(e) => e.key === "Enter" && ask()} aria-label="Question"
          className="flex-1 rounded-lg border border-slate-300 dark:border-slate-700 bg-transparent px-3 py-2" placeholder="Ask about your course…" />
        <button onClick={ask} disabled={busy || !q} className="rounded-lg bg-brand text-white px-4 disabled:opacity-50">Ask</button>
      </div>
      {err && <p className="text-rose-600 text-sm">{err}</p>}
      {res && (
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 p-4 space-y-2">
          <GroundingBadge status={res.grounding} />
          <p>{res.answer}</p>
          <div>{res.citations.map((c) => <CitationChip key={c.chunk_id} c={c} />)}</div>
        </div>
      )}
    </div>
  );
}
