# Round 4: Race It — Normalized vs. Denormalized Reporting

## Reporting table

`setup.sql` builds the reporting table from the normalized source tables:

```sql
CREATE TABLE report_jobpart AS
SELECT j.job_id, m.machine_id, m.site, j.technician, jp.part_no,
       p.part_price, j.done_on
FROM job AS j
JOIN machine AS m ON m.machine_id = j.machine_id
JOIN job_part AS jp ON jp.job_id = j.job_id
JOIN part AS p ON p.part_no = jp.part_no;
CREATE INDEX ix_report_machine ON report_jobpart(machine_id);
```

## Queries and equivalence

Both queries filter on the same date and return machine, site, technician, and summed part cost. `benchmark.py` checks exact result equivalence before timing. On this run both returned **350 grouped rows**.

The script ran seven warm-cache iterations, alternating the query order on each iteration. Each timed operation includes fetching all rows. The median includes all seven measured runs; all times are milliseconds.

| Design | Median with report index |
|---|---:|
| Normalized four-table join | 124.415 ms |
| Denormalized reporting table | 98.508 ms |

This run measured a 25.907 ms lower median for the reporting query. Run-to-run values varied, so this is evidence for this local setup and data, not a production guarantee. See [task5-price.md](./task5-price.md) for the index comparison, update costs, and storage.

## `EXPLAIN QUERY PLAN`

Captured with Python 3.14.8 and SQLite 3.53.1 from the run database. SQLite's numeric estimates are included as emitted by this build.

Normalized query:

```text
(14, 0, 216, 'SCAN jp')
(16, 0, 45, 'SEARCH j USING INTEGER PRIMARY KEY (rowid=?)')
(24, 0, 47, 'SEARCH m USING INDEX sqlite_autoindex_machine_1 (machine_id=?)')
(29, 0, 47, 'SEARCH p USING INDEX sqlite_autoindex_part_1 (part_no=?)')
(34, 0, 0, 'USE TEMP B-TREE FOR GROUP BY')
```

Reporting query:

```text
(8, 0, 224, 'SCAN report_jobpart USING INDEX ix_report_machine')
(16, 0, 0, 'USE TEMP B-TREE FOR GROUP BY')
```

The normalized plan scans the 200,000-row bridge table and looks up each related job, machine, and part. The reporting plan scans the reporting index and still builds a temporary B-tree for grouping. The plan describes operations; the repeated local timings measure their cost on this dataset.

## Reproduce

From the repository root, run:

```powershell
.\.venv\Scripts\python.exe Module05\benchmark.py --setup
```

The command builds `Module05/normalize-benchmark.db`, a git-ignored run database. It does not overwrite the existing `Module05/normalize.db`.
