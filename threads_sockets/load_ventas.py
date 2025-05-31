import pandas as pd
import os

def cargar_ventas_desde_csv(ruta_csv=None):
    if ruta_csv is None:
        ruta_actual = os.path.dirname(__file__)
        ruta_csv = os.path.join(ruta_actual, "..", "ventas.csv")
    
    df = pd.read_csv(ruta_csv)
    return df.to_dict(orient='records')

