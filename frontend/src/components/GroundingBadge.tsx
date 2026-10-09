const MAP = {
  grounded: ["bg-emerald-600", "COURSE GROUNDED"],
  partial: ["bg-amber-500", "PARTIALLY SUPPORTED"],
  not_covered: ["bg-rose-600", "NOT COVERED IN COURSE MATERIAL"],
} as const;

export default function GroundingBadge({ status }: { status: keyof typeof MAP }) {
  const [bg, label] = MAP[status];
  return <span className={`${bg} text-white text-xs font-semibold px-2 py-0.5 rounded`}>{label}</span>;
}
