# Task 1: Prove the Constraints Work

**1. Valid Insert & Generated Column Proof:**
```text
sqlite> INSERT INTO sensor VALUES (1,'cnc-01','temp_c','degC'), (2,'cnc-01','vib_rms','mm/s');
sqlite> INSERT INTO reading(sensor_id, ts, value, interval_s) VALUES (1,'2026-03-01 08:00:00', 41.5, 1);
sqlite> SELECT reading_id, value, interval_s, energy_j FROM reading;
1|41.5|1|41.5
```

**Rejected: Domain check (impossible temperature):**
```sqlite> INSERT INTO reading(sensor_id, ts, value, interval_s) VALUES (1,'2026-03-01 08:00:01', 9000, 1);
Runtime error: CHECK constraint failed: value >= -273.15 AND value <= 5000 (19)
```

**3. Rejected: STRICT type (text into a REAL):**
```sqlite> INSERT INTO reading(sensor_id, ts, value, interval_s) VALUES (1,'2026-03-01 08:00:02', 'hot', 1);
Runtime error: cannot store TEXT value in REAL column reading.value (19)
```

**4. Rejected: Referential integrity (sensor 99 does not exist):**
```sqlite> INSERT INTO reading(sensor_id, ts, value, interval_s) VALUES (99,'2026-03-01 08:00:03', 40, 1);
Runtime error: FOREIGN KEY constraint failed (19)
```

**5. Rejected: Entity integrity (duplicate machine_id + metric):**
```sqlite> INSERT INTO sensor VALUES (3,'cnc-01','temp_c','degC');
Runtime error: UNIQUE constraint failed: sensor.machine_id, sensor.metric (19)
```



