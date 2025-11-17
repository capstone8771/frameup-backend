import pymysql
import os

def get_connection():
    try:
        conn = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 3306)),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False    # 수동 커밋 방식 (API에서 커밋 제어)
        )
        return conn
    except Exception as e:
        print("🔴 DB CONNECTION ERROR:", e)
        return None
