# Task 2: Index Benchmark Results

**Dashboard Query Performance (Median of 3 runs):**
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
*   **After Index:** `SEARCH o USING INDEX ix_orders_ordered_on` (Time: ~1ms)

**Negative Result Explanation:** The `ix_orderline_product` index is entirely useless for the dashboard query because the planner already accesses the `product` table via its ultra-fast `INTEGER PRIMARY KEY`.