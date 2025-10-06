from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


class Visualizador:
    @staticmethod
    def mostrar_mapa_completo(mapa):
        table = Table(title="Mapa Completo del Dungeon")
        for y in range(mapa.alto):
            fila = []
            for x in range(mapa.ancho):
                if (x, y) in mapa.habitaciones:
                    h = mapa.habitaciones[(x, y)]
                    if h.inicial:
                        fila.append("[bold green]I[/bold green]")
                    elif h.contenido:
                        tipo = h.contenido.tipo
                        colores = {
                            "monstruo": "red",
                            "tesoro": "yellow",
                            "jefe": "magenta",
                            "evento": "cyan",
                        }
                        fila.append(f"[{colores.get(tipo, 'white')}]{tipo[0].upper()}[/{colores.get(tipo, 'white')}]")
                    else:
                        fila.append(".")
                else:
                    fila.append(" ")
            table.add_row(" ".join(fila))
        console.print(table)

    @staticmethod
    def mostrar_habitacion_actual(explorador):
        h = explorador.mapa.habitaciones[explorador.posicion_actual]
        console.print(f"[bold cyan]Habitación {h.id}[/bold cyan] ({h.x}, {h.y})")
        if h.inicial:
            console.print("Esta es la habitación inicial.")
        if h.contenido:
            console.print(f"Contenido: {h.contenido.descripcion}")
        else:
            console.print("Está vacía.")
        console.print(f"Conexiones disponibles: {', '.join(h.conexiones.keys())}")

    @staticmethod
    def mostrar_minimapa(explorador):
        mapa = explorador.mapa
        for y in range(mapa.alto):
            fila = ""
            for x in range(mapa.ancho):
                if (x, y) == explorador.posicion_actual:
                    fila += "[bold green]E[/bold green] "
                elif (x, y) in mapa.habitaciones:
                    h = mapa.habitaciones[(x, y)]
                    if h.visitada:
                        fila += "[white]·[/white] "
                    else:
                        fila += "  "
                else:
                    fila += "  "
            console.print(fila)

    @staticmethod
    def mostrar_estado_explorador(explorador):
        console.print(f"[bold yellow]Vida:[/bold yellow] {explorador.vida}")
        if explorador.inventario:
            items = ", ".join(obj.nombre for obj in explorador.inventario)
        else:
            items = "(vacío)"
        console.print(f"[bold yellow]Inventario:[/bold yellow] {items}")
