import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property


from hashlib import sha256

from sqladmin import ModelView
from app.db import Base

class User(Base):
    __tablename__ = 'user'
    
    login:          Mapped[str] = mapped_column(primary_key=True)
    password_hash:  Mapped[str]
    fullname:       Mapped[str | None]
    
    
    @classmethod
    def hash_password(cls, client_password: str) -> str:
        return sha256(client_password.encode('utf-8')).hexdigest()
    
    def verify_password(self, client_password: str) -> bool:
        return self.password == self.hash_password(client_password)
    
    @hybrid_property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self, client_password):
        self.password_hash = self.hash_password(client_password)

                
    
    
class UserAdmin(ModelView, model=User):
    column_list = [User.login, User.password, User.fullname]
    form_columns = [User.login, User.password_hash, User.fullname]
    form_include_pk = True
    
    async def on_model_change(self, data, model, is_created, request):
        data['password_hash'] = User.hash_password(data['password_hash'])