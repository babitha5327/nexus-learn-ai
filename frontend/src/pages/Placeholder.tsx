export default function Placeholder({ name, phase }: { name: string; phase: string }) {
  return (
    <div className="rounded-xl border border-dashed border-slate-300 dark:border-slate-700 p-8">
      <h1 className="text-xl font-bold">{name}</h1>
      <p className="text-sm text-slate-500 mt-1">Not implemented yet (roadmap phase {phase}).</p>
    </div>
  );
}
