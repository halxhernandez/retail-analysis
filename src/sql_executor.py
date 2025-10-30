"""
Módulo para ejecutar queries SQL sobre datos de Retail (SQL Server)
"""

import pandas as pd
import pyodbc
from pathlib import Path


class SQLServerExecutor:
    """Ejecutor de queries SQL sobre base de datos SQL Server"""

    def __init__(self, server: str, database: str, username: str = None, password: str = None, trusted_connection: bool = True):
        """
        Inicializa la conexión con SQL Server.

        Args:
            server (str): Nombre del servidor o instancia de SQL Server (ej. 'localhost\\SQLEXPRESS')
            database (str): Nombre de la base de datos
            username (str): Usuario SQL (si no se usa autenticación de Windows)
            password (str): Contraseña (si aplica)
            trusted_connection (bool): Usa autenticación de Windows si es True
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.trusted_connection = trusted_connection
        self.conn = None

    def connect(self):
        """Establece conexión con SQL Server"""
        if self.trusted_connection:
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
        else:
            conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};"

        self.conn = pyodbc.connect(conn_str)
        print(f"✅ Conectado a SQL Server: {self.server} / BD: {self.database}")

    def create_table_from_df(self, df: pd.DataFrame, table_name: str = 'retail_transactions'):
        """
        Crea o reemplaza una tabla en SQL Server a partir de un DataFrame.
        (Usa SQLAlchemy para cargar los datos fácilmente)
        """
        from sqlalchemy import create_engine

        # Cadena de conexión compatible con SQLAlchemy
        engine_url = f"mssql+pyodbc://{self.server}/{self.database}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        engine = create_engine(engine_url)

        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"📦 Tabla '{table_name}' creada con {len(df)} registros")

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Ejecuta una query SQL y devuelve un DataFrame con los resultados.
        """
        if self.conn is None:
            self.connect()

        return pd.read_sql(query, self.conn)

    def execute_query_file(self, query_file: str, query_number: int = 1) -> pd.DataFrame:
        """
        Ejecuta una query específica dentro de un archivo .sql
        Las queries se separan por comentarios de la forma '-- N.'
        """
        with open(query_file, 'r', encoding='utf-8') as f:
            content = f.read()

        queries = []
        current_query = []

        for line in content.split('\n'):
            if line.strip().startswith('-- ') and '. ' in line and not line.startswith('-- ='):
                if current_query:
                    queries.append('\n'.join(current_query))
                current_query = []
            elif line.strip() and not line.strip().startswith('--'):
                current_query.append(line)

        if current_query:
            queries.append('\n'.join(current_query))

        if query_number < 1 or query_number > len(queries):
            raise ValueError(f"Query {query_number} no existe. Hay {len(queries)} queries disponibles.")

        return self.execute_query(queries[query_number - 1])

    def close(self):
        """Cierra la conexión"""
        if self.conn:
            self.conn.close()
            print("🔒 Conexión cerrada")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    print("Módulo SQLServerExecutor listo para ejecutar queries en SQL Server.")
