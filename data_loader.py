import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st
from db_config import get_engine

# Obtener el motor de la base de datos
engine = get_engine()

# Configurar sesión para manejar transacciones
Session = sessionmaker(bind=engine)
session = Session()

# Funciones para obtener los datos necesarios con caché
@st.cache_data(ttl=600)
def get_egresos(start_date, end_date):
    query = f"""
    SELECT "FECHADOC", "TOTAL", "COD_EQUIPO", "NOMBREPROYECTO", "GLOSA"
    FROM maquinaria_out
    WHERE "FECHADOC" BETWEEN '{start_date}' AND '{end_date}'
    """
    try:
        result = pd.read_sql(query, engine)
        session.commit()  # Confirmar la transacción
        return result
    except Exception as e:
        session.rollback()  # Hacer rollback en caso de error
        st.error(f"Error al obtener egresos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
    finally:
        session.close()  # Asegurarse de cerrar la sesión

@st.cache_data(ttl=600)
def get_deudas(start_date, end_date):
    query = f"""
    SELECT *
    FROM maquinarias_activos
    WHERE "Fecha de vencimiento" BETWEEN '{start_date}' AND '{end_date}'
    """
    try:
        result = pd.read_sql(query, engine)
        session.commit()  # Confirmar la transacción
        return result
    except Exception as e:
        session.rollback()  # Hacer rollback en caso de error
        st.error(f"Error al obtener deudas: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
    finally:
        session.close()  # Asegurarse de cerrar la sesión

@st.cache_data(ttl=600)
def get_ingresos(start_date, end_date):
    query = f"""
    SELECT *
    FROM maquinarias_val
    WHERE "Fecha" BETWEEN '{start_date}' AND '{end_date}'
    """
    try:
        result = pd.read_sql(query, engine)
        session.commit()  # Confirmar la transacción
        return result
    except Exception as e:
        session.rollback()  # Hacer rollback en caso de error
        st.error(f"Error al obtener ingresos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
    finally:
        session.close()  # Asegurarse de cerrar la sesión

@st.cache_data(ttl=600)
def get_proyectos():
    query = """
    SELECT DISTINCT "Proyectos"
    FROM proyecto
    """
    try:
        result = pd.read_sql(query, engine)
        session.commit()  # Confirmar la transacción
        return result
    except Exception as e:
        session.rollback()  # Hacer rollback en caso de error
        st.error(f"Error al obtener proyectos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
    finally:
        session.close()  # Asegurarse de cerrar la sesión

@st.cache_data(ttl=600)
def get_lista_equipos():
    query = """
    SELECT "Id_equipo", "Name"
    FROM lista_equipos
    """
    try:
        result = pd.read_sql(query, engine)
        session.commit()  # Confirmar la transacción
        return result
    except Exception as e:
        session.rollback()  # Hacer rollback en caso de error
        st.error(f"Error al obtener lista de equipos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error
    finally:
        session.close()  # Asegurarse de cerrar la sesión



