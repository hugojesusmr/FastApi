from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.repositories.user import UserRepository
from app.services.user import UserService
from app.core.auth import get_current_active_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        user_repo = UserRepository(session)
        user_service = UserService(user_repo)
        return await user_service.register_user(user)
    except Exception as e:
        print(f"Error en registro: {str(e)}")
        raise

@router.post("/login")
async def login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    user_repo = UserRepository(session)
    user_service = UserService(user_repo)
    return await user_service.authenticate_user(user.username, user.password)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user


