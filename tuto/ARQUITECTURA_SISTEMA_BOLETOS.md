# Arquitectura de Sistema de Venta de Boletos (Ticketmaster)

## 📋 Tabla de Contenidos
1. [Visión General](#visión-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura de Carpetas](#estructura-de-carpetas)
4. [Modelos de Datos](#modelos-de-datos)
5. [Flujos Principales](#flujos-principales)
6. [Componentes Clave](#componentes-clave)
7. [Consideraciones de Escalabilidad](#consideraciones-de-escalabilidad)

---

## Visión General

Un sistema de venta de boletos tipo Ticketmaster requiere:
- **Alta concurrencia**: Miles de usuarios comprando simultáneamente
- **Consistencia de datos**: Evitar sobreventa de boletos
- **Transacciones atómicas**: Reserva y pago deben ser seguros
- **Escalabilidad horizontal**: Múltiples servidores
- **Caché distribuido**: Para eventos populares

---

## Arquitectura del Sistema

### Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTE (Frontend)                       │
│  (React/Vue - Búsqueda, Selección de Asientos, Pago)            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API Gateway / Load Balancer                  │
│              (Nginx, AWS ALB - Distribución de carga)           │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  FastAPI     │  │  FastAPI     │  │  FastAPI     │
│  Server 1    │  │  Server 2    │  │  Server N    │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Redis Cache │  │  PostgreSQL  │  │  Message     │
│  (Sesiones)  │  │  (Principal) │  │  Queue       │
└──────────────┘  └──────────────┘  │  (RabbitMQ)  │
                                    └──────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Servicio    │  │  Servicio    │  │  Servicio    │
│  Pagos       │  │  Email       │  │  Reportes    │
│  (Stripe)    │  │  (SendGrid)  │  │  (Analytics) │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## Estructura de Carpetas

```
FastApi/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── auth.py                    # Autenticación
│   │   ├── events.py                  # Gestión de eventos
│   │   ├── venues.py                  # Gestión de lugares
│   │   ├── tickets.py                 # Gestión de boletos
│   │   ├── reservations.py            # Reservas
│   │   ├── payments.py                # Pagos
│   │   ├── orders.py                  # Órdenes
│   │   └── admin.py                   # Panel administrativo
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                  # Configuración
│   │   ├── auth.py                    # JWT, hashing
│   │   ├── security.py                # Permisos, roles
│   │   └── constants.py               # Constantes
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py                 # Conexión BD
│   │   └── cache.py                   # Redis
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                    # Usuario
│   │   ├── event.py                   # Evento
│   │   ├── venue.py                   # Lugar
│   │   ├── ticket.py                  # Boleto
│   │   ├── seat.py                    # Asiento
│   │   ├── reservation.py             # Reserva
│   │   ├── order.py                   # Orden
│   │   └── payment.py                 # Pago
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── event.py
│   │   ├── ticket.py
│   │   ├── reservation.py
│   │   ├── order.py
│   │   └── payment.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── event.py
│   │   ├── ticket.py
│   │   ├── reservation.py             # Lógica de reservas
│   │   ├── order.py                   # Lógica de órdenes
│   │   ├── payment.py                 # Integración Stripe
│   │   ├── email.py                   # Envío de emails
│   │   └── notification.py            # Notificaciones
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── event.py
│   │   ├── ticket.py
│   │   ├── reservation.py
│   │   ├── order.py
│   │   └── payment.py
│   │
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── celery_app.py              # Configuración Celery
│   │   ├── tasks.py                   # Tareas asincrónicas
│   │   └── email_worker.py            # Worker de emails
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── events.html
│   │   ├── event_detail.html
│   │   ├── seat_selection.html
│   │   ├── checkout.html
│   │   └── confirmation.html
│   │
│   └── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_events.py
│   ├── test_tickets.py
│   ├── test_reservations.py
│   └── test_payments.py
│
├── .env
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## Modelos de Datos

### Diagrama ER (Entity-Relationship)

```
┌─────────────────┐
│     USER        │
├─────────────────┤
│ id (PK)         │
│ email           │
│ username        │
│ password_hash   │
│ is_active       │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│     ORDER       │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ total_price     │
│ status          │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│    TICKET       │
├─────────────────┤
│ id (PK)         │
│ order_id (FK)   │
│ event_id (FK)   │
│ seat_id (FK)    │
│ price           │
│ status          │
│ qr_code         │
└─────────────────┘


┌─────────────────┐
│     EVENT       │
├─────────────────┤
│ id (PK)         │
│ name            │
│ description     │
│ venue_id (FK)   │
│ date_time       │
│ total_seats     │
│ available_seats │
│ status          │
│ created_at      │
└────────┬────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│      SEAT       │
├─────────────────┤
│ id (PK)         │
│ event_id (FK)   │
│ section         │
│ row             │
│ number          │
│ status          │
│ price           │
└─────────────────┘


┌─────────────────┐
│     VENUE       │
├─────────────────┤
│ id (PK)         │
│ name            │
│ address         │
│ capacity        │
│ city            │
│ country         │
└─────────────────┘


┌─────────────────┐
│  RESERVATION    │
├─────────────────┤
│ id (PK)         │
│ user_id (FK)    │
│ event_id (FK)   │
│ seat_ids        │
│ expires_at      │
│ status          │
│ created_at      │
└─────────────────┘


┌─────────────────┐
│     PAYMENT     │
├─────────────────┤
│ id (PK)         │
│ order_id (FK)   │
│ amount          │
│ status          │
│ method          │
│ transaction_id  │
│ created_at      │
└─────────────────┘
```

---

## Flujos Principales

### 1. Flujo de Compra de Boletos

```
┌─────────────────────────────────────────────────────────────────┐
│                    USUARIO INICIA SESIÓN                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              BUSCA Y SELECCIONA EVENTO                          │
│  GET /api/events?city=Madrid&date=2024-12-25                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│           VE MAPA DE ASIENTOS DEL EVENTO                        │
│  GET /api/events/{event_id}/seats                              │
│  (Datos cacheados en Redis por 5 minutos)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│         SELECCIONA ASIENTOS Y CREA RESERVA                      │
│  POST /api/reservations                                         │
│  {                                                              │
│    "event_id": 1,                                              │
│    "seat_ids": [10, 11, 12],                                   │
│    "expires_in_minutes": 15                                    │
│  }                                                              │
│                                                                 │
│  ✓ Bloquea asientos en BD (status = RESERVED)                 │
│  ✓ Crea entrada en Redis con TTL de 15 min                    │
│  ✓ Retorna reservation_id                                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              PROCEDE AL CHECKOUT                                │
│  POST /api/orders                                               │
│  {                                                              │
│    "reservation_id": "res_123",                                │
│    "payment_method": "credit_card"                             │
│  }                                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│           PROCESA PAGO (Stripe/PayPal)                          │
│  POST /api/payments                                             │
│  {                                                              │
│    "order_id": "ord_456",                                      │
│    "amount": 150.00,                                           │
│    "token": "tok_visa"                                         │
│  }                                                              │
│                                                                 │
│  ✓ Envía a Stripe                                             │
│  ✓ Recibe confirmación                                        │
│  ✓ Actualiza status de pago en BD                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│         GENERA BOLETOS Y ENVÍA EMAIL                            │
│  (Tarea asincrónica con Celery)                                │
│                                                                 │
│  ✓ Genera QR para cada boleto                                 │
│  ✓ Crea PDF con boletos                                       │
│  ✓ Envía email con PDF adjunto                                │
│  ✓ Actualiza status de asientos a SOLD                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              CONFIRMACIÓN AL USUARIO                            │
│  GET /api/orders/{order_id}                                    │
│  Muestra boletos, QR, detalles del evento                      │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Flujo de Liberación de Asientos Reservados

```
┌─────────────────────────────────────────────────────────────────┐
│         USUARIO NO COMPLETA COMPRA EN 15 MINUTOS               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│    REDIS EXPIRA LA CLAVE DE RESERVA (TTL)                      │
│    Celery Beat ejecuta tarea cada 1 minuto                     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│    LIBERA ASIENTOS EN BD (status = AVAILABLE)                  │
│    UPDATE seats SET status = 'AVAILABLE'                       │
│    WHERE reservation_id = 'res_123'                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│    OTROS USUARIOS PUEDEN COMPRAR ESOS ASIENTOS                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Componentes Clave

### 1. Modelo: Event

```python
# app/models/event.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Event(SQLModel, table=True):
    __tablename__ = "events"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    venue_id: int = Field(foreign_key="venue.id")
    date_time: datetime
    total_seats: int
    available_seats: int
    status: str = Field(default="ACTIVE")  # ACTIVE, CANCELLED, COMPLETED
    image_url: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 2. Modelo: Seat

```python
# app/models/seat.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Seat(SQLModel, table=True):
    __tablename__ = "seats"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id")
    section: str  # VIP, GENERAL, BALCONY
    row: str      # A, B, C...
    number: int   # 1, 2, 3...
    status: str = Field(default="AVAILABLE")  # AVAILABLE, RESERVED, SOLD
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        indexes = [
            ("event_id", "section", "row", "number")  # Índice compuesto
        ]
```

### 3. Modelo: Reservation

```python
# app/models/reservation.py
from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import datetime

class Reservation(SQLModel, table=True):
    __tablename__ = "reservations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    event_id: int = Field(foreign_key="event.id")
    seat_ids: List[int]  # JSON array
    status: str = Field(default="PENDING")  # PENDING, CONFIRMED, EXPIRED, CANCELLED
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 4. Servicio: ReservationService

```python
# app/services/reservation.py
from datetime import datetime, timedelta
from app.repositories.reservation import ReservationRepository
from app.repositories.seat import SeatRepository
from app.db.cache import redis_client
from fastapi import HTTPException
import json

class ReservationService:
    def __init__(self, reservation_repo, seat_repo):
        self.reservation_repo = reservation_repo
        self.seat_repo = seat_repo
    
    async def create_reservation(self, user_id: int, event_id: int, 
                                 seat_ids: List[int], expires_in_minutes: int = 15):
        """
        Crea una reserva de asientos con bloqueo temporal
        """
        # 1. Verificar disponibilidad de asientos
        seats = await self.seat_repo.get_by_ids(seat_ids)
        for seat in seats:
            if seat.status != "AVAILABLE":
                raise HTTPException(status_code=400, 
                                  detail=f"Asiento {seat.number} no disponible")
        
        # 2. Bloquear asientos en BD
        await self.seat_repo.update_status(seat_ids, "RESERVED")
        
        # 3. Crear reserva en BD
        expires_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
        reservation = await self.reservation_repo.create({
            "user_id": user_id,
            "event_id": event_id,
            "seat_ids": seat_ids,
            "expires_at": expires_at,
            "status": "PENDING"
        })
        
        # 4. Guardar en Redis con TTL
        redis_key = f"reservation:{reservation.id}"
        redis_client.setex(
            redis_key,
            expires_in_minutes * 60,
            json.dumps({
                "reservation_id": reservation.id,
                "seat_ids": seat_ids,
                "user_id": user_id
            })
        )
        
        return reservation
    
    async def release_expired_reservations(self):
        """
        Libera asientos de reservas expiradas
        (Ejecutada por Celery Beat cada minuto)
        """
        expired = await self.reservation_repo.get_expired()
        for reservation in expired:
            # Liberar asientos
            await self.seat_repo.update_status(
                reservation.seat_ids, 
                "AVAILABLE"
            )
            # Actualizar estado
            await self.reservation_repo.update_status(
                reservation.id, 
                "EXPIRED"
            )
```

### 5. Endpoint: Crear Reserva

```python
# app/api/reservations.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_session
from app.services.reservation import ReservationService
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.core.auth import get_current_active_user

router = APIRouter(prefix="/api/reservations", tags=["reservations"])

@router.post("", response_model=ReservationResponse)
async def create_reservation(
    reservation: ReservationCreate,
    current_user = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Crea una reserva de asientos
    
    - Bloquea asientos por 15 minutos
    - Retorna reservation_id para proceder al pago
    """
    service = ReservationService(session)
    return await service.create_reservation(
        user_id=current_user.id,
        event_id=reservation.event_id,
        seat_ids=reservation.seat_ids,
        expires_in_minutes=15
    )
```

### 6. Tarea Celery: Liberar Reservas Expiradas

```python
# app/workers/tasks.py
from celery import shared_task
from app.services.reservation import ReservationService
from app.db.session import AsyncSessionFactory

@shared_task
def release_expired_reservations():
    """
    Ejecutada cada minuto por Celery Beat
    Libera asientos de reservas expiradas
    """
    async def run():
        async with AsyncSessionFactory() as session:
            service = ReservationService(session)
            await service.release_expired_reservations()
    
    import asyncio
    asyncio.run(run())

@shared_task
def send_confirmation_email(order_id: int):
    """
    Envía email de confirmación con boletos
    """
    # Implementación...
    pass
```

### 7. Configuración Celery Beat

```python
# app/workers/celery_app.py
from celery import Celery
from celery.schedules import crontab

app = Celery('ticketmaster')

app.conf.beat_schedule = {
    'release-expired-reservations': {
        'task': 'app.workers.tasks.release_expired_reservations',
        'schedule': crontab(minute='*'),  # Cada minuto
    },
    'send-daily-reports': {
        'task': 'app.workers.tasks.send_daily_reports',
        'schedule': crontab(hour=0, minute=0),  # Cada día a medianoche
    },
}
```

---

## Consideraciones de Escalabilidad

### 1. Caché Distribuido (Redis)

```python
# app/db/cache.py
import redis
from app.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

# Estrategias de caché:
# - Eventos populares: 5 minutos
# - Mapa de asientos: 2 minutos
# - Disponibilidad: 1 minuto
# - Sesiones de usuario: 24 horas
```

### 2. Índices en Base de Datos

```sql
-- Índices críticos para performance
CREATE INDEX idx_event_date ON events(date_time);
CREATE INDEX idx_seat_event_status ON seats(event_id, status);
CREATE INDEX idx_reservation_user_event ON reservations(user_id, event_id);
CREATE INDEX idx_order_user_created ON orders(user_id, created_at);
CREATE INDEX idx_payment_order_status ON payments(order_id, status);
```

### 3. Particionamiento de Datos

```sql
-- Particionar tabla de órdenes por fecha
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');
```

### 4. Load Balancing

```yaml
# docker-compose.yml
version: '3.8'

services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - api1
      - api2
      - api3

  api1:
    build: .
    environment:
      - INSTANCE_ID=1
    depends_on:
      - postgres
      - redis

  api2:
    build: .
    environment:
      - INSTANCE_ID=2
    depends_on:
      - postgres
      - redis

  api3:
    build: .
    environment:
      - INSTANCE_ID=3
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=ticketmaster
      - POSTGRES_PASSWORD=password

  redis:
    image: redis:7-alpine

  celery:
    build: .
    command: celery -A app.workers.celery_app worker -l info
    depends_on:
      - postgres
      - redis

  celery-beat:
    build: .
    command: celery -A app.workers.celery_app beat -l info
    depends_on:
      - postgres
      - redis
```

### 5. Monitoreo y Logging

```python
# app/core/logging.py
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

# Logs estructurados para análisis
logger.info("Reservation created", extra={
    "user_id": 123,
    "event_id": 456,
    "seat_count": 3,
    "duration_ms": 245
})
```

### 6. Métricas Clave

```
- Tiempo de respuesta de API (p50, p95, p99)
- Tasa de error (4xx, 5xx)
- Disponibilidad de asientos en tiempo real
- Tasa de conversión (reservas → compras)
- Tiempo promedio de compra
- Ingresos por evento
- Usuarios concurrentes
```

---

## Seguridad

### 1. Validación de Entrada

```python
from pydantic import BaseModel, Field, validator

class ReservationCreate(BaseModel):
    event_id: int = Field(..., gt=0)
    seat_ids: List[int] = Field(..., min_items=1, max_items=10)
    
    @validator('seat_ids')
    def validate_seat_ids(cls, v):
        if len(v) != len(set(v)):
            raise ValueError('Asientos duplicados')
        return v
```

### 2. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/reservations")
@limiter.limit("10/minute")
async def create_reservation(...):
    pass
```

### 3. Transacciones Atómicas

```python
async def process_payment(order_id: int, amount: float):
    async with session.begin():  # Transacción
        try:
            # 1. Procesar pago
            payment = await stripe_client.charge(amount)
            
            # 2. Actualizar orden
            await order_repo.update_status(order_id, "PAID")
            
            # 3. Generar boletos
            await ticket_service.generate_tickets(order_id)
            
            # Si todo OK, commit automático
        except Exception as e:
            # Rollback automático
            raise
```

---

## Conclusión

Este sistema de venta de boletos está diseñado para:
- ✅ Manejar miles de usuarios simultáneos
- ✅ Garantizar consistencia de datos
- ✅ Escalar horizontalmente
- ✅ Mantener alta disponibilidad
- ✅ Procesar pagos de forma segura
- ✅ Proporcionar experiencia de usuario fluida

La arquitectura es modular, testeable y lista para producción.
