import polars as pl
import numpy as np

def format_hours_decimal(horas_decimal):
    if horas_decimal is None or np.isnan(horas_decimal):
        return None
    total_segundos = int(horas_decimal * 3600)
    horas, remanente = divmod(total_segundos, 3600)
    minutos, segundos = divmod(remanente, 60)
    return f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}"

def apply_transformations(df: pl.DataFrame) -> pl.DataFrame:
    lf = df.lazy()
    
    # --- Crear columnas nuevas ---
    columnas_nuevas = [
        'Tiempo_1', 'Etapa_1', 'Horas_1', 'Hrs_1', 'SLA_NO',
        'Tiempo_2', 'Etapa_2', 'Horas_2', 'Hrs_2', 'SLA_Almacen',
        'Tiempo_3', 'Etapa_3', 'Horas_3', 'Hrs_3', 'SLA_Trafico'
    ]

    for col in columnas_nuevas:
        lf = lf.with_columns(pl.lit(None).alias(col))

    # --- Limpiar y transformar columnas a mayúsculas ---
    lf = lf.with_columns([
        pl.col('Tipo_de_solicitud').str.strip_chars().str.to_uppercase().alias('Tipo_de_solicitud'),
        pl.col('Estado').str.strip_chars().str.to_uppercase().alias('Estado'),
        pl.col('Prioridad').str.strip_chars().str.to_uppercase().alias('Prioridad'),
    ])

    # --- Definir filtros como expresiones ---
    condicion_tipo_solicitud = pl.col('Tipo_de_solicitud').is_in(['INVENTARIO ATT','ALMACÉN ATT', 'SPMS + ATT', 'SPMS'])
    condicion_tipo_spms = pl.col('Tipo_de_solicitud').is_in(['SPMS', 'SPMS + ATT'])
    condicion_estado = pl.col('Estado').is_in(['CLOSED COMPLETE','CERRADO','CERRADO INCOMPLETO'])
    condicion_motivo = df['Motivo_del_Estado'] == 'ATENCIÓN COMPLETADA'
    
    filtro_General = condicion_tipo_solicitud & condicion_estado & condicion_motivo
    filtro_spms = condicion_tipo_spms & condicion_estado & condicion_motivo
    
    filtro_prioridad_baja_media = pl.col('Prioridad').is_in(['MODERADA', 'BAJA', 'MEDIA','EN PLANIFICACIÓN'])
    filtro_prioridad_alta_critica = pl.col('Prioridad').is_in(['CRÍTICA', 'ALTA'])

    
    # 1. Cálculo base para General
    lf = lf.with_columns([
        pl.when(filtro_General)
        .then((pl.col('Fecha_solicitud_almacén') - pl.col('Fecha_de_creación')).dt.total_seconds().abs() / 86400)
        .otherwise(None).alias('Tiempo_1'),
        pl.when(filtro_General)
        .then((pl.col('Fecha_solicitud_almacén') - pl.col('Fecha_de_creación')).dt.total_seconds().abs() / 3600)
        .otherwise(None).alias('Horas_1'),
        pl.when(filtro_General)
        .then('Etapa_1').otherwise(None).alias('Etapa_1'),
    ])

    #2. Sobrescribe para SPMS donde corresponda
    lf = lf.with_columns([
        pl.when(filtro_spms)
        .then((pl.col('Fecha_solicitud_a_proveedor') - pl.col('Fecha_de_creación')).dt.total_seconds().abs() / 86400)
        .otherwise(pl.col('Tiempo_1')).alias('Tiempo_1'),
        pl.when(filtro_spms)
        .then((pl.col('Fecha_solicitud_a_proveedor') - pl.col('Fecha_de_creación')).dt.total_seconds().abs() / 3600)
        .otherwise(pl.col('Horas_1')).alias('Horas_1'),
        pl.when(filtro_spms)
        .then('Etapa_1').otherwise(pl.col('Etapa_1')).alias('Etapa_1'),
    ])

    # 3. SLA NO para cada caso, también en pasos separados
    lf = lf.with_columns([
        pl.when(filtro_General & filtro_prioridad_baja_media)
        .then(pl.when(pl.col('Horas_1') <= 24).then(pl.lit('Cumple')).otherwise(pl.lit('No Cumple')))
        .otherwise(pl.col('SLA_NO')).alias('SLA_NO')
    ])
    lf = lf.with_columns([
        pl.when(filtro_General & filtro_prioridad_alta_critica)
        .then(pl.when(pl.col('Horas_1') <= 3).then(pl.lit('Cumple')).otherwise(pl.lit('No Cumple')))
        .otherwise(pl.col('SLA_NO')).alias('SLA_NO')
    ])
    lf = lf.with_columns([
        pl.when(filtro_spms & filtro_prioridad_baja_media)
        .then(pl.when(pl.col('Horas_1') <= 24).then(pl.lit('Cumple')).otherwise(pl.lit('No Cumple')))
        .otherwise(pl.col('SLA_NO')).alias('SLA_NO')
    ])
    lf = lf.with_columns([
        pl.when(filtro_spms & filtro_prioridad_alta_critica)
        .then(pl.when(pl.col('Horas_1') <= 3).then(pl.lit('Cumple')).otherwise(pl.lit('No Cumple')))
        .otherwise(pl.col('SLA_NO')).alias('SLA_NO')
    ])

    # Aplica la función personalizada
    lf = lf.with_columns([
        pl.col('Horas_1').map_elements(format_hours_decimal, return_dtype=pl.Utf8).alias('Hrs_1'),
        pl.col('Horas_2').map_elements(format_hours_decimal, return_dtype=pl.Utf8).alias('Hrs_2'),
        pl.col('Horas_3').map_elements(format_hours_decimal, return_dtype=pl.Utf8).alias('Hrs_3'),
    ])

    return lf.fill_null(pl.lit(None)).collect()