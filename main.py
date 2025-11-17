from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import get_connection

app = FastAPI()

# CORS 설정 (필요 시)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 프론트와 연결 위해 전체 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 엔드포인트
@app.get("/")
def root():
    return {"message": "FrameUp Backend API Running!"}


# ✅ DB 연결 테스트 엔드포인트
@app.get("/test-db")
def test_db():
    conn = get_connection()

    # DB 연결 실패 시
    if conn is None:
        return {"db": "error", "detail": "connection failed"}

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        return {"db": "connected", "result": result}
    except Exception as e:
        return {"db": "error", "detail": str(e)}


# 여기에 다른 API 엔드포인트들이 계속 추가될 수 있음
# 예: 회원가입, 로그인, 분석 API 등
