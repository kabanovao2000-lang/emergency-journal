# routers/auth.py
from fastapi import APIRouter, HTTPException, Depends
from schemas.user import UserLogin, UserRegister, UserResponse, Token
from services.auth_service import AuthService
from dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Аутентификация"])

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, auth_service: AuthService = Depends()):
    """
    Аутентификация пользователя.
    
    Параметры:
        - username: str - логин пользователя
        - password: str - пароль
    
    Возвращает:
        - access_token: str - JWT-токен
        - token_type: str - тип токена ("bearer")
    """
    token = await auth_service.authenticate(user_data.username, user_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, auth_service: AuthService = Depends()):
    """
    Регистрация нового пользователя.
    
    Параметры:
        - username: str - логин (уникальный)
        - email: str - email (уникальный)
        - password: str - пароль
        - full_name: str - полное имя
        - role: str - роль (user/dispatcher/admin)
    
    Возвращает:
        - id: int - ID пользователя
        - username: str - логин
        - email: str - email
        - full_name: str - полное имя
        - role: str - роль
    """
    return await auth_service.register(user_data)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Получение информации о текущем пользователе."""
    return current_user
