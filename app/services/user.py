from app.repositories.user import UserRepository
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.auth import hash_password, verify_password, create_access_token
from fastapi import HTTPException
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def register_user(self, user_create: UserCreate) -> UserResponse:
        # Validar email único
        existing_email = await self.user_repo.get_by_email(user_create.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email ya existe")
        
        # Validar username único
        existing_user = await self.user_repo.get_by_username(user_create.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username ya existe")
        
        # Crear usuario
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hash_password(user_create.password)
        )
        
        created_user = await self.user_repo.create(db_user)
        
        return UserResponse(
            id=created_user.id,
            email=created_user.email,
            username=created_user.username,
            is_active=created_user.is_active
        )
    
    async def authenticate_user(self, username: str, password: str) -> dict:
        print(f"Intentando autenticar usuario: {username}")
        user = await self.user_repo.get_by_username(username)
        print(f"Usuario encontrado: {user}")
        
        if not user:
            print("Usuario no encontrado")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        password_valid = verify_password(password, user.hashed_password)
        print(f"Contraseña válida: {password_valid}")
        
        if not password_valid:
            print("Contraseña incorrecta")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse(
                id=user.id,
                email=user.email,
                username=user.username,
                is_active=user.is_active
            )
        }
