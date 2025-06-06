"""
Suite de pruebas para el módulo de algoritmos de ordenamiento.
Este módulo contiene pruebas para verificar la corrección de diversos algoritmos
de ordenamiento, incluyendo quicksort, mergesort, heapsort y radixsort.
"""

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
    """
    Prueba la implementación del algoritmo quicksort.

    Verifica que quicksort ordena correctamente una lista de diccionarios
    según la clave 'CANTIDAD'.
    """
    resultado = sa.quicksort(datos.copy(), key=lambda x: x["CANTIDAD"])
    assert resultado == ordenado_esperado

def test_mergesort():
    """
    Prueba la implementación del algoritmo mergesort.

    Verifica que mergesort ordena correctamente una lista de diccionarios
    según la clave 'CANTIDAD'.
    """
    resultado = sa.mergesort(datos.copy(), key=lambda x: x["CANTIDAD"])
    assert resultado == ordenado_esperado

def test_heapsort():
    """
    Prueba la implementación del algoritmo heapsort.

    Verifica que heapsort ordena correctamente una lista de diccionarios
    según la clave 'CANTIDAD'.
    """
    resultado = sa.heapsort(datos.copy(), key=lambda x: x["CANTIDAD"])
    assert resultado == ordenado_esperado

def test_radixsort():
    """
    Prueba la implementación del algoritmo radixsort.

    Verifica que radixsort ordena correctamente una lista de enteros.
    Nota: Esta prueba usa una entrada simplificada ya que radixsort
    espera enteros en lugar de diccionarios.
    """
    # radixsort espera enteros directamente, así que simplificamos:
    numeros = [5, 1, 4, 2, 3]
    resultado = sa.radixsort(numeros)
    assert resultado == [1, 2, 3, 4, 5]
