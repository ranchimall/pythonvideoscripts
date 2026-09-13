"""
Manim Community Edition scenes for the narration:

    "That's the ceiling. And Carnot goes further — he works out exactly
    what sets that ceiling, and what it depends on.
    Efficiency of ideal engines only depends on temperature. And this
    gives first clue that temperature is hiding some deep secrets like
    Entropy as we will find later.
    Carnot finds that the efficiency of this ideal engine depends on
    nothing but the temperatures of the two reservoirs — the hot one it
    draws heat from, and the cold one it dumps heat into.
    Not the substance inside the engine. Steam, air, any working fluid —
    in the ideal, reversible case, it makes no difference. Not the size
    of the engine, or its design.
    Just the two temperatures. Specifically, the ratio between them."

Three scenes, one per narration beat, so you can render/cut them
independently (mirrors the ~10s clip structure used for the video-gen
prompts):

    manim -pqh carnot_ceiling_manim.py CeilingIntro
    manim -pqh carnot_ceiling_manim.py TemperatureDependency
    manim -pqh carnot_ceiling_manim.py SubstanceIndependence

-pql = fast draft preview, -pqh = 1080p60, -pqk = 4K.
Install: pip install manim (requires a LaTeX distribution for MathTex).
"""

from manim import *

# Palette matched to the earlier storyboard clips
HOT_COLOR = "#EF9F27"
COLD_COLOR = "#378ADD"
GOLD = "#F2A623"
GRAY = "#D3D1C7"
BG = "#1c1c1a"


def make_engine_diagram() -> VGroup:
    """Hot box, cold box, engine (square + piston circle), connecting lines."""
    hot = RoundedRectangle(corner_radius=0.15, width=4, height=0.9, color=HOT_COLOR)
    hot_label = Text("HOT", color=HOT_COLOR, font_size=28).move_to(hot)
    hot_group = VGroup(hot, hot_label).to_edge(UP, buff=1)

    cold = RoundedRectangle(corner_radius=0.15, width=4, height=0.9, color=COLD_COLOR)
    cold_label = Text("COLD", color=COLD_COLOR, font_size=28).move_to(cold)
    cold_group = VGroup(cold, cold_label).to_edge(DOWN, buff=1)

    engine = Square(side_length=1.6, color=GRAY).move_to(ORIGIN)
    piston = Circle(radius=0.45, color=GRAY).move_to(engine)

    line_top = Line(hot_group.get_bottom(), engine.get_top(), color=GRAY, stroke_opacity=0.5)
    line_bottom = Line(engine.get_bottom(), cold_group.get_top(), color=GRAY, stroke_opacity=0.5)

    return VGroup(hot_group, cold_group, engine, piston, line_top, line_bottom)


class CeilingIntro(Scene):
    """Beat 1: 'That's the ceiling. Carnot goes further...'"""

    def construct(self):
        self.camera.background_color = BG

        diagram = make_engine_diagram()
        self.play(FadeIn(diagram), run_time=1.5)

        ceiling_line = DashedLine(LEFT * 4, RIGHT * 4, color=GOLD).next_to(diagram, UP, buff=0.3)
        ceiling_label = Text("the ceiling", color=GOLD, font_size=32).next_to(ceiling_line, UP, buff=0.2)
        self.play(Create(ceiling_line), FadeIn(ceiling_label), run_time=1.2)
        self.wait(0.5)

        caption1 = Text("That's the ceiling.", font_size=32, color=WHITE).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption1), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(caption1))

        caption2 = Text(
            "Carnot goes further — he works out\nexactly what sets that ceiling.",
            font_size=30, color=WHITE,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption2), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(caption2), FadeOut(ceiling_label), FadeOut(ceiling_line))


class TemperatureDependency(Scene):
    """Beat 2: efficiency depends only on temperature; hints at entropy."""

    def construct(self):
        self.camera.background_color = BG

        diagram = make_engine_diagram()
        self.add(diagram)

        th_label = MathTex("T_H", color=HOT_COLOR, font_size=44).next_to(diagram[0], RIGHT, buff=0.4)
        tc_label = MathTex("T_C", color=COLD_COLOR, font_size=44).next_to(diagram[1], RIGHT, buff=0.4)
        self.play(FadeIn(th_label), FadeIn(tc_label), run_time=1)

        caption1 = Text(
            "Efficiency of ideal engines\nonly depends on temperature.",
            font_size=30, color=WHITE,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption1), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(caption1))

        # Faint foreshadowing of entropy - appears softly behind the diagram, then fades
        entropy_word = Text("Entropy", font_size=40, color=GOLD).move_to(ORIGIN).set_opacity(0)
        self.add(entropy_word)
        caption2 = Text(
            "This is the first clue that temperature\nhides something deeper — entropy.",
            font_size=28, color=WHITE,
        ).to_edge(DOWN, buff=0.4)
        self.play(
            entropy_word.animate.set_opacity(0.25).scale(1.3),
            FadeIn(caption2),
            run_time=1.5,
        )
        self.wait(2)
        self.play(FadeOut(caption2), FadeOut(entropy_word), FadeOut(th_label), FadeOut(tc_label))


class SubstanceIndependence(Scene):
    """Beat 3: efficiency depends only on T_H, T_C — not substance, size, or design."""

    def construct(self):
        self.camera.background_color = BG

        diagram = make_engine_diagram().scale(0.7).to_edge(LEFT, buff=1)
        self.play(FadeIn(diagram), run_time=1)

        caption1 = Text(
            "Carnot finds efficiency depends on\nnothing but the two temperatures.",
            font_size=28, color=WHITE,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption1), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(caption1))

        # Row of substance labels — all feed the same result regardless of fluid
        steam = Text("steam", font_size=26, color=GRAY)
        air = Text("air", font_size=26, color=GRAY)
        fluid = Text("any fluid", font_size=26, color=GRAY)
        icons = VGroup(steam, air, fluid).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=1.5)

        caption2 = Text(
            "Not the substance inside — steam, air,\nany working fluid makes no difference.",
            font_size=26, color=WHITE,
        ).to_edge(DOWN, buff=0.4)
        self.play(LaggedStartMap(FadeIn, icons, lag_ratio=0.3), FadeIn(caption2), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(caption2))

        caption3 = Text(
            "Not the size of the engine, or its design.",
            font_size=28, color=WHITE,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption3), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(caption3), FadeOut(icons), FadeOut(diagram))

        # Final reveal: the efficiency formula, ratio of temperatures
        formula = MathTex(r"\eta_{\text{max}} = 1 - \frac{T_C}{T_H}", color=GOLD, font_size=64).move_to(ORIGIN)
        caption4 = Text(
            "Just the two temperatures.\nSpecifically, the ratio between them.",
            font_size=28, color=WHITE,
        ).to_edge(DOWN, buff=0.5)

        self.play(Write(formula), run_time=2)
        self.play(FadeIn(caption4), run_time=1)
        self.wait(2.5)

        box = SurroundingRectangle(formula, color=GOLD, buff=0.2)
        self.play(Create(box), run_time=1)
        self.wait(2)
