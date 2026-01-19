PASO 4: 🌐 Crear los Endpoints de API

📍 Archivo: app/api/auth.py
🔍 Imports explicados:

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.models import User
from app.schemas.schemas import UserCreate, UserRead, UserLogin, Token
from app.core.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

APIRouter → Agrupa endpoints relacionados

Depends → Inyección de dependencias (BD, autenticación)

HTTPException → Errores HTTP estructurados

Session, select → ORM para consultas a BD

router = APIRouter()

@router.post → Método HTTP POST

response_model=UserRead → Valida y documenta la respuesta

user: UserCreate → Valida automáticamente el JSON de entrada

session: Session = Depends(get_session) → Inyecta conexión a BD

select(User).where(...) → SQL: SELECT * FROM users WHERE username = ?

.first() → Devuelve el primer resultado o None

HTTPException → Error HTTP 400 con mensaje personalizado

Validación de duplicados:

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(User).where(User.username == user.username))
    existing_user = result.first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        
        )

select(User).where(...) → SQL: SELECT * FROM users WHERE username = ?

.first() → Devuelve el primer resultado o None

HTTPException → Error HTTP 400 con mensaje personalizado        
    
    result = await session.exec(select(User).where(User.email == user.email))
    existing_email = result.first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear nuevo usuario
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    
    return db_user

get_password_hash() → Convierte "123456" a hash bcrypt

User(...) → Crea instancia del modelo (aún no en BD)

session.add() → Prepara para insertar

session.commit() → Ejecuta INSERT en BD

session.refresh() → Obtiene el ID generado por la BD

🔑 Endpoint de Login:

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    user = authenticate_user(session, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

authenticate_user() → Busca usuario y verifica contraseña

HTTP_401_UNAUTHORIZED → Error estándar para credenciales incorrectas

"WWW-Authenticate": "Bearer" → Header estándar para JWT

Generación de token:
access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
access_token = create_access_token(
    data={"sub": user.username}, expires_delta=access_token_expires
)
return {"access_token": access_token, "token_type": "bearer"}

timedelta(minutes=30) → Token válido por 30 minutos

{"sub": user.username} → "sub" = subject (estándar JWT)

"token_type": "bearer" → Tipo estándar para JWT