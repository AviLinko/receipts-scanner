import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to the database
def connect_db():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

# Function to add or update a product
def add_or_update_product(product_name, quantity, user_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Search for a product by name and user_id
        cursor.execute("SELECT quantity FROM products WHERE name = %s AND user_id = %s", (product_name, user_id))
        result = cursor.fetchone()

        if result:
            # Update quantity of an existing product
            new_quantity = result[0] + quantity
            cursor.execute("UPDATE products SET quantity = %s WHERE name = %s AND user_id = %s", (new_quantity, product_name, user_id))
            message = f"Updated {product_name}, new quantity: {new_quantity}"
        else:
            # Add a new product
            cursor.execute("INSERT INTO products (name, quantity, user_id) VALUES (%s, %s, %s)", (product_name, quantity, user_id))
            message = f"Added new product: {product_name}, quantity: {quantity}"

        conn.commit()

        # Retrieve all products related to user_id
        cursor.execute("SELECT name, quantity FROM products WHERE user_id = %s", (user_id,))
        products = cursor.fetchall()
        products_dict = {name: quantity for name, quantity in products}

        return message, products_dict

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

# Function to delete a product
def delete_product(product_name, user_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Delete a product by name and user_id
        cursor.execute("DELETE FROM products WHERE name = %s AND user_id = %s", (product_name, user_id))
        conn.commit()

        # Retrieve all products related to user_id
        cursor.execute("SELECT name, quantity FROM products WHERE user_id = %s", (user_id,))
        products = cursor.fetchall()
        products_dict = {name: quantity for name, quantity in products}

        return f"Deleted {product_name}", products_dict

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

# Function to delete all products
def delete_all_products(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Delete all products related to user_id
        cursor.execute("DELETE FROM products WHERE user_id = %s", (user_id,))
        conn.commit()

        return "All products deleted", {}

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()

# Function to return all products
def get_all_products(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Retrieve all products related to user_id
        cursor.execute("SELECT name, quantity FROM products WHERE user_id = %s", (user_id,))
        products = cursor.fetchall()
        products_dict = {name: quantity for name, quantity in products}
        return products_dict

    except Exception as e:
        raise e

    finally:
        cursor.close()
        conn.close()
