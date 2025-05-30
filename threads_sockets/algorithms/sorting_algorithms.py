# Algoritmos de ordenamiento

def quicksort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    pivot_key = key(pivot)
    left = [x for x in arr[1:] if key(x) < pivot_key]
    middle = [x for x in arr if key(x) == pivot_key]
    right = [x for x in arr[1:] if key(x) > pivot_key]
    return quicksort(left, key=key) + middle + quicksort(right, key=key)

def mergesort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mergesort(arr[:mid], key=key)
    right = mergesort(arr[mid:], key=key)
    return merge(left, right, key)

def merge(left, right, key):
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
    import heapq
    decorated = [(key(item), i, item) for i, item in enumerate(arr)]  # avoid comparing values directly
    heapq.heapify(decorated)
    return [heapq.heappop(decorated)[2] for _ in range(len(decorated))]

def radixsort(arr, key=lambda x: x):
    if not arr:
        return []

    # Convertimos los valores clave a enteros
    int_arr = [(x, int(key(x))) for x in arr]

    # Encontramos el número máximo para saber la cantidad de dígitos
    max_num = max([val for _, val in int_arr])
    exp = 1

    while max_num // exp > 0:
        # Hacemos el conteo para cada dígito
        buckets = [[] for _ in range(10)]
        for original, val in int_arr:
            digit = (val // exp) % 10
            buckets[digit].append((original, val))

        int_arr = [item for sublist in buckets for item in sublist]
        exp *= 10

    # Retornamos la lista original ordenada
    return [item[0] for item in int_arr]
