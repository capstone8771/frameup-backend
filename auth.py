import hashlib

def hash_password(password: str) -> str:
    """비밀번호를 SHA-256 해시로 변환"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """입력 비밀번호가 해시와 일치하는지 검증"""
    return hashlib.sha256(password.encode()).hexdigest() == hashed
