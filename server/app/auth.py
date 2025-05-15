from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import jwt

from .db import DBView, get_db
from .config import Config
from .models import User
     
TOKEN_HEADER = APIKeyHeader(name="Authorization")
TOKEN_TTL = timedelta(minutes=300)

def create_access_token(user: User):
    expire = datetime.utcnow() + TOKEN_TTL
    data = {
        'exp': expire,
        'login': user.login,
    }
    return jwt.encode(data, Config.SECRET_KEY, algorithm='HS256')


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        login: str = payload.get('login')
        if login is None:
            raise HTTPException(status_code=401, detail='Некорректный токен')
        return login
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail='Некорректный токен')


async def get_current_user(token: str = Depends(TOKEN_HEADER), db: Session = Depends(get_db)):
    login = decode_access_token(token)
    user = db.query(User).filter(User.login == login).first()
    if user is None:
        raise HTTPException(status_code=401, detail='Некорректный токен')
    return user


class AuthView(DBView):
    # token: str = Depends(token_header)
    user: User = Depends(get_current_user)
    
    
    