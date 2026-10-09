export type Citation = { chunk_id: string; locator: string; source_type: string; file_name: string };
export type ChatResponse = { answer: string; grounding: "grounded" | "partial" | "not_covered"; citations: Citation[] };

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const r = await fetch(`/api${path}`, init);
  if (!r.ok) throw new Error((await r.json().catch(() => ({ detail: r.statusText }))).detail ?? r.statusText);
  return r.json();
}

export const api = {
  chat: (question: string) =>
    req<ChatResponse>("/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question }) }),
  upload: (file: File) => { const f = new FormData(); f.append("file", file); return req<{ source_id: number; status: string }>("/sources/upload", { method: "POST", body: f }); },
  status: (id: number) => req<{ status: string; error: string | null }>(`/sources/${id}/status`),
  twin: () => req<{ mastery: { topic_id: number; score: number; n: number; status: string }[] }>("/learner/twin"),
};
