from fastapi import Depends, FastAPI, APIRouter, HTTPException
from fastapi_utils.cbv import cbv
from app import app

from app.auth import AuthView


def get_x():
    return 10

router = APIRouter(prefix='/test', tags=['Тест'])  # Step 1: Create a router


@cbv(router)  # Step 2: Create and decorate a class to hold the endpoints
class Test:
    # Step 3: Add dependencies as class attributes
    x: int = Depends(get_x)

    @router.get('/')
    def test(self) -> int:
        # Step 4: Use `self.<dependency_name>` to access shared dependencies
        return self.x





@cbv(router)
class TestWithAuth(AuthView):
    @router.get('/auth')
    def test_token(self) -> dict:
        return {
            # 'token': self.token,
            'user': self.user.login
        }
    
    
    
    
app.include_router(router)