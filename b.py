# Función para mostrar el menú principal
def mostrar_menu():
    print("______JUEGO 4 en línea______")  # Muestra el título del juego
    print("1. Comenzar Juego")  # Opción para comenzar un nuevo juego
    print("2. Juegos Realizados")  # Opción para ver los juegos realizados
    print("3. Salir")  # Opción para salir del juego
    opcion = input("Seleccione una opción (1/2/3): ")  # Solicita al usuario que seleccione una opción
    return opcion  # Devuelve la opción seleccionada

# Función para verificar si hay un ganador
def verificar_ganador(tablero):
    # Verifica filas, columnas y diagonales para un ganador
    for fila in range(len(tablero)):
        for col in range(len(tablero[0]) - 3):
            if tablero[fila][col] == tablero[fila][col + 1] == tablero[fila][col + 2] == tablero[fila][col + 3] != " ":
                return tablero[fila][col]  # Devuelve el símbolo del ganador si hay 4 en línea

    for col in range(len(tablero[0])):
        for fila in range(len(tablero) - 3):
            if tablero[fila][col] == tablero[fila + 1][col] == tablero[fila + 2][col] == tablero[fila + 3][col] != " ":
                return tablero[fila][col]  # Devuelve el símbolo del ganador si hay 4 en línea

    for fila in range(len(tablero) - 3):
        for col in range(len(tablero[0]) - 3):
            if tablero[fila][col] == tablero[fila + 1][col + 1] == tablero[fila + 2][col + 2] == tablero[fila + 3][col + 3] != " ":
                return tablero[fila][col]  # Devuelve el símbolo del ganador si hay 4 en diagonal
            if tablero[fila + 3][col] == tablero[fila + 2][col + 1] == tablero[fila + 1][col + 2] == tablero[fila][col + 3] != " ":
                return tablero[fila + 3][col]  # Devuelve el símbolo del ganador si hay 4 en diagonal
    return None  # Devuelve None si no hay ganador
