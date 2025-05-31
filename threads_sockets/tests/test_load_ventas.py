import pandas as pd
import tempfile
import os
from threads_sockets import load_ventas

def test_load_ventas_structure():
    # Crear un archivo CSV temporal con contenido mínimo
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
        tmp.write("id,producto,ventas\n1,A,100\n2,B,200\n")
        test_csv_path = tmp.name

    try:
        df = load_ventas.load_ventas(test_csv_path)  # Tu función debe aceptar el path como parámetro
        assert not df.empty
        assert set(df.columns) == {"id", "producto", "ventas"}
    finally:
        os.remove(test_csv_path)  # Elimina el archivo temporal
