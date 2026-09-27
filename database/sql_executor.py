from sqlalchemy import text
from database.connection import engine


def execute_readonly_sql(query: str):

    query = query.strip()

    if not query.lower().startswith(("select", "with")):
        raise ValueError(
            "Only read-only SQL queries are allowed."
        )

    forbidden = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "grant",
        "revoke",
    ]

    query_lower = query.lower()

    if any(
        keyword in query_lower
        for keyword in forbidden
    ):
        raise ValueError(
            "Unsafe SQL operation detected."
        )

    with engine.connect() as connection:

        result = connection.execute(
            text(query)
        )

        rows = result.mappings().all()

    return [dict(row) for row in rows]