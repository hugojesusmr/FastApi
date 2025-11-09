#!/bin/bash

# Cargar variables de entorno
source .env

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Uso: ./restore_backup.sh <archivo_backup>"
    echo "Backups disponibles:"
    ls -la backups/*.sql 2>/dev/null || echo "No hay backups disponibles"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Archivo de backup no encontrado: $BACKUP_FILE"
    exit 1
fi

echo "⚠️  ADVERTENCIA: Esto restaurará la base de datos desde el backup"
echo "Archivo: $BACKUP_FILE"
read -p "¿Continuar? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Restaurando backup..."
    mysql -h${MYSQL_HOST} -P${MYSQL_PORT} -u${MYSQL_USER} -p${MYSQL_PASSWORD} ${MYSQL_DB_NAME} < $BACKUP_FILE
    
    if [ $? -eq 0 ]; then
        echo "✅ Backup restaurado exitosamente"
        echo "Sincronizando Alembic..."
        alembic stamp base
        alembic upgrade head
    else
        echo "❌ Error restaurando backup"
        exit 1
    fi
else
    echo "❌ Operación cancelada"
fi