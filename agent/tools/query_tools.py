from langchain_core.tools import tool

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

from agent.schemas import (
    OrderLookupInput,
    CustomerLookupInput,
    SellerLookupInput,
    ProductLookupInput,
    LimitInput,
)


# ============================================================
# ORDER TOOLS
# ============================================================

@tool(args_schema=OrderLookupInput)
def order_details(order_id: str):
    """
    Retrieve the basic details of ONE specific Olist order.

    USE THIS TOOL WHEN:
    - The user asks about a specific order.
    - The user asks for an order's status.
    - The user asks when an order was purchased or approved.
    - The user asks for the estimated delivery date.
    - The user asks for the actual carrier or customer delivery dates.
    - The user provides an exact Olist order ID.

    DO NOT USE THIS TOOL WHEN:
    - The user asks about all orders.
    - The user asks for a customer's order history.
    - The user asks for an order's products or sellers.
      Use `order_items` instead.
    - The user asks specifically about payments.
      Use `order_payments` or `payment_summary` instead.

    RETURNS:
    Basic information about the specified order, including
    order status and relevant purchase, approval, estimated
    delivery, and actual delivery timestamps.

    ARGUMENT:
    order_id: The exact 32-character hexadecimal Olist order ID.
    """
    return get_order_details(order_id)


@tool(args_schema=OrderLookupInput)
def order_items(order_id: str):
    """
    Retrieve all product items associated with ONE specific order.

    USE THIS TOOL WHEN:
    - The user asks what products were included in an order.
    - The user asks which sellers supplied products in an order.
    - The user asks about product prices within an order.
    - The user asks about freight charges for an order.
    - The user wants the individual order-item records.

    DO NOT USE THIS TOOL WHEN:
    - The user only wants basic order status or dates.
      Use `order_details` instead.
    - The user only wants payment information.
      Use `order_payments` or `payment_summary` instead.
    - The user wants aggregate sales statistics for a seller or product.
      Use the corresponding statistics tool.

    RETURNS:
    The individual products/items belonging to the order,
    including seller information, product information,
    item price, freight value, and related item-level data.

    ARGUMENT:
    order_id: The exact 32-character hexadecimal Olist order ID.
    """
    return get_order_items(order_id)


@tool(args_schema=OrderLookupInput)
def order_payments(order_id: str):
    """
    Retrieve ALL payment records associated with ONE specific order.

    USE THIS TOOL WHEN:
    - The user asks how an order was paid.
    - The user asks about payment methods.
    - The user asks about payment amounts.
    - The user asks about installments.
    - The user asks whether an order had multiple payment records.
    - The user wants the individual payment records.

    DO NOT USE THIS TOOL WHEN:
    - The user only wants a summarized payment result.
      Use `payment_summary` instead.
    - The user asks about products or sellers.
      Use `order_items` instead.

    RETURNS:
    Individual payment records for the order, including payment
    type, payment value, installment count, and related payment data.

    ARGUMENT:
    order_id: The exact 32-character hexadecimal Olist order ID.
    """
    return get_order_payments(order_id)


@tool(args_schema=OrderLookupInput)
def complete_order_details(order_id: str):
    """
    Retrieve comprehensive information about ONE specific Olist order.

    USE THIS TOOL WHEN:
    - The user asks for a complete overview of an order.
    - The user asks multiple questions about the same order.
    - The user wants order, customer, product, seller, price,
      freight, and category information together.
    - The user's question requires information from multiple
      order-related tables.

    DO NOT USE THIS TOOL WHEN:
    - The user only needs one small piece of information and a
      specialized tool can answer it directly.

    RETURNS:
    A comprehensive view combining order information with
    customer, product, seller, pricing, freight, and category
    information.

    ARGUMENT:
    order_id: The exact 32-character hexadecimal Olist order ID.
    """
    return get_complete_order_details(order_id)


# ============================================================
# CUSTOMER TOOLS
# ============================================================

@tool(args_schema=CustomerLookupInput)
def customer_details(customer_id: str):
    """
    Retrieve profile and location information for ONE Olist customer.

    USE THIS TOOL WHEN:
    - The user asks where a customer is located.
    - The user asks for customer identifiers or basic customer information.
    - The user provides an exact customer ID.

    DO NOT USE THIS TOOL WHEN:
    - The user asks about the customer's orders.
      Use `customer_orders`.
    - The user asks how many orders the customer placed.
      Use `customer_order_count`.

    RETURNS:
    Basic customer information, including customer location
    and Olist customer identifiers.

    ARGUMENT:
    customer_id: The exact 32-character hexadecimal Olist customer ID.
    """
    return get_customer_details(customer_id)


@tool(args_schema=CustomerLookupInput)
def customer_orders(customer_id: str):
    """
    Retrieve the order history of ONE Olist customer.

    USE THIS TOOL WHEN:
    - The user asks which orders a customer placed.
    - The user asks for a customer's order history.
    - The user asks for order IDs associated with a customer.
    - The user asks for details about multiple orders belonging
      to a customer.

    DO NOT USE THIS TOOL WHEN:
    - The user only asks how many orders the customer placed.
      Use `customer_order_count`.
    - The user asks for general customer location information.
      Use `customer_details`.

    RETURNS:
    Orders associated with the specified customer.

    ARGUMENT:
    customer_id: The exact 32-character hexadecimal Olist customer ID.
    """
    return get_customer_orders(customer_id)


@tool(args_schema=CustomerLookupInput)
def customer_order_count(customer_id: str):
    """
    Return the total number of orders placed by ONE Olist customer.

    USE THIS TOOL WHEN:
    - The user asks "How many orders did this customer place?"
    - The user asks for the number or count of orders belonging
      to a specific customer.

    DO NOT USE THIS TOOL WHEN:
    - The user wants the actual order records.
      Use `customer_orders`.

    RETURNS:
    A single aggregate count representing the total number of
    orders associated with the customer.

    ARGUMENT:
    customer_id: The exact 32-character hexadecimal Olist customer ID.
    """
    return get_customer_order_count(customer_id)


# ============================================================
# SELLER TOOLS
# ============================================================

@tool(args_schema=SellerLookupInput)
def seller_details(seller_id: str):
    """
    Retrieve basic information about ONE Olist seller.

    USE THIS TOOL WHEN:
    - The user asks where a seller is located.
    - The user asks for basic seller information.
    - The user provides an exact seller ID.

    DO NOT USE THIS TOOL WHEN:
    - The user asks about the seller's orders.
      Use `seller_orders`.
    - The user asks about seller sales performance.
      Use `seller_statistics`.

    RETURNS:
    Basic seller information, including seller location
    and seller identifiers.

    ARGUMENT:
    seller_id: The exact 32-character hexadecimal Olist seller ID.
    """
    return get_seller_details(seller_id)


@tool(args_schema=SellerLookupInput)
def seller_orders(seller_id: str):
    """
    Retrieve orders associated with ONE Olist seller.

    USE THIS TOOL WHEN:
    - The user asks which orders a seller fulfilled.
    - The user asks for a seller's order history.
    - The user asks to see individual orders associated with a seller.

    DO NOT USE THIS TOOL WHEN:
    - The user asks for aggregated seller performance.
      Use `seller_statistics`.
    - The user asks about the seller's location.
      Use `seller_details`.

    RETURNS:
    Order records associated with the specified seller.

    ARGUMENT:
    seller_id: The exact 32-character hexadecimal Olist seller ID.
    """
    return get_seller_orders(seller_id)


@tool(args_schema=SellerLookupInput)
def seller_statistics(seller_id: str):
    """
    Retrieve aggregate sales statistics for ONE Olist seller.

    USE THIS TOOL WHEN:
    - The user asks how much a seller sold.
    - The user asks for a seller's total sales.
    - The user asks how many orders a seller has.
    - The user asks how many items a seller sold.
    - The user asks about total freight generated by a seller.
    - The user asks for an overall performance summary of a seller.

    DO NOT USE THIS TOOL WHEN:
    - The user wants individual seller orders.
      Use `seller_orders`.
    - The user only wants seller location information.
      Use `seller_details`.

    RETURNS:
    Aggregate seller statistics, including total orders,
    total items, product sales, freight, and total sales.

    ARGUMENT:
    seller_id: The exact 32-character hexadecimal Olist seller ID.
    """
    return get_seller_statistics(seller_id)


# ============================================================
# PRODUCT TOOLS
# ============================================================

@tool(args_schema=ProductLookupInput)
def product_details(product_id: str):
    """
    Retrieve descriptive information about ONE Olist product.

    USE THIS TOOL WHEN:
    - The user asks about a specific product.
    - The user asks for the product category.
    - The user asks about product dimensions or weight.
    - The user asks about description length, name length,
      or number of product photos.
    - The user provides an exact product ID.

    DO NOT USE THIS TOOL WHEN:
    - The user asks about the product's sales performance.
      Use `product_sales`.

    RETURNS:
    Product attributes including category, dimensions, weight,
    description length, name length, and photo count.

    ARGUMENT:
    product_id: The exact 32-character hexadecimal Olist product ID.
    """
    return get_product_details(product_id)


@tool(args_schema=ProductLookupInput)
def product_sales(product_id: str):
    """
    Retrieve aggregate sales statistics for ONE Olist product.

    USE THIS TOOL WHEN:
    - The user asks how many times a product was sold.
    - The user asks how many orders contain a product.
    - The user asks how much a product generated in sales.
    - The user asks about freight generated by a product.
    - The user asks for the sales performance of a product.

    DO NOT USE THIS TOOL WHEN:
    - The user asks for product attributes or category.
      Use `product_details`.

    RETURNS:
    Aggregate product sales statistics including total orders,
    total items sold, sales value, and freight value.

    ARGUMENT:
    product_id: The exact 32-character hexadecimal Olist product ID.
    """
    return get_product_sales(product_id)


# ============================================================
# PAYMENT TOOLS
# ============================================================

@tool(args_schema=OrderLookupInput)
def payment_summary(order_id: str):
    """
    Return a summarized payment analysis for ONE Olist order.

    USE THIS TOOL WHEN:
    - The user asks for the total amount paid for an order.
    - The user asks how many payments were made.
    - The user asks for the maximum number of installments.
    - The user wants a concise payment summary rather than
      individual payment records.

    DO NOT USE THIS TOOL WHEN:
    - The user asks for every individual payment record.
      Use `order_payments`.

    RETURNS:
    A payment summary containing the number of payments,
    total payment value, and maximum installment count.

    ARGUMENT:
    order_id: The exact 32-character hexadecimal Olist order ID.
    """
    return get_payment_summary(order_id)


# ============================================================
# ANALYTICS TOOLS
# ============================================================

@tool
def order_status_summary():
    """
    Return the overall distribution of Olist orders by order status.

    USE THIS TOOL WHEN:
    - The user asks how many orders are delivered, canceled,
      shipped, invoiced, processing, etc.
    - The user asks for an overall order-status breakdown.
    - The question concerns order status across the entire dataset.

    DO NOT USE THIS TOOL WHEN:
    - The user asks about the status of ONE specific order.
      Use `order_details`.

    RETURNS:
    Aggregate counts of orders grouped by order status.
    """
    return get_order_status_summary()


@tool(args_schema=LimitInput)
def sales_by_seller(limit: int = 10):
    """
    Return the top Olist sellers ranked by total sales.

    USE THIS TOOL WHEN:
    - The user asks for the highest-selling sellers.
    - The user asks for top sellers.
    - The user asks which sellers generated the most sales.
    - The user asks for a ranked seller sales list.

    DO NOT USE THIS TOOL WHEN:
    - The user asks about ONE specific seller.
      Use `seller_statistics`.
    - The user asks for a seller's individual orders.
      Use `seller_orders`.

    RETURNS:
    Sellers ranked by total sales, limited to the requested
    number of results.

    ARGUMENT:
    limit: Number of top sellers to return.
           Must be an integer between 1 and 100.
           Defaults to 10.
    """
    return get_sales_by_seller(limit)


@tool(args_schema=LimitInput)
def sales_by_category(limit: int = 10):
    """
    Return product categories ranked by total sales.

    USE THIS TOOL WHEN:
    - The user asks for the best-selling categories.
    - The user asks which product categories generate the most sales.
    - The user asks for top product categories by sales.

    DO NOT USE THIS TOOL WHEN:
    - The user asks about ONE specific product.
      Use `product_details` or `product_sales`.

    RETURNS:
    Product categories ranked by total sales, limited to
    the requested number of categories.

    ARGUMENT:
    limit: Number of top categories to return.
           Must be an integer between 1 and 100.
           Defaults to 10.
    """
    return get_sales_by_category(limit)


@tool
def sales_by_state():
    """
    Return total sales grouped by Brazilian customer state.

    USE THIS TOOL WHEN:
    - The user asks which Brazilian states generate the most sales.
    - The user asks about sales distribution across states.
    - The user asks for state-level sales statistics.

    DO NOT USE THIS TOOL WHEN:
    - The user asks about one specific customer.
      Use `customer_details`.

    RETURNS:
    Aggregate sales statistics grouped by customer state.
    """
    return get_sales_by_state()


@tool
def monthly_sales():
    """
    Return total sales grouped by month.

    USE THIS TOOL WHEN:
    - The user asks about sales trends over time.
    - The user asks how sales changed month by month.
    - The user asks for monthly sales totals.
    - The user asks about sales patterns across months.

    RETURNS:
    Aggregate sales values grouped chronologically by month.
    """
    return get_monthly_sales()


# ============================================================
# DELIVERY TOOLS
# ============================================================

@tool
def delivery_statistics():
    """
    Return overall delivery performance statistics.

    USE THIS TOOL WHEN:
    - The user asks about overall delivery performance.
    - The user asks for average delivery time.
    - The user asks how long orders generally take to be delivered.
    - The user asks for overall delivered-order statistics.

    DO NOT USE THIS TOOL WHEN:
    - The user asks whether a specific order was late.
      Use `order_details` for that order.
    - The user asks specifically about late versus on-time orders.
      Use `late_delivery_statistics`.

    RETURNS:
    Overall delivery statistics, including the number of delivered
    orders and average delivery time in days.
    """
    return get_delivery_statistics()


@tool
def late_delivery_statistics():
    """
    Return aggregate statistics comparing estimated and actual
    delivery dates.

    USE THIS TOOL WHEN:
    - The user asks how many orders were late.
    - The user asks how many orders were delivered on time.
    - The user asks for the overall late-delivery rate or statistics.
    - The user asks about delivery delays across the dataset.

    DO NOT USE THIS TOOL WHEN:
    - The user asks whether ONE specific order was late.
      Use `order_details`.

    RETURNS:
    Aggregate delivery statistics including total delivered
    orders, late orders, and on-time orders.
    """
    return get_late_delivery_statistics()


# ============================================================
# TOOL COLLECTION
# ============================================================

QUERY_TOOLS = [
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