from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):

    customer_state: str
    seller_state: str
    payment_type: str
    product_category_name: str

    number_of_items: int = Field(ge=0)
    number_of_products: int = Field(ge=0)
    number_of_sellers: int = Field(ge=0)

    total_price: float = Field(ge=0)
    total_freight: float = Field(ge=0)

    total_product_weight: float | None = Field(default=None, ge=0)
    total_product_volume: float | None = Field(default=None, ge=0)
    total_payment_value: float | None = Field(default=None, ge=0)

    max_payment_installments: int | None = Field(default=None, ge=0)
    number_of_payments: int | None = Field(default=None, ge=0)

    order_purchase_hour: int = Field(ge=0, le=23)
    order_purchase_day_of_week: int = Field(ge=0, le=6)
    order_purchase_month: int = Field(ge=1, le=12)
    order_purchase_year: int

    order_approval_delay_hours: float | None = None
    estimated_delivery_days: float


class PredictionResponse(BaseModel):

    is_late: int
    late_probability: float