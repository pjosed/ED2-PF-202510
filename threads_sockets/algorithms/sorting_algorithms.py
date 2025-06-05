"""
Módulo que contiene implementaciones de diferentes algoritmos de ordenamiento.
Cada algoritmo está optimizado para trabajar con diccionarios y permite especificar
una función key para determinar el criterio de ordenamiento.
"""

def quicksort(arr, key=lambda x: x):
    """
    Implementación del algoritmo QuickSort.
    
    Args:
        arr (list): Lista a ordenar
        key (function): Función que extrae el valor de comparación de cada elemento
        
    Returns:
        list: Lista ordenada
        
    Example:
        >>> datos = [{"valor": 3}, {"valor": 1}, {"valor": 2}]
        >>> quicksort(datos, key=lambda x: x["valor"])
        [{"valor": 1}, {"valor": 2}, {"valor": 3}]
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    pivot_key = key(pivot)
    left = [x for x in arr[1:] if key(x) < pivot_key]
    middle = [x for x in arr if key(x) == pivot_key]
    right = [x for x in arr[1:] if key(x) > pivot_key]
    return quicksort(left, key=key) + middle + quicksort(right, key=key)

def mergesort(arr, key=lambda x: x):
    """
    Implementación del algoritmo MergeSort.
    
    Args:
        arr (list): Lista a ordenar
        key (function): Función que extrae el valor de comparación de cada elemento
        
    Returns:
        list: Lista ordenada
        
    Example:
        >>> datos = [{"valor": 3}, {"valor": 1}, {"valor": 2}]
        >>> mergesort(datos, key=lambda x: x["valor"])
        [{"valor": 1}, {"valor": 2}, {"valor": 3}]
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mergesort(arr[:mid], key=key)
    right = mergesort(arr[mid:], key=key)
    return merge(left, right, key)

def merge(left, right, key):
    """
    Función auxiliar para MergeSort que combina dos listas ordenadas.
    
    Args:
        left (list): Lista ordenada izquierda
        right (list): Lista ordenada derecha
        key (function): Función que extrae el valor de comparación
        
    Returns:
        list: Lista combinada y ordenada
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def heapsort(arr, key=lambda x: x):
    """
    Implementación del algoritmo HeapSort utilizando heapq.
    
    Args:
        arr (list): Lista a ordenar
        key (function): Función que extrae el valor de comparación de cada elemento
        
    Returns:
        list: Lista ordenada
        
    Example:
        >>> datos = [{"valor": 3}, {"valor": 1}, {"valor": 2}]
        >>> heapsort(datos, key=lambda x: x["valor"])
        [{"valor": 1}, {"valor": 2}, {"valor": 3}]
    """
    import heapq
    decorated = [(key(item), i, item) for i, item in enumerate(arr)]
    heapq.heapify(decorated)
    return [heapq.heappop(decorated)[2] for _ in range(len(decorated))]

def radixsort(arr, key=lambda x: x):
    """
    Implementación del algoritmo RadixSort para números enteros.
    
    Args:
        arr (list): Lista a ordenar
        key (function): Función que extrae el valor entero de comparación
        
    Returns:
        list: Lista ordenada
        
    Example:
        >>> datos = [{"valor": 3}, {"valor": 1}, {"valor": 2}]
        >>> radixsort(datos, key=lambda x: x["valor"])
        [{"valor": 1}, {"valor": 2}, {"valor": 3}]
    """
    if not arr:
        return []

    int_arr = [(x, int(key(x))) for x in arr]
    max_num = max([val for _, val in int_arr])
    exp = 1

    while max_num // exp > 0:
        buckets = [[] for _ in range(10)]
        for original, val in int_arr:
            digit = (val // exp) % 10
            buckets[digit].append((original, val))

        int_arr = [item for sublist in buckets for item in sublist]
        exp *= 10

    return [item[0] for item in int_arr]
