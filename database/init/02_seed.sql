-- ============================================================
-- Seed Data — ~1000 rows of realistic Retail/SaaS data
-- ============================================================

-- ---- Customers (200 rows) ----
INSERT INTO customers (first_name, last_name, email, segment, region, created_at)
SELECT
    (ARRAY['James','Mary','Robert','Patricia','John','Jennifer','Michael','Linda','David','Elizabeth',
           'William','Barbara','Richard','Susan','Joseph','Jessica','Thomas','Sarah','Charles','Karen',
           'Christopher','Lisa','Daniel','Nancy','Matthew','Betty','Anthony','Margaret','Mark','Sandra',
           'Donald','Ashley','Steven','Kimberly','Paul','Emily','Andrew','Donna','Joshua','Michelle',
           'Kenneth','Carol','Kevin','Amanda','Brian','Dorothy','George','Melissa','Timothy','Deborah'])[floor(random() * 50 + 1)::int],
    (ARRAY['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez',
           'Hernandez','Lopez','Gonzalez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin',
           'Lee','Perez','Thompson','White','Harris','Sanchez','Clark','Ramirez','Lewis','Robinson',
           'Walker','Young','Allen','King','Wright','Scott','Torres','Nguyen','Hill','Flores',
           'Green','Adams','Nelson','Baker','Hall','Rivera','Campbell','Mitchell','Carter','Roberts'])[floor(random() * 50 + 1)::int],
    'user' || gs.id || '_' || floor(random() * 10000)::int || '@example.com',
    (ARRAY['Enterprise','SMB','SMB','Consumer','Consumer'])[floor(random() * 5 + 1)::int],
    (ARRAY['North America','Europe','Asia Pacific','Latin America','Middle East'])[floor(random() * 5 + 1)::int],
    NOW() - (random() * INTERVAL '730 days')
FROM generate_series(1, 200) AS gs(id);

-- ---- Products (50 rows) ----
INSERT INTO products (name, category, price, is_active, created_at)
VALUES
    ('Cloud Analytics Pro', 'SaaS Tools', 299.99, true, NOW() - INTERVAL '400 days'),
    ('Data Pipeline Starter', 'SaaS Tools', 49.99, true, NOW() - INTERVAL '380 days'),
    ('API Gateway Enterprise', 'SaaS Tools', 599.99, true, NOW() - INTERVAL '360 days'),
    ('Monitoring Dashboard', 'SaaS Tools', 149.99, true, NOW() - INTERVAL '340 days'),
    ('CI/CD Platform Basic', 'SaaS Tools', 79.99, true, NOW() - INTERVAL '320 days'),
    ('CI/CD Platform Pro', 'SaaS Tools', 199.99, true, NOW() - INTERVAL '300 days'),
    ('Log Aggregator', 'SaaS Tools', 129.99, true, NOW() - INTERVAL '280 days'),
    ('Security Scanner', 'SaaS Tools', 249.99, true, NOW() - INTERVAL '260 days'),
    ('Load Balancer Pro', 'SaaS Tools', 179.99, true, NOW() - INTERVAL '240 days'),
    ('Database Optimizer', 'SaaS Tools', 349.99, false, NOW() - INTERVAL '220 days'),
    ('Server Rack 42U', 'Hardware', 2499.99, true, NOW() - INTERVAL '500 days'),
    ('Network Switch 48-Port', 'Hardware', 1299.99, true, NOW() - INTERVAL '480 days'),
    ('SSD Storage Array 10TB', 'Hardware', 3999.99, true, NOW() - INTERVAL '460 days'),
    ('UPS Battery 3000VA', 'Hardware', 899.99, true, NOW() - INTERVAL '440 days'),
    ('Firewall Appliance', 'Hardware', 1799.99, true, NOW() - INTERVAL '420 days'),
    ('GPU Compute Node', 'Hardware', 4999.99, true, NOW() - INTERVAL '400 days'),
    ('Wireless Access Point', 'Hardware', 349.99, true, NOW() - INTERVAL '380 days'),
    ('KVM Switch 16-Port', 'Hardware', 599.99, false, NOW() - INTERVAL '360 days'),
    ('Patch Panel 24-Port', 'Hardware', 89.99, true, NOW() - INTERVAL '340 days'),
    ('Cable Management Kit', 'Hardware', 49.99, true, NOW() - INTERVAL '320 days'),
    ('Cloud Migration Assessment', 'Services', 4999.00, true, NOW() - INTERVAL '300 days'),
    ('Security Audit Package', 'Services', 7500.00, true, NOW() - INTERVAL '280 days'),
    ('Database Optimization Review', 'Services', 3500.00, true, NOW() - INTERVAL '260 days'),
    ('Architecture Consulting (10h)', 'Services', 2500.00, true, NOW() - INTERVAL '240 days'),
    ('DevOps Setup Package', 'Services', 5000.00, true, NOW() - INTERVAL '220 days'),
    ('Training Workshop (1 day)', 'Services', 1500.00, true, NOW() - INTERVAL '200 days'),
    ('Incident Response Retainer', 'Services', 8000.00, true, NOW() - INTERVAL '180 days'),
    ('Compliance Review (SOC2)', 'Services', 6000.00, true, NOW() - INTERVAL '160 days'),
    ('Performance Tuning Session', 'Services', 2000.00, true, NOW() - INTERVAL '140 days'),
    ('Custom Integration Build', 'Services', 10000.00, true, NOW() - INTERVAL '120 days'),
    ('USB-C Hub 7-Port', 'Accessories', 79.99, true, NOW() - INTERVAL '300 days'),
    ('Ethernet Cable Cat6a (50ft)', 'Accessories', 24.99, true, NOW() - INTERVAL '280 days'),
    ('Monitor Stand Dual', 'Accessories', 149.99, true, NOW() - INTERVAL '260 days'),
    ('Webcam 4K Pro', 'Accessories', 199.99, true, NOW() - INTERVAL '240 days'),
    ('Mechanical Keyboard', 'Accessories', 129.99, true, NOW() - INTERVAL '220 days'),
    ('Noise-Cancelling Headset', 'Accessories', 249.99, true, NOW() - INTERVAL '200 days'),
    ('Laptop Docking Station', 'Accessories', 299.99, true, NOW() - INTERVAL '180 days'),
    ('Wireless Mouse Pro', 'Accessories', 69.99, true, NOW() - INTERVAL '160 days'),
    ('Cable Organizer Set', 'Accessories', 19.99, true, NOW() - INTERVAL '140 days'),
    ('Screen Privacy Filter', 'Accessories', 39.99, true, NOW() - INTERVAL '120 days'),
    ('CTO Advisory (Monthly)', 'Consulting', 15000.00, true, NOW() - INTERVAL '200 days'),
    ('Data Strategy Workshop', 'Consulting', 8000.00, true, NOW() - INTERVAL '180 days'),
    ('AI/ML Readiness Assessment', 'Consulting', 12000.00, true, NOW() - INTERVAL '160 days'),
    ('Cloud Cost Optimization', 'Consulting', 6000.00, true, NOW() - INTERVAL '140 days'),
    ('Tech Due Diligence', 'Consulting', 20000.00, true, NOW() - INTERVAL '120 days'),
    ('Platform Engineering Review', 'Consulting', 9000.00, true, NOW() - INTERVAL '100 days'),
    ('Vendor Selection Support', 'Consulting', 5000.00, true, NOW() - INTERVAL '80 days'),
    ('Disaster Recovery Planning', 'Consulting', 7000.00, true, NOW() - INTERVAL '60 days'),
    ('API Strategy Consulting', 'Consulting', 8500.00, true, NOW() - INTERVAL '40 days'),
    ('Org Design for Engineering', 'Consulting', 11000.00, true, NOW() - INTERVAL '20 days');

-- ---- Orders (400 rows) ----
INSERT INTO orders (customer_id, order_date, status, total_amount, channel)
SELECT
    floor(random() * 200 + 1)::int,
    (NOW() - (random() * INTERVAL '540 days'))::date,
    (ARRAY['delivered','delivered','delivered','delivered','delivered','delivered','delivered',
           'shipped','shipped','pending','cancelled','refunded'])[floor(random() * 12 + 1)::int],
    round((random() * 5000 + 50)::numeric, 2),
    (ARRAY['web','web','web','mobile','mobile','in-store','api'])[floor(random() * 7 + 1)::int]
FROM generate_series(1, 400);

-- ---- Order Items (~800 rows, 1-3 per order) ----
INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount)
SELECT
    o.id,
    floor(random() * 50 + 1)::int,
    floor(random() * 5 + 1)::int,
    round((random() * 500 + 10)::numeric, 2),
    round((random() * 20)::numeric, 2)
FROM orders o
CROSS JOIN generate_series(1, 2);

-- Add a third item for ~40% of orders
INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount)
SELECT
    o.id,
    floor(random() * 50 + 1)::int,
    floor(random() * 3 + 1)::int,
    round((random() * 300 + 10)::numeric, 2),
    round((random() * 15)::numeric, 2)
FROM orders o
WHERE random() < 0.4;

-- ---- Subscriptions (150 rows) ----
INSERT INTO subscriptions (customer_id, plan_name, monthly_price, status, start_date, end_date, mrr)
SELECT
    floor(random() * 200 + 1)::int,
    plan_info.name,
    plan_info.price,
    (ARRAY['active','active','active','active','active','active',
           'active','churned','trial','paused'])[floor(random() * 10 + 1)::int],
    (NOW() - (random() * INTERVAL '365 days'))::date,
    CASE WHEN random() < 0.15 THEN (NOW() - (random() * INTERVAL '60 days'))::date ELSE NULL END,
    plan_info.price
FROM generate_series(1, 150) gs(id)
CROSS JOIN LATERAL (
    SELECT * FROM (VALUES
        ('Free Trial', 0.00),
        ('Starter', 29.00),
        ('Starter', 29.00),
        ('Professional', 99.00),
        ('Professional', 99.00),
        ('Professional', 99.00),
        ('Enterprise', 299.00),
        ('Enterprise', 299.00)
    ) AS plans(name, price)
    ORDER BY random()
    LIMIT 1
) plan_info;

-- ---- Support Tickets (100 rows) ----
INSERT INTO support_tickets (customer_id, subject, priority, status, created_at, resolved_at)
SELECT
    floor(random() * 200 + 1)::int,
    (ARRAY[
        'Cannot access dashboard', 'Billing discrepancy', 'API rate limit exceeded',
        'Integration not working', 'Data export failed', 'Account locked out',
        'Slow query performance', 'Missing invoice', 'Feature request: bulk import',
        'SSL certificate issue', 'Webhook delivery failing', 'Password reset not working',
        'Custom report not loading', 'Mobile app crash', 'Permission denied error',
        'Subscription upgrade issue', 'Data sync delay', 'SAML SSO configuration',
        'Audit log not available', 'Backup restoration needed'
    ])[floor(random() * 20 + 1)::int],
    (ARRAY['low','medium','medium','medium','high','high','critical'])[floor(random() * 7 + 1)::int],
    (ARRAY['open','open','in_progress','in_progress','resolved','resolved','resolved','closed','closed'])[floor(random() * 9 + 1)::int],
    NOW() - (random() * INTERVAL '180 days'),
    CASE WHEN random() < 0.65 THEN NOW() - (random() * INTERVAL '90 days') ELSE NULL END
FROM generate_series(1, 100);

-- ---- Customer PII (50 rows — for guardrail testing) ----
INSERT INTO customer_pii (customer_id, ssn, credit_card, date_of_birth)
SELECT
    gs.id,
    lpad(floor(random() * 999)::text, 3, '0') || '-' ||
    lpad(floor(random() * 99)::text, 2, '0') || '-' ||
    lpad(floor(random() * 9999)::text, 4, '0'),
    lpad(floor(random() * 9999)::text, 4, '0') || '-' ||
    lpad(floor(random() * 9999)::text, 4, '0') || '-' ||
    lpad(floor(random() * 9999)::text, 4, '0') || '-' ||
    lpad(floor(random() * 9999)::text, 4, '0'),
    '1970-01-01'::date + (random() * 15000)::int
FROM generate_series(1, 50) AS gs(id);

-- Update order totals to match items
UPDATE orders o SET total_amount = sub.total
FROM (
    SELECT order_id, SUM(quantity * unit_price * (1 - discount / 100)) AS total
    FROM order_items
    GROUP BY order_id
) sub
WHERE o.id = sub.order_id;
