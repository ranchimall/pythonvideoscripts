from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_rate = 60
config.background_color = "#0B1120"


class BondingCurveExamples(Scene):
    def construct(self):
        # ---------------- EXAMPLE 1 ----------------
        self.show_example(
            title="Example 1: More Tokens, Lower Price",
            accent="#2E86AB",
            x_desc="High",
            y_desc="Low",
            bar_width=8.0,
            bar_height=1.3,
            x_supply="10,000",
            y_money="100",
            calc_num="100",
            calc_den="10,000",
            price_result="0.01 SOL per RanchiMall",
            hold_time=4.0,
        )

        # ---------------- EXAMPLE 2 ----------------
        self.show_example(
            title="Example 2: Fewer Tokens, Higher Price",
            accent="#C0392B",
            x_desc="Low",
            y_desc="High",
            bar_width=1.3,
            bar_height=8.0,
            x_supply="1,000",
            y_money="100,000",
            calc_num="100,000",
            calc_den="1,000",
            price_result="100 SOL per RanchiMall",
            hold_time=4.0,
        )

    def show_example(self, title, accent, x_desc, y_desc, bar_width, bar_height,
                      x_supply, y_money, calc_num, calc_den, price_result, hold_time):

        accent_color = ManimColor(accent)

        # ---------------- UPPER SECTION ----------------
        title_text = Text(title, weight=BOLD, font_size=28, color=accent_color)
        title_text.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.6)

        formula_box = RoundedRectangle(
            corner_radius=0.12, width=2.6, height=0.85,
            color=GREY_B, stroke_width=2,
            fill_color="#232833", fill_opacity=1,
        )
        formula_text = Text("Price = y / x", font_size=22, weight=BOLD, color=WHITE)
        formula_text.move_to(formula_box)
        formula_group = VGroup(formula_box, formula_text)
        formula_group.to_corner(UR, buff=0.4)

        token_label = Text(f"Token (X: RanchiMall): {x_desc}", font_size=20, color=GREY_A)
        money_label = Text(f"Money (Y: SOL): {y_desc}", font_size=20, color=GREY_A)
        info_labels = VGroup(token_label, money_label).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        info_labels.next_to(title_text, DOWN, buff=0.3).align_to(title_text, LEFT)

        # ---------------- AXES + GRID ----------------
        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 10, 1],
            x_length=6.0, y_length=2.7,
            axis_config={"color": GREY_B, "include_tip": True, "stroke_width": 2},
        )
        axes.move_to(LEFT * 0.9 + UP * 0.55)

        grid = NumberPlane(
            x_range=[0, 10, 1], y_range=[0, 10, 1],
            x_length=6.0, y_length=2.7,
            background_line_style={"stroke_color": GREY_D, "stroke_width": 1, "stroke_opacity": 0.25},
            axis_config={"stroke_opacity": 0},
        )
        grid.move_to(axes)

        x_axis_label = Text("RanchiMall (X)\n(Token)", font_size=17, color=GREY_A, line_spacing=0.9)
        x_axis_label.next_to(axes.x_axis, DOWN, buff=0.2)

        y_axis_label = Text("SOL (Y)\n(Money)", font_size=17, color=GREY_A, line_spacing=0.9)
        y_axis_label.next_to(axes.y_axis, LEFT, buff=0.2).align_to(axes.y_axis, UP)

        origin_label = Text("(0,0)", font_size=15, color=GREY_A)
        origin_label.next_to(axes.c2p(0, 0), DOWN * 0.6 + LEFT * 0.6, buff=0.1)

        # ---------------- BAR ----------------
        origin_pt = axes.c2p(0, 0)
        corner_pt = axes.c2p(bar_width, bar_height)
        bar = Rectangle(
            width=corner_pt[0] - origin_pt[0],
            height=corner_pt[1] - origin_pt[1],
            fill_color=[accent_color, WHITE],
            fill_opacity=1,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        bar.move_to(origin_pt, aligned_edge=DL)

        # ---------------- BOTTOM SECTION ----------------
        values_header = Text("Example Values (illustrative)", weight=BOLD, font_size=19, color=WHITE)
        line1 = Text(f"Token Supply (X: RanchiMall) = {x_supply}", font_size=18, color=GREY_A)
        line2 = Text(f"Total Money (Y: SOL) = {y_money}", font_size=18, color=GREY_A)
        divider = Line(LEFT, RIGHT, color=GREY_B, stroke_width=1)
        divider.set_width(max(line1.width, line2.width))
        calc_label = Text("Price Calculation:", weight=BOLD, font_size=18, color=WHITE)
        calc_line = Text(
            f"Price = y/x = {calc_num} / {calc_den} = {price_result}",
            font_size=20, weight=BOLD, color=accent_color,
        )

        bottom_group = VGroup(
            values_header, line1, line2, divider, calc_label, calc_line
        ).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        bottom_group.to_corner(DL, buff=0.5)

        # ---------------- PHASE 1: graph + upper text ----------------
        self.play(Write(title_text), run_time=0.8)
        self.play(
            FadeIn(formula_group, shift=DOWN * 0.2),
            FadeIn(info_labels, shift=RIGHT * 0.2),
            run_time=0.7,
        )
        self.play(
            Create(axes), FadeIn(grid),
            FadeIn(x_axis_label), FadeIn(y_axis_label), FadeIn(origin_label),
            run_time=1.0,
        )
        self.play(GrowFromPoint(bar, origin_pt), run_time=1.0)
        self.wait(0.3)

        # ---------------- PHASE 2: bottom text ----------------
        self.play(
            LaggedStart(
                *[FadeIn(m, shift=UP * 0.15) for m in bottom_group],
                lag_ratio=0.15,
            ),
            run_time=1.4,
        )

        self.wait(hold_time)

        # ---------------- CLEANUP before next example ----------------
        self.play(
            FadeOut(VGroup(
                title_text, formula_group, info_labels, axes, grid,
                x_axis_label, y_axis_label, origin_label, bar, bottom_group,
            )),
            run_time=0.6,
        )
