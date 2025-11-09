#!/bin/bash

# --- VARIABLES DE CONDFIGURACIÓN ----
MIGRATION_NAME=${1:-"Nueva Migración Automática"}

set -e
echo "---------------------------------------------------------------------"
echo "--- Ejecutando Migraciones de ALembic ----"
echo "---------------------------------------------------------------------"

# Verificar y agregar import sqlmodel al template si no existe
if ! grep -q "import sqlmodel" alembic/script.py.mako; then
    echo "Agregando import sqlmodel al template..."
    sed -i '/import sqlalchemy as sa/a import sqlmodel' alembic/script.py.mako
fi

echo "0. Aplicando migraciones pendientes..."
if ! alembic upgrade head 2>/dev/null; then
    echo "Base de datos desactualizada. Sincronizando..."
    if ! alembic stamp head 2>/dev/null; then
        echo "Revisión no encontrada. Reiniciando desde cero..."
        alembic stamp base
        alembic upgrade head
    else
        alembic upgrade head
    fi
fi

echo "1. Generando Nueva Revisión: $MIGRATION_NAME..."
alembic revision --autogenerate -m "$MIGRATION_NAME"

LAST_REV=$(alembic history --verbose | head -n 1 | awk '{print $1}')
if [ -z "$LAST_REV" ] || ! grep -q "def upgrade():" alembic/versions/${LAST_REV}*.py; then
    echo "No se detectaron cambios en el modelo. Saltando el paso de 'upgrade'"
else
    echo "2. Aplicando migración a la base de datos (alembic upgrade head)..."
    alembic upgrade head
    echo "Migración '$MIGRATION_NAME' aplicada con éxito."
fi 
echo "---------------------------------------------------------------------"
echo "------------- Proceso de Migración Finalizado  ----------------------"
echo "---------------------------------------------------------------------"