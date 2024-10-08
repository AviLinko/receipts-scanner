import psycopg2
import bcrypt
from dotenv import load_dotenv
import os

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

# Function to hash a password using bcrypt
def hash_password(password):
    salt = bcrypt.gensalt() 
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  

# Function to save a new user
def save_user(email, password):
    conn = connect_db()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        # Print the hashed password before saving
        print(f"Hashed password: {hashed_password}")

        # Save the hashed password as a string
        cursor.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
            (email, hashed_password)
        )
        conn.commit()
        print("User saved successfully.")
    except Exception as e:
        print(f"Error saving user: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Function to verify passwords during login
def login_user(email, password):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result is None:
            print("User does not exist.")
            return False

        stored_password = result[0]  

        # Check if the hashed password matches the provided password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            print("Login successful.")
            return True
        else:
            print("Invalid password.")
            return False

    except Exception as e:
        print(f"Error logging in: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
