
from sqlalchemy import text
from database.connection import engine
from langchain_core.tools import tool
from agent.schemas import CustomSQLInput
from agent.guardrails import validate_sql_query


@tool(args_schema=CustomSQLInput)
def run_custom_sql_query(sql_query: str):
    """
    Execute a validated, read-only PostgreSQL query against
    the Olist database.

    Use this tool when the user's database question cannot
    be answered by the specialized database tools.

    Use it for custom:
    - aggregations
    - GROUP BY queries
    - filtering
    - joins
    - calculations
    - analytical queries

    Do not use it for:
    - ML delivery predictions
    - documentation/knowledge-base questions
    - questions that can be answered directly by a
      specialized database tool.

    Only generate read-only SELECT SQL using the allowed
    Olist database schema. Never invent tables or columns.
    """

    safe_query = validate_sql_query(sql_query)

    try:
        with engine.begin() as connection:
            connection.execute(
                text("SET TRANSACTION READ ONLY")
            )
            connection.execute(
                text("SET LOCAL statement_timeout = '10s'")
            )

            result = connection.execute(text(safe_query))
            rows = result.mappings().all()

            return [dict(row) for row in rows]

    except Exception:
        
        return {
            "error": "The database query could not be completed."
        }

