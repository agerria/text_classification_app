from .base import OrmModel, BaseModel

class SUserOut(OrmModel):
    login: str
    fullname: str | None

class SUserToken(OrmModel):    
    login: str
    token: str | None
    
    

class SUserLogin(BaseModel):
    login: str
    password: str