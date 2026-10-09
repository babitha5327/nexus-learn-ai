# NEXUS LEARN AI

> An AI tutor that knows your course AND knows you.

Multimodal AI Hackathon 2026 · Track D: Personalized Tutoring & Adaptive Learning

- **Live demo (website prototype):** [https://github.com/babitha5327/nexus-learn-ai/](https://babitha5327.github.io/nexus-learn-ai/)
- **Demo video:** _add YouTube link_
- **Devpost:** _add link_

## Problem
Students study from videos, textbooks and slides in different places. General chatbots give answers that are not tied to the course or to what the student already understands.

## Solution
NEXUS turns course material into a source-linked **Course Universe** and tracks the student in a **Learning Twin**. Answers are cited, unsupported questions are refused, and quizzes adapt to a transparent mastery model.

Loop: understand → teach → assess → diagnose → adapt → reteach → reassess

## What is in this repo

| Folder | What it is |
|---|---|
| `docs/index.html` | **Working website prototype.** Single file, no API keys, runs in the browser (hosted via GitHub Pages). |
| `backend/` | FastAPI backend: ingestion, RAG, grounding, learner model, API. |
| `frontend/` | React + Vite + Tailwind app. |
| `tests/` | Unit tests for mastery, recommender, chunker, citations, verification. |
| `data/` | Demo and evaluation data folders. |

## Honest status

| Feature | Status |
|---|---|
| Source-linked demo course, citations that open the source unit | Implemented (website, text input) |
| Grounding Shield: grounded / partial / not covered, refusal | Implemented (retrieval-coverage based) |
| Extractive tutor personalised by mastery, prerequisites, misconceptions | Implemented (no generative LLM) |
| Verified, non-repeating adaptive MCQs | Implemented (rule-based checks) |
| Diagnostic, adaptive quiz, Mastery Battle with measured before/after | Implemented |
| Learner model `m' = (1-α)·m + α·e` (α configurable) | Implemented |
| Misconception tracking, Next Best Action, Learning Twin, Course Universe | Implemented (heuristic) |
| Evaluation: hit@k, refusal accuracy; student simulation | Implemented (14-question set; simulation validates the mechanism, not real learning gains) |
| Teach-It-Back, study planner | Prototype |
| Voice input | Experimental |
| PDF / PPTX / video parsers, upload API, DB schema, tests | Backend written; **embedding/indexing step not wired yet** |
| Image/diagram understanding, RAGAS, short-answer/numeric questions, Hindi/audio | **Future Enhancement** |

Evaluation numbers are computed live by the code; none are hard-coded.

## Run the website
Open `docs/index.html` in a browser (or VS Code Live Server).

## Run the full-stack app
```bash
cp .env.example .env
# Terminal 1
cd backend && python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000
# Terminal 2
cd frontend && npm install && npm run dev
```
API docs: http://localhost:8000/docs · App: http://localhost:5173

Optional heavy dependencies: `pip install chromadb sentence-transformers faster-whisper`.

## Learner model
Mastery starts at 0.5. After each answer: `m' = (1-α)·m + α·e`, default α = 0.3. Evidence `e` depends on difficulty (correct: 0.7+0.1·d; wrong: 0.1·(d−1)). Every change is logged.

## Grounding method
Query terms are matched with IDF weighting. Coverage ≥ 75% = grounded, ≥ 40% = partial, otherwise not covered. Citations are validated against retrieved units, so fake citations cannot reach the UI.

## Roadmap
1. Index chunks on ingest so real uploads get cited answers · 2. RAGAS evaluation · 3. Vision for diagrams · 4. More question types · 5. Flashcards, forgetting curve, Hindi/audio



## Credits
Built with Python, FastAPI, SQLAlchemy, React, Vite, Tailwind CSS. Developed with AI-assisted coding (Claude).
