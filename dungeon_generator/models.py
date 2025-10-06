import random
from abc import ABC, abstractmethod
from typing import Optional, Dict, List, Tuple
 
# CLASE OBJETO
 
class Objeto:
    def __init__(self, nombre: str, valor: int, descripcion: str):
        self.nombre = nombre
        self.valor = valor
        self.descripcion = descripcion

    def __repr__(self):
        return f"{self.nombre} (Valor: {self.valor})"


 
# CLASE ABSTRACTA ContenidoHabitacion
 
class ContenidoHabitacion(ABC):
    @property
    @abstractmethod
    def descripcion(self) -> str:
        pass

    @property
    @abstractmethod
    def tipo(self) -> str:
        pass

    @abstractmethod
    def interactuar(self, explorador: "Explorador") -> str:
        pass


 
# CLASE TESORO
 
class Tesoro(ContenidoHabitacion):
    def __init__(self, recompensa: Objeto):
        self.recompensa = recompensa

    @property
    def descripcion(self):
        return f"Un cofre con {self.recompensa.nombre}"

    @property
    def tipo(self):
        return "tesoro"

    def interactuar(self, explorador: "Explorador") -> str:
        explorador.inventario.append(self.recompensa)
        return f"Has encontrado un tesoro: {self.recompensa.nombre}!"


 
# CLASE MONSTRUO
 
class Monstruo(ContenidoHabitacion):
    def __init__(self, nombre: str, vida: int, ataque: int):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque

    @property
    def descripcion(self):
        return f"Un monstruo feroz llamado {self.nombre}"

    @property
    def tipo(self):
        return "monstruo"

    def interactuar(self, explorador: "Explorador") -> str:
        resultado = [f"Te enfrentas al monstruo {self.nombre}!"]
        while self.vida > 0 and explorador.esta_vivo:
            if random.random() < 0.6:
                self.vida -= 1
                resultado.append("Golpeas al monstruo!")
            else:
                explorador.recibir_dano(self.ataque)
                resultado.append(f"El monstruo te golpea! Vida: {explorador.vida}")
            if not explorador.esta_vivo:
                resultado.append("Has sido derrotado...")
                break
            if self.vida <= 0:
                resultado.append(f"Derrotaste a {self.nombre}!")
        return "\n".join(resultado)


 
# CLASE JEFE
 
class Jefe(Monstruo):
    def __init__(self, nombre: str, vida: int, ataque: int, recompensa_especial: Objeto):
        super().__init__(nombre, vida, ataque)
        self.recompensa_especial = recompensa_especial

    @property
    def tipo(self):
        return "jefe"

    def interactuar(self, explorador: "Explorador") -> str:
        resultado = [f"¡El jefe {self.nombre} aparece!"]
        while self.vida > 0 and explorador.esta_vivo:
            if random.random() < 0.4:
                self.vida -= 1
                resultado.append("Golpeas al jefe!")
            else:
                explorador.recibir_dano(self.ataque)
                resultado.append(f"El jefe te golpea! Vida: {explorador.vida}")
            if not explorador.esta_vivo:
                resultado.append("Has sido derrotado...")
                break
            if self.vida <= 0:
                explorador.inventario.append(self.recompensa_especial)
                resultado.append(
                    f"Derrotaste al jefe {self.nombre} y obtuviste {self.recompensa_especial.nombre}!"
                )
        return "\n".join(resultado)


 
# CLASE EVENTO
 
class Evento(ContenidoHabitacion):
    def __init__(self, nombre: str, descripcion: str, efecto: callable):
        self.nombre = nombre
        self._descripcion = descripcion
        self.efecto = efecto

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def tipo(self):
        return "evento"

    def interactuar(self, explorador: "Explorador") -> str:
        return self.efecto(explorador)


 
# CLASE HABITACION
 
class Habitacion:
    def __init__(
        self,
        id: int,
        x: int,
        y: int,
        inicial: bool = False,
        contenido: Optional[ContenidoHabitacion] = None,
    ):
        self.id = id
        self.x = x
        self.y = y
        self.inicial = inicial
        self.contenido = contenido
        self.conexiones: Dict[str, "Habitacion"] = {}
        self.visitada = False

    def conectar(self, direccion: str, otra: "Habitacion"):
        opuestos = {"norte": "sur", "sur": "norte", "este": "oeste", "oeste": "este"}
        self.conexiones[direccion] = otra
        otra.conexiones[opuestos[direccion]] = self


 
# CLASE MAPA
 
class Mapa:
    def __init__(self, ancho: int, alto: int):
        self.ancho = ancho
        self.alto = alto
        self.habitaciones: Dict[Tuple[int, int], Habitacion] = {}
        self.habitacion_inicial: Optional[Habitacion] = None

    def generar_estructura(self, n_habitaciones: int):
        if n_habitaciones > self.ancho * self.alto:
            raise ValueError("Demasiadas habitaciones para el tamaño del mapa.")

        # habitacion inicial en el borde
        bordes = [(x, 0) for x in range(self.ancho)] + [(x, self.alto - 1) for x in range(self.ancho)] + \
                 [(0, y) for y in range(self.alto)] + [(self.ancho - 1, y) for y in range(self.alto)]
        inicio_x, inicio_y = random.choice(bordes)
        habitacion_inicial = Habitacion(0, inicio_x, inicio_y, inicial=True)
        self.habitaciones[(inicio_x, inicio_y)] = habitacion_inicial
        self.habitacion_inicial = habitacion_inicial

        # expansion aleatoria
        direcciones = [(0, 1, "norte"), (0, -1, "sur"), (1, 0, "este"), (-1, 0, "oeste")]
        disponibles = [(inicio_x, inicio_y)]
        contador = 1

        while contador < n_habitaciones and disponibles:
            x, y = random.choice(disponibles)
            habitacion = self.habitaciones[(x, y)]
            random.shuffle(direcciones)
            for dx, dy, dir in direcciones:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.ancho and 0 <= ny < self.alto and (nx, ny) not in self.habitaciones:
                    nueva = Habitacion(contador, nx, ny)
                    habitacion.conectar(dir, nueva)
                    self.habitaciones[(nx, ny)] = nueva
                    disponibles.append((nx, ny))
                    contador += 1
                    if contador >= n_habitaciones:
                        break
            if all(
                (x + dx, y + dy) in self.habitaciones or not (0 <= x + dx < self.ancho and 0 <= y + dy < self.alto)
                for dx, dy, _ in direcciones
            ):
                disponibles.remove((x, y))

    def colocar_contenido(self):
        coords = [c for c in self.habitaciones if not self.habitaciones[c].inicial]
        random.shuffle(coords)
        n_total = len(coords)
        n_jefes = 1
        n_monstruos = int(random.uniform(0.2, 0.3) * n_total)
        n_tesoros = int(random.uniform(0.15, 0.25) * n_total)
        n_eventos = int(random.uniform(0.05, 0.1) * n_total)

        # jefes
        for _ in range(n_jefes):
            c = coords.pop()
            self.habitaciones[c].contenido = Jefe(
                "Jefe Final",
                random.randint(4, 6),
                random.randint(1, 2),
                Objeto("Artefacto Legendario", 100, "Un objeto poderoso"),
            )

        # monstruos
        for _ in range(n_monstruos):
            if not coords: break
            c = coords.pop()
            self.habitaciones[c].contenido = Monstruo(
                "Goblin",
                random.randint(2, 4),
                random.randint(1, 2),
            )

        # tesoros
        for _ in range(n_tesoros):
            if not coords: break
            c = coords.pop()
            self.habitaciones[c].contenido = Tesoro(
                Objeto("Oro", random.randint(5, 20), "Monedas de oro")
            )

        # eventos
        def efecto_aleatorio(explorador: "Explorador"):
            tipo = random.choice(["trampa", "fuente", "portal"])
            if tipo == "trampa":
                explorador.recibir_dano(1)
                return "Una trampa! Pierdes 1 punto de vida."
            elif tipo == "fuente":
                explorador.vida += 1
                return "Bebes de una fuente y recuperas 1 punto de vida."
            else:
                destino = random.choice(list(self.habitaciones.keys()))
                explorador.posicion_actual = destino
                return f"Un portal te teletransporta a {destino}!"

        for _ in range(n_eventos):
            if not coords: break
            c = coords.pop()
            self.habitaciones[c].contenido = Evento(
                "Evento misterioso", "Algo inesperado sucede", efecto_aleatorio
            )

    def obtener_estadisticas_mapa(self):
        tipos = {"vacia": 0, "tesoro": 0, "monstruo": 0, "jefe": 0, "evento": 0}
        for h in self.habitaciones.values():
            if h.contenido:
                tipos[h.contenido.tipo] += 1
            else:
                tipos["vacia"] += 1
        prom_conexiones = sum(len(h.conexiones) for h in self.habitaciones.values()) / len(self.habitaciones)
        return {
            "total_habitaciones": len(self.habitaciones),
            **tipos,
            "promedio_conexiones": prom_conexiones,
        }


 
# CLASE EXPLORADOR
 
class Explorador:
    def __init__(self, mapa: Mapa):
        self.vida = 5
        self.inventario: List[Objeto] = []
        self.mapa = mapa
        self.posicion_actual = (mapa.habitacion_inicial.x, mapa.habitacion_inicial.y)

    @property
    def esta_vivo(self):
        return self.vida > 0

    def mover(self, direccion: str) -> bool:
        habitacion = self.mapa.habitaciones[self.posicion_actual]
        if direccion in habitacion.conexiones:
            nueva = habitacion.conexiones[direccion]
            self.posicion_actual = (nueva.x, nueva.y)
            return True
        return False

    def explorar_habitacion(self) -> str:
        h = self.mapa.habitaciones[self.posicion_actual]
        h.visitada = True
        if not h.contenido:
            return "La habitacion esta vacia."
        return h.contenido.interactuar(self)

    def obtener_habitaciones_adyacentes(self) -> List[str]:
        h = self.mapa.habitaciones[self.posicion_actual]
        return list(h.conexiones.keys())

    def recibir_dano(self, cantidad: int):
        self.vida = max(0, self.vida - cantidad)
