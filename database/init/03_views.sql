-- ============================================================
-- Pre-built Analytics Views
-- ============================================================

CREATE VIEW monthly_revenue AS
SELECT
    date_trunc('month', o.order_date)::date AS month,
    SUM(o.total_amount) AS revenue,
    COUNT(DISTINCT o.id) AS order_count,
    COUNT(DISTINCT o.customer_id) AS unique_customers
FROM orders o
WHERE o.status NOT IN ('cancelled', 'refunded')
GROUP BY 1
ORDER BY 1;

CREATE VIEW customer_ltv AS
SELECT
    c.id,
    c.first_name || ' ' || c.last_name AS name,
    c.email,
    c.segment,
    c.region,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    COUNT(o.id) AS order_count,
    MIN(o.order_date) AS first_order,
    MAX(o.order_date) AS last_order
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id AND o.status NOT IN ('cancelled', 'refunded')
GROUP BY c.id;

CREATE VIEW subscription_metrics AS
SELECT
    plan_name,
    COUNT(*) AS total_subscriptions,
    COUNT(*) FILTER (WHERE status = 'active') AS active_count,
    COUNT(*) FILTER (WHERE status = 'churned') AS churned_count,
    COUNT(*) FILTER (WHERE status = 'trial') AS trial_count,
    COUNT(*) FILTER (WHERE status = 'paused') AS paused_count,
    SUM(mrr) FILTER (WHERE status = 'active') AS total_mrr
FROM subscriptions
GROUP BY plan_name
ORDER BY total_mrr DESC NULLS LAST;

CREATE VIEW product_performance AS
SELECT
    p.id,
    p.name,
    p.category,
    p.price AS list_price,
    COUNT(DISTINCT oi.order_id) AS times_ordered,
    SUM(oi.quantity) AS total_units_sold,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount / 100)) AS total_revenue,
    AVG(oi.discount) AS avg_discount_pct
FROM products p
LEFT JOIN order_items oi ON oi.product_id = p.id
LEFT JOIN orders o ON o.id = oi.order_id AND o.status NOT IN ('cancelled', 'refunded')
GROUP BY p.id
ORDER BY total_revenue DESC NULLS LAST;

CREATE VIEW support_overview AS
SELECT
    priority,
    COUNT(*) AS total_tickets,
    COUNT(*) FILTER (WHERE status IN ('open', 'in_progress')) AS open_tickets,
    COUNT(*) FILTER (WHERE status IN ('resolved', 'closed')) AS closed_tickets,
    AVG(EXTRACT(EPOCH FROM (resolved_at - created_at)) / 3600)
        FILTER (WHERE resolved_at IS NOT NULL) AS avg_resolution_hours
FROM support_tickets
GROUP BY priority
ORDER BY
    CASE priority WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 ELSE 4 END;
