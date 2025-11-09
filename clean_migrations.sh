#!/bin/bash

echo "⚠️  ADVERTENCIA: Esto eliminará TODAS las migraciones"
echo "Solo usar en desarrollo sin datos importantes"
read -p "¿Continuar? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Eliminando migraciones..."
    rm -f alembic/versions/*.py
    
    echo "Reiniciando base de datos..."
    alembic stamp base
    
    echo "Creando migración inicial..."
    alembic revision --autogenerate -m "Migración inicial"
    alembic upgrade head
    
    echo "✅ Limpieza completada"
else
    echo "❌ Operación cancelada"
fi