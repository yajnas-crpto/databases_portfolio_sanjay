-- queries.sql
SELECT machine, COUNT(*) AS n FROM readings GROUP BY machine;
SELECT machine, MAX(vib_rms) AS peak_vib FROM readings GROUP BY machine;