#!/bin/bash

# Instalar dependencias del backend
cd /home/hugo/proyectos/FastApi
pip install -r requirements.txt

# Ejecutar migraciones
cd /home/hugo/proyectos/FastApi/backend
alembic upgrade head

# Iniciar backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
