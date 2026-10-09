import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Dashboard() {
  const [rows, setRows] = useState<{ topic_id: number; score: number; status: string }[]>([]);
  const [err, setErr] = useState("");
  useEffect(() => { api.twin().then((t) => setRows(t.mastery)).catch((e) => setErr(String(e.message))); }, []);
  const avg = rows.length ? rows.reduce((a, r) => a + r.score, 0) / rows.length : null;
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-extrabold">Hello, Student</h1>
      {err && <p className="text-rose-600 text-sm">Backend unavailable: {err}</p>}
      <div className="rounded-2xl p-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
        <div className="text-sm text-slate-500">Overall mastery</div>
        <div className="text-4xl font-extrabold">{avg === null ? "—" : `${Math.round(avg * 100)}%`}</div>
      </div>
      {/* TODO: next best action, weak concepts, recent progress, quick actions */}
    </div>
  );
}
