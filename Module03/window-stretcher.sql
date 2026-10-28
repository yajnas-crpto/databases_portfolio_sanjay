-- Original Group By
SELECT c.customer_id, c.name, COUNT(*) AS late_orders
FROM orders o JOIN customer c ON c.customer_id = o.customer_id
WHERE o.status = 'late' GROUP BY c.customer_id, c.name;

-- Window Function Rewrite
SELECT DISTINCT c.customer_id, c.name, 
       COUNT(*) OVER (PARTITION BY c.customer_id) AS late_orders
FROM orders o JOIN customer c ON c.customer_id = o.customer_id
WHERE o.status = 'late';
