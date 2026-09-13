"""
Manim Community Edition scenes for the "temperature ceiling" narration beat,
built around your actual assets:

  - assets/Carnot_engine.svg   -> the detailed Carnot engine icon
  - a generic "dial" icon      -> built procedurally (circle + line + dot),
                                   matching the simple engine symbol in your
                                   HOT/COLD reference image

No narrative captions are drawn anywhere. The only text on screen is
diagram labels that exist in your reference images: HOT, COLD, CARNOT,
and the T_H / T_C / ratio symbols in the later beats.

Voice script this maps to (for your own reference while timing cuts):
  Clip 1: "That's the ceiling. And Carnot goes further — he works out
           exactly what sets that ceiling, and what it depends on."
  Clip 2: "Efficiency of ideal engines only depends on temperature. And
           this gives first clue that temperature is hiding some deep
           secrets like Entropy as we will find later."
  Clip 3: "Carnot finds that the efficiency of this ideal engine depends
           on nothing but the temperatures of the two reservoirs — the
           hot one it draws heat from, and the cold one it dumps heat
           into."
  Clip 4: "Not the substance inside the engine... Not the size of the
           engine, or its design. Just the two temperatures.
           Specifically, the ratio between them."

Render each independently:
    manim -pqh carnot_temperature_manim.py HotColdDialPushIn
    manim -pqh carnot_temperature_manim.py DialPulseTease
    manim -pqh carnot_temperature_manim.py CarnotLabeling
    manim -pqh carnot_temperature_manim.py SubstanceInvariance

-pql = fast draft preview, -pqh = 1080p60, -pqk = 4K.
Requires: pip install manim  (plus a LaTeX install for the MathTex formula
in the last scene).

IMPORTANT: update SVG_PATH below to point at your Carnot_engine.svg file.
"""

import os
from manim import *

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SVG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "Carnot_engine.svg")

HOT_COLOR_1 = "#F2B33D"   # gold end of the HOT gradient
HOT_COLOR_2 = "#E8672A"   # orange end of the HOT gradient
COLD_COLOR = "#3B8FE0"    # COLD bar color
GRAY = "#D3D1C7"          # line-art gray, matches your icon's stroke color
GOLD = "#F2A623"
BG = "#1c1c1a"


# ---------------------------------------------------------------------------
# Shared builders
# ---------------------------------------------------------------------------
def make_hot_bar() -> VGroup:
    bar = RoundedRectangle(corner_radius=0.18, width=4.4, height=1.0)
    bar.set_fill(color=[HOT_COLOR_1, HOT_COLOR_2], opacity=1)
    bar.set_stroke(width=0)
    label = Text("HOT", color=WHITE, font_size=30, weight=BOLD).move_to(bar)
    return VGroup(bar, label).to_edge(UP, buff=1.0)


def make_cold_bar() -> VGroup:
    bar = RoundedRectangle(corner_radius=0.18, width=4.4, height=1.0, color=COLD_COLOR)
    bar.set_fill(color=COLD_COLOR, opacity=1)
    bar.set_stroke(width=0)
    label = Text("COLD", color=WHITE, font_size=30, weight=BOLD).move_to(bar)
    return VGroup(bar, label).to_edge(DOWN, buff=1.0)


def make_generic_dial() -> VGroup:
    """The simple circular dial icon from the HOT/COLD reference image:
    a circle, a horizontal line through its middle, and a small center dot."""
    circle = Circle(radius=0.55, color=GRAY, stroke_width=3)
    line = Line(circle.get_left(), circle.get_right(), color=GRAY, stroke_width=3)
    dot = Dot(circle.get_center(), radius=0.06, color=GRAY)
    return VGroup(circle, line, dot)


def make_connector(top_point, bottom_point) -> Line:
    return Line(top_point, bottom_point, color=GRAY, stroke_width=2, stroke_opacity=0.6)


def load_carnot_icon() -> SVGMobject:
    """Loads the real Carnot engine SVG. First load can take a few seconds
    since the file is an auto-traced vector with ~425 individual paths."""
    icon = SVGMobject(SVG_PATH)
    icon.set(width=2.6)
    return icon


# ---------------------------------------------------------------------------
# Clip 1: callback to "the ceiling" + push toward the mechanism
# ---------------------------------------------------------------------------
class HotColdDialPushIn(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG

        hot = make_hot_bar()
        cold = make_cold_bar()
        dial = make_generic_dial().move_to(ORIGIN)
        top_wire = make_connector(hot.get_bottom(), dial.get_top())
        bottom_wire = make_connector(dial.get_bottom(), cold.get_top())

        self.play(FadeIn(hot), FadeIn(cold), run_time=1.0)
        self.play(Create(top_wire), Create(bottom_wire), FadeIn(dial), run_time=1.2)
        self.wait(0.5)

        # Callback to "the ceiling": a faint dashed line briefly above the
        # whole diagram, echoing the previous clip's ceiling motif, then
        # dissolving as the camera pushes toward the dial.
        ceiling_echo = DashedLine(LEFT * 3.5, RIGHT * 3.5, color=GOLD, stroke_opacity=0.5)
        ceiling_echo.next_to(hot, UP, buff=0.3)
        self.play(FadeIn(ceiling_echo), run_time=0.8)
        self.wait(0.6)
        self.play(FadeOut(ceiling_echo), run_time=0.6)

        # Push in toward the dial — "going further" / descending into the
        # mechanism that sets the ceiling. Requires MovingCameraScene
        # (plain Scene has no camera.frame to animate).
        self.play(
            self.camera.frame.animate.scale(0.55).move_to(dial.get_center()),
            run_time=2.5,
            rate_func=smooth,
        )
        self.wait(1.0)


# ---------------------------------------------------------------------------
# Clip 2: temperature dependency + unresolved entropy tease (no text)
# ---------------------------------------------------------------------------
class DialPulseTease(Scene):
    def construct(self):
        self.camera.background_color = BG

        hot = make_hot_bar()
        cold = make_cold_bar()
        dial = make_generic_dial().move_to(ORIGIN)
        top_wire = make_connector(hot.get_bottom(), dial.get_top())
        bottom_wire = make_connector(dial.get_bottom(), cold.get_top())

        self.add(hot, cold, dial, top_wire, bottom_wire)
        self.wait(0.4)

        # First pulse: a clean, confident glow — "efficiency depends on
        # temperature" being demonstrated directly.
        glow_ring = Circle(radius=0.7, color=GOLD, stroke_width=2, stroke_opacity=0.0).move_to(dial)
        self.add(glow_ring)
        self.play(
            glow_ring.animate.set_stroke(opacity=0.8).scale(1.3),
            dial.animate.set_color(GOLD),
            run_time=1.0,
        )
        self.play(
            glow_ring.animate.set_stroke(opacity=0).scale(1 / 1.3),
            dial.animate.set_color(GRAY),
            run_time=1.0,
        )
        self.wait(0.4)

        # Second beat: an unresolved flicker inside the dial itself —
        # something stirring that isn't shown clearly. This is the entropy
        # tease, done wordlessly: a small internal shape appears faintly,
        # trembles, and vanishes before resolving into anything.
        hidden_mark = RegularPolygon(n=6, color=GOLD, stroke_width=1.5, stroke_opacity=0)
        hidden_mark.scale(0.18).move_to(dial.get_center())
        self.add(hidden_mark)

        for _ in range(3):
            self.play(
                hidden_mark.animate.set_stroke(opacity=0.5).rotate(PI / 6),
                run_time=0.3,
            )
            self.play(
                hidden_mark.animate.set_stroke(opacity=0.05).rotate(-PI / 6),
                run_time=0.3,
            )
        self.play(FadeOut(hidden_mark), run_time=0.6)
        self.wait(1.0)


# ---------------------------------------------------------------------------
# Clip 3: temperatures attach to reservoirs, Carnot icon replaces the dial
# ---------------------------------------------------------------------------
class CarnotLabeling(Scene):
    def construct(self):
        self.camera.background_color = BG

        hot = make_hot_bar()
        cold = make_cold_bar()
        dial = make_generic_dial().move_to(ORIGIN)
        top_wire = make_connector(hot.get_bottom(), dial.get_top())
        bottom_wire = make_connector(dial.get_bottom(), cold.get_top())

        self.add(hot, cold, dial, top_wire, bottom_wire)
        self.wait(0.4)

        # T_H / T_C labels attach to the reservoirs (diagram labels, not
        # narrative captions).
        th_label = MathTex("T_H", color=WHITE, font_size=40).next_to(hot, RIGHT, buff=0.4)
        tc_label = MathTex("T_C", color=WHITE, font_size=40).next_to(cold, RIGHT, buff=0.4)
        self.play(FadeIn(th_label, shift=LEFT * 0.2), run_time=0.8)
        self.wait(0.3)
        self.play(FadeIn(tc_label, shift=LEFT * 0.2), run_time=0.8)
        self.wait(0.6)

        # Swap the generic dial for the real Carnot icon — the mechanism
        # now has an identity.
        carnot_icon = load_carnot_icon().move_to(dial.get_center())
        carnot_name = Text("CARNOT", color=WHITE, font_size=26, weight=BOLD)
        carnot_name.next_to(carnot_icon, DOWN, buff=0.25)

        self.play(
            FadeOut(dial),
            FadeIn(carnot_icon, scale=0.85),
            run_time=1.2,
        )
        self.play(FadeIn(carnot_name, shift=UP * 0.2), run_time=0.7)
        self.wait(1.2)


# ---------------------------------------------------------------------------
# Clip 4: substance/size invariance (icon stays constant) + ratio reveal
# ---------------------------------------------------------------------------
class SubstanceInvariance(Scene):
    def construct(self):
        self.camera.background_color = BG

        hot = make_hot_bar()
        cold = make_cold_bar()
        carnot_icon = load_carnot_icon().move_to(ORIGIN)
        carnot_name = Text("CARNOT", color=WHITE, font_size=26, weight=BOLD)
        carnot_name.next_to(carnot_icon, DOWN, buff=0.25)
        top_wire = make_connector(hot.get_bottom(), carnot_icon.get_top())
        bottom_wire = make_connector(carnot_icon.get_bottom(), cold.get_top())

        th_label = MathTex("T_H", color=WHITE, font_size=40).next_to(hot, RIGHT, buff=0.4)
        tc_label = MathTex("T_C", color=WHITE, font_size=40).next_to(cold, RIGHT, buff=0.4)

        self.add(hot, cold, carnot_icon, carnot_name, top_wire, bottom_wire, th_label, tc_label)
        self.wait(0.4)

        # "Testing" pulses — the icon briefly glows and wobbles in size as
        # if being substituted (different fluid, different size), then
        # resolves back to itself completely unchanged. The icon staying
        # the same IS the argument, so its actual fill colors are never
        # touched (that would destroy the ~100+ shades of shading baked
        # into the traced SVG) — instead a separate halo glows behind it,
        # and the icon itself only scales up/down and back by an inverse
        # factor each pass, so it returns to its exact original size.
        icon_anchor = carnot_icon.get_center()
        halo = Circle(radius=carnot_icon.width * 0.75, color=GOLD, stroke_width=0, fill_opacity=0)
        halo.move_to(icon_anchor)
        self.add(halo)
        self.bring_to_back(halo)

        for factor in (0.94, 1.08, 1.0):
            self.play(
                carnot_icon.animate.scale(factor).move_to(icon_anchor),
                halo.animate.set_fill(opacity=0.18),
                run_time=0.5,
            )
            self.play(
                carnot_icon.animate.scale(1 / factor).move_to(icon_anchor),
                halo.animate.set_fill(opacity=0.0),
                run_time=0.5,
            )
        self.wait(0.6)

        # Ratio reveal — the actual payoff of this whole beat.
        formula = MathTex(r"\eta_{\text{max}} = 1 - \frac{T_C}{T_H}", color=GOLD, font_size=56)
        formula.next_to(carnot_icon, RIGHT, buff=1.0)
        box = SurroundingRectangle(formula, color=GOLD, buff=0.2)

        self.play(Write(formula), run_time=1.8)
        self.play(Create(box), run_time=0.8)
        self.wait(2.0)
