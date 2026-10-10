# Task 9: SQLite Shell Power Moves

### 1. Commands Executed
- **Replayed queries from a file:** `.read Module01/queries.sql` inside the SQLite shell.
- **Exported JSON using .once and .mode json:** 
  `sqlite3 -cmd ".mode json" -cmd ".once Module01/result.json" Module01/telemetry.db "SELECT machine, MAX(vib_rms) FROM readings GROUP BY machine;"`
- **Database Backup & Compaction:**
  `sqlite3 Module01/telemetry.db ".backup Module01/backup.db"`
  `sqlite3 Module01/telemetry.db "VACUUM INTO 'Module01/compact.db';"`

### 2. Surprising Finding
Using `VACUUM INTO` builds a pristine, tightly packed copy of the database from scratch, removing unused pages and defragmenting internal structures. Comparing the file sizes showed that `VACUUM INTO` resulted in an optimized file layout compared to a standard binary `.backup`.