import mysql.connector
from typing import List, Dict

host = # Add connection details
port = 3306
user = "root"
password = "root"

def load(data: List[Dict[str, str]]) -> None:
    """
    Load the provided data into a MySQL database.

    Args:
        data (List[Dict[str, str]]): A list of dictionaries containing product details such as brand, price, category, and gender.

    Returns:
        None
    """
    connection = None

    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

        if connection.is_connected():
            print("Connected to MySQL database")

            cursor = connection.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS products_db")
            print("Database created or already exists")

            cursor.execute("USE products_db")

            cursor.execute("CREATE TABLE IF NOT EXISTS products (id INT PRIMARY KEY AUTO_INCREMENT, brand VARCHAR(255), price DECIMAL(10,2), category VARCHAR(255), gender VARCHAR(255))")
            print("Table created or already exists")

            for x in data:
                values = (x["brand"], float(x["price"][1:].replace(",", "")), x["category"], x["gender"])
                cursor.execute("INSERT INTO products (brand, price, category, gender) VALUES (%s, %s, %s, %s)", values)

            connection.commit()
            print(f"Successfully inserted {len(data)} rows into the 'products' table.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Connection closed.")
