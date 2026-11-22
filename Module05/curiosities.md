# Harvest: Technical Curiosities

The notes below separate documented SQLite behavior from observations made by `benchmark.py` on this repository's local dataset.

1. **Recursive CTE plus `CROSS JOIN` expansion** — SQLite documents recursive common table expressions as a way to generate sequences and `CROSS JOIN` as a Cartesian product. In this experiment, the generated job sequence crossed with ten part values to create exactly 200,000 rows. The exact count and runtime are experiment facts, not a performance guarantee. [SQLite WITH clause](https://www.sqlite.org/lang_with.html)

2. **Prices begin as text** — SQLite's `printf()` returns formatted text, so `printf('%.2f', ...)` deliberately makes `flat_jobpart.part_price` textual. The setup casts it to `REAL` during decomposition into `part`; this is visible in the SQL and was accepted by the executed script. [SQLite core functions](https://www.sqlite.org/lang_corefunc.html)

3. **The planner scans the reporting index** — The captured plan says `SCAN report_jobpart USING INDEX ix_report_machine`, followed by a temporary B-tree for grouping. In this run, dropping the index changed the plan to a table scan and the median changed from 98.508 ms to 89.405 ms. The plan text is documented output; the timing is a local observation with seven interleaved runs and varied measurements. [EXPLAIN QUERY PLAN](https://www.sqlite.org/eqp.html)

4. **Allocated pages belong to tables and indexes** — SQLite's `dbstat` virtual table reports page-level information by database object. This run summed `pgsize` for each design's tables and indexes, giving 8,155,136 bytes for the normalized objects and 14,077,952 bytes for the reporting objects. Those are allocated page bytes for this database, not logical row sizes. [SQLite dbstat](https://www.sqlite.org/dbstat.html)

5. **`SELECT DISTINCT` does not validate a business rule by itself** — The setup uses `SELECT DISTINCT` to remove duplicate source tuples while loading entities. A conflicting row for the same primary key would still be rejected by the target key constraint; that is the enforcement mechanism. [SQLite CREATE TABLE constraints](https://www.sqlite.org/lang_createtable.html)
