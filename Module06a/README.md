# Module 6a — The Analytical Engine (DuckDB)

This module reuses `Module05/normalize.db`, expands its 200,000-row `report_jobpart` relation across ten 91-day shifts, exports an original-size CSV, and produces equivalent two-million-row SQLite and Parquet analytical inputs. It measures dashboard and monthly workloads in SQLite and DuckDB, records actual plans, measures the transactional boundary, and produces the zstd compression evidence required by the core homework.

The official Module 6a specification marks its draft boundary as provisional. This implementation follows its stated learning goals and distinguishes core work from optional S1–S3 stretchers and the optional intense `refresh.py` track. The separately clarified zstd homework is treated as core. The syllabus counts Modules 6a and 6b together for Module 6’s core points and expects a reflection for each studio.

## Files

- `prepare.py` — opens the Module 5 database read-only; builds `history.db` and exports the original 200,000 rows to `report_jobpart.csv`.
- `to_parquet.py` — expands the CSV once in DuckDB to Snappy Parquet, makes a zstd copy, compares aggregate results with historical SQLite, and measures warm dashboard reads from both compression variants.
- `race.py` — verifies and benchmarks equivalent dashboard and monthly queries with warm-ups, seven interleaved runs by default, medians, min/max, and speedup ratios.
- `explain.py` — saves DuckDB `EXPLAIN ANALYZE` for the same dashboard and monthly SQL templates used by `race.py`.
- `boundary.py` — compares single-row inserts, batched/repeated inserts, point lookups, and a small selective query in isolated in-memory databases.
- `duckdb-notes.md`, `decision.md` — technical notes and a measured engineering memo. Discussion and personal sections remain placeholders.
- `benchmark-results/` — machine-specific JSON/CSV measurements, plans, and validation outputs.

## Dependencies

Use the repository's existing Python 3.14 `uv` environment. DuckDB is already declared in `pyproject.toml`; no package or lockfile change is required. The standard library provides SQLite, CSV, JSON, statistics, and test tools. The pipeline does not install extensions and does not use `sqlite_scanner`.

## Run from the repository root

```powershell
.\.venv\Scripts\python.exe Module06a\prepare.py
.\.venv\Scripts\python.exe Module06a\to_parquet.py
.\.venv\Scripts\python.exe Module06a\race.py
.\.venv\Scripts\python.exe Module06a\explain.py
.\.venv\Scripts\python.exe Module06a\boundary.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_module06a.py" -v
```

Scripts resolve paths from their own location, so the equivalent Python invocations also work from another current directory. `prepare.py` will stop with a clear error if the original database or `report_jobpart` schema is absent. It never rebuilds or writes to the Module 5 source. It builds temporary outputs and replaces generated Module 6a outputs only after validation succeeds. Run `prepare.py` before `to_parquet.py`; Parquet reads the 200k CSV and performs the tenfold expansion once, while SQLite `history.db` independently uses the same ten shifts.

Generated source CSV, SQLite databases, and Parquet files are ignored by Git. Benchmark CSV/JSON and plans are intentional portfolio evidence. A benchmark result is specific to the saved environment and run; compare query equivalence, median, range, and plan together rather than treating a speedup as universal.

## Evidence interpretation and outstanding input

The pipeline validates source and output row counts, date bounds, total sums, dashboard groups, and month-by-machine aggregates. `EXPLAIN ANALYZE` runs the actual query; the scan and group-by operators should be read from the saved output rather than presumed. `boundary.py` deliberately tests OLTP-style operations where SQLite may be the better fit. The zstd paragraph in `decision.md` reports measured file sizes and timing on this machine and discusses refresh failure and staleness.

Still for the student: nearest-pod discussion, observed surprises, peer comparisons/defence, personal engineering choice, and personal reflection in `Reflections/ref06a.md`. The intense `refresh.py` track and the S1/S2/S3 stretchers are optional; no `refresh.py` implementation is required here.
