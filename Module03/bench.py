import sqlite3
import time
from pathlib import Path

DB = Path(__file__).with_name("warehouse.db")
conn = sqlite3.connect(DB)

query = """
SELECT c.city, COUNT(DISTINCT c.customer_id), SUM(ol.qty * p.price)
FROM customer c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_line ol ON ol.order_id = o.order_id
JOIN product p ON p.product_id = ol.product_id
WHERE o.ordered_on >= '2025-01-01' AND o.ordered_on < '2026-01-01'
GROUP BY c.city;
"""

# Run 3 times to simulate our median benchmark process
for i in range(3):
    start = time.perf_counter()
    conn.execute(query).fetchall()
    end = time.perf_counter()
    print(f"Run {i+1}: {(end - start) * 1000:.2f} ms")
    