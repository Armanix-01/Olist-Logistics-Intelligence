
import logging
import re
import sqlglot
from sqlglot import exp

logger = logging.getLogger(__name__)

MAX_INPUT_LENGTH = 2000

def validate_user_input(question: str) -> str:
    """Validate and normalize a user's question."""

    if not isinstance(question, str):
        logger.warning("Invalid input type received.")
        raise ValueError("Question must be text.")

    question = question.strip()

    if not question:
        logger.warning("Empty question received.")
        raise ValueError("Question cannot be empty.")

    if len(question) > MAX_INPUT_LENGTH:
        logger.warning("Question exceeded maximum input length.")
        raise ValueError("Question is too long.")

    if not re.search(r"[a-zA-Z0-9]", question):
        logger.warning("Question did not contain meaningful characters.")
        raise ValueError("Please enter a meaningful question.")

    logger.info("User input validated successfully.")
    return question





ALLOWED_TABLES = {
    "customers",
    "sellers",
    "products",
    "orders",
    "order_items",
    "order_payments",
}

BLOCKED_FUNCTIONS = {
    "pg_sleep",
    "pg_read_file",
    "pg_read_binary_file",
    "pg_ls_dir",
    "pg_terminate_backend",
    "pg_cancel_backend",
    "dblink",
    "lo_import",
    "lo_export",
}


def validate_sql_query(sql_query: str) -> str:
    """Parse and validate a read-only SQL query."""

    if not isinstance(sql_query, str):
        raise ValueError("SQL query must be text.")

    sql_query = sql_query.strip()

    if not sql_query or len(sql_query) > 5000:
        raise ValueError("SQL query is empty or too long.")

    # Parse the SQL using PostgreSQL syntax.
    statements = sqlglot.parse(
        sql_query,
        read="postgres"
    )

    # Only one statement is allowed.
    if len(statements) != 1 or statements[0] is None:
        raise ValueError("Only one SQL statement is allowed.")

    tree = statements[0]

    # Allow SELECT and read-only query expressions,
    # including SELECT statements with CTEs and UNION.
    if not isinstance(
        tree,
        (exp.Select, exp.Union, exp.Intersect, exp.Except)
    ):
        raise ValueError("Only read-only SELECT queries are allowed.")

    # Reject SELECT INTO and locking clauses.
    if tree.find(exp.Into) is not None:
        raise ValueError("SELECT INTO is not allowed.")

    if tree.find(exp.Lock) is not None:
        raise ValueError("Locking queries are not allowed.")

    # Only allow known tables.
    # Collect names of CTEs defined in the query.
    cte_names = {
    cte.alias_or_name.lower()
    for cte in tree.find_all(exp.CTE)
    }

    # Validate table references.
    for table in tree.find_all(exp.Table):

        table_name = table.name.lower()

        # Do not allow schema/database-qualified references.
        if table.db or table.catalog:
            raise ValueError(
                "Schema-qualified tables are not allowed."
            )

        # A CTE is a temporary result created by this query,
        # so it does not need to be in ALLOWED_TABLES.
        if table_name in cte_names:
            continue

        # Any real database table must be explicitly allowed.
        if table_name not in ALLOWED_TABLES:
            raise ValueError(
                f"Table is not allowed: {table.name}"
            )

    # Reject potentially dangerous function calls.
    for func in tree.find_all(exp.Func):
        name = func.sql_name().lower()

        if name in BLOCKED_FUNCTIONS:
            raise ValueError(
                f"Function is not allowed: {name}"
            )

    # Apply a result limit, even if the LLM forgot one.
    limit = tree.args.get("limit")

    if limit is None:
        tree = tree.limit(100)
    else:
        try:
            value = int(limit.expression.this)
        except (AttributeError, TypeError, ValueError):
            raise ValueError("LIMIT must be a fixed integer.")

        if value < 1:
            raise ValueError("LIMIT must be positive.")

        if value > 100:
            tree = tree.limit(100)

    return tree.sql(dialect="postgres")

