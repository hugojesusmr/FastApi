import pandas as pd
import numpy as np


def format_hours_decimal(horas_decimal):
    if horas_decimal is None or np.isnan(horas_decimal):
        return None
    total_segundos = int(horas_decimal * 3600)
    horas, remanente = divmod(total_segundos, 3600)
    minutos, segundos = divmod(remanente, 60)
    return f"{int(horas):02}:{int(minutos):02}:{int(segundos):02}"


def apply_transformations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica transformaciones directamente con Pandas
    """
    return procesar_datos(df)


def procesar_datos(df):
    """
    Realiza los calculos de Horas, Tiempos y SLA para cada etapa.
    """
    # 1.--- Comprobación si hay registros por procesar    
    if df.empty:
        print("No hay Registros por procesar :(")
        return df

    # Convertir columnas de fecha
    columnas_fecha = [
        'fecha_de_creacion', 'fecha_de_envio_del_proveedor', 'fecha_entrega_en_sitio',
        'fecha_entrega_en_sitio_spms', 'fecha_liberacion_almacen', 
        'fecha_solicitud_a_proveedor', 'fecha_solicitud_almacen'
    ]

    for col in columnas_fecha:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Inicializar columnas calculadas ANTES de usarlas
    df['tiempo_1'] = None
    df['etapa_1'] = None
    df['horas_1'] = None
    df['hrs_1'] = None
    df['dias_1'] = None
    df['sla_no'] = None
    df['tiempo_2'] = None
    df['etapa_2'] = None
    df['horas_2'] = None
    df['hrs_2'] = None
    df['dias_2'] = None
    df['sla_almacen'] = None
    df['tiempo_3'] = None
    df['etapa_3'] = None
    df['horas_3'] = None
    df['hrs_3'] = None
    df['dias_3'] = None
    df['sla_trafico'] = None
    df['es_top_10'] = None
    df['status_calculo'] = None

    df['prioridad'] = df['prioridad'].str.replace(r'^\d+\s*-\s*', '', regex=True)
    df['prioridad'] = df['prioridad'].str.strip().str.upper()
    df['tipo_de_solicitud'] = df['tipo_de_solicitud'].str.strip().str.upper()
    df['estado'] = df['estado'].str.strip().str.upper()
    df['motivo_del_estado'] = df['motivo_del_estado'].str.strip().str.upper()

    # --- Reglas de Filtrado Almacen ATT , SPMS + ATT , SPMS ----
    condicion_tipo_solicitud = df['tipo_de_solicitud'].isin(['INVENTARIO ATT','ALMACÉN ATT', 'SPMS + ATT','SPMS'])

    # -- Reglas de Filtrado 'SPMS','SPMS + ATT' --- 
    condicion_tipo_spms = df['tipo_de_solicitud'].isin(['SPMS','SPMS + ATT']) 

    # --- Reglas de Filtrado General para prioridades ---
    condicion_estado = df['estado'].isin(['CLOSED COMPLETE','CERRADO','CERRADO INCOMPLETO'])

    condicion_motivo = df['motivo_del_estado'] == 'ATENCIÓN COMPLETADA'

    # --- Combina ambas condiciones para un solo filtro ---
    filtro_General = condicion_tipo_solicitud & condicion_estado & condicion_motivo
    filtro_spms = condicion_tipo_spms & condicion_estado & condicion_motivo
    
    # --- Filtro Priorodad Baja, Media, Planificación 24 Hrs para Atender ---
    filtro_prioridad_baja_media = df['prioridad'].isin(['MODERADA','BAJA', 'MEDIA','EN PLANIFICACIÓN'])

    # --- Filtro Prioridad Alta, Critica 3 Hrs a nivel Logistica ---
    filtro_prioridad_alta_critica = df['prioridad'].isin(['CRÍTICA','ALTA'])

    ########################################## ETAPA 1 INVENTARIO ATT , SPMS + ATT ########################################

    # ----- Logica para Filtrado 1 : ['Tiempo 1', 'Etapa 1', 'Horas 1','Hrs-1', 'SLA NO] ---
  
    tiempo_transcurrido_1 = abs(df['fecha_de_creacion'] - df['fecha_solicitud_almacen'])

    # --- Asigna la diferencia en días decimales a Tiempo 1 ---
    df.loc[filtro_General, 'tiempo_1'] = tiempo_transcurrido_1.dt.total_seconds() / 86400   

    # --- Asigna el valor por defecto 'Etapa 1 ---
    df.loc[filtro_General, 'etapa_1'] = 'Etapa 1'

    # --- Asigna las hrs en días decimales a Horas 1 ---
    df.loc[filtro_General, 'horas_1'] = tiempo_transcurrido_1.dt.total_seconds() / 3600

    # --- Conversión de los Días a Texto ---
    df.loc[filtro_General,'dias_1'] = tiempo_transcurrido_1.astype(str).replace('0 days','')

    # --- Lògica para el SLA NO 24 hrs par atender ---
    df.loc[filtro_General & filtro_prioridad_baja_media, 'sla_no'] = np.where(df.loc[filtro_General & filtro_prioridad_baja_media,'horas_1'] <= 24, 'Cumple', 'No Cumple')

    # --- Logica para el SLA NO 3 hrs para atender ---
    df.loc[filtro_General & filtro_prioridad_alta_critica, 'sla_no'] = np.where(df.loc[filtro_General & filtro_prioridad_alta_critica, 'horas_1'] <= 3, 'Cumple','No Cumple')

   ###########################################  ETAPA 1 'SPMS,SPMS + ATT' ###################################################

    # ----- Logica para Filtrado SPMS: ['Tiempo 1', 'Etapa 1', 'Horas 1','Hrs-1', 'SLA NO] ---

    # --- Calcula la diferencia para Tiempo 1 ---
    tiempo_transcurrido_1_spms = abs(df['fecha_de_creacion'] - df['fecha_solicitud_a_proveedor'])

    # --- Asignar la diferencia en días decimales a Tiempo 1 ---
    df.loc[filtro_spms, 'tiempo_1'] = tiempo_transcurrido_1_spms.dt.total_seconds() / 86400

    # --- Asignar el valor por defecto Etapa 1  ---
    df.loc[filtro_spms, 'etapa_1'] = 'Etapa 1'

    # --- Asignar las Hrs en Días decimales a Hrs 1 ---
    df.loc[filtro_spms, 'horas_1'] = tiempo_transcurrido_1_spms.dt.total_seconds() / 3600

    # --- Conversión de los Días a Texto ---
    df.loc[filtro_spms,'dias_1'] = tiempo_transcurrido_1_spms.astype(str).replace('0 days','')

    # --- Lógica para el SLA NO 24 hrs para atender ---
    df.loc[filtro_spms & filtro_prioridad_baja_media, 'sla_no'] = np.where(df.loc[filtro_spms & filtro_prioridad_baja_media, 'horas_1'] <= 24, 'Cumple', 'No Cumple')

    # --- Lógica para el SLA NO 3 hrs para atender ---
    df.loc[filtro_spms & filtro_prioridad_alta_critica, 'sla_no'] = np.where(df.loc[filtro_spms & filtro_prioridad_alta_critica, 'horas_1'] <= 3, 'Cumple', 'No Cumple')

    # --- Crea una nueva columna para el formato de horas ---
    df['hrs_1'] = df['horas_1'].apply(format_hours_decimal)

    ####################################           ETAPA 2          #######################################################

    # ----- Logica para Filtrado 2 INVENTARIO ATT Y SPMS + ATT:: ['Tiempo 2', 'Etapa 2', 'Horas 2','Hrs-2', 'SLA Almacen'] ---

    # --- Calcular la diferencia parta Timepo 2 ---
    tiempo_transcurrido_2 = abs(df['fecha_solicitud_almacen'] - df['fecha_liberacion_almacen'])

    # --- Asignar la diferencia en dìas decimales a 'Tiempo 2' ---
    df.loc[filtro_General, 'tiempo_2'] = tiempo_transcurrido_2.dt.total_seconds() / 86400

    # Asigna el valor por defecto 'Etapa 2 ---'
    df.loc[filtro_General, 'etapa_2'] = 'Etapa 2'

    # --- Asignar las hrs en dìas decimales a 'Horas 2' ---
    df.loc[filtro_General, 'horas_2'] = tiempo_transcurrido_2.dt.total_seconds() / 3600

        # --- Conversión de los Días a Texto ---
    df.loc[filtro_General,'dias_2'] = tiempo_transcurrido_2.astype(str).replace('0 days','')

    # --- Lògica para el SLA NO 24 hrs par atender ---
    df.loc[filtro_General & filtro_prioridad_baja_media, 'sla_almacen'] = np.where(df.loc[filtro_General & filtro_prioridad_baja_media,'horas_2']<= 24, 'Cumple', 'No Cumple')

    # --- Logica para el SLA NO 3 hrs para atender ---
    df.loc[filtro_General & filtro_prioridad_alta_critica, 'sla_almacen'] = np.where(df.loc[filtro_General & filtro_prioridad_alta_critica, 'horas_2'] <=3, 'Cumple','No Cumple')

    # --- Crea una nueva columna para el formato de horas ---
    df['hrs_2'] = df.loc[filtro_General,'horas_2'].apply(format_hours_decimal)

    ######################################             ETAPA 3           ###################################################

    # ----- Logica para Filtrado 3 INVENTARIO ATT Y SPMS + ATT:: ['Tiempo 3', 'Etapa 3', 'Horas 3','Hrs-3', 'SLA Trafico'] ---

    tiempo_transcurrido_3 = abs(df['fecha_liberacion_almacen'] - df['fecha_entrega_en_sitio'])

    # --- Asignar la diferencia en dìas decimales a 'Tiempo 3' ---
    df.loc[filtro_General, 'tiempo_3'] = tiempo_transcurrido_3.dt.total_seconds() / 86400

    # --- Asigna el valor por defecto 'Etapa 3 ---'
    df.loc[filtro_General, 'etapa_3'] = 'Etapa 3'

    # --- Asignar las hrs en dìas decimales a 'Horas 3 ---'
    df.loc[filtro_General, 'horas_3'] = tiempo_transcurrido_3.dt.total_seconds() / 3600

        # --- Conversión de los Días a Texto ---
    df.loc[filtro_General,'dias_3'] = tiempo_transcurrido_3.astype(str).replace('0 days','')

    # --- Lògica para el SLA NO 24 hrs par atender ---
    df.loc[filtro_General & filtro_prioridad_baja_media, 'sla_trafico'] = np.where(df.loc[filtro_General & filtro_prioridad_baja_media,'horas_3']<= 24, 'Cumple', 'No Cumple')

    # --- Logica para el SLA NO 3 hrs para atender ---
    df.loc[filtro_General & filtro_prioridad_alta_critica, 'sla_trafico'] = np.where(df.loc[filtro_General & filtro_prioridad_alta_critica, 'horas_3'] <=3, 'Cumple','No Cumple')

    # --- Crea una nueva columna para el formato de horas ---
    df['hrs_3'] = df.loc[filtro_General,'horas_3'].apply(format_hours_decimal)

    # --- Calculo del Tiempo Maximo en Horas ---
    df['dias_1_td'] = pd.to_timedelta(df['dias_1'])

    # --- Ordenar el Dataframe para encontrar los 10 tiempos maximos ---
    df_ordenado = df.sort_values(by="dias_1_td", ascending=False)

    # --- Selccionar los 10 incientes que no sean nulos
    top_10_tareas = df_ordenado.dropna(subset=['dias_1_td']).head(10).index

    df['es_top_10'] = 'No'
    df.loc[top_10_tareas, 'es_top_10'] = 'Si'

    df = df.drop(columns=['dias_1_td'], errors='ignore')

    status_calculado = filtro_General
    df.loc[status_calculado, 'status_calculo'] = 'Procesado'
    
    return df