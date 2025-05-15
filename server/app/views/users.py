from typing import List
from fastapi import Depends, FastAPI, APIRouter, HTTPException
from fastapi_utils.cbv import cbv
from pydantic import parse_obj_as

from app import app
from app.db import DBView
from app.auth import AuthView
from app.shema.user import SUserOut, SUserLogin, SUserToken
from app.models import User

from app.auth import create_access_token

router = APIRouter(prefix='/users', tags=['Пользователи'])  # Step 1: Create a router


@cbv(router)
class Users(AuthView):
    @router.get('/')
    async def list(self) -> List[SUserOut]:
        users = self.db.query(
            User
        )
        
        data = self.query_to_schemas(SUserOut, users)
        
        return data

@cbv(router)
class Users(DBView):
    @router.post('/login/')
    async def login(self, user: SUserLogin) -> SUserToken:
        db_user = self.db.query(User).filter(User.login == user.login).first()
        if not db_user or not db_user.verify_password(user.password):
            raise HTTPException(status_code=401, detail="Неверный логин ли пароль")
        
        token = create_access_token(db_user)
        return SUserToken(login=db_user.login, token=token)



app.include_router(router)