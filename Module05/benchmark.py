"""Build and benchmark the Module 5 SQLite normalization example.

Run from the repository root with:
    .venv/Scripts/python.exe Module05/benchmark.py --setup

The default database is a separate, git-ignored file so normalize.db is kept.
"""

from __future__ import annotations

import argparse
import platform
import sqlite3
import statistics
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DB_PATH = HERE / "normalize-benchmark.db"
SETUP_PATH = HERE / "setup.sql"
REPEATS = 7

NORMALIZED_QUERY = """
SELECT m.machine_id, m.site, j.technician, SUM(p.part_price) AS cost
FROM job AS j
JOIN machine AS m ON m.machine_id = j.machine_id
JOIN job_part AS jp ON jp.job_id = j.job_id
JOIN part AS p ON p.part_no = jp.part_no
WHERE j.done_on >= date('2026-03-01')
GROUP BY m.machine_id, j.technician
ORDER BY m.machine_id, j.technician
"""

DENORMALIZED_QUERY = """
SELECT machine_id, site, technician, SUM(part_price) AS cost
FROM report_jobpart
WHERE done_on >= date('2026-03-01')
GROUP BY machine_id, technician
ORDER BY machine_id, technician
"""


def median_query_ms(connection: sqlite3.Connection, query: str) -> float:
    samples: list[float] = []
    for _ in range(REPEATS):
        started = time.perf_counter_ns()
        connection.execute(query).fetchall()
        samples.append((time.perf_counter_ns() - started) / 1_000_000)
    return statistics.median(samples)


def interleaved_query_ms(
    connection: sqlite3.Connection,
) -> tuple[float, float, list[tuple[float, float]]]:
    normalized: list[float] = []
    denormalized: list[float] = []
    pairs: list[tuple[float, float]] = []
    for run in range(REPEATS):
        order = (
            (NORMALIZED_QUERY, DENORMALIZED_QUERY)
            if run % 2 == 0
            else (DENORMALIZED_QUERY, NORMALIZED_QUERY)
        )
        measured: dict[str, float] = {}
        for query in order:
            started = time.perf_counter_ns()
            connection.execute(query).fetchall()
            elapsed = (time.perf_counter_ns() - started) / 1_000_000
            measured["normalized" if query == NORMALIZED_QUERY else "denormalized"] = elapsed
        normalized.append(measured["normalized"])
        denormalized.append(measured["denormalized"])
        pairs.append((measured["normalized"], measured["denormalized"]))
    return statistics.median(normalized), statistics.median(denormalized), pairs


def update_samples(connection: sqlite3.Connection, design: str) -> tuple[float, int]:
    table, where = (
        ("machine", "machine_id = 'cnc-02'")
        if design == "normalized"
        else ("report_jobpart", "machine_id = 'cnc-02'")
    )
    samples: list[float] = []
    affected: list[int] = []
    for _ in range(REPEATS):
        connection.execute("BEGIN")
        started = time.perf_counter_ns()
        cursor = connection.execute(
            f"UPDATE {table} SET site = 'Bielefeld' WHERE {where}"
        )
        samples.append((time.perf_counter_ns() - started) / 1_000_000)
        affected.append(cursor.rowcount)
        connection.rollback()
    if len(set(affected)) != 1:
        raise AssertionError(f"Unstable {design} update row counts: {affected}")
    return statistics.median(samples), affected[0]


def object_storage(connection: sqlite3.Connection, tables: tuple[str, ...]) -> int:
    placeholders = ",".join("?" for _ in tables)
    names = [
        row[0]
        for row in connection.execute(
            f"SELECT name FROM sqlite_master WHERE type IN ('table','index') "
            f"AND tbl_name IN ({placeholders})",
            tables,
        )
    ]
    if not names:
        raise AssertionError(f"No SQLite objects found for {tables}")
    marks = ",".join("?" for _ in names)
    return int(
        connection.execute(
            f"SELECT COALESCE(SUM(pgsize), 0) FROM dbstat WHERE name IN ({marks})",
            names,
        ).fetchone()[0]
    )


def explain(connection: sqlite3.Connection, query: str) -> list[tuple]:
    return connection.execute("EXPLAIN QUERY PLAN " + query).fetchall()


def validate(connection: sqlite3.Connection) -> dict[str, int]:
    connection.execute("PRAGMA foreign_keys = ON")
    fk_enabled = connection.execute("PRAGMA foreign_keys").fetchone()[0]
    if fk_enabled != 1:
        raise AssertionError("Foreign-key enforcement did not enable")

    expected_primary_keys = {
        "machine": ["machine_id"],
        "part": ["part_no"],
        "job": ["job_id"],
        "job_part": ["job_id", "part_no"],
    }
    for table, expected in expected_primary_keys.items():
        info = connection.execute(f"PRAGMA table_info({table})").fetchall()
        actual = [name for _, name, _, _, _, key_position in sorted(info, key=lambda row: row[5]) if key_position]
        if actual != expected:
            raise AssertionError(f"Unexpected {table} primary key: {actual}")

    expected_foreign_keys = {
        ("job", "machine_id", "machine", "machine_id"),
        ("job_part", "job_id", "job", "job_id"),
        ("job_part", "part_no", "part", "part_no"),
    }
    actual_foreign_keys = {
        (table, source, target, target_column)
        for table in ("job", "job_part")
        for _, _, target, source, target_column, *_ in connection.execute(
            f"PRAGMA foreign_key_list({table})"
        ).fetchall()
    }
    if actual_foreign_keys != expected_foreign_keys:
        raise AssertionError(f"Unexpected foreign keys: {actual_foreign_keys}")

    counts = {
        table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        for table in (
            "flat_jobpart",
            "machine",
            "part",
            "job",
            "job_part",
            "report_jobpart",
        )
    }
    if counts["flat_jobpart"] != 200_000:
        raise AssertionError(f"Expected 200,000 flat rows, got {counts['flat_jobpart']}")
    if counts["job_part"] != counts["flat_jobpart"]:
        raise AssertionError("Normalized job_part count differs from flat source")
    if counts["report_jobpart"] != counts["flat_jobpart"]:
        raise AssertionError("Reporting table count differs from flat source")

    fk_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
    if fk_errors:
        raise AssertionError(f"Foreign-key violations: {fk_errors[:5]}")

    integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    if integrity != "ok":
        raise AssertionError(f"SQLite integrity_check returned {integrity!r}")

    normalized = connection.execute(NORMALIZED_QUERY).fetchall()
    denormalized = connection.execute(DENORMALIZED_QUERY).fetchall()
    if normalized != denormalized:
        raise AssertionError("Normalized and denormalized query results differ")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--setup",
        action="store_true",
        help="rebuild the separate normalize-benchmark.db before benchmarking",
    )
    args = parser.parse_args()

    if args.setup:
        DB_PATH.unlink(missing_ok=True)
        with sqlite3.connect(DB_PATH) as setup_connection:
            setup_connection.executescript(SETUP_PATH.read_text(encoding="utf-8"))

    if not DB_PATH.exists():
        parser.error(f"{DB_PATH.name} does not exist; run with --setup first")

    # Disable sqlite3's prepared-statement cache so the dropped-index experiment
    # prepares a fresh statement against the changed schema.
    connection = sqlite3.connect(DB_PATH, cached_statements=0)
    try:
        counts = validate(connection)
        normalized_ms, denormalized_ms, interleaved = interleaved_query_ms(connection)
        normalized_update_ms, normalized_changed = update_samples(connection, "normalized")
        denormalized_update_ms, denormalized_changed = update_samples(connection, "denormalized")
        normalized_bytes = object_storage(
            connection, ("machine", "part", "job", "job_part")
        )
        denormalized_bytes = object_storage(connection, ("report_jobpart",))

        normalized_plan = explain(connection, NORMALIZED_QUERY)
        denormalized_plan = explain(connection, DENORMALIZED_QUERY)

        connection.execute("DROP INDEX ix_report_machine")
        no_index_normalized_ms, no_index_report_ms, no_index_pairs = interleaved_query_ms(connection)
        no_index_report_plan = explain(connection, DENORMALIZED_QUERY)
        connection.execute("CREATE INDEX ix_report_machine ON report_jobpart(machine_id)")

        print(f"Python: {platform.python_version()} ({platform.python_implementation()})")
        print(f"SQLite: {sqlite3.sqlite_version}")
        print(f"Database: {DB_PATH.relative_to(ROOT).as_posix()}")
        print(f"Query methodology: {REPEATS} warm-cache interleaved runs; medians; fetchall included")
        print(f"Run pairs normalized/report (ms): {interleaved}")
        print(f"Query medians with report index (ms): {normalized_ms:.3f} / {denormalized_ms:.3f}")
        print(f"Query medians without report index (ms): {no_index_normalized_ms:.3f} / {no_index_report_ms:.3f}")
        print(f"No-index run pairs normalized/report (ms): {no_index_pairs}")
        print(f"Update medians normalized/report (ms): {normalized_update_ms:.3f} / {denormalized_update_ms:.3f}")
        print(f"Rows changed normalized/report: {normalized_changed} / {denormalized_changed}")
        print(f"dbstat bytes normalized/report (tables and indexes): {normalized_bytes} / {denormalized_bytes}")
        print(f"Query result equivalence: PASS ({len(connection.execute(NORMALIZED_QUERY).fetchall())} grouped rows)")
        print(f"Row counts: {counts}")
        print("PRAGMA foreign_key_check: PASS (0 rows)")
        print(f"PRAGMA integrity_check: {connection.execute('PRAGMA integrity_check').fetchone()[0]}")
        print("EXPLAIN QUERY PLAN normalized:")
        for row in normalized_plan:
            print(f"  {row}")
        print("EXPLAIN QUERY PLAN denormalized:")
        for row in denormalized_plan:
            print(f"  {row}")
        print("EXPLAIN QUERY PLAN denormalized (report index dropped):")
        for row in no_index_report_plan:
            print(f"  {row}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
