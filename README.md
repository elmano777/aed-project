# Suffix Array — CS2023

Proyecto Final 1 del curso de Algoritmos y Estructuras de Datos (UTEC, 2026-2). Nos tocó
implementar y animar un Suffix Array.

**Integrantes:**
- Aguirre Milla, Fernando
- Velásquez Díaz, Eliseo David
- Díaz Jara, Rolando David

## De qué se trata

Un Suffix Array de un string `S` es la lista de todas las posiciones donde empieza cada
sufijo de `S`, ordenada alfabéticamente según cómo se lee el sufijo desde ahí. Por ejemplo,
para `"banana"`, el sufijo que empieza en la posición 5 es `"a"`, el que empieza en la
posición 3 es `"ana"`, etc. Ordenando todos esos sufijos queda `[5, 3, 1, 0, 4, 2]`.

Sirve para buscar patrones dentro de un texto más rápido que recorriéndolo letra por letra
cada vez, porque una vez ordenado se puede usar búsqueda binaria. Se usa en motores de
búsqueda de texto, bioinformática (coincidencias en genomas) o compresión de datos.

Lo implementamos en C++, sin usar ninguna librería de suffix arrays:

- Construcción con *prefix doubling*: en vez de comparar los sufijos completos, los ordena
  en rondas comparando el doble de caracteres en cada ronda.
- LCP array con el algoritmo de Kasai.
- Búsqueda de un patrón con dos binary searches sobre el arreglo ya ordenado.

## Qué necesitas para correr esto

Para el código en C++:
- Compilador con soporte de C++17 (`g++`)
- `make`

Para regenerar la animación:
- Python 3
- Manim Community (`pip install manim --break-system-packages`)
- FFmpeg instalado y en el PATH

## Cómo compilar y correr

Desde la raíz del proyecto:

```bash
make
```

Compila dos binarios: uno con la suite de pruebas y otro que genera datos de traza.

```bash
make test
```

Debería imprimir `OK: todas las pruebas pasaron` — corre casos borde (string vacío, un
carácter, todo el string con el mismo carácter repetido) y 3000 casos aleatorios comparados
contra una implementación por fuerza bruta.

```bash
./build/sa_trace "banana" "ana"
```

Esto devuelve un JSON con el `sa` final, el `lcp`, cada ronda de la construcción, y si se le
pasa un patrón, los pasos de la búsqueda binaria. Son los datos que usa el video para animar.

## El video

Está en `media/suffix_array.mp4`, generado con `animation/scene.py` usando
[Manim](https://www.manim.community/). Para volver a generarlo:

```bash
make
cd animation
manim -pqh scene.py SuffixArrayScene
```

El resultado queda en `animation/media/videos/scene/1080p60/SuffixArrayScene.mp4`. La
narración de los tres integrantes se agregó después, sobre el video ya renderizado.

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