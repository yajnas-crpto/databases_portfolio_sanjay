**Exercising the Triggers:**
```text
sqlite> INSERT INTO reading(sensor_id, ts, value, interval_s) VALUES (2,'2026-03-01 09:00:00', 2.7, 1);
sqlite> UPDATE reading SET value = 1.4 WHERE sensor_id = 2;
```

**1. Alarm Row Produced (via AFTER INSERT trigger):**
sqlite> SELECT * FROM alarm;
1|2|2026-03-01 09:00:00|2.7|vibration over 2.0 mm/s

**2. Audit Row Produced (via AFTER UPDATE trigger):**
sqlite> SELECT * FROM audit;
1|1|2.7|1.4|2026-11-07 15:07:00

Trigger Cost Note:
Triggers run synchronously as part of the transaction. A trigger on a hot ingest path is not a free lunch. During an ingest of 10,000 rows, an AFTER INSERT alarm trigger forces the database to evaluate the WHEN clause 10,000 times. If the condition is met frequently, it triggers thousands of secondary INSERTs into the alarm table, drastically increasing disk I/O and slowing down the overall ingestion time compared to a raw table insert.