    # Module 3 — LLM-Assisted SQL & Query Profiling

This module covers advanced DQL querying, Query Optimization, and Relational Algebra. Instead of just writing SQL manually, the focus is on generating SQL with an LLM and using SQLite's `EXPLAIN QUERY PLAN` to prove the generated code is fast, correct, and secure against SQL injection.

## 🎯 Learning Goals
1. Build complex **DQL** queries: joins, aggregation with `GROUP BY`/`HAVING`, subqueries, and window functions.
2. Read **`EXPLAIN QUERY PLAN`** as *primary evidence*: say what the engine will do for a given query, tell a `SCAN` from a `SEARCH`, and a table lookup from a covering index.
3. **Benchmark** the effect of an index and explain when the planner ignores one.
4. Generate a query with an **LLM**, then **verify** it: correctness, performance, and edge cases.
5. **Prevent SQL injection** with bound parameters and demonstrate why string concatenation is exploitable.

## 📝 Task Execution & Evidence

*Note: For this module, Jomarie was absent. However, our pod welcomed a new permanent member, Myo Min Lin, and was joined by a temporary member, [Isa Babayev](https://github.com/isa-babayev-ibabayev). We split the conceptual workstreams using a Divide & Conquer strategy.*

### Divide & Conquer Pod Study (Tasks A, B, C)
My repository serves as the central hub for our pod's shared workstream results. I took the "Plan Vocabulary" workstream, defining `SCAN`, `SEARCH`, and `COVERING` indexes, while my pod mates (Sebastian, Myo, and Isa) handled Relational Algebra, Clause Order, and Tuning/Security. 
* **Shared Evidence:** [sql-notes.md](./sql-notes.md)

### LLM Generation & Query Profiling (Task 1)
I prompted an LLM to generate a complex aggregation query, predicted the execution plan, and then verified it using `EXPLAIN QUERY PLAN` to check for full table scans.
* **Evidence:** [task1-profiling.md](./task1-profiling.md)

### Index Benchmarking (Task 2)
I built a Python script to benchmark execution times (medians of 3 runs). I documented how adding indexes changed `SCAN` to `SEARCH`, and successfully proved that an index can actually *slow down* a massive aggregation query due to B-Tree traversal overhead.
* **Database Setup:** [setup.sql](./setup.sql)
* **Python Benchmark:** [bench.py](./bench.py)
* **Results & Proof:** [benchmark-results.md](./benchmark-results.md)

### Security: SQL Injection (Task 3)
I reproduced a classic `' OR '1'='1` injection payload and demonstrated how the vulnerability is eliminated by using bound parameters (`?`) rather than manual string escaping.
* **Evidence:** [injection_demo.py](./injection_demo.py) (Explanation stored in `sql-notes.md`)

### Stretcher Task (Task 5)
I rewrote a standard `GROUP BY` report using both a Correlated Subquery and a modern Window Function (`OVER (PARTITION BY ...)`).
* **Evidence:** [window-stretcher.sql](./window-stretcher.sql)

## 🧠 Reflection
* **Module 3 Logbook Entry:** [Reflection 3](../Reflections/ref03.md)