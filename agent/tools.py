from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from database.prediction.prediction_service import prediction

from database.queries import (
    # Order
    get_order_details,
    get_order_items,
    get_order_payments,
    get_complete_order_details,

    # Customer
    get_customer_details,
    get_customer_orders,
    get_customer_order_count,

    # Seller
    get_seller_details,
    get_seller_orders,
    get_seller_statistics,

    # Product
    get_product_details,
    get_product_sales,

    # Payment
    get_payment_summary,

    # Analytics
    get_order_status_summary,
    get_sales_by_seller,
    get_sales_by_category,
    get_sales_by_state,
    get_monthly_sales,

    # Delivery
    get_delivery_statistics,
    get_late_delivery_statistics,
)
@tool
def order_details(order_id: str):
    """
    Get the basic details of a specific order.

    Use this when the user asks about the status,
    purchase date, approval date, estimated delivery date,
    or actual delivery dates of a particular order.

    Args:
        order_id: The unique ID of the order.

    Returns:
        Basic order information.
    """
    return get_order_details(order_id)

@tool
def order_items(order_id: str):
    """
    Get all products and sellers associated with an order.

    Use this when the user asks what products were included
    in an order, which sellers were involved, or asks about
    item prices and freight charges.

    Args:
        order_id: The unique ID of the order.

    Returns:
        List of order items.
    """
    return get_order_items(order_id)


@tool
def order_payments(order_id: str):
    """
    Get all payment records associated with an order.

    Use this when the user asks about payment method,
    payment amount, installments, or multiple payments
    associated with an order.

    Args:
        order_id: The unique ID of the order.

    Returns:
        List of payment records.
    """
    return get_order_payments(order_id)

@tool
def complete_order_details(order_id: str):
    """
    Get comprehensive information about an order.

    Includes order information, customer information,
    products, sellers, prices, freight, and product
    categories.

    Use this when the user asks for a broad overview
    of a specific order.

    Args:
        order_id: The unique ID of the order.

    Returns:
        Detailed order information.
    """
    return get_complete_order_details(order_id)

@tool
def customer_details(customer_id: str):
    """
    Get information about a customer.

    Includes customer location and customer identifiers.

    Args:
        customer_id: The unique customer ID.

    Returns:
        Customer information.
    """
    return get_customer_details(customer_id)

@tool
def customer_orders(customer_id: str):
    """
    Get the orders associated with a customer.

    Use this when the user asks about a customer's
    order history.

    Args:
        customer_id: The unique customer ID.

    Returns:
        List of customer orders.
    """
    return get_customer_orders(customer_id)

@tool
def customer_order_count(customer_id: str):
    """
    Get the total number of orders placed by a customer.

    Args:
        customer_id: The unique customer ID.

    Returns:
        Number of orders.
    """
    return get_customer_order_count(customer_id)


@tool
def seller_details(seller_id: str):
    """
    Get information about a seller.

    Includes seller location and seller identifiers.

    Args:
        seller_id: The unique seller ID.

    Returns:
        Seller information.
    """
    return get_seller_details(seller_id)

@tool
def seller_orders(seller_id: str):
    """
    Get orders associated with a seller.

    Use this when the user asks about a seller's
    order history.

    Args:
        seller_id: The unique seller ID.

    Returns:
        List of orders associated with the seller.
    """
    return get_seller_orders(seller_id)

@tool
def seller_statistics(seller_id: str):
    """
    Get sales statistics for a seller.

    Includes total orders, total items, product sales,
    freight, and total sales.

    Args:
        seller_id: The unique seller ID.

    Returns:
        Seller sales statistics.
    """
    return get_seller_statistics(seller_id)


@tool
def product_details(product_id: str):
    """
    Get information about a product.

    Includes product category, dimensions, weight,
    description length, name length, and photo count.

    Args:
        product_id: The unique product ID.

    Returns:
        Product information.
    """
    return get_product_details(product_id)

@tool
def product_sales(product_id: str):
    """
    Get sales statistics for a product.

    Includes total orders, total items, sales, and freight.

    Args:
        product_id: The unique product ID.

    Returns:
        Product sales statistics.
    """
    return get_product_sales(product_id)

@tool
def payment_summary(order_id: str):
    """
    Get a summary of payments for an order.

    Includes number of payments, total payment value,
    and maximum number of installments.

    Args:
        order_id: The unique ID of the order.

    Returns:
        Payment summary.
    """
    return get_payment_summary(order_id)

@tool
def order_status_summary():
    """
    Get the number of orders grouped by order status.

    Use this for questions about the overall distribution
    of order statuses.
    
    Returns:
        Order counts grouped by status.
    """
    return get_order_status_summary()

@tool
def sales_by_seller(limit: int = 10):
    """
    Get the top sellers ranked by total sales.

    Use this when the user asks which sellers have the
    highest sales.

    Args:
        limit: Maximum number of sellers to return.

    Returns:
        Top sellers ranked by total sales.
    """
    return get_sales_by_seller(limit)

@tool
def sales_by_category(limit: int = 10):
    """
    Get product categories ranked by total sales.

    Use this when the user asks about the highest-selling
    product categories.

    Args:
        limit: Maximum number of categories to return.

    Returns:
        Categories ranked by total sales.
    """
    return get_sales_by_category(limit)

@tool
def sales_by_state():
    """
    Get total sales grouped by customer state.

    Use this when the user asks about sales across
    different Brazilian states.

    Returns:
        Sales statistics grouped by customer state.
    """
    return get_sales_by_state()

@tool
def monthly_sales():
    """
    Get total sales grouped by month.

    Use this for questions about sales trends over time.

    Returns:
        Monthly sales statistics.
    """
    return get_monthly_sales()

@tool
def delivery_statistics():
    """
    Get overall delivery statistics.

    Includes the number of delivered orders and
    average delivery time in days.

    Returns:
        Overall delivery statistics.
    """
    return get_delivery_statistics()

@tool
def late_delivery_statistics():
    """
    Get statistics comparing estimated delivery dates
    with actual delivery dates.

    Includes total delivered orders, late orders,
    and on-time orders.

    Returns:
        Late and on-time delivery statistics.
    """
    return get_late_delivery_statistics()

@tool
def predict_delivery_delay(order_id: str):
    """
    Predict whether a specific order is likely to be delivered late.

    This uses the trained machine learning model and
    information available for the order at prediction time.

    Use this when the user asks whether an order is likely
    to be late.

    Args:
        order_id: The unique ID of the order.

    Returns:
        Machine learning prediction where:
        1 means predicted late delivery.
        0 means predicted on-time delivery.
    """
    result = prediction(order_id)

    return {
        "order_id": order_id,
        "is_late": result
    }


TOOLS = [
    # Orders
    order_details,
    order_items,
    order_payments,
    complete_order_details,

    # Customers
    customer_details,
    customer_orders,
    customer_order_count,

    # Sellers
    seller_details,
    seller_orders,
    seller_statistics,

    # Products
    product_details,
    product_sales,

    # Payments
    payment_summary,

    # Analytics
    order_status_summary,
    sales_by_seller,
    sales_by_category,
    sales_by_state,
    monthly_sales,

    # Delivery
    delivery_statistics,
    late_delivery_statistics,
]