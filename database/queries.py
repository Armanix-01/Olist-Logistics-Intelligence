
from sqlalchemy import text
import os
from database.connection import CloudDb
from dotenv import load_dotenv



url = os.getenv("CLOUD_DB_URL")
engine = CloudDb(url=url).engine
# ============================================================
# ORDER QUERIES
# ============================================================

def get_order_details(order_id: str):
    """
    Get basic details of a specific order.
    """

    query = text("""
        SELECT
            o.order_id,
            o.customer_id,
            o.order_status,
            o.order_purchase_timestamp,
            o.order_approved_at,
            o.order_delivered_carrier_date,
            o.order_delivered_customer_date,
            o.order_estimated_delivery_date
        FROM orders AS o
        WHERE o.order_id = :order_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"order_id": order_id}
        )

        row = result.mappings().first()

    return dict(row) if row else None


def get_order_items(order_id: str):
    """
    Get all products/items contained in an order.
    """

    query = text("""
        SELECT
            oi.order_id,
            oi.order_item_id,
            oi.product_id,
            oi.seller_id,
            oi.shipping_limit_date,
            oi.price,
            oi.freight_value
        FROM order_items AS oi
        WHERE oi.order_id = :order_id
        ORDER BY oi.order_item_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"order_id": order_id}
        )

        rows = result.mappings().all()

    return [dict(row) for row in rows]


def get_order_payments(order_id: str):
    """
    Get all payment information for an order.
    """

    query = text("""
        SELECT
            order_id,
            payment_sequential,
            payment_type,
            payment_installments,
            payment_value
        FROM order_payments
        WHERE order_id = :order_id
        ORDER BY payment_sequential
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"order_id": order_id}
        )

        rows = result.mappings().all()

    return [dict(row) for row in rows]


def get_complete_order_details(order_id: str):
    """
    Get order information together with customer,
    products, sellers and payment information.
    """

    query = text("""
        SELECT
            o.order_id,
            o.order_status,

            o.order_purchase_timestamp,
            o.order_approved_at,
            o.order_delivered_carrier_date,
            o.order_delivered_customer_date,
            o.order_estimated_delivery_date,

            c.customer_id,
            c.customer_unique_id,
            c.customer_city,
            c.customer_state,

            oi.order_item_id,
            oi.product_id,
            oi.seller_id,
            oi.price,
            oi.freight_value,

            p.product_category_name,
            p.product_weight_g,

            s.seller_city,
            s.seller_state

        FROM orders AS o

        LEFT JOIN customers AS c
            ON o.customer_id = c.customer_id

        LEFT JOIN order_items AS oi
            ON o.order_id = oi.order_id

        LEFT JOIN products AS p
            ON oi.product_id = p.product_id

        LEFT JOIN sellers AS s
            ON oi.seller_id = s.seller_id

        WHERE o.order_id = :order_id

        ORDER BY oi.order_item_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"order_id": order_id}
        )

        rows = result.mappings().all()

    return [dict(row) for row in rows]


# ============================================================
# CUSTOMER QUERIES
# ============================================================

def get_customer_details(customer_id: str):
    """
    Get customer information.
    """

    query = text("""
        SELECT
            customer_id,
            customer_unique_id,
            customer_zip_code_prefix,
            customer_city,
            customer_state
        FROM customers
        WHERE customer_id = :customer_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"customer_id": customer_id}
        )

        row = result.mappings().first()

    return dict(row) if row else None


def get_customer_orders(customer_id: str):
    """
    Get all orders belonging to a customer.
    """

    query = text("""
        SELECT
            order_id,
            order_status,
            order_purchase_timestamp,
            order_approved_at,
            order_delivered_customer_date,
            order_estimated_delivery_date
        FROM orders
        WHERE customer_id = :customer_id
        ORDER BY order_purchase_timestamp DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"customer_id": customer_id}
        )

        rows = result.mappings().all()

    return [dict(row) for row in rows]


def get_customer_order_count(customer_id: str):
    """
    Get the number of orders placed by a customer.
    """

    query = text("""
        SELECT
            COUNT(*) AS order_count
        FROM orders
        WHERE customer_id = :customer_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"customer_id": customer_id}
        )

        row = result.mappings().first()

    return dict(row) if row else None


# ============================================================
# SELLER QUERIES
# ============================================================

def get_seller_details(seller_id: str):
    """
    Get seller information.
    """

    query = text("""
        SELECT
            seller_id,
            seller_zip_code_prefix,
            seller_city,
            seller_state
        FROM sellers
        WHERE seller_id = :seller_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"seller_id": seller_id}
        )

        row = result.mappings().first()

    return dict(row) if row else None


def get_seller_orders(seller_id: str):
    """
    Get orders associated with a seller.
    """

    query = text("""
        SELECT DISTINCT
            o.order_id,
            o.order_status,
            o.order_purchase_timestamp,
            o.order_delivered_customer_date,
            o.order_estimated_delivery_date
        FROM orders AS o

        INNER JOIN order_items AS oi
            ON o.order_id = oi.order_id

        WHERE oi.seller_id = :seller_id

        ORDER BY o.order_purchase_timestamp DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"seller_id": seller_id}
        )

        rows = result.mappings().all()

    return [dict(row) for row in rows]


def get_seller_statistics(seller_id: str):
    """
    Get basic sales statistics for a seller.
    """

    query = text("""
        SELECT
            oi.seller_id,

            COUNT(DISTINCT oi.order_id) AS total_orders,

            COUNT(*) AS total_items,

            COALESCE(SUM(oi.price), 0) AS total_product_sales,

            COALESCE(SUM(oi.freight_value), 0) AS total_freight,

            COALESCE(
                SUM(oi.price + oi.freight_value),
                0
            ) AS total_sales

        FROM order_items AS oi

        WHERE oi.seller_id = :seller_id

        GROUP BY oi.seller_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"seller_id": seller_id}
        )

        row = result.mappings().first()

    return dict(row) if row else None


# ============================================================
# PRODUCT QUERIES
# ============================================================

def get_product_details(product_id: str):
    """
    Get product information.
    """

    query = text("""
        SELECT
            p.product_id,
            p.product_category_name,
            p.product_name_length,
            p.product_description_length,
            p.product_photos_qty,
            p.product_weight_g,
            p.product_length_cm,
            p.product_height_cm,
            p.product_width_cm
        FROM products AS p
        WHERE p.product_id = :product_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"product_id": product_id}
        )

        row = result.mappings().first()

    return dict(row) if row else None


def get_product_sales(product_id: str):
    """
    Get sales information for a product.
    """

    query = text("""
        SELECT
            oi.product_id,

            COUNT(DISTINCT oi.order_id) AS total_orders,

            COUNT(*) AS total_items,

            COALESCE(SUM(oi.price), 0) AS total_sales,

            COALESCE(SUM(oi.freight_value), 0) AS total_freight

        FROM order_items AS oi

        WHERE oi.product_id = :product_id

        GROUP BY oi.product_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"product_id": product_id}
        )

        row = result.mappings().first()

    return dict(row) if row else None


# ============================================================
# PAYMENT QUERIES
# ============================================================

def get_payment_summary(order_id: str):
    """
    Get total payment information for an order.
    """

    query = text("""
        SELECT
            order_id,

            COUNT(*) AS number_of_payments,

            COALESCE(SUM(payment_value), 0)
                AS total_payment_value,

            MAX(payment_installments)
                AS max_payment_installments

        FROM order_payments

        WHERE order_id = :order_id

        GROUP BY order_id
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"order_id": order_id}
        )

        row = result.mappings().first()

    return dict(row) if row else None


# ============================================================
# GENERAL ANALYTICS
# ============================================================

def get_order_status_summary():
    """
    Get number of orders by order status.
    """

    query = text("""
        SELECT
            order_status,
            COUNT(*) AS order_count
        FROM orders
        GROUP BY order_status
        ORDER BY order_count DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        rows = result.mappings().all()

    return [dict(row) for row in rows]


def get_sales_by_seller(limit: int = 10):
    """
    Get top sellers by total sales.
    """

    query = text("""
        SELECT
            oi.seller_id,

            COUNT(DISTINCT oi.order_id)
                AS total_orders,

            SUM(oi.price)
                AS total_product_sales,

            SUM(oi.freight_value)
                AS total_freight,

            SUM(oi.price + oi.freight_value)
                AS total_sales

        FROM order_items AS oi

        GROUP BY oi.seller_id

        ORDER BY total_sales DESC

        LIMIT :limit
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"limit": limit}
        )

        rows = result.mappings().all()

    return [dict(row) for row in rows]


def get_sales_by_category(limit: int = 10):
    """
    Get product categories ranked by total sales.
    """

    query = text("""
        SELECT
            p.product_category_name,

            COUNT(DISTINCT oi.order_id)
                AS total_orders,

            COUNT(*) AS total_items,

            SUM(oi.price)
                AS total_product_sales,

            SUM(oi.price + oi.freight_value)
                AS total_sales

        FROM order_items AS oi

        INNER JOIN products AS p
            ON oi.product_id = p.product_id

        GROUP BY p.product_category_name

        ORDER BY total_sales DESC

        LIMIT :limit
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"limit": limit}
        )

        rows = result.mappings().all()

    return [dict(row) for row in rows]


def get_sales_by_state():
    """
    Get total sales by customer state.
    """

    query = text("""
        SELECT
            c.customer_state,

            COUNT(DISTINCT o.order_id)
                AS total_orders,

            SUM(oi.price)
                AS total_product_sales,

            SUM(oi.price + oi.freight_value)
                AS total_sales

        FROM orders AS o

        INNER JOIN customers AS c
            ON o.customer_id = c.customer_id

        INNER JOIN order_items AS oi
            ON o.order_id = oi.order_id

        GROUP BY c.customer_state

        ORDER BY total_sales DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        rows = result.mappings().all()

    return [dict(row) for row in rows]


def get_monthly_sales():
    """
    Get total sales grouped by month.
    """

    query = text("""
        SELECT
            DATE_TRUNC(
                'month',
                o.order_purchase_timestamp
            ) AS month,

            COUNT(DISTINCT o.order_id)
                AS total_orders,

            SUM(oi.price)
                AS total_product_sales,

            SUM(oi.price + oi.freight_value)
                AS total_sales

        FROM orders AS o

        INNER JOIN order_items AS oi
            ON o.order_id = oi.order_id

        GROUP BY month

        ORDER BY month
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        rows = result.mappings().all()

    return [dict(row) for row in rows]


# ============================================================
# DELIVERY ANALYTICS
# ============================================================

def get_delivery_statistics():
    """
    Get basic delivery statistics for delivered orders.
    """

    query = text("""
        SELECT

            COUNT(*) AS delivered_orders,

            AVG(
                EXTRACT(
                    EPOCH FROM (
                        order_delivered_customer_date
                        - order_purchase_timestamp
                    )
                ) / 86400
            ) AS average_delivery_days

        FROM orders

        WHERE
            order_delivered_customer_date IS NOT NULL
            AND order_purchase_timestamp IS NOT NULL
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        row = result.mappings().first()

    return dict(row) if row else None


def get_late_delivery_statistics():
    """
    Compare estimated delivery date with actual delivery date.
    """

    query = text("""
        SELECT

            COUNT(*) AS delivered_orders,

            COUNT(*) FILTER (
                WHERE order_delivered_customer_date
                      > order_estimated_delivery_date
            ) AS late_orders,

            COUNT(*) FILTER (
                WHERE order_delivered_customer_date
                      <= order_estimated_delivery_date
            ) AS on_time_orders

        FROM orders

        WHERE
            order_delivered_customer_date IS NOT NULL
            AND order_estimated_delivery_date IS NOT NULL
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        row = result.mappings().first()

    return dict(row) if row else None



