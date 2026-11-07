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

Comparison Note:
On a PostgreSQL server, access control is handled internally using CREATE ROLE and GRANT SELECT ON ... TO ... commands. Because embedded SQLite has no concept of users, security shifts to the host operating system (Unix file permissions like chmod 444) and connection strings (mode=ro). File-permission-based control is acceptable for a local edge gateway where only one specific service writes data, but it would completely fail in a multi-tenant web application because all users ultimately connect through the same OS file handle.

# Task 5 (Stretcher): Break Your Own Alarm
The difference between BEFORE and AFTER Triggers:
If we switch the alarm trigger to BEFORE INSERT, the alarm gets written to the alarm table before the reading is actually committed to the primary reading table.

Why AFTER is the right default:
If the primary INSERT INTO reading fails (e.g., due to a STRICT type violation or a CHECK constraint violation), a BEFORE trigger would still execute and log an alarm for a reading that was ultimately rejected by the database. AFTER INSERT guarantees that the alarm is only generated if the primary data was safely written to the disk.