"""
Módulo para cargar datos de ventas desde archivos CSV.
Este módulo proporciona funciones para leer y procesar datos de ventas
desde archivos CSV, con manejo de rutas relativas y absolutas.
"""

import pandas as pd
import os

def cargar_ventas_desde_csv(ruta_csv=None):
    """
    Carga datos de ventas desde un archivo CSV.
    
    Args:
        ruta_csv (str, optional): Ruta al archivo CSV. Si es None, usa la ruta por defecto.
        
    Returns:
        list: Lista de diccionarios con los datos de ventas
        
    Example:
        >>> datos = cargar_ventas_desde_csv()
        >>> print(len(datos))
        1000
    """
    if ruta_csv is None:
        ruta_actual = os.path.dirname(__file__)
        ruta_csv = os.path.join(ruta_actual, "..", "ventas.csv")
    
    df = pd.read_csv(ruta_csv)
    return df.to_dict(orient='records')

