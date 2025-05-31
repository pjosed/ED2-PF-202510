from threads_sockets import load_ventas
import tempfile
import pandas as pd
import os

def test_load_ventas_structure():
    # Crear un archivo CSV temporal de prueba
    contenido = "id,producto,ventas\n1,producto1,100\n2,producto2,200\n"
    
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as temp_csv:
        temp_csv.write(contenido)
        temp_csv.flush()
        temp_path = temp_csv.name

    try:
        # Usar la función con la ruta del archivo temporal
        datos = load_ventas.cargar_ventas_desde_csv(temp_path)
        assert isinstance(datos, list)
        assert len(datos) == 2
        assert all("ventas" in registro for registro in datos)
    finally:
        os.remove(temp_path)  # Limpieza

