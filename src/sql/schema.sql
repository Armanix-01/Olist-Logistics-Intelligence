CREATE TABLE customers(
customer_id TEXT PRIMARY KEY,
customer_unique_id TEXT,
customer_zip_code_prefix INTEGER,
customer_city TEXT,
customer_state CHAR(2)
); 

CREATE TABLE geolocation (

    geolocation_zip_code_prefix INTEGER,

    geolocation_lat DOUBLE PRECISION,

    geolocation_lng DOUBLE PRECISION,

    geolocation_city TEXT,

    geolocation_state CHAR(2)

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

    order_id TEXT,

    order_item_id INTEGER,

    product_id TEXT,

    seller_id TEXT,

    shipping_limit_date TIMESTAMP,

    price NUMERIC(10,2),

    freight_value NUMERIC(10,2),

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

    order_id TEXT,

    payment_sequential INTEGER,

    payment_type TEXT,

    payment_installments INTEGER,

    payment_value NUMERIC(10,2),

    PRIMARY KEY (order_id, payment_sequential),

    CONSTRAINT fk_order_payments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)

);
CREATE TABLE order_reviews (

    review_id TEXT PRIMARY KEY,

    order_id TEXT,

    review_score INTEGER,

    review_comment_title TEXT,

    review_comment_message TEXT,

    review_creation_date TIMESTAMP,

    review_answer_timestamp TIMESTAMP,

    CONSTRAINT fk_reviews_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)

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
    CONSTRAINT fk_products_category
    FOREIGN KEY (product_category_name)
    REFERENCES category_name_translation(product_category_name)

);
CREATE TABLE sellers (

    seller_id TEXT PRIMARY KEY,

    seller_zip_code_prefix INTEGER,

    seller_city TEXT,

    seller_state CHAR(2)

);
CREATE TABLE category_name_translation (

    product_category_name TEXT PRIMARY KEY,

    product_category_name_english TEXT

);