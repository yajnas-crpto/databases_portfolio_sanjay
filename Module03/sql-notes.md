# Module 3 Pod Notes & Curiosities

**Pod Members:**
* Sanjay Maheshwari (Workstream 3 - Plan Vocabulary)
* Sebastian Soon (Workstream 2 - Clause order)
* Isa Babayev (Guest - Workstream 1 - Algebra ↔ SQL)
* Myo Min Lin (Workstream 4 -  Tuning & security)
* Jomarie (Absent for this session)

---

## Workstream 1: Algebra ↔ SQL 
For `SELECT * FROM maint_job WHERE technician = 'Beier';`, the logic and sequence should be like this: $\sigma_{technician='Beier'}(maint\_job)$ (because we select from WHERE? from technician) equals 'Beier' is text value and (maint_job) means this means we are doing filtering to the main_job table.

**LLM Comparison:** I asked Gemini to translate the same query. We completely agreed on using the selection operator ($\sigma$) for the WHERE clause. The only difference in our approach was a minor learning point: the LLM pointed out that the projection operator ($\pi$) is usually omitted entirely when the SQL query uses `SELECT *`.

## Workstream 2: Clause Order 
*   **Written order:** `SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY`
*   **Evaluated order:** `FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY`
*   **Counterexample:** `SELECT technician AS tech FROM maint_job WHERE tech = 'Beier';` fails because the database evaluates the `WHERE` clause before the `SELECT` clause even creates the `tech` alias.

## Workstream 3: Plan Vocabulary 
*   **SCAN:** The database reads every single row in the table top-to-bottom. (Slow for large tables).
*   **SEARCH:** The database uses an index to jump straight to the matching rows. (Fast).
*   **COVERING:** The index contains all the columns the query asked for, so the database doesn't even need to open the main table.

## Workstream 4: Tuning & Security 
*   **Defeating an index:** Wrapping a column in a function, like `WHERE date(ordered_on) = '2025-01-01'`, will defeat an index on `ordered_on` and force a SCAN.
*   **SQL Injection Payload:** `' OR '1'='1` tricks the database into returning all rows by permanently evaluating to TRUE.

---

## Task A: Plan Safari Predictions
*   `SELECT * FROM maint_job WHERE technician = 'Beier';` 
    *   **Prediction:** SCAN. **Actual:** SCAN (no index exists yet).
*   `SELECT * FROM machine WHERE machine_name = 'cnc-02';` 
    *   **Prediction:** SEARCH. **Actual:** SEARCH (uses the primary key index).
*   `SELECT * FROM maint_job WHERE technician LIKE '%ei%';` 
    *   **Prediction:** SCAN. **Actual:** SCAN (wildcard at the start of a string defeats indexes).

## Task B: Algebra Check
*(Completed in Workstream 1 by Isa)*
* **For Task B**, we need to make mathematical equation. For SELECT * FROM maint_job WHERE technician = 'Beier'; command, Logic and sequanece should be like this: sigma technician (because we select from WHERE? from technician) equals 'Beier' is text value and (maint\_job) means this means we are doing filtering to the main_job table
$\sigma_{technician='Beier'}(maint\_job)$

* **LLM Comparison**: I asked Gemini to translate the same query. We completely agreed on using the selection operator ($\sigma$) for the WHERE clause. The only difference in our approach was a minor learning point: the LLM pointed out that the projection operator ($\pi$) is usually omitted entirely when the SQL query uses SELECT *.

## Task C: Pod Discussion
Our pod shared these notes and verified that our local SQLite plans matched the expected behavior. We agreed that covering indexes are the most powerful tool for speeding up read-heavy queries.




