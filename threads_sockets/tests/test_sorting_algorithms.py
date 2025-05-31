import pytest
from threads_sockets.algorithms import sorting_algorithms as sa

# Datos de prueba
datos = [
    {"CANTIDAD": 5},
    {"CANTIDAD": 1},
    {"CANTIDAD": 4},
    {"CANTIDAD": 2},
    {"CANTIDAD": 3}
]

ordenado_esperado = [
    {"CANTIDAD": 1},
    {"CANTIDAD": 2},
    {"CANTIDAD": 3},
    {"CANTIDAD": 4},
    {"CANTIDAD": 5}
]

def test_quicksort():
    resultado = sa.quicksort(datos.copy(), key=lambda x: x["CANTIDAD"])
    assert resultado == ordenado_esperado

def test_mergesort():
    resultado = sa.mergesort(datos.copy(), key=lambda x: x["CANTIDAD"])
    assert resultado == ordenado_esperado

def test_heapsort():
    resultado = sa.heapsort(datos.copy(), key=lambda x: x["CANTIDAD"])
    assert resultado == ordenado_esperado

def test_radixsort():
    # radixsort espera enteros directamente, así que simplificamos:
    numeros = [5, 1, 4, 2, 3]
    resultado = sa.radixsort(numeros)
    assert resultado == [1, 2, 3, 4, 5]
