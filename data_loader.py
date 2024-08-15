import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from db_config import get_engine
import time

# Obtener el motor de la base de datos
engine = get_engine()

def retry_connection(func):
    """Decorator to retry a function in case of a database connection error."""
    def wrapper(*args, **kwargs):
        retries = 3
        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                st.error(f"Error de conexión a la base de datos: {e}. Reintentando...")
                time.sleep(2)
                continue
        st.error(f"Error persistente al conectar a la base de datos después de {retries} intentos.")
        return pd.DataFrame()
    return wrapper

@st.cache_data(ttl=600)
@retry_connection
def get_egresos(start_date, end_date):
    query = f"""
    SELECT "FECHADOC", "TOTAL", "COD_EQUIPO", "NOMBREPROYECTO", "GLOSA", "SOCIO DE NEGOCIOS"
    FROM maquinaria_out
    WHERE "FECHADOC" BETWEEN '{start_date}' AND '{end_date}'
    """
    with engine.connect() as connection:
        return pd.read_sql(query, connection)

@st.cache_data(ttl=600)
@retry_connection
def get_deudas(start_date, end_date):
    query = f"""
    SELECT *
    FROM maquinarias_activos
    WHERE "Fecha de vencimiento" BETWEEN '{start_date}' AND '{end_date}'
    """
    with engine.connect() as connection:
        return pd.read_sql(query, connection)

@st.cache_data(ttl=600)
@retry_connection
def get_ingresos(start_date, end_date):
    query = f"""
    SELECT *
    FROM maquinarias_val
    WHERE "Fecha" BETWEEN '{start_date}' AND '{end_date}'
    """
    with engine.connect() as connection:
        return pd.read_sql(query, connection)

@st.cache_data(ttl=600)
@retry_connection
def get_proyectos():
    query = """
    SELECT DISTINCT "Proyectos"
    FROM proyecto
    """
    with engine.connect() as connection:
        return pd.read_sql(query, connection)

@st.cache_data(ttl=600)
@retry_connection
def get_lista_equipos():
    query = """
    SELECT "Id_equipo", "Name"
    FROM lista_equipos
    """
    with engine.connect() as connection:
        return pd.read_sql(query, connection)



