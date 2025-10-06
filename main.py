from dungeon_generator import Mapa, Explorador, Visualizador, guardar_partida


def main():
    print("Generando dungeon...\n")

    # Crear mapa
    mapa = Mapa(ancho=6, alto=6)
    mapa.generar_estructura(n_habitaciones=12)
    mapa.colocar_contenido()

    # Crear explorador
    explorador = Explorador(mapa=mapa)
    vis = Visualizador()

    # Mostrar estado inicial
    vis.mostrar_mapa_completo(mapa)
    vis.mostrar_estado_explorador(explorador)

    # Bucle principal de exploracion
    while explorador.esta_vivo:
        print("\n" + "-" * 50)
        vis.mostrar_minimapa(explorador)
        vis.mostrar_habitacion_actual(explorador)
        print("-" * 50)

        comando = input("\nMover (norte/sur/este/oeste) o 'salir': ").strip().lower()

        if comando == "salir":
            print("\nGuardando partida...")
            guardar_partida(mapa, explorador, "partida.json")
            print("Partida guardada en 'partida.json'. Fin del juego.\n")
            break

        if explorador.mover(comando):
            resultado = explorador.explorar_habitacion()
            print(f"\n{resultado}")
        else:
            print("\nMovimiento invalido. No hay salida en esa direccion.")

        # Mostrar el mapa actualizado cada vez que el jugador se mueve
        vis.mostrar_minimapa(explorador)
        vis.mostrar_estado_explorador(explorador)

        # Verificar si el jugador sigue vivo
        if not explorador.esta_vivo:
            print("\nHas muerto en el dungeon... Fin del juego.")
            break


if __name__ == "__main__":
    main()
