import psycopg2
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

# התחברות לבסיס הנתונים
def connect_db():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

# פונקציה להצפנת סיסמא עם bcrypt
def hash_password(password):
    salt = bcrypt.gensalt() 
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  

# פונקציה לשמירת משתמש חדש
def save_user(email, password):
    conn = connect_db()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    try:
        # הדפסת הסיסמא המוצפנת לפני השמירה
        print(f"Hashed password: {hashed_password}")

        # שמירת הסיסמא המוצפנת כמחרוזת טקסט
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

# פונקציה לבדוק סיסמאות בזמן כניסה
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

        # בדיקה אם הסיסמה המוצפנת תואמת את הסיסמה שסופקה
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
