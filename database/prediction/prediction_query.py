from sqlalchemy import text

from database.connection import engine


def get_prediction_data(order_id: str):

    query = text("""
        WITH item_features AS (

            SELECT
                oi.order_id,

                COUNT(*) AS number_of_items,

                COUNT(DISTINCT oi.product_id)
                    AS number_of_products,

                COUNT(DISTINCT oi.seller_id)
                    AS number_of_sellers,

                SUM(oi.price)
                    AS total_price,

                SUM(oi.freight_value)
                    AS total_freight

            FROM order_items oi

            WHERE oi.order_id = :order_id

            GROUP BY oi.order_id
        ),


        product_features AS (

            SELECT
                oi.order_id,

                SUM(p.product_weight_g)
                    AS total_product_weight,

                SUM(
                    p.product_length_cm
                    * p.product_height_cm
                    * p.product_width_cm
                ) AS total_product_volume,

                MIN(p.product_category_name)
                    AS product_category_name

            FROM order_items oi

            JOIN products p
                ON oi.product_id = p.product_id

            WHERE oi.order_id = :order_id

            GROUP BY oi.order_id
        ),


        payment_features AS (

            SELECT
                op.order_id,

                SUM(op.payment_value)
                    AS total_payment_value,

                MAX(op.payment_installments)
                    AS max_payment_installments,

                COUNT(*)
                    AS number_of_payments,

                MIN(op.payment_type)
                    AS payment_type

            FROM order_payments op

            WHERE op.order_id = :order_id

            GROUP BY op.order_id
        ),


        seller_features AS (

            SELECT
                oi.order_id,

                MIN(s.seller_state)
                    AS seller_state

            FROM order_items oi

            JOIN sellers s
                ON oi.seller_id = s.seller_id

            WHERE oi.order_id = :order_id

            GROUP BY oi.order_id
        )


        SELECT

            -- Order information
            o.order_id,
            o.order_purchase_timestamp,
            o.order_approved_at,
            o.order_estimated_delivery_date,

            -- Customer
            c.customer_state,

            -- Seller
            sf.seller_state,

            -- Payment
            pf.payment_type,
            pf.total_payment_value,
            pf.max_payment_installments,
            pf.number_of_payments,

            -- Items
            i.number_of_items,
            i.number_of_products,
            i.number_of_sellers,
            i.total_price,
            i.total_freight,

            -- Products
            prf.total_product_weight,
            prf.total_product_volume,
            prf.product_category_name

        FROM orders o

        JOIN customers c
            ON o.customer_id = c.customer_id

        LEFT JOIN item_features i
            ON o.order_id = i.order_id

        LEFT JOIN product_features prf
            ON o.order_id = prf.order_id

        LEFT JOIN payment_features pf
            ON o.order_id = pf.order_id

        LEFT JOIN seller_features sf
            ON o.order_id = sf.order_id

        WHERE o.order_id = :order_id
    """)

    with engine.connect() as connection:

        result = connection.execute(
            query,
            {"order_id": order_id}
        )

        row = result.mappings().first()

    return dict(row) if row else None

