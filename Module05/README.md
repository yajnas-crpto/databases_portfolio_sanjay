# Module 5: Normalization vs. Denormalization Benchmarking Studio

This module derives functional dependencies, normalizes a job-part relation, creates a deliberate reporting table, and measures the read, write, and storage trade-offs on a 200,000-row SQLite dataset.

## Learning goals

1. Derive [functional dependencies and candidate keys](./normalization-notes.md).
2. Explain [1NF, 2NF, and 3NF](./normalization-notes.md) and the anomalies each decomposition addresses.
3. Deliberately denormalize a [dashboard reporting table](./task4-race.md).
4. Measure query latency, write cost, storage, integrity, and query plans with [reproducible scripts and results](./task5-price.md).
5. Defend a workload-specific design choice in the [recommendation memo](./memo.md).

## Evidence files

- `normalization-notes.md`: FDs, candidate key reasoning, two Mermaid ER diagrams, normal forms, and reproducible anomaly examples.
- `setup.sql`: flat dataset generation, normalized schema, reporting table, and indexes.
- `benchmark.py`: schema/integrity checks, query equivalence, interleaved timing, write costs, storage measurements, and query plans.
- `task4-race.md`: reporting-table definition, dashboard query medians, and normalized/denormalized query plans.
- `task5-price.md`: update results, storage results, index experiment, integrity results, and reproducibility details.
- `memo.md`: recommendation based on this machine's measured results.
- `curiosities.md`: sourced SQLite facts separated from local experiment observations.
- [`../Reflections/ref05.md`](../Reflections/ref05.md): Module 5 engineering decision logbook entry.

## Reproduce the setup and benchmark

From the repository root in PowerShell:

```powershell
.\.venv\Scripts\python.exe Module05\benchmark.py --setup
```

This uses the project's Python environment and writes `Module05/normalize-benchmark.db`, which is ignored by Git. It preserves any existing `Module05/normalize.db`. To rerun measurements without rebuilding the database, omit `--setup`.

The recorded local run used Python 3.14.8 and SQLite 3.53.1. Results can vary with SQLite build, operating system, storage, cache state, and background load; the benchmark script prints the environment and raw query samples on each run.
