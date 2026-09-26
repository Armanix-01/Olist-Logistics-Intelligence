from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd




PROJECT_ROOT = Path(__file__).resolve().parents[1]



load_dotenv()

cloud_db_url = os.getenv("CLOUD_DB_URL")

if not cloud_db_url:
    raise ValueError("CLOUD_DB_URL is not set in environment variables")


class CloudDb:

    def __init__(self, url: str):

        self.engine = create_engine(
            url=url,
            pool_pre_ping=True
        )


    def create_tables(self):

        schema_path = (
            PROJECT_ROOT
            / "database"
            / "sql"
            / "schema.sql"
        )

        with open(
            schema_path,
            "r",
            encoding="utf-8"
        ) as file:

            schema = file.read()


        with self.engine.begin() as conn:

            for statement in schema.split(";"):

                statement = statement.strip()

                if statement:

                    conn.execute(
                        text(statement)
                    )


    def load(self):

        
        self.create_tables()
        table_files = {

            "customers":
                PROJECT_ROOT
                / "data"
                / "cleaned"
                / "cleaned_customers_dataset.csv",

            "sellers":
                PROJECT_ROOT
                / "data"
                / "cleaned"
                / "cleaned_sellers_dataset.csv",

            "products":
                PROJECT_ROOT
                / "data"
                / "cleaned"
                / "cleaned_products_dataset.csv",

            "orders":
                PROJECT_ROOT
                / "data"
                / "cleaned"
                / "cleaned_orders_dataset.csv",

            "order_items":
                PROJECT_ROOT
                / "data"
                / "cleaned"
                / "cleaned_order_items_dataset.csv",

            "order_payments":
                PROJECT_ROOT
                / "data"
                / "cleaned"
                / "cleaned_order_payments_dataset.csv",
        }


        with self.engine.begin() as conn:

            for table_name, csv_path in table_files.items():

                print(
                    f"Loading {table_name}..."
                )

                df = pd.read_csv(csv_path)

                # Remove accidental pandas index columns
                df = df.loc[:, ~df.columns.str.contains("^Unnamed")]


                df.to_sql(
                    name=table_name,
                    con=conn,
                    if_exists="append",
                    index=False,
                    chunksize=5000
                )

                print(
                    f"Loaded {len(df)} rows into {table_name}"
                )


if __name__ == "__main__":

    db = CloudDb(cloud_db_url)

    db.load()