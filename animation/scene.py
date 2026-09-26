"""
Animación del proyecto Suffix Array (CS2023 - UTEC 2026-2).
Equipo: Aguirre Milla, Fernando Eliseo David; Velásquez Díaz, [nombre]; Díaz Jara, Rolando David.

IMPORTANTE: esta escena NO simula valores a mano. Cada arreglo, ronda y paso de
búsqueda que se anima viene de ejecutar de verdad el binario build/sa_trace,
compilado a partir de src/suffix_array.hpp (la implementación real del grupo).

Uso:
    make -C ..                       # compila build/sa_trace si no existe
    manim -pql scene.py SuffixArrayScene     # render rápido (borrador)
    manim -pqh scene.py SuffixArrayScene     # render final en alta calidad
"""

import json
import subprocess
from pathlib import Path

from manim import *

ROOT = Path(__file__).resolve().parent.parent


def _find_sa_trace_bin() -> Path:
    """Busca el binario compilado, con o sin extensión .exe (Windows vs Linux/Mac)."""
    for name in ("sa_trace.exe", "sa_trace"):
        candidate = ROOT / "build" / name
        if candidate.exists():
            return candidate
    return ROOT / "build" / "sa_trace"  # por defecto, para el mensaje de error


SA_TRACE_BIN = _find_sa_trace_bin()

STRING = "banana"
PATTERN = "ana"
EDGE_STRING = "aaa"  # caso borde: todos los caracteres repetidos


def run_trace(s: str, pattern: str = "") -> dict:
    """Llama al binario real compilado desde la implementación del grupo y
    parsea su salida JSON. Esto es lo que hace que la animación sea 'real'."""
    if not SA_TRACE_BIN.exists():
        raise FileNotFoundError(
            f"No se encontró {SA_TRACE_BIN}. Corre 'make' en la raíz del proyecto primero."
        )
    args = [str(SA_TRACE_BIN), s]
    if pattern:
        args.append(pattern)
    out = subprocess.run(args, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


class SuffixArrayScene(Scene):
    def construct(self):
        self.show_title()
        self.show_intro()
        data = run_trace(STRING, PATTERN)
        self.show_construction(data)
        self.show_edge_case()
        self.show_search(data)
        self.show_complexity()
        self.show_applications()
        self.show_credits()

    # ------------------------------------------------------------------
    def show_title(self):
        title = Text("Suffix Array", font_size=64, weight=BOLD)
        subtitle = Text(
            "CS2023 - Algoritmos y Estructuras de Datos, UTEC 2026-2",
            font_size=24,
            color=GRAY_B,
        )
        subtitle.next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))

    def show_intro(self):
        header = Text("¿Qué es un Suffix Array?", font_size=40, weight=BOLD)
        lines = VGroup(
            Text(
                "Arreglo con las posiciones de todos los sufijos de un string,",
                font_size=28,
            ),
            Text("ordenados lexicográficamente.", font_size=28),
            Text(
                "TDA: permite búsqueda eficiente de patrones en texto.",
                font_size=28,
                color=YELLOW,
            ),
        ).arrange(DOWN, buff=0.35)
        group = VGroup(header, lines).arrange(DOWN, buff=0.5)
        self.play(Write(header))
        self.play(FadeIn(lines))
        self.wait(1.5)
        self.play(FadeOut(group))

    def show_construction(self, data):
        s = data["s"]
        header = Text(f'Construyendo el Suffix Array de "{s}"', font_size=32)
        header.to_edge(UP)
        self.play(Write(header))

        chars = VGroup(*[Text(c, font_size=36) for c in s]).arrange(RIGHT, buff=0.3)
        idx = VGroup(
            *[Text(str(i), font_size=20, color=GRAY_B) for i in range(len(s))]
        )
        for c, ix in zip(chars, idx):
            ix.next_to(c, DOWN, buff=0.15)
        string_group = VGroup(chars, idx).move_to(UP * 1.7)
        self.play(FadeIn(string_group))

        prev_group = None
        for round_data in data["rounds"]:
            k = round_data["k"]
            sa = round_data["sa"]
            label = Text(f"Ronda k={k}", font_size=26, color=BLUE)
            row = VGroup(*[Text(str(v), font_size=28) for v in sa]).arrange(
                RIGHT, buff=0.4
            )
            group = VGroup(label, row).arrange(DOWN, buff=0.3)
            group.move_to(DOWN * 0.7)

            if prev_group is None:
                self.play(FadeIn(group))
            else:
                self.play(Transform(prev_group, group))
            if prev_group is None:
                prev_group = group
            self.wait(0.5)

        final_label = Text("Suffix Array final ↑", font_size=24, color=GREEN)
        final_label.next_to(prev_group, DOWN, buff=0.4)
        self.play(Write(final_label))
        self.wait(1)
        self.play(FadeOut(VGroup(header, string_group, prev_group, final_label)))

    def show_edge_case(self):
        section_title = Text("Casos borde", font_size=40, weight=BOLD)
        self.play(Write(section_title))
        self.wait(0.8)
        self.play(FadeOut(section_title))

        cases = [
            ("", "String vacío"),
            ("a", "Un solo carácter"),
            (EDGE_STRING, "Todos los caracteres iguales"),
        ]
        for s_val, label in cases:
            data = run_trace(s_val)
            shown = s_val if s_val else "(vacío)"
            header = Text(f'{label}:  "{shown}"', font_size=30)
            header.to_edge(UP)
            sa_text = Text(f'sa  = {data["sa"]}', font_size=32)
            lcp_text = Text(f'lcp = {data["lcp"]}', font_size=32, color=YELLOW)
            group = VGroup(sa_text, lcp_text).arrange(DOWN, buff=0.4)
            self.play(Write(header))
            self.play(FadeIn(group))
            self.wait(1.8)
            self.play(FadeOut(VGroup(header, group)))

        note = Text(
            "El código maneja estos casos sin errores: n=0 retorna\n"
            "temprano, y los empates de rank se resuelven bien.",
            font_size=24,
            color=GRAY_B,
        )
        self.play(FadeIn(note))
        self.wait(2)
        self.play(FadeOut(note))

    def show_search(self, data):
        s = data["s"]
        p = data["pattern"]
        sa = data["sa"]
        steps = data["steps"]

        header = Text(f'Buscando "{p}" en "{s}"', font_size=32)
        header.to_edge(UP)
        self.play(Write(header))

        row = VGroup(*[Text(str(v), font_size=30) for v in sa]).arrange(RIGHT, buff=0.5)
        row.move_to(ORIGIN)
        self.play(FadeIn(row))

        def pos_of(i):
            i = max(0, min(i, len(row) - 1))
            return row[i].get_center()

        lo_marker = Triangle(color=RED, fill_opacity=1).scale(0.12).rotate(PI)
        hi_marker = Triangle(color=RED, fill_opacity=1).scale(0.12).rotate(PI)
        mid_marker = Triangle(color=YELLOW, fill_opacity=1).scale(0.15)

        first = steps[0]
        lo_marker.next_to(pos_of(first["lo"]), DOWN, buff=0.2)
        hi_marker.next_to(pos_of(first["hi"] - 1), DOWN, buff=0.2)
        self.play(FadeIn(lo_marker), FadeIn(hi_marker))

        for st in steps:
            mid_marker.next_to(pos_of(st["mid"]), UP, buff=0.15)
            self.play(FadeIn(mid_marker), run_time=0.25)
            self.play(
                lo_marker.animate.next_to(pos_of(st["lo"]), DOWN, buff=0.2),
                hi_marker.animate.next_to(pos_of(max(st["hi"] - 1, 0)), DOWN, buff=0.2),
                run_time=0.35,
            )
            self.play(FadeOut(mid_marker), run_time=0.15)

        l, r = data["range"]
        result = Text(
            f"Rango de coincidencias: [{l}, {r})  ->  {r - l} ocurrencia(s)",
            font_size=28,
            color=GREEN,
        )
        result.next_to(row, DOWN, buff=1.2)
        self.play(Write(result))
        self.wait(1.5)
        self.play(FadeOut(VGroup(header, row, lo_marker, hi_marker, result)))

    def show_complexity(self):
        title = Text("Complejidad", font_size=36, weight=BOLD)
        rows = VGroup(
            Text("Construcción (prefix doubling):  O(n log^2 n)", font_size=26),
            Text("LCP array (Kasai):  O(n)", font_size=26),
            Text("Búsqueda de patrón:  O(m log n)", font_size=26),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        group = VGroup(title, rows).arrange(DOWN, buff=0.5)
        self.play(Write(title))
        self.play(FadeIn(rows))
        self.wait(2.5)
        self.play(FadeOut(group))

    def show_applications(self):
        title = Text("¿Para qué se usa en la práctica?", font_size=34, weight=BOLD)
        rows = VGroup(
            Text("• Motores de búsqueda de texto y grep sobre archivos grandes", font_size=25),
            Text("• Bioinformática: alineamiento y búsqueda en genomas", font_size=25),
            Text("• Detección de plagio y de substrings repetidos", font_size=25),
            Text("• Compresión de datos (Burrows-Wheeler Transform)", font_size=25),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        group = VGroup(title, rows).arrange(DOWN, buff=0.6)
        self.play(Write(title))
        for row in rows:
            self.play(FadeIn(row), run_time=0.5)
        self.wait(2.5)
        self.play(FadeOut(group))

    def show_credits(self):
        title = Text("Suffix Array — Proyecto Final 1", font_size=32, weight=BOLD)
        names = VGroup(
            Text("Aguirre Milla, Fernando", font_size=24),
            Text("Velásquez Díaz, Eliseo David", font_size=24),
            Text("Díaz Jara, Rolando David", font_size=24),
        ).arrange(DOWN, buff=0.25)
        group = VGroup(title, names).arrange(DOWN, buff=0.6)
        self.play(Write(group))
        self.wait(2.5)