"""
Manim Community Edition scenes for the "temperature ceiling" narration beat,
built around your actual assets:

  - assets/Carnot_engine.png   -> the detailed Carnot engine icon
                                   (transparent PNG — swapped in place of
                                   an earlier low-quality auto-traced SVG)
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
    manim -pqh carnot_temperature_manim.py HotZoomBoilingReveal

-pql = fast draft preview, -pqh = 1080p60, -pqk = 4K.
Requires: pip install manim  (plus a LaTeX install for the MathTex formula
in the last scene).

IMPORTANT: update PNG_PATH below to point at your Carnot_engine.png file.
"""

import os
import random
import numpy as np
from manim import *

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PNG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "Carnot_engine.png")

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


def load_carnot_icon() -> ImageMobject:
    """Loads the transparent Carnot engine PNG. Using ImageMobject instead
    of SVGMobject here — the original SVG was a poor-quality auto-trace
    (~425 tiny overlapping paths), while this PNG has a clean alpha
    channel and renders sharper. Note the different API surface: an
    ImageMobject doesn't have set_color()/set_fill() like the SVG version
    did, since it's a raster image, not vector paths — any color changes
    to it in existing scenes (there are none currently) would need to be
    done via opacity/overlay effects instead."""
    icon = ImageMobject(PNG_PATH)
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
        # the same IS the argument, so it's never recolored directly
        # anyway (ImageMobject doesn't support set_color/set_fill since
        # it's a raster image, not vector paths) — instead a separate
        # halo glows behind it, and the icon itself only scales up/down
        # and back by an inverse factor each pass, so it returns to its
        # exact original size.
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


# ---------------------------------------------------------------------------
# Continuation of Clip 1: zoom into HOT, dissolve into a literal boiling
# close-up — the wordless "temperature is hiding something" tease.
# Voice line this maps to:
#   "And Carnot goes further — he works out exactly what sets that
#    ceiling, and what it depends on. Efficiency of ideal engines only
#    depends on temperature. And this gives first clue that temperature
#    is hiding some deep secrets like Entropy as we will find later."
# ---------------------------------------------------------------------------
def build_liquid_container(width, height, position):
    """Returns (backing rect, wave line as always_redraw, phase tracker,
    bubble circles). The rect and bubbles are plain Mobjects you add/animate
    yourself; the wave is already a live always_redraw hooked to `phase` —
    just add it once and animate `phase` to make it undulate."""
    rect = RoundedRectangle(corner_radius=0.05, width=width, height=height)
    rect.set_fill(color=[HOT_COLOR_2, HOT_COLOR_1], opacity=1)
    rect.set_stroke(width=0)
    rect.move_to(position)

    phase = ValueTracker(0)

    def wave_points():
        n = 40
        amp = height * 0.05
        top_y = rect.get_top()[1]
        left_x = rect.get_left()[0]
        pts = []
        for i in range(n + 1):
            x = left_x + width * i / n
            y = top_y + amp * np.sin(2 * PI * (i / n) * 2 + phase.get_value())
            pts.append(np.array([x, y, 0]))
        return pts

    wave = always_redraw(
        lambda: VMobject(color=WHITE, stroke_width=2, stroke_opacity=0.55).set_points_as_corners(wave_points())
    )

    rng = random.Random(7)  # fixed seed so bubble layout is reproducible across renders
    bubbles = VGroup()
    for _ in range(9):
        r = rng.uniform(0.03, 0.08) * width
        x = rect.get_left()[0] + rng.uniform(0.12, 0.88) * width
        y = rect.get_bottom()[1] + rng.uniform(0.05, 0.3) * height
        bubble = Circle(radius=r, color=WHITE, fill_opacity=0.35, stroke_width=1, stroke_color=WHITE, stroke_opacity=0.5)
        bubble.move_to([x, y, 0])
        bubbles.add(bubble)

    return rect, wave, phase, bubbles


class HotZoomBoilingReveal(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG

        hot = make_hot_bar()
        cold = make_cold_bar()
        dial = make_generic_dial().move_to(ORIGIN)
        top_wire = make_connector(hot.get_bottom(), dial.get_top())
        bottom_wire = make_connector(dial.get_bottom(), cold.get_top())
        self.add(hot, cold, dial, top_wire, bottom_wire)
        self.wait(0.3)

        # Step 1: push camera in, framing only the HOT bar.
        self.play(
            self.camera.frame.animate.scale(0.5).move_to(hot.get_center()),
            run_time=2.0,
        )
        self.wait(0.4)

        # Step 2: push in further, until the bar nearly fills the frame —
        # "going further" into what temperature actually is.
        self.play(
            self.camera.frame.animate.scale(0.35).move_to(hot.get_center()),
            run_time=1.6,
        )
        self.wait(0.3)

        # Step 3: dissolve the flat HOT label/bar into a literal boiling
        # close-up. FadeTransform gives a cross-dissolve feel rather than a
        # hard cut, so the transition reads as "entering" the surface.
        rect, wave, phase, bubbles = build_liquid_container(
            hot[0].width, hot[0].height, hot[0].get_center()
        )
        self.play(FadeOut(hot[1]), run_time=0.4)  # drop the "HOT" text first
        self.play(FadeTransform(hot[0], rect), run_time=1.2)
        self.add(wave)
        self.play(FadeIn(bubbles, lag_ratio=0.15), run_time=1.0)

        # Step 4: the bubbling itself — surface undulates, bubbles rise and
        # thin out near the top, all wordless. This is the "hidden secret"
        # beat: something is moving beneath what looked like a flat, simple
        # label a moment ago.
        bubble_anims = []
        for b in bubbles:
            rise = rect.height * random.Random(hash(tuple(b.get_center())) % (2**32)).uniform(0.7, 1.0)
            target = b.get_center() + UP * rise
            bubble_anims.append(b.animate.move_to(target).scale(0.35).set_fill(opacity=0))

        self.play(
            phase.animate.increment_value(4 * PI),
            AnimationGroup(*bubble_anims, lag_ratio=0.08),
            run_time=4.0,
            rate_func=linear,
        )
        self.wait(0.6)


# ---------------------------------------------------------------------------
# Continuation of HotZoomBoilingReveal, ~6s — picks up exactly where that
# scene's crop leaves off (tight on the boiling HOT surface, no dial/cold/
# wires in frame) and pushes into a single bubble until its interior
# becomes a new nested liquid surface — layer beneath layer.
# Voice line this covers:
#   "...temperature is hiding some deep secrets like Entropy as we will
#    find later."
# ---------------------------------------------------------------------------
class BubbleWithinBubbleReveal(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG

        # Recreate the same tight crop the previous scene ends on: the
        # boiling HOT rectangle filling the frame, nothing else visible.
        # Dimensions match make_hot_bar()'s bar exactly for continuity.
        rect_width, rect_height = 4.4, 1.0
        rect, wave, phase, bubbles = build_liquid_container(rect_width, rect_height, ORIGIN)

        # Shift the bubbles up to roughly where they'd have risen to by the
        # end of the previous clip (mid-flight near the surface), so the
        # very first rendered frame here already matches that cut point.
        for b in bubbles:
            b.shift(UP * rect_height * 0.65)

        self.add(rect, wave, bubbles)
        self.camera.frame.scale(0.35).move_to(ORIGIN)  # same crop as prior scene's end
        self.wait(0.4)

        # Clear the ordinary bubbles out of frame, singling out one to
        # become the hero — the rest drift up and fade, same wordless
        # bubbling motion as before, just thinning out to make room.
        hero = max(bubbles, key=lambda b: b.width)
        others = [b for b in bubbles if b is not hero]
        clear_anims = [b.animate.shift(UP * rect_height * 0.6).set_fill(opacity=0) for b in others]
        self.play(
            AnimationGroup(*clear_anims, lag_ratio=0.05),
            phase.animate.increment_value(PI),
            run_time=1.0,
            rate_func=linear,
        )

        # A brief halo pulse marks the hero bubble as significant before
        # it grows — still just motion/light, no text.
        halo = Circle(radius=hero.width * 0.9, color=GOLD, stroke_width=0, fill_opacity=0)
        halo.move_to(hero.get_center())
        self.add(halo)
        self.play(halo.animate.set_fill(opacity=0.25), run_time=0.4)
        self.play(halo.animate.set_fill(opacity=0.0), run_time=0.4)

        # Camera pushes into the hero bubble until its edge fills the
        # frame. Computed relative to the frame's current width so this
        # works regardless of how the earlier zoom levels were tuned.
        hero_center = hero.get_center()
        current_width = self.camera.frame.width
        target_width = hero.width * 3.2  # padding so the bubble's edge clears frame nicely
        scale_factor = target_width / current_width
        self.play(
            self.camera.frame.animate.scale(scale_factor).move_to(hero_center),
            run_time=1.8,
        )

        # Dissolve the hero bubble into a nested liquid surface — one
        # layer deeper, same visual language, slightly more saturated to
        # suggest depth without introducing a new color.
        nested_width = self.camera.frame.width * 1.3
        nested_height = nested_width * (rect_height / rect_width)
        nested_rect, nested_wave, nested_phase, nested_bubbles = build_liquid_container(
            nested_width, nested_height, hero_center
        )
        nested_rect.set_fill(color=[HOT_COLOR_2, "#C94A1A"], opacity=1)  # deeper, more saturated red-orange

        self.play(FadeTransform(hero, nested_rect), FadeOut(halo), run_time=1.0)
        self.add(nested_wave)
        self.play(FadeIn(nested_bubbles, lag_ratio=0.15), run_time=0.5)

        # Brief ambient hold on the nested layer to close out the beat.
        self.play(nested_phase.animate.increment_value(PI), run_time=0.5, rate_func=linear)
        self.wait(0.1)


# ---------------------------------------------------------------------------
# Beat 1 of the next voice line: "Carnot finds that the efficiency of this
# ideal engine depends on nothing but the temperatures of the two
# reservoirs — the hot one it draws heat from, and the cold one it dumps
# heat into."
#
# Same HOT/COLD/dial composition as HotColdDialPushIn. T_H/T_C labels
# attach to the bars, then two separate directional pulses (Option B):
# one travels HOT -> dial ("draws heat from"), a pause, then a second
# departs dial -> COLD ("dumps heat into"). Each clause of the sentence
# gets its own beat of motion rather than one continuous dot.
# ---------------------------------------------------------------------------
class HeatFlowLabeling(Scene):
    def construct(self):
        self.camera.background_color = BG

        hot = make_hot_bar()
        cold = make_cold_bar()
        dial = make_generic_dial().move_to(ORIGIN)
        top_wire = make_connector(hot.get_bottom(), dial.get_top())
        bottom_wire = make_connector(dial.get_bottom(), cold.get_top())
        self.add(hot, cold, dial, top_wire, bottom_wire)
        self.wait(0.3)

        # T_H / T_C labels attach to the reservoirs — diagram labels, not
        # narrative captions.
        th_label = MathTex("T_H", color=WHITE, font_size=40).next_to(hot, RIGHT, buff=0.4)
        tc_label = MathTex("T_C", color=WHITE, font_size=40).next_to(cold, RIGHT, buff=0.4)
        self.play(FadeIn(th_label, shift=LEFT * 0.2), run_time=0.7)
        self.wait(0.2)
        self.play(FadeIn(tc_label, shift=LEFT * 0.2), run_time=0.7)
        self.wait(0.5)

        # Pulse 1 — "draws heat from": travels HOT -> dial along the top
        # wire, arriving with a small flash at the dial.
        pulse_in = Dot(radius=0.08, color=GOLD)
        pulse_in.move_to(top_wire.get_start())
        self.add(pulse_in)
        self.play(MoveAlongPath(pulse_in, top_wire), run_time=1.0, rate_func=smooth)
        self.play(Flash(dial.get_center(), color=GOLD, flash_radius=0.6, line_length=0.25), run_time=0.4)
        self.play(FadeOut(pulse_in), run_time=0.3)

        # Beat between the two clauses of the sentence.
        self.wait(0.6)

        # Pulse 2 — "dumps heat into": departs the dial with a flash, then
        # travels dial -> COLD along the bottom wire.
        self.play(Flash(dial.get_center(), color=COLD_COLOR, flash_radius=0.5, line_length=0.2), run_time=0.3)
        pulse_out = Dot(radius=0.08, color=COLD_COLOR)
        pulse_out.move_to(bottom_wire.get_start())
        self.add(pulse_out)
        self.play(MoveAlongPath(pulse_out, bottom_wire), run_time=1.0, rate_func=smooth)
        self.play(FadeOut(pulse_out), run_time=0.3)

        self.wait(1.0)


# ---------------------------------------------------------------------------
# 10-second extension for: "...but the two temperatures... hot one it draws
# heat from, cold one it dumps into"
#
# Beat 1 (0:00-0:04, "but the two temperatures"): HOT and COLD bars both
#   pop up slightly in size (twice — a bigger pop then a smaller echo).
# Beat 2 (0:04-0:07, "hot one it draws heat from"): HOT bar pops once
#   more, then a stream of gold heat-dots flows out of HOT, down the top
#   wire, and arrives at the dial.
# Beat 3 (0:07-0:10, "cold one it dumps into"): the heat stream continues
#   down the bottom wire into COLD, and the COLD bar's fill warms from
#   blue to a yellowish gold as the heat is dumped into it.
#
# Total run time: exactly 10.0s. Built entirely from the same procedural
# mobjects as the rest of this file (make_hot_bar / make_cold_bar /
# make_generic_dial / make_connector) so it matches the established look
# exactly rather than importing the reference PNG.
#
# Render:
#   manim -pqh carnot_temperature_manim4.py TemperaturesHeatFlowExtension
# ---------------------------------------------------------------------------
class TemperaturesHeatFlowExtension(Scene):
    def construct(self):
        self.camera.background_color = BG

        hot = make_hot_bar()
        cold = make_cold_bar()
        dial = make_generic_dial().move_to(ORIGIN)
        top_wire = make_connector(hot.get_bottom(), dial.get_top())
        bottom_wire = make_connector(dial.get_bottom(), cold.get_top())

        th_label = MathTex("T_H", color=WHITE, font_size=40).next_to(hot, RIGHT, buff=0.4)
        tc_label = MathTex("T_C", color=WHITE, font_size=40).next_to(cold, RIGHT, buff=0.4)

        self.add(hot, cold, dial, top_wire, bottom_wire, th_label, tc_label)

        # -------------------------------------------------------------
        # Beat 1 (4.0s) — "but the two temperatures"
        # Both bars pop up slightly in size: one confident pop, then a
        # smaller echo pop, with breathing room around each.
        # -------------------------------------------------------------
        self.play(
            hot.animate(rate_func=there_and_back).scale(1.15),
            cold.animate(rate_func=there_and_back).scale(1.15),
            run_time=1.2,
        )
        self.wait(0.4)
        self.play(
            hot.animate(rate_func=there_and_back).scale(1.08),
            cold.animate(rate_func=there_and_back).scale(1.08),
            run_time=0.9,
        )
        self.wait(1.5)
        # Beat 1 subtotal: 1.2 + 0.4 + 0.9 + 1.5 = 4.0s

        # -------------------------------------------------------------
        # Beat 2 (3.0s) — "hot one it draws heat from"
        # HOT pops again, then heat (gold dots) streams out of HOT and
        # down the top wire, arriving at the dial.
        # -------------------------------------------------------------
        self.play(hot.animate(rate_func=there_and_back).scale(1.12), run_time=0.7)
        self.wait(0.2)

        n_heat_dots = 5
        heat_dots = VGroup(*[
            Dot(radius=0.09, color=GOLD, fill_opacity=0.9).move_to(top_wire.get_start())
            for _ in range(n_heat_dots)
        ])
        self.add(heat_dots)
        self.play(
            AnimationGroup(*[
                MoveAlongPath(dot, top_wire) for dot in heat_dots
            ], lag_ratio=0.18),
            run_time=2.1,
            rate_func=smooth,
        )
        # Beat 2 subtotal: 0.7 + 0.2 + 2.1 = 3.0s

        # -------------------------------------------------------------
        # Beat 3 (3.0s) — "cold one it dumps into"
        # Heat continues down the bottom wire and is dumped into COLD:
        # the dots travel on, fade as they land, and COLD's fill warms
        # from blue to a yellowish gold.
        # -------------------------------------------------------------
        for dot in heat_dots:
            dot.move_to(bottom_wire.get_start())
        self.play(
            AnimationGroup(*[
                MoveAlongPath(dot, bottom_wire) for dot in heat_dots
            ], lag_ratio=0.15),
            run_time=1.6,
            rate_func=smooth,
        )

        cold_bar = cold[0]
        self.play(
            FadeOut(heat_dots),
            cold_bar.animate.set_fill(color=[HOT_COLOR_1, GOLD], opacity=1),
            Flash(cold.get_center(), color=GOLD, flash_radius=1.6, line_length=0.3),
            run_time=1.0,
        )
        self.wait(0.4)
        # Beat 3 subtotal: 1.6 + 1.0 + 0.4 = 3.0s

        # Total: 4.0 + 3.0 + 3.0 = 10.0s


# ---------------------------------------------------------------------------
# Hand-built line-art icons (steam / air / fluid) — no external assets,
# built from primitives to match the existing gray line-art style used by
# make_generic_dial().
# ---------------------------------------------------------------------------
def make_steam_icon() -> VGroup:
    """Three small wavy squiggles suggesting rising steam."""
    wisps = VGroup()
    for dx in (-0.16, 0.0, 0.16):
        pts = [np.array([dx + 0.05 * np.sin(i * PI / 1.4), i * 0.09, 0]) for i in range(7)]
        wisp = VMobject(color=GRAY, stroke_width=2.5)
        wisp.set_points_smoothly(pts)
        wisps.add(wisp)
    wisps.move_to(ORIGIN)
    return wisps


def make_air_icon() -> VGroup:
    """Two curved 'wind' arcs suggesting moving air."""
    arc1 = Arc(radius=0.26, start_angle=PI * 0.85, angle=-PI * 0.85, color=GRAY, stroke_width=2.5)
    arc2 = Arc(radius=0.17, start_angle=PI * 0.85, angle=-PI * 0.65, color=GRAY, stroke_width=2.5)
    arc2.next_to(arc1, DOWN, buff=0.05)
    return VGroup(arc1, arc2)


def make_fluid_icon() -> VGroup:
    """A simple teardrop / droplet outline — pointed top, rounded bottom."""
    pts = [
        np.array([0, 0.30, 0]), np.array([0.17, 0.02, 0]), np.array([0.19, -0.14, 0]),
        np.array([0.09, -0.27, 0]), np.array([-0.09, -0.27, 0]), np.array([-0.19, -0.14, 0]),
        np.array([-0.17, 0.02, 0]), np.array([0, 0.30, 0]),
    ]
    drop = VMobject(color=GRAY, stroke_width=2.5)
    drop.set_points_smoothly(pts)
    return VGroup(drop)


# Shared zoom target so SubstanceZoomToCarnot and SubstanceIconsNoDifference
# use an identical crop — the second scene picks up exactly where the
# first one's camera settles, same continuity trick used for
# BubbleWithinBubbleReveal picking up from HotZoomBoilingReveal.
SUBSTANCE_ZOOM_SCALE = 0.42
SUBSTANCE_ZOOM_CENTER = ORIGIN


# ---------------------------------------------------------------------------
# "Not the substance inside the engine." (~5.0s)
# Push in on the dial, then cross-dissolve it into the real Carnot icon —
# fade out / fade in at the same center rather than a literal shape morph.
# A literal Transform from a plain circle into the detailed engine icon
# produce a messy stretching artifact rather than a clean reveal, so this
# uses a cross-dissolve instead, as discussed.
# ---------------------------------------------------------------------------
class SubstanceZoomToCarnot(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG

        hot = make_hot_bar()
        cold = make_cold_bar()
        dial = make_generic_dial().move_to(ORIGIN)
        top_wire = make_connector(hot.get_bottom(), dial.get_top())
        bottom_wire = make_connector(dial.get_bottom(), cold.get_top())
        th_label = MathTex("T_H", color=WHITE, font_size=40).next_to(hot, RIGHT, buff=0.4)
        tc_label = MathTex("T_C", color=WHITE, font_size=40).next_to(cold, RIGHT, buff=0.4)
        self.add(hot, cold, dial, top_wire, bottom_wire, th_label, tc_label)
        self.wait(0.3)

        # Slow push into the dial — "the engine" the line is pointing at.
        self.play(
            self.camera.frame.animate.scale(SUBSTANCE_ZOOM_SCALE).move_to(SUBSTANCE_ZOOM_CENTER),
            run_time=3.2,
            rate_func=smooth,
        )
        self.wait(0.2)

        # Cross-dissolve: dial fades out, Carnot icon fades in at the same
        # center — the "real" engine resolving into view.
        carnot_icon = load_carnot_icon().move_to(dial.get_center())
        self.play(FadeOut(dial), FadeIn(carnot_icon, scale=0.9), run_time=1.0)
        self.wait(0.3)
        # Total: 0.3 + 3.2 + 0.2 + 1.0 + 0.3 = 5.0s


# ---------------------------------------------------------------------------
# "Steam, air, any working fluid — in the ideal, reversible case, it makes
# no difference." (~5.0s)
# Picks up already zoomed on the Carnot icon (same crop SubstanceZoomToCarnot
# ends on). Three hand-built icons appear one at a time into fixed slots in
# a row above the engine — no repositioning needed as each new one arrives,
# matching "beside it" rather than "replacing it." All three then zoom out
# and vanish together; the engine itself never changes the whole time.
# ---------------------------------------------------------------------------
class SubstanceIconsNoDifference(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG

        carnot_icon = load_carnot_icon().move_to(ORIGIN)
        self.add(carnot_icon)
        self.camera.frame.scale(SUBSTANCE_ZOOM_SCALE).move_to(SUBSTANCE_ZOOM_CENTER)
        self.wait(0.2)

        row_y = carnot_icon.get_top()[1] + 0.35
        steam = make_steam_icon().scale(0.55).move_to([-0.55, row_y, 0])
        air = make_air_icon().scale(0.55).move_to([0, row_y, 0])
        fluid = make_fluid_icon().scale(0.55).move_to([0.55, row_y, 0])

        # "Steam"
        self.play(FadeIn(steam, shift=UP * 0.15), run_time=0.7)
        self.wait(0.3)

        # "air"
        self.play(FadeIn(air, shift=UP * 0.15), run_time=0.7)
        self.wait(0.3)

        # "any working fluid"
        self.play(FadeIn(fluid, shift=UP * 0.15), run_time=0.7)
        self.wait(0.4)

        # "in the ideal, reversible case, it makes no difference" — all
        # three zoom out together and vanish; the engine underneath never
        # changed the entire time.
        icons = VGroup(steam, air, fluid)
        self.play(icons.animate.scale(1.6).set_opacity(0), run_time=1.3)
        self.wait(0.4)
        # Total: 0.2 + 0.7+0.3 + 0.7+0.3 + 0.7+0.4 + 1.3 + 0.4 = 5.0s
