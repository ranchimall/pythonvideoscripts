from manim import *
import numpy as np

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60
config.background_color = "#0B1120"


class BondingCurveScenarios(Scene):
    def construct(self):

        # ---------------- DATA (area X*Y = K is constant at every point) ----------------
        K = 24
        xs = [12, 10.75, 9.5, 8.25, 7, 5.75, 4.5, 3.25, 2]   # RanchiMall token remaining
        ys = [K / x for x in xs]                             # SOL in pool (derived, not free)

        titles = [
            "Start", "Slightly Lower Token", "Lower Token",
            "Moderately Lower Token", "Middle Point", "Lower Token",
            "Slightly Lower Token", "Very Low Token", "End",
        ]
        subtitles = [
            "Token highest, Money lowest", "Slightly higher money", "Higher money",
            "Moderately higher money", "Balanced point", "Higher money",
            "Much higher money", "Very high money", "Token lowest, Money highest",
        ]
        colors = [
            ManimColor("#3B82F6"), ManimColor("#8B5CF6"), ManimColor("#F97316"),
            ManimColor("#10B981"), ManimColor("#EC4899"), ManimColor("#06B6D4"),
            ManimColor("#7C3AED"), ManimColor("#14B8A6"), ManimColor("#EF4444"),
        ]

        # ---------------- TITLE / HEADER ----------------
        main_title = Text("Bonding Curve Scenarios", weight=BOLD, font_size=32)
        main_title.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.6)
        tagline = Text("TOKEN SUPPLY DOWN   ·   PRICE UP", font_size=16, color=GREY_B)
        tagline.next_to(main_title, DOWN, buff=0.12).align_to(main_title, LEFT)

        formula = Text("Price = Y / X", font_size=24, weight=BOLD, color=YELLOW)
        formula_note = Text("Y = SOL     X = RanchiMall", font_size=15, color=GREY_B)
        formula_group = VGroup(formula, formula_note).arrange(DOWN, buff=0.1)
        formula_group.to_corner(UR, buff=0.4)

        self.play(Write(main_title), FadeIn(tagline, shift=UP * 0.2), run_time=1.0)
        self.play(FadeIn(formula_group, shift=DOWN * 0.2), run_time=0.6)

        # ---------------- AXES ----------------
        axes = Axes(
            x_range=[0, 13.5, 1],
            y_range=[0, 13.5, 1],
            x_length=6.5,
            y_length=5.2,
            axis_config={"color": GREY_B, "include_tip": True, "stroke_width": 2},
        )
        axes.shift(DOWN * 0.35 + LEFT * 1.3)

        x_label = Text("RanchiMall (X)", font_size=19, color=GREY_B)
        x_label.next_to(axes.x_axis, DOWN, buff=0.2)

        y_label = Text("SOL (Y)", font_size=19, color=GREY_B)
        y_label.next_to(axes.y_axis, UP, buff=0.15).align_to(axes.y_axis, LEFT).shift(RIGHT * 0.05)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.1)

        # faint hyperbola x*y = K, showing the TRUE curve the system moves along
        curve = axes.plot(
            lambda x: K / x, x_range=[1.7, 13, 0.05],
            color=WHITE, stroke_opacity=0.3, stroke_width=2,
        )
        self.play(Create(curve), run_time=1.0)

        # ---------------- TRACKER driving BOTH x and y from one parameter ----------------
        t = ValueTracker(0)

        def get_x():
            return float(np.interp(t.get_value(), range(9), xs))

        def get_y():
            return K / get_x()

        def get_color():
            val = t.get_value()
            idx = min(int(np.floor(val)), 7)
            frac = val - idx
            return interpolate_color(colors[idx], colors[idx + 1], frac)

        # ---------------- RECTANGLE : width*height == K at every instant ----------------
        def make_rect():
            origin = axes.c2p(0, 0)
            corner = axes.c2p(get_x(), get_y())
            rect = Rectangle(
                width=max(corner[0] - origin[0], 0.001),
                height=max(corner[1] - origin[1], 0.001),
                stroke_color=WHITE,
                stroke_width=1.5,
                fill_color=get_color(),
                fill_opacity=0.8,
            )
            rect.move_to(origin, aligned_edge=DL)
            return rect

        rect = always_redraw(make_rect)

        # dot riding along the true xy=K curve, synced to the rectangle's far corner
        dot = always_redraw(lambda: Dot(axes.c2p(get_x(), get_y()), radius=0.08, color=WHITE))

        # live price readout = Y / X, recomputed every frame (not interpolated separately)
        def make_price():
            val = get_y() / get_x()
            txt = Text(f"Price = {val:.2f} SOL", font_size=22, color=YELLOW, weight=BOLD)
            txt.to_corner(DR, buff=0.5)
            return txt

        price_label = always_redraw(make_price)

        # constant-area readout, to visually prove k never changes
        def make_k_readout():
            val = get_x() * get_y()
            txt = Text(f"X · Y = {val:.1f}  (constant)", font_size=18, color=GREY_B)
            txt.next_to(price_label, UP, buff=0.15).align_to(price_label, RIGHT)
            return txt

        k_label = always_redraw(make_k_readout)

        # ---------------- SCENARIO LABEL (centered above the curve, safe zone) ----------------
        def build_label(i):
            num = Text(f"{i + 1}", font_size=26, weight=BOLD, color=colors[i])
            circle = Circle(radius=0.22, color=colors[i], stroke_width=2).move_to(num)
            badge = VGroup(circle, num)
            head = Text(titles[i], weight=BOLD, font_size=25)
            sub = Text(subtitles[i], font_size=17, color=GREY_B)
            text_col = VGroup(head, sub).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            group = VGroup(badge, text_col).arrange(RIGHT, buff=0.2)
            # Anchor at data-coords (7.8, 10.2): since X*Y=24 always, any point where
            # X*Y > 24 sits above the curve and the rectangle can never reach it —
            # this spot stays clear through all 9 scenarios.
            group.move_to(axes.c2p(7.8, 10.2), aligned_edge=LEFT)
            return group    

        label_group = build_label(0)

        self.play(
            FadeIn(rect), FadeIn(dot), FadeIn(price_label), FadeIn(k_label),
            FadeIn(label_group, shift=RIGHT * 0.2),
            run_time=0.8,
        )
        self.wait(0.3)

        # ---------------- STEP THROUGH THE 9 SCENARIOS ----------------
        for i in range(1, 9):
            new_label = build_label(i)
            self.play(
                t.animate.set_value(i),
                FadeOut(label_group, shift=UP * 0.12),
                FadeIn(new_label, shift=UP * 0.12),
                run_time=1.9,
                rate_func=smooth,
            )
            label_group = new_label
            self.wait(0.3)

        self.wait(0.8)

        # ---------------- OUTRO ----------------
        # clear the scene first so the closing line has room to breathe
        self.play(
            FadeOut(rect), FadeOut(dot), FadeOut(price_label), FadeOut(k_label),
            FadeOut(label_group), FadeOut(curve), FadeOut(axes),
            FadeOut(x_label), FadeOut(y_label),
            FadeOut(formula_group), FadeOut(tagline),
            run_time=0.7,
        )
        self.play(main_title.animate.move_to(UP * 1.0), run_time=0.5)

        outro_line1 = Text("Same Formula. A Different Story", font_size=30, weight=BOLD, color=WHITE)
        outro_line2 = Text("at Every Point.", font_size=30, weight=BOLD, color=WHITE)
        outro = VGroup(outro_line1, outro_line2).arrange(DOWN, buff=0.15)
        outro.move_to(DOWN * 0.6)
        self.play(FadeIn(outro, shift=UP * 0.2), run_time=0.8)
        self.wait(2.0)
