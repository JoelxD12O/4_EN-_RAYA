from a import iniciar_juego, juegos_realizados, mostrar_estadisticas, cargar_partidas, guardar_partidas, mostrar_logo
from b import mostrar_menu
# Función principal
def main():
    mostrar_logo()  # Mostrar el logo al inicio
    cargar_partidas()
    while True:
        opcion = mostrar_menu()  # Muestra el menú y obtiene la opción del usuario
        if opcion == '1':
            iniciar_juego()  # Inicia un nuevo juego
        elif opcion == '2':
            juegos_realizados()# Muestra los juegos realizados
            mostrar_estadisticas()
        elif opcion == '3':
            guardar_partidas()
            print("¡JUGAMOS LUEGO :D")  # Mensaje de salida
            break  # Sale del bucle
        else:
            print("La opción es inválida")  # Mensaje de error si la opción no es válida

if __name__ == "__main__":  # Comprueba si el script se está ejecutando directamente
    main()  # Llama a la función principal
