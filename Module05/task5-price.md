# Round 5: Price It — Writes, Storage, and Index Experiment

## Method

Results below came from `benchmark.py` on Python 3.14.8 (CPython) with SQLite 3.53.1, using `Module05/normalize-benchmark.db`. Dashboard queries were run seven times in warm cache, alternating normalized-first and reporting-first order; the table reports medians and includes `fetchall()` time. Update timings are medians of seven update statements, each wrapped in a transaction and rolled back so every repetition starts from the same data. The reported row counts are SQLite's affected-row counts. Storage is allocated page size from SQLite's `dbstat` virtual table for each design's tables and indexes; it excludes the flat source table.

## Measured results

| Measure | Normalized (3NF) | Denormalized report |
|---|---:|---:|
| Dashboard query median, report index present | 124.415 ms | 98.508 ms |
| Dashboard query median, report index dropped | 128.583 ms | 89.405 ms |
| Update median for site change on `cnc-02` | 0.998 ms | 8.028 ms |
| Rows affected by that update | 1 | 4,000 |
| `dbstat` allocated bytes (tables and indexes) | 8,155,136 | 14,077,952 |
| `dbstat` allocated KiB | 7,964 KiB | 13,748 KiB |

The report design uses about **72.6% more allocated bytes** in this run. The update changes 4,000 duplicate site values in the report table compared with one source value in `machine`. The query medians are machine-specific: on this run the reporting table was faster, but the seven individual timings varied. These numbers should not be generalized beyond this SQLite build, dataset, and local machine.

## Index experiment

The benchmark alternated the same queries seven times with `ix_report_machine` present, dropped that index, then repeated the interleaved measurements. With the index present, the reporting-query median was **98.508 ms**; without it, the median was **89.405 ms**. The index therefore did not help this full aggregation in this run. The no-index result is noisy, so the evidence supports testing the query without this index for this workload, not a universal claim that the index slows SQLite.

Plan after dropping the report index:

```text
(7, 0, 216, 'SCAN report_jobpart')
(14, 0, 0, 'USE TEMP B-TREE FOR GROUP BY')
```

The benchmark disables Python's prepared-statement cache so the post-drop query is prepared against the changed schema. It recreates `ix_report_machine` after measuring; the on-disk benchmark database is left with the index in place.

## Integrity and result checks

The same run verified the schema primary keys (`machine`, `part`, `job`, and composite `job_part`), the three declared foreign-key relationships, and enabled foreign-key enforcement on the connection. Results:

- Row counts: `flat_jobpart` 200,000; `machine` 50; `part` 10; `job` 20,000; `job_part` 200,000; `report_jobpart` 200,000.
- `PRAGMA foreign_key_check`: **0 rows**.
- `PRAGMA integrity_check`: **ok**.
- Normalized and denormalized dashboard results: **equivalent**, 350 grouped rows.

Reproduce all checks and measurements with `.\.venv\Scripts\python.exe Module05\benchmark.py --setup` from the repository root. `--setup` rebuilds the separate ignored `normalize-benchmark.db`; it leaves the existing `normalize.db` alone.
