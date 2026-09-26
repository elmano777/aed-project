# Suffix Array — CS2023

Proyecto Final 1 del curso de Algoritmos y Estructuras de Datos (UTEC, 2026-2). Nos tocó
implementar y animar un **Suffix Array**.

**Integrantes:**
- Aguirre Milla, Fernando
- Velásquez Díaz, Eliseo David
- Díaz Jara, Rolando David

## De qué se trata

Un Suffix Array de un string `S` es, básicamente, la lista de todas las posiciones donde
empieza cada sufijo de `S`, pero ordenada alfabéticamente según cómo se lee el sufijo desde
ahí. Por ejemplo, para `"banana"`, el sufijo que empieza en la posición 5 es `"a"`, el que
empieza en la posición 3 es `"ana"`, etc. Ordenando todos esos sufijos queda `[5, 3, 1, 0, 4, 2]`.

Sirve para buscar patrones dentro de un texto mucho más rápido que recorriéndolo letra por
letra cada vez, porque una vez que está ordenado se puede usar búsqueda binaria. Se usa en
cosas como motores de búsqueda de texto, bioinformática (buscar coincidencias en genomas) o
compresión de datos.

Lo implementamos desde cero en C++ (nada de usar una librería que ya traiga esto hecho):

- Construcción del arreglo con el método de *prefix doubling*, que en vez de comparar los
  sufijos completos de una, los va ordenando en rondas comparando el doble de caracteres en
  cada ronda.
- El LCP array (cuánto se parece cada sufijo con el anterior en el orden) con el algoritmo
  de Kasai.
- Búsqueda de un patrón con dos binary searches sobre el arreglo ya ordenado.

## Qué necesitas para correr esto

Para el código en C++:
- Un compilador con soporte de C++17 (probamos con `g++`)
- `make`

Para regenerar la animación (esto es opcional si solo quieren compilar y correr el código,
pero necesario si quieren volver a renderizar el video):
- Python 3
- Manim Community (`pip install manim --break-system-packages`)
- FFmpeg instalado y en el PATH

## Cómo compilar y correr

Desde la raíz del proyecto:

```bash
make
```

Esto compila dos binarios: uno con la suite de pruebas y otro que genera datos de traza.
Para correr los tests:

```bash
make test
```

Debería imprimir `OK: todas las pruebas pasaron` — corre casos borde (string vacío, un
carácter, todo el string con el mismo carácter repetido) además de 3000 casos aleatorios
comparados contra una implementación por fuerza bruta.

También se puede pedirle al binario de traza que muestre paso a paso cómo se construyó el
arreglo para un string dado, y de paso buscar un patrón:

```bash
./build/sa_trace "banana" "ana"
```

Esto devuelve un JSON con el `sa` final, el `lcp`, cada ronda intermedia de la construcción,
y si se le pasa un patrón, los pasos de la búsqueda binaria. Justo esos datos son los que usa
el video para animar, para que quede claro que no estamos poniendo valores inventados a mano.

## El video

Está en `media/suffix_array.mp4` y se genera con el script en `animation/scene.py`, usando
[Manim](https://www.manim.community/). El script llama al binario `sa_trace` en el momento de
renderizar, así que los números que se ven en pantalla (el orden del suffix array, el LCP, los
pasos de la búsqueda) salen de ejecutar la implementación real, no de escribirlos a mano.

Para volver a generarlo:

```bash
make                          # por si no está compilado build/sa_trace todavía
cd animation
manim -pqh scene.py SuffixArrayScene
```

El resultado queda en `animation/media/videos/scene/1080p60/SuffixArrayScene.mp4`. La
narración de los tres integrantes se le agregó después, encima del video ya renderizado.

## Estructura del repo

```
src/
  suffix_array.hpp        implementación (build, kasai, search)
  test_suffix_array.cpp   pruebas
  trace_main.cpp          genera el JSON que usa la animación
animation/
  scene.py                script de Manim
media/
  suffix_array.mp4        video final, con narración
Makefile
```
