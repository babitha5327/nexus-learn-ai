install:
	cd backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install
api:
	cd backend && . .venv/bin/activate && uvicorn app.main:app --reload --port 8000
web:
	cd frontend && npm run dev
test:
	cd backend && PYTHONPATH=. pytest -q ../tests
