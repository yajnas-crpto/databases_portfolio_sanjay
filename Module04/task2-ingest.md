# Task 2: Idempotent Edge Ingestion with UPSERT

**Terminal Output (Double Run Proof):**
```powershell
PS D:\...\databases_portfolio_sanjay> uv run python Module04/ingest.py
Total readings for sensor 1: 3
PS D:\...\databases_portfolio_sanjay> uv run python Module04/ingest.py
Total readings for sensor 1: 3
