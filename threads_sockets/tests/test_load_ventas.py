import pytest
from threads_sockets import load_ventas

def test_load_ventas_structure():
    datos = load_ventas.cargar_ventas_desde_csv()
    assert isinstance(datos, list)
    assert len(datos) > 0
    assert isinstance(datos[0], dict)
    assert "VENTA" in datos[0] or "CANTIDAD" in datos[0]

