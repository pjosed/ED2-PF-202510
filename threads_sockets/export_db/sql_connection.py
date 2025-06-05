"""
Módulo para manejar la conexión y operaciones con la base de datos MySQL.
Este módulo proporciona funciones para establecer conexiones y ejecutar consultas
utilizando credenciales almacenadas en variables de entorno.
"""

from mysql.connector import connect, errorcode, Error
from os import environ
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path #Para que pueda leer el .env que esta fuera de la carpeta

# Carga variables de entorno desde el archivo .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')

# Configuración de la conexión a la base de datos
config = {
    "user": environ['DATABASE_USERNAME'],
    "password": environ['DATABASE_PASSWORD'],
    "host": environ['DATABASE_HOST'],
    "database": environ['DATABASE_NAME'],
    "charset": 'utf8'
}

def get_connection():
    """
    Establece una conexión con la base de datos MySQL.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Objeto de conexión a la base de datos
        None: Si ocurre un error al conectar
        
    Raises:
        Error: Si hay problemas con las credenciales o la base de datos
    """
    try:
        return connect(**config)
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

def get_data(connection: connect, query: str):
    """
    Ejecuta una consulta SQL y retorna los resultados.
    
    Args:
        connection (mysql.connector.connection.MySQLConnection): Conexión a la base de datos
        query (str): Consulta SQL a ejecutar
        
    Returns:
        list: Lista de tuplas con los resultados de la consulta
    """
    my_cursor = connection.cursor()
    my_cursor.execute(query)
    data = my_cursor.fetchall()
    my_cursor.close()
    return data

# Ejemplo de uso
if __name__ == "__main__":
    cnx = get_connection()
    print("Connection established")

    data = get_data(cnx, "SELECT * FROM UN.VENTAS LIMIT 10")

    df = pd.DataFrame(data, columns=['ID_VENTA', 'FECHA_VENTA', 'ID_CLIENTE', 'ID_EMPLEADO',
                      'ID_PRODUCTO', 'CANTIDAD', 'PRECIO_UNITARIO', 'DESCUENTO', 'FORMA_PAGO'])

    print(df)