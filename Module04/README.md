# Module 4: Data Integrity, Constraints & Edge Triggers

This module covers deploying data integrity directly at the edge, where no server is available to validate incoming IoT telemetry. It focuses on pushing constraints, derived data, and event triggers down into the SQLite engine itself[cite: 4].

## 🎯 Learning Goals

1. Create tables with the full constraint toolkit: `NOT NULL`, `UNIQUE`, `CHECK`, `PRIMARY KEY`, `FOREIGN KEY`, and **[`STRICT` typing](./setup.sql)**[cite: 4].
2. Use **[generated columns](./task1-constraints.md)** to derive values at the engine instead of in application code[cite: 4].
3. Write **[triggers](./task3-triggers.md)** that enforce domain rules and maintain audit/rollup tables automatically[cite: 4].
4. Use **[DML correctly](./task2-ingest.md)** — including `UPSERT` (`ON CONFLICT`) for idempotent edge ingestion[cite: 4].
5. Reason about **[access control (DCL)](./task4-and-5.md)**: who may read or write, and how that maps from server `GRANT`s to an embedded, local-first world[cite: 4].

## File Overview
* `integrity-notes.md`: Pod study notes on integrity layers.
* `setup.sql`: The strict edge telemetry schema.
* `task1-constraints.md`: Proof of constraint rejections.
* `readings.csv` & `ingest.py`: Dummy data and Python ingestion script.
* `task2-ingest.md`: Proof of idempotent edge ingestion using UPSERT.
* `task3-triggers.md`: Proof of alarm and audit triggers firing.
* `task4-and-5.md`: Access control comparisons and BEFORE vs AFTER trigger analysis.