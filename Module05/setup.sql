PRAGMA foreign_keys = ON;

-- This script rebuilds the Module 5 tables in the selected SQLite database.
-- The runner uses a new ignored database file so the existing normalize.db is
-- preserved.
DROP TABLE IF EXISTS report_jobpart;
DROP TABLE IF EXISTS job_part;
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS part;
DROP TABLE IF EXISTS machine;
DROP TABLE IF EXISTS flat_jobpart;

CREATE TABLE flat_jobpart (
    job_id      INTEGER,
    machine_id  TEXT,
    site        TEXT,
    technician  TEXT,
    part_no     TEXT,
    part_price  TEXT,
    done_on     TEXT
);

-- 20,000 jobs x 10 parts = 200,000 job-part rows.
WITH RECURSIVE
  d10(v) AS (SELECT 0 UNION ALL SELECT v + 1 FROM d10 WHERE v < 9),
  d2(w) AS (SELECT 0 UNION ALL SELECT 1),
  j(n) AS (
    SELECT a.v + b.v * 10 + c.v * 100 + d.v * 1000 + e.w * 10000 + 1
    FROM d10 AS a CROSS JOIN d10 AS b CROSS JOIN d10 AS c
    CROSS JOIN d10 AS d CROSS JOIN d2 AS e
    WHERE a.v + b.v * 10 + c.v * 100 + d.v * 1000 + e.w * 10000 < 20000
  ),
  p(k) AS (SELECT 1 UNION ALL SELECT k + 1 FROM p WHERE k < 10)
INSERT INTO flat_jobpart
SELECT n,
       'cnc-' || printf('%02d', (n % 50) + 1),
       CASE (n % 50) WHEN 0 THEN 'Bielefeld' ELSE 'Gütersloh' END,
       'tech-' || (n % 7),
       'P-' || printf('%04d', k),
       printf('%.2f', 5 + k),
       date('2026-01-01', '+' || (n % 90) || ' days')
FROM j CROSS JOIN p;

CREATE INDEX ix_flat_machine ON flat_jobpart(machine_id);

CREATE TABLE machine (
    machine_id TEXT PRIMARY KEY,
    site       TEXT NOT NULL
) STRICT;

CREATE TABLE part (
    part_no    TEXT PRIMARY KEY,
    part_price REAL NOT NULL
) STRICT;

CREATE TABLE job (
    job_id     INTEGER PRIMARY KEY,
    machine_id TEXT NOT NULL REFERENCES machine(machine_id),
    technician TEXT NOT NULL,
    done_on    TEXT NOT NULL
) STRICT;

CREATE TABLE job_part (
    job_id  INTEGER NOT NULL REFERENCES job(job_id),
    part_no TEXT NOT NULL REFERENCES part(part_no),
    PRIMARY KEY (job_id, part_no)
) STRICT;

INSERT INTO machine
SELECT DISTINCT machine_id, site FROM flat_jobpart;
INSERT INTO part
SELECT DISTINCT part_no, CAST(part_price AS REAL) FROM flat_jobpart;
INSERT INTO job
SELECT DISTINCT job_id, machine_id, technician, done_on FROM flat_jobpart;
INSERT INTO job_part
SELECT DISTINCT job_id, part_no FROM flat_jobpart;

CREATE TABLE report_jobpart AS
SELECT j.job_id, m.machine_id, m.site, j.technician, jp.part_no,
       p.part_price, j.done_on
FROM job AS j
JOIN machine AS m ON m.machine_id = j.machine_id
JOIN job_part AS jp ON jp.job_id = j.job_id
JOIN part AS p ON p.part_no = jp.part_no;
CREATE INDEX ix_report_machine ON report_jobpart(machine_id);

-- A SQL client displays these count results when this setup script is run.
-- benchmark.py independently executes and verifies its own count queries.
SELECT 'flat_jobpart' AS table_name, COUNT(*) AS row_count FROM flat_jobpart
UNION ALL SELECT 'machine', COUNT(*) FROM machine
UNION ALL SELECT 'part', COUNT(*) FROM part
UNION ALL SELECT 'job', COUNT(*) FROM job
UNION ALL SELECT 'job_part', COUNT(*) FROM job_part
UNION ALL SELECT 'report_jobpart', COUNT(*) FROM report_jobpart;

PRAGMA foreign_key_check;
