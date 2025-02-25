import os
import snowflake.connector
from typing import List, Dict
import csv
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('SNOWFLAKE_USER')
password = os.getenv('SNOWFLAKE_PASSWORD')
account = os.getenv('SNOWFLAKE_ACCOUNT')
warehouse = os.getenv('SNOWFLAKE_WAREHOUSE')
database = os.getenv('SNOWFLAKE_DATABASE')
schema = os.getenv('SNOWFLAKE_SCHEMA')

def load(file: str) -> None:
    """
    Load the provided data into a Snowflake database.

    Args:
        data (List[Dict[str, str]]): A list of dictionaries containing product details such as brand, price, category, and gender.

    Returns:
        None
    """
    connection = None

    try:
       
        connection = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )

        if connection:
            print("Connected to Snowflake database")

            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT PRIMARY KEY AUTOINCREMENT,
                    price FLOAT,
                    brand STRING,
                    category STRING,
                    gender STRING
                )
            """)
            print("Table created or already exists")

            file_name = os.path.basename(file)

            cursor.execute("CREATE STAGE IF NOT EXISTS products")
            print("Stage created or already exists")

            print(f'Removing file if it exists in stage...')
            try:
                cursor.execute(f"REMOVE @products/{file_name}")
            except snowflake.connector.errors.ProgrammingError:
                pass
            
            print(f'Uploading {file_name} to stage...')

            cursor.execute(f"PUT file://{file} @products auto_compress=true")

            print(f' {file_name} uploaded to stage')

            copy_sql = f"""
                COPY INTO products (price, brand, category, gender)
                FROM @products/{file_name}
                FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
            """
            cursor.execute(copy_sql)
        
            connection.commit()
            print(f"Successfully inserted {file_name} into the 'products' table.")

    except snowflake.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection:
            connection.close()
            print("Connection closed.")


def overwrite_csv(file: str, data: List[Dict[str, str]]):
    """
    Overwrite the specified CSV file with the provided data.

    Args:
        file (str): The path to the CSV file to be overwritten.
        data (List[Dict[str, str]]): A list of dictionaries containing the data to be written.
                                     Each dictionary represents a row in the CSV file, with keys
                                     corresponding to column headers.

    Returns:
        None
    """

    with open(file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

