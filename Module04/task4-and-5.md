# Task 4: Access Control Without a Server

**1. Exposing a Safe Subset View:**
```text
sqlite> CREATE VIEW machine_health AS
   ...> SELECT s.machine_id, s.metric, MAX(r.value) AS peak, COUNT(*) AS n
   ...> FROM sensor s JOIN reading r USING(sensor_id) GROUP BY s.machine_id, s.metric;
```

**2. Connection-Level Read-Only Test (mode=ro):**
```
PS D:\...\databases_portfolio_sanjay> sqlite3 "file:Module04/edge.db?mode=ro" "DELETE FROM reading;"
Runtime error: attempt to write a readonly database (8)
```