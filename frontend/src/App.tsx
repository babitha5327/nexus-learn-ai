import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Tutor from "./pages/Tutor";
import Upload from "./pages/Upload";
import Placeholder from "./pages/Placeholder";

const NAV = [
  ["/", "Dashboard"], ["/tutor", "Tutor"], ["/quiz", "Quiz"], ["/universe", "Course Universe"],
  ["/upload", "Upload"], ["/eval", "Evaluation"],
] as const;

export default function App() {
  return (
    <div className="flex min-h-screen">
      <aside className="w-56 shrink-0 border-r border-slate-200 dark:border-slate-800 p-4 space-y-1">
        <div className="font-extrabold text-brand mb-4">NEXUS LEARN AI</div>
        {NAV.map(([to, label]) => (
          <NavLink key={to} to={to} end={to === "/"}
            className={({ isActive }) => `block rounded-lg px-3 py-2 text-sm ${isActive ? "bg-brand text-white" : "hover:bg-slate-100 dark:hover:bg-slate-800"}`}>
            {label}
          </NavLink>
        ))}
      </aside>
      <main className="flex-1 p-6 max-w-5xl">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/tutor" element={<Tutor />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/quiz" element={<Placeholder name="Adaptive Quiz" phase="8-9" />} />
          <Route path="/universe" element={<Placeholder name="Course Universe" phase="6" />} />
          <Route path="/eval" element={<Placeholder name="Evaluation Center" phase="15" />} />
        </Routes>
      </main>
    </div>
  );
}
