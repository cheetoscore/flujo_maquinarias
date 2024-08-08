# db_config.py
import psycopg2
from sqlalchemy import create_engine

# Configuración de la conexión a la base de datos
def get_db_connection():
    conn = psycopg2.connect(
        host='ep-proud-cake-84703835-pooler.us-east-2.aws.neon.tech',
        database='neondb',
        user='f.chirinosg',
        password='glRtLDTu01ib',
        port='5432'
    )
    return conn

# Configuración del motor SQLAlchemy
def get_engine():
    engine = create_engine('postgresql+psycopg2://f.chirinosg:glRtLDTu01ib@ep-proud-cake-84703835-pooler.us-east-2.aws.neon.tech/neondb')
    return engine

engine = get_engine()

conn = get_db_connection()
engine = get_engine()
