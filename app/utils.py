from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
from .config import settings
from fastapi import status, HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    return serializer.dumps(email, salt=settings.SECURITY_PASSWORD_SALT)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    try:
        email = serializer.loads(token, salt=settings.SECURITY_PASSWORD_SALT, max_age=expiration)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Unable to validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return email