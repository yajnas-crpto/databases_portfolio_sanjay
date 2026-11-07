import sqlite3
import csv
from pathlib import Path

DB = Path(__file__).with_name("edge.db")
CSV_FILE = Path(__file__).with_name("readings.csv")

conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys = ON;")

# Read the CSV file
incoming_data = []
with open(CSV_FILE, 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip header
    for row in reader:
        incoming_data.append((int(row[0]), row[1], float(row[2]), int(row[3])))

upsert_query = """
INSERT INTO reading(sensor_id, ts, value, interval_s)
VALUES (?, ?, ?, ?)
ON CONFLICT(sensor_id, ts) DO UPDATE SET value = excluded.value;
"""

conn.executemany(upsert_query, incoming_data)
conn.commit()

count = conn.execute("SELECT COUNT(*) FROM reading WHERE sensor_id = 1").fetchone()[0]
print(f"Total readings for sensor 1: {count}")