import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Olist Delivery Prediction",
    page_icon="📦",
    layout="wide"
)


st.title("📦 Olist Delivery Prediction")
st.write(
    "Predict whether an order is likely to be delivered late."
)
st.header("Order Information")

col1, col2 = st.columns(2)

with col1:

    customer_state = st.text_input(
        "Customer State",
        value="SP"
    )

    seller_state = st.text_input(
        "Seller State",
        value="SP"
    )

    product_category_name = st.text_input(
        "Product Category",
        value="Electronics & Computers"
    )

    payment_type = st.selectbox(
        "Payment Type",
        [
            "credit_card",
            "boleto",
            "voucher",
            "debit_card",
            "unknown"
        ]
    )


with col2:

    number_of_items = st.number_input(
        "Number of Items",
        min_value=0,
        value=1
    )

    number_of_products = st.number_input(
        "Number of Products",
        min_value=0,
        value=1
    )

    number_of_sellers = st.number_input(
        "Number of Sellers",
        min_value=0,
        value=1
    )

    total_price = st.number_input(
        "Total Price",
        min_value=0.0,
        value=100.0
    )

    total_freight = st.number_input(
        "Total Freight",
        min_value=0.0,
        value=20.0
    )
st.header("Product & Payment Information")

col1, col2, col3 = st.columns(3)

with col1:

    total_product_weight = st.number_input(
        "Product Weight",
        min_value=0.0,
        value=1.0
    )

    total_product_volume = st.number_input(
        "Product Volume",
        min_value=0.0,
        value=100.0
    )

    total_payment_value = st.number_input(
        "Total Payment Value",
        min_value=0.0,
        value=100.0
    )


with col2:

    max_payment_installments = st.number_input(
        "Max Payment Installments",
        min_value=0,
        value=1
    )

    number_of_payments = st.number_input(
        "Number of Payments",
        min_value=0,
        value=1
    )


with col3:

    order_purchase_hour = st.number_input(
        "Purchase Hour",
        min_value=0,
        max_value=23,
        value=12
    )

    order_purchase_day_of_week = st.number_input(
        "Purchase Day of Week",
        min_value=0,
        max_value=6,
        value=2
    )

    order_purchase_month = st.number_input(
        "Purchase Month",
        min_value=1,
        max_value=12,
        value=6
    )

    order_purchase_year = st.number_input(
        "Purchase Year",
        min_value=2016,
        max_value=2030,
        value=2017
    )
st.header("Delivery Information")

col1, col2 = st.columns(2)

with col1:

    order_approval_delay_hours = st.number_input(
        "Order Approval Delay (hours)",
        min_value=0.0,
        value=2.0
    )


with col2:

    estimated_delivery_days = st.number_input(
        "Estimated Delivery Days",
        min_value=0.0,
        value=15.0
    )
if st.button(
    "Predict Delivery",
    type="primary"
):

    payload = {

        "customer_state": customer_state,
        "seller_state": seller_state,
        "payment_type": payment_type,
        "product_category_name": product_category_name,

        "number_of_items": number_of_items,
        "number_of_products": number_of_products,
        "number_of_sellers": number_of_sellers,

        "total_price": total_price,
        "total_freight": total_freight,

        "total_product_weight": total_product_weight,
        "total_product_volume": total_product_volume,
        "total_payment_value": total_payment_value,

        "max_payment_installments": (
            max_payment_installments
        ),
        "number_of_payments": number_of_payments,

        "order_purchase_hour": order_purchase_hour,
        "order_purchase_day_of_week": (
            order_purchase_day_of_week
        ),
        "order_purchase_month": order_purchase_month,
        "order_purchase_year": order_purchase_year,

        "order_approval_delay_hours": (
            order_approval_delay_hours
        ),
        "estimated_delivery_days": (
            estimated_delivery_days
        )
    }
    try:

        response = requests.post(
            f"{API_URL}/predict",
            json=payload,
            timeout=30
        )

        if response.status_code == 200:

            result = response.json()

            st.success("Prediction completed!")

            prediction = result["is_late"]
            probability = result["late_probability"]

            st.subheader("Prediction Result")

            if prediction == 1:
                st.error("⚠️ Likely Late")
            else:
                st.success("✅ Likely On Time")

            st.metric(
                "Late Probability",
                f"{probability:.2%}"
            )

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

            st.write(response.text)

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to FastAPI. "
            "Make sure the API is running."
        )

    except requests.exceptions.Timeout:

        st.error(
            "The prediction request timed out."
        )

    except Exception as e:

        st.error(
            f"Unexpected error: {str(e)}"
        )