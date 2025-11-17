from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db import get_connection
import hashlib

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# 비밀번호 해시 함수 (SHA-256)
# -------------------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hashlib.sha256(password.encode()).hexdigest() == hashed


# -------------------------------
# 기본 엔드포인트
# -------------------------------
@app.get("/")
def root():
    return {"message": "FrameUp Backend API Running!"}


# -------------------------------
# DB 연결 테스트
# -------------------------------
@app.get("/test-db")
def test_db():
    conn = get_connection()

    if conn is None:
        return {"db": "error", "detail": "connection failed"}

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        return {"db": "connected", "result": result}
    except Exception as e:
        return {"db": "error", "detail": str(e)}


# -------------------------------
# 회원가입 API
# -------------------------------
@app.post("/signup")
def signup(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="이메일과 비밀번호를 입력해주세요.")

    conn = get_connection()
    cursor = conn.cursor()

    # 이메일 중복 확인
    cursor.execute("SELECT id FROM user WHERE email = %s", (email,))
    existing = cursor.fetchone()

    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    # 비밀번호 해싱
    hashed_pw = hash_password(password)

    # DB 저장
    cursor.execute(
        "INSERT INTO user (email, password_hash) VALUES (%s, %s)",
        (email, hashed_pw)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "회원가입 성공"}


# -------------------------------
# 로그인 API
# -------------------------------
@app.post("/login")
def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="이메일과 비밀번호를 모두 입력해주세요.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    # 패스워드 검증
    if not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    return {
        "message": "로그인 성공",
        "user": {
            "id": user["id"],
            "email": user["email"]
        }
    }


# -------------------------------
# 앞으로 추가할 API
# -------------------------------
# /profile
# /profile/update
# /reset-password
# /auto-login
# /upload-image
