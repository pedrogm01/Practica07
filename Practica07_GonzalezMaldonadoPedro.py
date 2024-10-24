import os

def leer_archivos_desde_txt(filename):
    file_sizes = []
    with open(filename, 'r') as f:
        for line in f:
            nombre, size = line.split(',')
            size = int(size.strip().replace('kb', ''))  # Convertir el tamaño a entero
            file_sizes.append((nombre.strip(), size))  # Guardar como una tupla (nombre, tamaño)
    return file_sizes

def first_fit(memory_blocks, file_sizes):
    assignments = []
    for file_name, file_size in file_sizes:
        assigned = False
        for i, block in enumerate(memory_blocks):
            if block >= file_size:
                assignments.append((file_name, file_size, block))
                memory_blocks[i] -= file_size  # Actualizamos el bloque de memoria disponible
                assigned = True
                break
        if not assigned:
            assignments.append((file_name, file_size, None))  # No se encontró un bloque adecuado
    return assignments

def best_fit(memory_blocks, file_sizes):
    assignments = []
    for file_name, file_size in file_sizes:
        best_index = None
        best_fit_size = float('inf')
        for i, block in enumerate(memory_blocks):
            if block >= file_size and block < best_fit_size:
                best_fit_size = block
                best_index = i
        if best_index is not None:
            assignments.append((file_name, file_size, memory_blocks[best_index]))
            memory_blocks[best_index] -= file_size  # Actualizamos el bloque de memoria disponible
        else:
            assignments.append((file_name, file_size, None))  # No se encontró un bloque adecuado
    return assignments

def worst_fit(memory_blocks, file_sizes):
    assignments = []
    for file_name, file_size in file_sizes:
        worst_index = None
        worst_fit_size = -1
        for i, block in enumerate(memory_blocks):
            if block >= file_size and block > worst_fit_size:
                worst_fit_size = block
                worst_index = i
        if worst_index is not None:
            assignments.append((file_name, file_size, memory_blocks[worst_index]))
            memory_blocks[worst_index] -= file_size  # Actualizamos el bloque de memoria disponible
        else:
            assignments.append((file_name, file_size, None))  # No se encontró un bloque adecuado
    return assignments

def next_fit(memory_blocks, file_sizes):
    assignments = []
    start_index = 0  # Recordar el último bloque donde se realizó una asignación
    for file_name, file_size in file_sizes:
        assigned = False
        for i in range(start_index, len(memory_blocks)):
            if memory_blocks[i] >= file_size:
                assignments.append((file_name, file_size, memory_blocks[i]))
                memory_blocks[i] -= file_size
                start_index = i  # Actualizamos el índice de inicio para la próxima asignación
                assigned = True
                break
        if not assigned:
            assignments.append((file_name, file_size, None))  # No se encontró un bloque adecuado
    return assignments

def show_results(assignments):
    print("\n")
    for file_name, file_size, block in assignments:
        if block is not None:
            print(f"El archivo '{file_name}' de {file_size} Kb fue asignado al bloque de {block} Kb.")
        else:
            print(f"El archivo '{file_name}' de {file_size} Kb no pudo ser asignado a ningún bloque.")

def limpiar_pantalla():
    # Limpiar la pantalla dependiendo del sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Espacios de memoria disponibles
    memory_blocks = [1000, 400, 1800, 700, 900, 1200, 1500]
    
    # Leer los archivos desde archivos.txt
    file_sizes = leer_archivos_desde_txt('archivos.txt')

    while True:
        # Mostrar los bloques de memoria disponibles antes de la asignación
        print("\nBloques de memoria disponibles:")
        print(memory_blocks)

        # Preguntar por el algoritmo a usar
        print("\nSeleccione el algoritmo de asignación de memoria:")
        print("1. Primer ajuste")
        print("2. Mejor ajuste")
        print("3. Peor ajuste")
        print("4. Siguiente ajuste")
        choice = int(input("Opción: "))

        # Realizar asignación de acuerdo al algoritmo
        if choice == 1:
            assignments = first_fit(memory_blocks[:], file_sizes)
        elif choice == 2:
            assignments = best_fit(memory_blocks[:], file_sizes)
        elif choice == 3:
            assignments = worst_fit(memory_blocks[:], file_sizes)
        elif choice == 4:
            assignments = next_fit(memory_blocks[:], file_sizes)
        else:
            print("Opción no válida.")
            continue

        # Mostrar resultados
        show_results(assignments)

        # Preguntar si el usuario quiere intentar nuevamente
        retry = input("\n¿Desea intentar nuevamente? (s/n): ").lower()
        if retry == 's':
            limpiar_pantalla()
        else:
            break

if __name__ == "__main__":
    main()
