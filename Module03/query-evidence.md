# Module 3 Query & Profiling Evidence

## Task 1: Ask the LLM, then check the plan
**Prompt:** "SQLite schema: `customer(customer_id, name, city)`, `product(product_id, sku, price)`, `orders(order_id, customer_id, ordered_on, status)`, `order_line(order_id, product_id, qty)`. Write a query that returns, for each city, the number of distinct customers and the total revenue (sum of `qty*price`) of orders placed in 2025, ordered by revenue descending."

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

**Correctness:** Yes, the query is correct. It properly uses `COUNT(DISTINCT)` and safely scopes the date without wrapping `ordered_on` in a function.
**My Predicted Plan:** SCAN customer, SCAN orders, SEARCH order_line, SEARCH product.
**Actual Plan (EXPLAIN QUERY PLAN):**
`SCAN c`
`SCAN o`
`SEARCH ol USING AUTOMATIC COVERING INDEX (order_id=?)`
`SEARCH p USING INTEGER PRIMARY KEY (rowid=?)`
`USE TEMP B-TREE FOR GROUP BY`
`USE TEMP B-TREE FOR ORDER BY`

---

## Task 2: Index Benchmark

**Dashboard Query Performance Table (Median of 3 runs):**
| State | Median Time | Plan Changes |
| :--- | :--- | :--- |
| Baseline (No Indexes) | ~45ms | SCAN c, SCAN o |
| Add `ix_orders_ordered_on` | ~45ms | No plan change for this specific query |
| Add `ix_orderline_order` | ~38ms | `SEARCH ol USING INDEX ix_orderline_order` |
| Add `ix_orderline_product` | ~38ms | No plan change (ignored in favor of PK) |

**The query an index CAN win (Single-day lookup):**
sql
SELECT o.order_id, o.ordered_on, c.name
FROM orders o JOIN customer c ON c.customer_id = o.customer_id
WHERE o.ordered_on = '2026-02-14';

*   **Before Index:** `SCAN o` (Time: ~12ms)
*   **After Index:** `SEARCH o USING INDEX ix_orders_ordered_on (ordered_on=?)` (Time: ~1ms)

**Negative Result Explanation:** The `ix_orderline_product` index is entirely useless for the dashboard query because the planner already accesses the `product` table via its ultra-fast `INTEGER PRIMARY KEY`. 

---

## Task 4: One query, from algebra to plan
**Single-Day Lookup Algebra:**
$\pi_{order\_id, ordered\_on, name}(\sigma_{ordered\_on='2026-02-14'}(orders \bowtie customer))$
*The SQL matches this perfectly: filter the rows first (WHERE), join the tables, then select the final columns.*

---

## Task 5 (Stretcher): Window functions vs Subqueries
**Original Group By:**
sql
SELECT c.customer_id, c.name, COUNT(*) AS late_orders
FROM orders o JOIN customer c ON c.customer_id = o.customer_id
WHERE o.status = 'late' GROUP BY c.customer_id, c.name;

**Window Function Rewrite:**
sql
SELECT DISTINCT c.customer_id, c.name,
COUNT(*) OVER (PARTITION BY c.customer_id) AS late_orders
FROM orders o JOIN customer c ON c.customer_id = o.customer_id
WHERE o.status = 'late';

*Comparison:* The LLM prefers the `GROUP BY` naturally. The Window Function allows keeping individual order details alongside the aggregate count if we needed them, but requires `DISTINCT` here to mimic a standard grouping, making it slightly more awkward for this specific report.