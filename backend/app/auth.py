import hashlib
import secrets
from sqlalchemy.orm import Session
from .models import User

# Demo token store. For production, replace with JWT + refresh tokens.
TOKENS: dict[str, int] = {}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash

def create_token(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    TOKENS[token] = user_id
    return token

def get_user_from_token(db: Session, token: str | None) -> User | None:
    if not token:
        return None
    token = token.replace("Bearer ", "")
    user_id = TOKENS.get(token)
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()
