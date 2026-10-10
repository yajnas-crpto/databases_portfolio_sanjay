# Task 7: LLM-Assisted SQL Profiling

### 1. The Prompt Used
Here is my SQLite table: readings(ts TEXT, machine TEXT, temp_c REAL, vib_rms REAL, spindle_load REAL). Write a query that returns, for each machine, the average spindle load for readings taken overnight (after 18:00), ordered by average load descending.

### 2. The Generated SQL
SELECT machine, AVG(spindle_load) AS avg_spindle_load
FROM readings
WHERE TIME(ts) > '18:00:00'
GROUP BY machine
ORDER BY avg_spindle_load DESC;

### 3. EXPLAIN QUERY PLAN Output
text
QUERY PLAN
|--SCAN readings
|--USE TEMP B-TREE FOR GROUP BY
`--USE TEMP B-TREE FOR ORDER BY

### 4. Verification Paragraph
The model successfully generated a syntactically correct query using `GROUP BY`, `AVG`, and `ORDER BY DESC` to calculate average spindle loads. However, it relied on the `TIME()` function over a raw text timestamp column (`ts`), which forced a full-table scan (`SCAN readings`) and would fail to correctly isolate overnight hours that cross midnight. I verified its behavior by running `EXPLAIN QUERY PLAN` in the SQLite shell to profile its execution performance.
