from typing import Annotated, Literal
from pydantic import BaseModel, Field, ConfigDict, StringConstraints
class ToolInput(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

# Original Olist IDs are 32 hexadecimal characters.
OlistID = Annotated[
    str,
    StringConstraints(
        min_length=32,
        max_length=32,
        pattern=r"^[a-fA-F0-9]{32}$"
    )
]
class RetrieverInput(ToolInput):
    query: str = Field(
        description="Question to search in the knowledge base.",
        min_length=3
    )

    query: str = Field(
        description="Question to search in the knowledge base",
        min_length=3
    )

class OrderLookupInput(ToolInput):
    order_id: OlistID = Field(
        description="The exact Olist order ID."
    )

class CustomerLookupInput(ToolInput):
    customer_id: OlistID = Field(
        description="The exact Olist customer ID."
    )

class SellerLookupInput(ToolInput):
    seller_id: OlistID = Field(
        description="The exact Olist seller ID."
    )

class ProductLookupInput(ToolInput):
    product_id: OlistID = Field(
        description="The exact Olist product ID."
    )

class CustomSQLInput(ToolInput):
    sql_query: str = Field(
        min_length=7,
        max_length=5000,
        description="A read-only PostgreSQL query."
    )

class PredictionInput(ToolInput):
    order_id: OlistID = Field(
        description="Olist order ID for delivery-delay prediction."
    )

class LimitInput(ToolInput):
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of records to return."
    )

class RoutingDecision(BaseModel):
    agents: list[
        Literal["query", "prediction", "retriever"]
    ]

from typing import Literal
from pydantic import BaseModel, Field


AgentType = Literal[
    "query",
    "prediction",
    "retriever"
]


class SubQuestion(BaseModel):
    id: str = Field(
        description="Unique ID for this subquestion, e.g. q1, q2."
    )

    question: str = Field(
        description="The specific question that must be answered."
    )

    agent: AgentType = Field(
        description="The specialized agent responsible for this question."
    )

    depends_on: list[str] = Field(
        default_factory=list,
        description="IDs of subquestions that must finish first."
    )


class Plan(BaseModel):
    subquestions: list[SubQuestion]