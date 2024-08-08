# data_loader.py
import pandas as pd
from sqlalchemy import create_engine
from db_config import get_engine

def get_connection():
    return get_engine()

def check_columns(engine, table_name):
    with engine.connect() as conn:
        query = f"SELECT * FROM {table_name} LIMIT 5"
        df = pd.read_sql(query, conn)
        print(f"Columnas de {table_name}:", df.columns)

def get_egresos(start_date, end_date):
    engine = get_connection()
    check_columns(engine, 'maquinaria_out')
    query = f'SELECT * FROM maquinaria_out WHERE "FECHADOC" BETWEEN \'{start_date}\' AND \'{end_date}\''
    return pd.read_sql(query, engine)

def get_deudas(start_date, end_date):
    engine = get_connection()
    check_columns(engine, 'maquinarias_activos')
    query = f'SELECT * FROM maquinarias_activos WHERE "Fecha de vencimiento" BETWEEN \'{start_date}\' AND \'{end_date}\''
    return pd.read_sql(query, engine)

def get_ingresos(start_date, end_date):
    engine = get_connection()
    check_columns(engine, 'maquinarias_val')
    query = f'SELECT * FROM maquinarias_val WHERE "Fecha" BETWEEN \'{start_date}\' AND \'{end_date}\''
    return pd.read_sql(query, engine)

def get_proyectos():
    engine = get_connection()
    check_columns(engine, 'proyecto')
    query = "SELECT * FROM proyecto"
    return pd.read_sql(query, engine)

def get_lista_equipos():
    engine = get_connection()
    check_columns(engine, 'lista_equipos')
    query = "SELECT * FROM lista_equipos"
    return pd.read_sql(query, engine)
