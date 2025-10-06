# Dungeon Explorer

Un pequeño juego de exploracion de mazmorras en consola, hecho en Python. El jugador recorre un dungeon generado aleatoriamente, encuentra tesoros, lucha contra monstruos y puede guardar su partida.

  
Estructura del proyecto
  

BDD2/
├── main.py
├── dungeon_generator/
│   ├── __init__.py
│   ├── models.py
│   ├── visualizer.py
│   ├── serializer.py

(cuando le da a editar en el git se ve bien)
  
Requisitos

Asegurate de tener Python 3.8 o superior instalado.
Luego instala las dependencias necesarias con el siguiente comando:

pip install rich pyyaml

  
Ejecucion
  

Para iniciar el juego:

python main.py

Se generara un dungeon aleatorio y aparecera el mapa junto con las instrucciones.
Podras moverte con los comandos:

norte
sur
este
oeste
salir

El progreso se guarda automaticamente si eliges salir.

  
Guardado de partida
  

El juego guarda tu estado (mapa + explorador) en un archivo partida.json.
Si el archivo existe, se cargara automaticamente al iniciar el juego.

  
Simbolos del mapa
  

Simbolo - Significado
M - Monstruo
T - Tesoro
I - item
J - Jefe
. - Habitacion vacia
E - Explorador

  
Archivos principales
  

main.py: punto de entrada del juego
mapa.py: genera y estructura el dungeon
explorador.py: controla al jugador y sus acciones
visualizer.py: maneja la visualizacion con Rich
serializer.py: guarda y carga partidas

  
Ejemplo de ejecucion
  

Generando dungeon...

 Mapa Completo 
  del Dungeon  
┏━━━━━━━━━━━━━┓
┃             ┃
┡━━━━━━━━━━━━━┩
│   M I T J   │
│ . . T . . . │
└─────────────┘

(cuando le da a editar en el git se ve bien)

Vida: 5
Inventario: (vacio)
Mover (norte/sur/este/oeste) o 'salir': norte

Has encontrado un tesoro: Oro!
