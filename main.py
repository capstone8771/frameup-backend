from fastapi import FastAPI
from db import get_connection

app = FastAPI()

@app.get("/test-db")
def test_db():
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
        return {"db": "connected"}
    except Exception as e:
        return {"db": "error", "detail": str(e)}
