# Task 2: Idempotent Edge Ingestion with UPSERT

**Terminal Output (Double Run Proof):**
```powershell
PS D:\...\databases_portfolio_sanjay> uv run python Module04/ingest.py
Total readings for sensor 1: 3
PS D:\...\databases_portfolio_sanjay> uv run python Module04/ingest.py
Total readings for sensor 1: 3
```

Proof: Running the network ingestion script twice did not duplicate the rows. The ON CONFLICT(sensor_id, ts) clause safely caught the collision and idempotently updated the existing records instead of inserting new ones.

