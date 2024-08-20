import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from db_config import get_engine

# Obtener el motor de la base de datos
engine = get_engine()

# Funciones para obtener los datos necesarios con caché
@st.cache_data(ttl=600)
def get_egresos(start_date, end_date):
    query = f"""
    SELECT "FECHADOC", "TOTAL", "COD_EQUIPO", "NOMBREPROYECTO", "GLOSA"
    FROM maquinaria_out
    WHERE "FECHADOC" BETWEEN '{start_date}' AND '{end_date}'
    """
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error al obtener egresos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

@st.cache_data(ttl=600)
def get_deudas(start_date, end_date):
    query = f"""
    SELECT *
    FROM maquinarias_activos
    WHERE "Fecha de vencimiento" BETWEEN '{start_date}' AND '{end_date}'
    """
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error al obtener deudas: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

@st.cache_data(ttl=600)
def get_ingresos(start_date, end_date):
    query = f"""
    SELECT *
    FROM maquinarias_val
    WHERE "Fecha" BETWEEN '{start_date}' AND '{end_date}'
    """
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error al obtener ingresos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

@st.cache_data(ttl=600)
def get_proyectos():
    query = """
    SELECT DISTINCT "Proyectos"
    FROM proyecto
    """
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error al obtener proyectos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

@st.cache_data(ttl=600)
def get_lista_equipos():
    query = """
    SELECT "Id_equipo", "Name"
    FROM lista_equipos
    """
    try:
        return pd.read_sql(query, engine)
    except Exception as e:
        st.error(f"Error al obtener lista de equipos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error


