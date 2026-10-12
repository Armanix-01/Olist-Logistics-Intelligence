# API Reference

## Base URL

For local development, the API is typically available at `http://127.0.0.1:8000`.

FastAPI interactive documentation is normally available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## `POST /predict`

Accepts order features and returns a late-delivery prediction. The enhanced implementation also returns SHAP contributions and an LLM-generated explanation.

### Example Request

Field names and types must match `PredictionRequest` in `api/schemas.py`.

```json
{
  "customer_state": "SP",
  "seller_state": "SP",
  "product_category_name": "Electronics & Computers",
  "payment_type": "credit_card",
  "number_of_items": 1,
  "number_of_products": 1,
  "number_of_sellers": 1,
  "total_price": 100.0,
  "total_freight": 20.0,
  "total_product_weight": 1.0,
  "total_product_volume": 100.0,
  "total_payment_value": 100.0,
  "max_payment_installments": 1,
  "number_of_payments": 1,
  "order_purchase_hour": 12,
  "order_purchase_day_of_week": 2,
  "order_purchase_month": 6,
  "order_purchase_year": 2017,
  "order_approval_delay_hours": 2.0,
  "estimated_delivery_days": 15.0
}
```

These values are illustrative. Use categories, state codes, and feature values compatible with the fitted preprocessing pipeline.

### Response Fields

The enhanced response is designed to include the following fields:

| Field | Meaning |
|---|---|
| `is_late` | Predicted class: `1` = late, `0` = not late |
| `late_probability` | Model-estimated probability of class 1 |
| `shap_baseline_probability` | Reference probability used by SHAP |
| `explanation` | List of top feature contributions |
| `llm_explanation` | Natural-language explanation based on the prediction and SHAP results |

Each item in `explanation` contains:

- `feature`: Transformed feature name.
- `shap_value`: Signed contribution on the probability scale.
- `direction`: `increases_late_probability`, `decreases_late_probability`, or `no_effect`.

Example response values should be obtained from a live request; do not treat illustrative values as actual results. The Pydantic response model in `api/schemas.py` is authoritative.

### cURL Example

The following command sends the same example payload to the prediction endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_state": "SP",
    "seller_state": "SP",
    "product_category_name": "Electronics & Computers",
    "payment_type": "credit_card",
    "number_of_items": 1,
    "number_of_products": 1,
    "number_of_sellers": 1,
    "total_price": 100.0,
    "total_freight": 20.0,
    "total_product_weight": 1.0,
    "total_product_volume": 100.0,
    "total_payment_value": 100.0,
    "max_payment_installments": 1,
    "number_of_payments": 1,
    "order_purchase_hour": 12,
    "order_purchase_day_of_week": 2,
    "order_purchase_month": 6,
    "order_purchase_year": 2017,
    "order_approval_delay_hours": 2.0,
    "estimated_delivery_days": 15.0
  }'
```

Run the API before executing this command. The example is intended for Bash-compatible shells; Windows PowerShell may require different quoting.

## Errors

Potential failure sources include:

- Invalid or missing request fields.
- Missing or incompatible model artifacts.
- Mismatched input columns or unsupported categories.
- SHAP initialization or explanation errors.
- External LLM failures.
- Database or retrieval service connection failures in relevant workflows.

Inspect server logs for diagnostics. Do not expose internal stack traces, API keys, database credentials, or other secrets to public clients.

## Health and Chat Endpoints

Verify the exact root and health endpoint paths and response bodies in `api/main.py`.

Document the chatbot endpoint, request schema, and response schema from the actual router and source code rather than assuming endpoint names or response fields.
