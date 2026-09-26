
DROP TABLE IF EXISTS order_payments CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS sellers CASCADE;
DROP TABLE IF EXISTS customers CASCADE;



CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    customer_unique_id TEXT,
    customer_zip_code_prefix INTEGER,
    customer_city TEXT,
    customer_state CHAR(2)
);



CREATE TABLE sellers (
    seller_id TEXT PRIMARY KEY,
    seller_zip_code_prefix INTEGER,
    seller_city TEXT,
    seller_state CHAR(2)
);


CREATE TABLE products (
    product_id TEXT PRIMARY KEY,

    product_category_name TEXT,

    product_name_length INTEGER,

    product_description_length INTEGER,

    product_photos_qty INTEGER,

    product_weight_g INTEGER,

    product_length_cm DOUBLE PRECISION,

    product_height_cm DOUBLE PRECISION,

    product_width_cm DOUBLE PRECISION
);



CREATE TABLE orders (
    order_id TEXT PRIMARY KEY,

    customer_id TEXT NOT NULL,

    order_status TEXT NOT NULL,

    order_purchase_timestamp TIMESTAMP NOT NULL,

    order_approved_at TIMESTAMP,

    order_delivered_carrier_date TIMESTAMP,

    order_delivered_customer_date TIMESTAMP,

    order_estimated_delivery_date TIMESTAMP,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);



CREATE TABLE order_items (
    order_id TEXT NOT NULL,

    order_item_id INTEGER NOT NULL,

    product_id TEXT,

    seller_id TEXT,

    shipping_limit_date TIMESTAMP,

    price NUMERIC(10, 2),

    freight_value NUMERIC(10, 2),

    PRIMARY KEY (order_id, order_item_id),

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT fk_order_items_seller
        FOREIGN KEY (seller_id)
        REFERENCES sellers(seller_id)
);



CREATE TABLE order_payments (
    order_id TEXT NOT NULL,

    payment_sequential INTEGER NOT NULL,

    payment_type TEXT,

    payment_installments INTEGER,

    payment_value NUMERIC(10, 2),

    PRIMARY KEY (order_id, payment_sequential),

    CONSTRAINT fk_order_payments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);




CREATE INDEX idx_orders_customer_id
    ON orders(customer_id);

CREATE INDEX idx_orders_purchase_timestamp
    ON orders(order_purchase_timestamp);



CREATE INDEX idx_order_items_product_id
    ON order_items(product_id);

CREATE INDEX idx_order_items_seller_id
    ON order_items(seller_id);


CREATE INDEX idx_order_payments_order_id
    ON order_payments(order_id);



CREATE INDEX idx_customers_unique_id
    ON customers(customer_unique_id);



CREATE INDEX idx_products_category
    ON products(product_category_name);



CREATE INDEX idx_sellers_state
    ON sellers(seller_state);

