import pandas as pd
from sqlalchemy import create_engine

def get_engine():
    try:
        # Detalles de conexión proporcionados
        user = "f.chirinosg"
        password = "glRtLDTu01ib"
        host = "ep-proud-cake-84703835-pooler.us-east-2.aws.neon.tech"
        port = "5432"
        database = "neondb"
        
        engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}", connect_args={'options': '-c client_encoding=UTF8'})
        print("Conexión a la base de datos establecida.")
        return engine
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def check_columns():
    engine = get_engine()
    if engine is None:
        return

    tables = ['proyecto', 'lista_equipos', 'maquinaria_out', 'maquinarias_val', 'maquinarias_activos']
    for table in tables:
        try:
            query = f'SELECT * FROM {table} LIMIT 5'
            df = pd.read_sql(query, engine)
            print(f"Columnas en la tabla '{table}': {df.columns.tolist()}")
            print(f"Primeras filas de la tabla '{table}':\n{df.head()}\n")
        except Exception as e:
            print(f"Error al acceder a la tabla '{table}': {e}")

if __name__ == "__main__":
    check_columns()
