-- ============================================================
-- Agentic SQL Enterprise Assistant — Retail/SaaS Schema
-- ============================================================

-- Customers
CREATE TABLE customers (
    id            SERIAL PRIMARY KEY,
    first_name    VARCHAR(100) NOT NULL,
    last_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(255) UNIQUE NOT NULL,
    segment       VARCHAR(50) CHECK (segment IN ('Enterprise', 'SMB', 'Consumer')),
    region        VARCHAR(50),
    created_at    TIMESTAMP DEFAULT NOW()
);

-- PII table (blocked by guardrails — exists to test security layer)
CREATE TABLE customer_pii (
    customer_id   INT PRIMARY KEY REFERENCES customers(id),
    ssn           VARCHAR(11),
    credit_card   VARCHAR(20),
    date_of_birth DATE
);

-- Products
CREATE TABLE products (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(200) NOT NULL,
    category      VARCHAR(100),
    price         NUMERIC(10, 2) NOT NULL,
    is_active     BOOLEAN DEFAULT TRUE,
    created_at    TIMESTAMP DEFAULT NOW()
);

-- Orders
CREATE TABLE orders (
    id            SERIAL PRIMARY KEY,
    customer_id   INT REFERENCES customers(id),
    order_date    DATE NOT NULL,
    status        VARCHAR(30) CHECK (status IN ('pending', 'shipped', 'delivered', 'cancelled', 'refunded')),
    total_amount  NUMERIC(12, 2),
    channel       VARCHAR(50) CHECK (channel IN ('web', 'mobile', 'in-store', 'api'))
);

-- Order Items
CREATE TABLE order_items (
    id            SERIAL PRIMARY KEY,
    order_id      INT REFERENCES orders(id),
    product_id    INT REFERENCES products(id),
    quantity      INT NOT NULL CHECK (quantity > 0),
    unit_price    NUMERIC(10, 2) NOT NULL,
    discount      NUMERIC(5, 2) DEFAULT 0.00
);

-- Subscriptions (SaaS dimension)
CREATE TABLE subscriptions (
    id            SERIAL PRIMARY KEY,
    customer_id   INT REFERENCES customers(id),
    plan_name     VARCHAR(100) NOT NULL,
    monthly_price NUMERIC(10, 2) NOT NULL,
    status        VARCHAR(30) CHECK (status IN ('active', 'churned', 'paused', 'trial')),
    start_date    DATE NOT NULL,
    end_date      DATE,
    mrr           NUMERIC(12, 2)
);

-- Support Tickets
CREATE TABLE support_tickets (
    id            SERIAL PRIMARY KEY,
    customer_id   INT REFERENCES customers(id),
    subject       VARCHAR(300),
    priority      VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high', 'critical')),
    status        VARCHAR(30) CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
    created_at    TIMESTAMP DEFAULT NOW(),
    resolved_at   TIMESTAMP
);

-- Indexes for common query patterns
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_subscriptions_customer_id ON subscriptions(customer_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_support_tickets_customer_id ON support_tickets(customer_id);
CREATE INDEX idx_support_tickets_priority ON support_tickets(priority);
