import socket
import json
import time
import os
import sys
import threading
from load_ventas import cargar_ventas_desde_csv
from algorithms.sorting_algorithms import quicksort, mergesort, heapsort, radixsort

algos = {
    "quicksort": quicksort,
    "mergesort": mergesort,
    "heapsort": heapsort,
    "radixsort": radixsort
}

SERVER = "127.0.0.1"
PORT = 8080

ventas = cargar_ventas_desde_csv()

def ejecutar_algoritmo(nombre_algo):
    print(f"▶ Ejecutando {nombre_algo}...")
    algoritmo = algos[nombre_algo]
    
    inicio = time.time()
    datos_ordenados = algoritmo(ventas.copy(), key=lambda x: x["CANTIDAD"])
    fin = time.time()

    tiempo_total = fin - inicio

    # Guardar archivo ordenado
    with open(f"{nombre_algo}_ordenado.txt", "w") as f:
        f.write(str(datos_ordenados))

    # Enviar resultado por socket
    payload = {
        "algoritmo": nombre_algo,
        "tiempo": tiempo_total,
        "cantidad_datos": len(ventas)
    }

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))
        client.sendall(json.dumps(payload).encode("utf-8"))
        client.close()
        print(f"✅ {nombre_algo} completado y enviado. Tiempo: {tiempo_total:.4f} segundos.")
    except Exception as e:
        print(f"❌ Error al enviar datos de {nombre_algo}: {e}")

    # Guardar en resultados.json
    if os.path.exists("resultados.json"):
        with open("resultados.json", "r") as f:
            resultados = json.load(f)
    else:
        resultados = []

    resultados.append(payload)

    with open("resultados.json", "w") as f:
        json.dump(resultados, f, indent=4)


if __name__ == "__main__":
    print("Algoritmos disponibles:", ", ".join(algos.keys()))
    seleccion = input("⤵ Escribí el nombre del algoritmo a ejecutar o 'todos' para correr todos: ").strip().lower()

    if seleccion == "todos":
        hilos = []
        for nombre in algos:
            hilo = threading.Thread(target=ejecutar_algoritmo, args=(nombre,))
            hilo.start()
            hilos.append(hilo)

        for h in hilos:
            h.join()
        print("✅ Todos los algoritmos completados.")
    elif seleccion in algos:
        ejecutar_algoritmo(seleccion)
    else:
        print("❌ Algoritmo no válido. Intenta con: quicksort, mergesort, heapsort, bubblesort o todos.")

# Comparar resultados

with open("resultados.json", "r") as f:
    resultados = json.load(f)

# Ordenar por tiempo
resultados_ordenados = sorted(resultados, key=lambda x: x["tiempo"])

print("\n📊 Comparativa de algoritmos de ordenamiento:")
print("{:<12} | {:<10} | {:<15}".format("Algoritmo", "Tiempo (s)", "Cantidad de datos"))
print("-" * 45)
for r in resultados_ordenados:
    print("{:<12} | {:<10.5f} | {:<15}".format(r["algoritmo"], r["tiempo"], r["cantidad_datos"]))

# Mostrar el más rápido
ganador = resultados_ordenados[0]
print(f"\n🏆 El algoritmo más rápido fue: {ganador['algoritmo']} con {ganador['tiempo']:.5f} segundos.")