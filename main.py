from fastapi import FastAPI
from db import get_connection

app = FastAPI()

@app.get("/test-db")
def test_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT NOW()")
        result = cursor.fetchone()
        conn.close()
        return {"success": True, "db_time": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
