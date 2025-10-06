import json
import yaml


def guardar_partida(mapa, explorador, archivo: str):
    data = {
        "mapa": {
            "ancho": mapa.ancho,
            "alto": mapa.alto,
            "habitaciones": [
                {
                    "id": h.id,
                    "x": h.x,
                    "y": h.y,
                    "inicial": h.inicial,
                    "visitada": h.visitada,
                    "contenido": h.contenido.tipo if h.contenido else None,
                }
                for h in mapa.habitaciones.values()
            ],
        },
        "explorador": {
            "vida": explorador.vida,
            "inventario": [obj.nombre for obj in explorador.inventario],
            "posicion_actual": explorador.posicion_actual,
        },
    }

    if archivo.endswith(".json"):
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    elif archivo.endswith(".yaml") or archivo.endswith(".yml"):
        with open(archivo, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f)
    else:
        raise ValueError("Formato no soportado. Usa .json o .yaml")


def cargar_partida(archivo: str):
    if archivo.endswith(".json"):
        with open(archivo, "r", encoding="utf-8") as f:
            return json.load(f)
    elif archivo.endswith(".yaml") or archivo.endswith(".yml"):
        with open(archivo, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        raise ValueError("Formato no soportado. Usa .json o .yaml")
