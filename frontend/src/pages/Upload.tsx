import { useState } from "react";
import { api } from "../services/api";

export default function Upload() {
  const [msg, setMsg] = useState("");
  const onFile = async (f?: File) => {
    if (!f) return;
    try {
      const { source_id } = await api.upload(f);
      setMsg("Processing…");
      const t = setInterval(async () => {
        const s = await api.status(source_id);
        if (s.status === "ready" || s.status === "error") { clearInterval(t); setMsg(s.status === "ready" ? "Ready" : `Error: ${s.error}`); }
      }, 1500);
    } catch (e) { setMsg((e as Error).message); }
  };
  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-extrabold">Upload Center</h1>
      <input type="file" accept=".pdf,.ppt,.pptx,.mp4,.mov,.png,.jpg,.jpeg,.txt" onChange={(e) => onFile(e.target.files?.[0])} aria-label="Upload course material" />
      <p className="text-sm text-slate-500">{msg}</p>
      {/* TODO: staged progress (extract → understand → concepts → source map → graph) via SSE */}
    </div>
  );
}
