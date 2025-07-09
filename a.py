from datetime import datetime  # Importa el módulo datetime para trabajar con fechas y horas
from b import verificar_ganador

import json  # Importa el módulo json para trabajar con archivos JSON

partidas_hechas = []  # Lista global para almacenar las partidas realizadas
archivo_partidas = "partidas.json"  # Nombre del archivo para guardar las partidas


# Función para guardar las partidas en un archivo JSON
def guardar_partidas():
    with open(archivo_partidas, "w") as archivo:
        json.dump(partidas_hechas, archivo, indent=4)



# Función para cargar las partidas desde un archivo JSON
def cargar_partidas():
    global partidas_hechas
    try:
        with open(archivo_partidas, "r") as archivo:
            partidas_hechas = json.load(archivo)
    except FileNotFoundError:
        partidas_hechas = []

# Función para mostrar los juegos realizados
def juegos_realizados():
    print("\n_______JUEGOS REALIZADOS______")  # Encabezado de la sección de juegos realizados
    print("%15s %20s %15s" % ("Jugadores", "FechaHora", "Ganador"))  # Encabezado de la tabla
    for juego in partidas_hechas:  # Itera sobre la lista de partidas realizadas
        jugadores = juego["jugadores"]  # Obtiene los nombres de los jugadores
        fecha_hora = juego["fecha y hora"]  # Obtiene la fecha y hora de la partida
        ganador = juego["ganador"]  # Obtiene el nombre del ganador
        print("%15s %20s %15s" % (jugadores, fecha_hora, ganador))  # Imprime los detalles de cada partida
    print()  # Línea en blanco para separación

#-------------------------------------------------------------------------------
# Función para mostrar las estadísticas de los juegos realizados
def mostrar_estadisticas():
    total_juegos = len(partidas_hechas)
    ganados_por_computadora = sum(1 for juego in partidas_hechas if juego["ganador"] == "IA")
    jugadores = {}
    for juego in partidas_hechas:
        for jugador in juego["jugadores"].split(" vs "):
            if jugador not in jugadores:
                jugadores[jugador] = 0
            jugadores[jugador] += 1

    jugadores_ordenados = sorted(jugadores.items(), key=lambda x: x[1], reverse=True)

    print("______ESTADÍSTICAS______")
    print(f"Total de juegos: {total_juegos}")
    print(f"Juegos ganados por la computadora: {ganados_por_computadora}")
    print("Jugadores ordenados por cantidad de juegos:")
    for jugador, cantidad in jugadores_ordenados:
        print(f"{jugador}: {cantidad} juegos")
    print()  # Línea en blanco para separación

#-----------------------------------------------------------------------


# Función para inicializar el tablero
def tablero():
    tab = []  # Lista para almacenar las filas del tablero
    for i in range(6):  # Crea 6 filas
        tab.append([])  # Añade una nueva fila vacía
        for j in range(7):  # Cada fila tiene 7 columnas
            tab[i].append(" ")  # Añade un espacio vacío en cada celda de la fila
    return tab  # Devuelve el tablero

# Función para imprimir el tablero
def imprimir_tablero(tablero):
    # Imprime números de columnas
    print("|", end="")
    for f in range(1, len(tablero[0]) + 1):
        print(f, end="|")
    print("")
    # Datos del tablero
    for fila in tablero:
        print("|", end="")
        for valor in fila:
            print(valor, end="|")
        print("")
    # Lo mismo que arriba pero abajo
    print("|", end="")
    for f in range(1, len(tablero[0]) + 1):
        print(f, end="|")
    print("")

# Función para encontrar la fila correcta donde colocar la pieza
def filacorrecta(columna, tablero):
    x = len(tablero) - 1  # Empieza desde la última fila
    while x >= 0:  # Itera hacia arriba
        if tablero[x][columna] == " ":  # Si encuentra una celda vacía
            return x  # Devuelve el índice de la fila
        x -= 1  # Decrementa el índice de la fila
    return -1  # Devuelve -1 si la columna está llena

# Función para pedir la columna donde colocar la pieza
def pedir_columna(tablero):
    while True:  # Bucle infinito hasta que se introduzca una columna válida
        try:
            col = int(input("Ingrese una columna para colocar la pieza (1-7): "))  # Pide la columna al jugador
            if col == -1:  # Si el jugador introduce -1, cancela el juego
                print("\n******Juego cancelado******")  # Mensaje de cancelación
                return None
            elif col < 1 or col > 7:  # Si la columna no está entre 1 y 7
                print("Columna inválida")  # Mensaje de error
            elif tablero[0][col - 1] != " ":  # Si la columna está llena
                print("la columna esta llena")  # Mensaje de error
            else:
                return col - 1  # Devuelve el índice de la columna (ajustado a índice base 0)
        except ValueError:  # Si se introduce un valor no numérico
            print("Por favor ingrese un número válido.")  # Mensaje de error

# Función para colocar la pieza en el tablero
def colocarla(columna, turno, tablero):
    # Se asigna un signo según el jugador
    pieza = "X" if turno % 2 != 0 else "O"
    # Se determina en qué fila caerá
    fila = filacorrecta(columna, tablero)
    if fila != -1:
        tablero[fila][columna] = pieza  # Coloca la pieza en la posición correcta
        return True  # Devuelve True si la pieza se coloca correctamente
    return False  # Devuelve False si no se puede colocar la pieza

#--------------------------------------------------------------------------------------------------------------------------------------
# Función heurística para evaluar el tablero
def heuristico():
    valor = 0
    filas = get_filas()
    diagonales = get_diagonales()
    columnas = [[fila[i] for fila in filas] for i in range(len(filas[0]))]
    lineas = diagonales + filas + columnas
    for linea in lineas:
        valor += heuristico_linea(linea)
        if valor < -1000 or valor > 1000:
            return valor
    return valor

def heuristico_linea(linea):
    puntuacion = 0
    for i in range(len(linea) - 3):
        puntuacion += evaluar_4_elementos(linea[i:4 + i])
        if puntuacion < -1000 or puntuacion > 1000:
            return puntuacion
    return puntuacion

def evaluar_4_elementos(linea):
    cant_o = 0
    cant_x = 0
    for elemento in linea:
        if elemento == 'X':
            cant_x += 1
        elif elemento == 'O':
            cant_o += 1
    if cant_x == 0:
        return 100000 if cant_o == 4 else cant_o
    elif cant_o == 0:
        return -1000000 if cant_x == 4 else -1 * cant_x
    return 0

# Función para obtener todas las filas del tablero
def get_filas():
    return [[fila[i] for fila in tablero_actual] for i in range(len(tablero_actual[0]))]

# Función para obtener todas las diagonales del tablero
def get_diagonales():
    diagonales = []
    for i in range(3, 6):
        for j in range(4):
            diagonales.append([tablero_actual[i-k][j+k] for k in range(4)])
    for i in range(3, 6):
        for j in range(3, 7):
            diagonales.append([tablero_actual[i-k][j-k] for k in range(4)])
    return diagonales

# Función para obtener las posiciones abiertas en el tablero
def get_abiertos():
    return [i for i in range(7) if tablero_actual[0][i] == " "]

# Algoritmo Minimax con poda alfa-beta
def minimax_alpha_beta(profundidad, alpha, beta, jugador):
    if profundidad == 0 or verificar_ganador(tablero_actual):
        return heuristico(), None

    if jugador == 'O':
        valor = -10000000
        abiertos = get_abiertos()
        mejor_columna = abiertos[0]
        for col in abiertos:
            fila = filacorrecta(col, tablero_actual)
            tablero_actual[fila][col] = jugador
            valor_hijo, _ = minimax_alpha_beta(profundidad - 1, alpha, beta, 'X')
            tablero_actual[fila][col] = " "
            if valor_hijo > valor:
                valor = valor_hijo
                mejor_columna = col
            alpha = max(alpha, valor)
            if alpha >= beta:
                break
        return valor, mejor_columna
    else:
        valor = 10000000
        abiertos = get_abiertos()
        mejor_columna = abiertos[0]
        for col in abiertos:
            fila = filacorrecta(col, tablero_actual)
            tablero_actual[fila][col] = jugador
            valor_hijo, _ = minimax_alpha_beta(profundidad - 1, alpha, beta, 'O')
            tablero_actual[fila][col] = " "
            if valor_hijo < valor:
                valor = valor_hijo
                mejor_columna = col
            beta = min(beta, valor)
            if alpha >= beta:
                break
        return valor, mejor_columna

# Función para iniciar el juego
def iniciar_juego():
    global tablero_actual  # Hace que el tablero_actual sea global
    fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M')  # Obtiene la fecha y hora actual
    print("INICIAMOS")  # Mensaje de inicio del juego

    player1 = input("Nombre Jugador 1: ")  # Pide el nombre del jugador 1
    player2 = input("Nombre Jugador 2 (o 'IA' para jugar contra la computadora): ")  # Pide el nombre del jugador 2
    print()
    jugadores = f"{player1} vs {player2}"  # Crea una cadena con los nombres de los jugadores
    print("--------------------------------------")
    print("Juego:", jugadores, fecha_hora_actual)  # Imprime los nombres de los jugadores y la fecha y hora

    print("--------------------------------------")
    print("-1: Para cancelar")  # Instrucción para cancelar el juego

    tablero_actual = tablero()  # Inicializa el tablero
    turno = 1  # Inicia con el turno 1
    while True:
        print()
        imprimir_tablero(tablero_actual)  # Imprime el tablero
        if turno % 2 != 0:  # Determina de quién es el turno
            jugador_actual = player1
            simbolo_actual = "X"
        else:
            jugador_actual = player2
            simbolo_actual = "O"
        print("--------------------------------------")
        print(f"Es el turno de {jugador_actual} ({simbolo_actual})")  # Imprime el turno del jugador actual

        if jugador_actual == 'IA':
            ___, columna = minimax_alpha_beta(7, -1000000000, 1000000000, 'O')
            print(f"La IA coloca su pieza en la columna {columna + 1}")
        else:
            columna = pedir_columna(tablero_actual)  # Pide la columna al jugador
            if columna is None:
                print()
                return

        if colocarla(columna, turno, tablero_actual):  # Coloca la pieza en el tablero
            ganador = verificar_ganador(tablero_actual)  # Verifica si hay un ganador
            if ganador:
                imprimir_tablero(tablero_actual)  # Imprime el tablero final
                if ganador == "X":
                    winner = player1
                else:
                    winner = player2
                print(f"Ha ganado {winner}!!!\n")  # Imprime el nombre del ganador
                partidas_hechas.append({"jugadores": jugadores, "fecha y hora": fecha_hora_actual, "ganador": winner})  # Añade la partida a la lista de partidas realizadas
                break
            turno += 1  # Incrementa el turno
        else:
            print("Movimiento inválido, prueba con un valor del 1 al 7")  # Mensaje de error si el movimiento no es válido

        if turno > 42:  # Si se han jugado más de 42 turnos, es un empate
            imprimir_tablero(tablero_actual)  # Imprime el tablero final
            print("¡ES UN EMPATE!")  # Mensaje de empate
            partidas_hechas.append({"jugadores": jugadores, "fecha y hora": fecha_hora_actual, "ganador": "Ninguno, fue empate"})  # Añade la partida a la lista de partidas realizadas
            break

def mostrar_logo():
    print(r'''
==========================================================================
  _  _              
 | || |     
 | || |_    
 |__   _|   
    |_|    
| ____|| \ | |
|  _|  |  \| |
| |___ | |\  |
|_____||_| \_|
_____      __   __     __     __     
|  _ \    /  \   \ \   /  /   /  \    
| |_) |  / __ \   \ \ /  /   / __ \   
|  _ <| / /__\ \   \ V  /   / /__\ \  
|_| \_\/_/    \_\   \  /   /_/    \_\ 
                 __/ /        
                |___/      
============================================================================= 
''')
