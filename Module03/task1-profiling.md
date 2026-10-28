# Task 1: Ask the LLM, then check the plan

**Prompt:** "SQLite schema: `customer`, `product`, `orders`, `order_line`. Write a query that returns, for each city, the number of distinct customers and the total revenue (sum of `qty*price`) of orders placed in 2025, ordered by revenue descending."

**LLM Generated SQL:**
sql
SELECT c.city, COUNT(DISTINCT c.customer_id) AS customers,
SUM(ol.qty * p.price) AS revenue
FROM customer c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_line ol ON ol.order_id = o.order_id
JOIN product p ON p.product_id = ol.product_id
WHERE o.ordered_on >= '2025-01-01' AND o.ordered_on < '2026-01-01'
GROUP BY c.city
ORDER BY revenue DESC;

**Correctness:** Yes, it is correct. It uses `COUNT(DISTINCT)` and safely scopes the date.

**My Predicted Plan:** SCAN customer, SCAN orders, SEARCH order_line, SEARCH product.

**Actual Plan (EXPLAIN QUERY PLAN):**
`SCAN c`
`SCAN o`
`SEARCH ol USING AUTOMATIC COVERING INDEX (order_id=?)`
`SEARCH p USING INTEGER PRIMARY KEY (rowid=?)`
`USE TEMP B-TREE FOR GROUP BY`
`USE TEMP B-TREE FOR ORDER BY`