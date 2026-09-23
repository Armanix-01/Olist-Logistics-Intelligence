WITH item_summary AS (

    SELECT
        oi.order_id,

        -- Item information
        COUNT(*) AS number_of_items,
        COUNT(DISTINCT oi.product_id) AS number_of_products,
        COUNT(DISTINCT oi.seller_id) AS number_of_sellers,

        -- Financial information
        SUM(oi.price) AS total_price,
        SUM(oi.freight_value) AS total_freight,

        -- Product information
        SUM(p.product_weight_g) AS total_product_weight,

        SUM(
            p.product_length_cm
            * p.product_height_cm
            * p.product_width_cm
        ) AS total_product_volume,

        -- Category information
        MODE() WITHIN GROUP (
            ORDER BY p.product_category_name
        ) AS product_category_name,

        -- Seller information
        MODE() WITHIN GROUP (
            ORDER BY s.seller_state
        ) AS seller_state,

        MODE() WITHIN GROUP (
            ORDER BY s.seller_city
        ) AS seller_city

    FROM order_items oi

    LEFT JOIN products p
        ON oi.product_id = p.product_id

    LEFT JOIN sellers s
        ON oi.seller_id = s.seller_id

    GROUP BY oi.order_id
),

payment_summary AS (

    SELECT
        op.order_id,

        SUM(op.payment_value) AS total_payment_value,

        MAX(op.payment_installments) AS max_payment_installments,

        COUNT(*) AS number_of_payments,

        MODE() WITHIN GROUP (
            ORDER BY op.payment_type
        ) AS payment_type

    FROM order_payments op

    GROUP BY op.order_id
),

review_summary AS (

    SELECT
        r.order_id,

        AVG(r.review_score) AS average_review_score

    FROM order_reviews r

    GROUP BY r.order_id
)

SELECT

    -- Order identifiers
    o.order_id,
    o.customer_id,

    -- Customer information
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,

    -- Order timestamps
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    -- Item summary
    i.number_of_items,
    i.number_of_products,
    i.number_of_sellers,

    i.total_price,
    i.total_freight,

    i.total_product_weight,
    i.total_product_volume,

    i.product_category_name,

    -- Seller summary
    i.seller_city,
    i.seller_state,

    -- Payment summary
    p.total_payment_value,
    p.max_payment_installments,
    p.number_of_payments,
    p.payment_type,

    -- Review information
    r.average_review_score,

    -- Target
    CASE
        WHEN o.order_delivered_customer_date >
             o.order_estimated_delivery_date
        THEN 1
        ELSE 0
    END AS is_late

FROM orders o

JOIN customers c
    ON o.customer_id = c.customer_id

JOIN item_summary i
    ON o.order_id = i.order_id

LEFT JOIN payment_summary p
    ON o.order_id = p.order_id

LEFT JOIN review_summary r
    ON o.order_id = r.order_id

WHERE
    o.order_status = 'delivered'
    AND o.order_delivered_customer_date IS NOT NULL
    AND o.order_estimated_delivery_date IS NOT NULL;