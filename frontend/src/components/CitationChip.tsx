import type { Citation } from "../services/api";

// TODO: onClick should open the Source Viewer (PDF page / slide / video at timestamp).
export default function CitationChip({ c, onOpen }: { c: Citation; onOpen?: (c: Citation) => void }) {
  return (
    <button onClick={() => onOpen?.(c)} className="border border-brand text-brand rounded-full px-3 py-0.5 text-xs font-semibold mr-2">
      {c.source_type} · {c.locator}
    </button>
  );
}
