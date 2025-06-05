# export/export_analysis.py

"""
Módulo para exportar y analizar datos de ventas desde la base de datos.
Este módulo realiza la exportación de datos a formatos CSV y JSON,
y realiza un análisis comparativo de los tiempos de lectura.
"""

from sql_connection import get_connection, get_data
import pandas as pd
import time
import sys
import os

# Añadir el directorio padre al path para importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def exportar_datos():
    """
    Exporta los datos de ventas a formatos CSV y JSON.
    
    Returns:
        tuple: (tamaño_csv, tamaño_json, tiempo_csv, tiempo_json)
    """
    # Conexión
    cnx = get_connection()
    print("Conexión establecida.")

    # Consulta
    query = "SELECT * FROM UN.VENTAS"
    data = get_data(cnx, query)

    column_names = ['ID_VENTA', 'FECHA_VENTA', 'ID_CLIENTE', 'ID_EMPLEADO',
                    'ID_PRODUCTO', 'CANTIDAD', 'PRECIO_UNITARIO', 'DESCUENTO', 'FORMA_PAGO']

    df = pd.DataFrame(data, columns=column_names)

    # Exportar
    csv_file = "ventas.csv"
    json_file = "ventas.json"

    df.to_csv(csv_file, index=False)
    df.to_json(json_file, orient="records", lines=True)

    # Tamaño
    csv_size = os.path.getsize(csv_file) / 1024
    json_size = os.path.getsize(json_file) / 1024

    print(f"Tamaño CSV: {csv_size:.2f} KB")
    print(f"Tamaño JSON: {json_size:.2f} KB")

    # Tiempos de lectura
    start_csv = time.perf_counter()
    _ = pd.read_csv(csv_file)
    end_csv = time.perf_counter()

    start_json = time.perf_counter()
    _ = pd.read_json(json_file, lines=True)
    end_json = time.perf_counter()

    tiempo_csv = end_csv - start_csv
    tiempo_json = end_json - start_json

    print(f"Tiempo de lectura CSV: {tiempo_csv:.4f} s")
    print(f"Tiempo de lectura JSON: {tiempo_json:.4f} s")

    return csv_size, json_size, tiempo_csv, tiempo_json

if __name__ == "__main__":
    exportar_datos()