import sqlite3
import csv
from pathlib import Path

DB = Path(__file__).with_name("edge.db")
CSV_FILE = Path(__file__).with_name("readings.csv")

conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys = ON;")

# Read the CSV file safely, ignoring headers and empty lines
incoming_data = []
with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        # Skip empty rows or the header row itself
        if not row or row[0] == 'sensor_id':
            continue
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