"""
Manim Community Edition scene for the "efficiency gap" narration beat.

Voice line this maps to (18.0s total):
  "A bigger gap between hot and cold means a higher possible efficiency.
   A smaller gap means less. And if the two reservoirs were at the same
   temperature, the ideal engine could do no work at all."

Picks up from the exact ending layout of RatioSplitReveal (in
carnot_temperature_manim7.py):
    carnot_icon + "CARNOT" label -> centered at LEFT*2.0
    HOT bar + T_H                -> centered at RIGHT*2.7 + UP*0.6
    COLD bar + T_C                -> centered at RIGHT*2.7 + DOWN*0.6
This file is self-contained (re-declares the same helper builders/colors
as manim7) so it renders standalone.

Beat breakdown:
  1. 0.0 - 7.0s  "A bigger gap ... higher possible efficiency."
     Engine slides off the left edge, fading once it clears frame.
     HOT/COLD recenter into the middle of frame and spread apart.
     "HIGH EFFICIENCY" (small-caps) fades in between them.
  2. 7.0 - 10.0s "A smaller gap means less."
     HOT/COLD move closer together. Text swaps to "LOW EFFICIENCY".
  3. 10.0 - 18.0s "...same temperature ... no work at all."
     T_H/T_C fade out, HOT/COLD collapse into full overlap at center,
     dissolve into a single merged bar whose fill shimmers unstably
     between a muddy blend and flickers of orange/blue (never settling
     on either), while "NO WORK AT ALL" fades in beneath it.

Render:
    manim -pqh carnot_temperature_manim8.py EfficiencyGapCollapse
"""

import os
import numpy as np
from manim import *

# ---------------------------------------------------------------------------
# Config (matches carnot_temperature_manim7.py)
# ---------------------------------------------------------------------------
PNG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "Carnot_engine.png")

HOT_COLOR_1 = "#F2B33D"   # gold end of the HOT gradient
HOT_COLOR_2 = "#E8672A"   # orange end of the HOT gradient
COLD_COLOR = "#3B8FE0"    # COLD bar color
GRAY = "#D3D1C7"
GOLD = "#F2A623"
BG = "#1c1c1a"

# Muddy blend used as the shimmer's resting color — halfway between the
# HOT and COLD hues, so it reads as neither "hot" nor "cold".
# NOTE: interpolate_color in Manim CE 0.21 requires ManimColor objects,
# not raw hex strings, hence the explicit wraps here and in shimmer_updater.
HOT_COLOR_2_MC = ManimColor(HOT_COLOR_2)
COLD_COLOR_MC = ManimColor(COLD_COLOR)
MUDDY_COLOR = interpolate_color(HOT_COLOR_2_MC, COLD_COLOR_MC, 0.5)


# ---------------------------------------------------------------------------
# Shared builders (identical to manim7, reproduced so this file is standalone)
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


def load_carnot_icon() -> ImageMobject:
    icon = ImageMobject(PNG_PATH)
    icon.set(width=2.6)
    return icon


def make_small_caps(text: str, big_size: int = 26, small_size: int = 18, color=WHITE) -> VGroup:
    """Bold white label styled as small caps: first letter of each word at
    `big_size`, remaining letters at `small_size`, baseline-aligned —
    matching the HOT/COLD look at a smaller, typographic-small-caps scale.
    """
    word_groups = []
    for word in text.split(" "):
        first = Text(word[0].upper(), color=color, font_size=big_size, weight=BOLD)
        if len(word) > 1:
            rest = Text(word[1:].upper(), color=color, font_size=small_size, weight=BOLD)
            rest.align_to(first, DOWN)
            rest.next_to(first, RIGHT, buff=0.02)
            word_groups.append(VGroup(first, rest))
        else:
            word_groups.append(VGroup(first))
    return VGroup(*word_groups).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)


# ---------------------------------------------------------------------------
# "A bigger gap ... higher possible efficiency. A smaller gap means less.
#  And if the two reservoirs were at the same temperature, the ideal
#  engine could do no work at all." (18.0s total)
# ---------------------------------------------------------------------------
class EfficiencyGapCollapse(Scene):
    def construct(self):
        self.camera.background_color = BG

        # --- Recreate RatioSplitReveal's exact ending layout ---
        hot = make_hot_bar()
        cold = make_cold_bar()
        carnot_icon = load_carnot_icon()
        carnot_name = Text("CARNOT", color=WHITE, font_size=26, weight=BOLD)
        carnot_name.next_to(carnot_icon, DOWN, buff=0.25)

        th_label = MathTex("T_H", color=WHITE, font_size=40).next_to(hot, RIGHT, buff=0.4)
        tc_label = MathTex("T_C", color=WHITE, font_size=40).next_to(cold, RIGHT, buff=0.4)

        hot_group = VGroup(hot, th_label)
        cold_group = VGroup(cold, tc_label)
        engine_group = Group(carnot_icon, carnot_name)

        engine_group.move_to(LEFT * 2.0)
        hot_group.move_to(RIGHT * 2.7 + UP * 0.6)
        cold_group.move_to(RIGHT * 2.7 + DOWN * 0.6)

        self.add(engine_group, hot_group, cold_group)

        # =====================================================================
        # Beat 1 (7.0s) — "A bigger gap between hot and cold means a higher
        # possible efficiency."
        # =====================================================================

        # Stage A (2.0s): engine slides toward/past the left edge (frame
        # half-width ~7.1, so a 6.5-unit shift from x=-2.0 clears it);
        # HOT/COLD begin recentering and spreading apart at the same time.
        self.play(
            engine_group.animate.shift(LEFT * 6.5),
            hot_group.animate.move_to(UP * 1.4),
            cold_group.animate.move_to(DOWN * 1.4),
            run_time=2.0,
            rate_func=smooth,
        )

        # Stage B (0.6s): engine has cleared the frame — fade it out there
        # (slide, then fade, as requested) while HOT/COLD finish spreading
        # to their widest gap.
        self.play(
            FadeOut(engine_group),
            hot_group.animate.move_to(UP * 2.3),
            cold_group.animate.move_to(DOWN * 2.3),
            run_time=0.6,
        )

        # Stage C (0.8s): "HIGH EFFICIENCY" fades in, centered in the gap.
        high_eff = make_small_caps("HIGH EFFICIENCY").move_to(ORIGIN)
        self.play(FadeIn(high_eff, shift=UP * 0.1), run_time=0.8)

        # Hold on the wide-gap / high-efficiency state.
        self.wait(3.6)
        # Beat 1 total: 2.0 + 0.6 + 0.8 + 3.6 = 7.0s

        # =====================================================================
        # Beat 2 (3.0s) — "A smaller gap means less."
        # =====================================================================

        low_eff = make_small_caps("LOW EFFICIENCY").move_to(ORIGIN)

        # Stage A (1.2s): bars move closer together; old text fades as the
        # gap starts shrinking.
        self.play(
            FadeOut(high_eff),
            hot_group.animate.move_to(UP * 0.9),
            cold_group.animate.move_to(DOWN * 0.9),
            run_time=1.2,
        )

        # Stage B (0.8s): "LOW EFFICIENCY" fades in at the smaller gap.
        self.play(FadeIn(low_eff, shift=UP * 0.1), run_time=0.8)

        self.wait(1.0)
        # Beat 2 total: 1.2 + 0.8 + 1.0 = 3.0s

        # =====================================================================
        # Beat 3 (8.0s) — "...if the two reservoirs were at the same
        # temperature, the ideal engine could do no work at all."
        # =====================================================================

        # Stage A (1.5s): temperature labels drop out (they're about to
        # become meaningless — same temperature, no gap), "LOW EFFICIENCY"
        # fades, and the bars start closing the remaining distance.
        self.play(
            FadeOut(low_eff),
            FadeOut(th_label),
            FadeOut(tc_label),
            hot.animate.move_to(UP * 0.5),
            cold.animate.move_to(DOWN * 0.5),
            run_time=1.5,
        )

        # Stage B (2.0s): bars close in fully, overlapping at center.
        self.play(
            hot.animate.move_to(ORIGIN),
            cold.animate.move_to(ORIGIN),
            run_time=2.0,
            rate_func=smooth,
        )

        # Stage C1 (0.5s): dissolve both overlapping bars (with their HOT/
        # COLD text) into a single plain merged shape — the two identities
        # blur together rather than one simply sitting on top of the other.
        merged_bar = RoundedRectangle(corner_radius=0.18, width=4.4, height=1.0)
        merged_bar.set_stroke(width=0)
        merged_bar.set_fill(color=MUDDY_COLOR, opacity=1)
        merged_bar.move_to(ORIGIN)

        self.play(FadeTransform(VGroup(hot, cold), merged_bar), run_time=0.5)

        # Stage C2 (3.0s): the merged region shimmers unstably — never
        # settling into orange or blue, just restlessly drifting through a
        # muddy blend with flickers of each, while "NO WORK AT ALL" fades
        # in beneath it. Driven by summed sine waves (deterministic, but
        # visually reads as "can't decide what it is").
        def shimmer_updater(mob, alpha):
            t = alpha * 3.0
            mix = (
                0.5
                + 0.35 * np.sin(2 * PI * 0.7 * t)
                + 0.25 * np.sin(2 * PI * 1.9 * t + 1.1)
                + 0.15 * np.sin(2 * PI * 4.3 * t + 2.2)
            )
            mix = float(np.clip(mix, 0.0, 1.0))
            if mix > 0.5:
                c = interpolate_color(MUDDY_COLOR, HOT_COLOR_2_MC, (mix - 0.5) * 2)
            else:
                c = interpolate_color(MUDDY_COLOR, COLD_COLOR_MC, (0.5 - mix) * 2)
            mob.set_fill(color=c, opacity=1)

        no_work = make_small_caps("NO WORK AT ALL").next_to(merged_bar, DOWN, buff=0.6)

        self.play(
            UpdateFromAlphaFunc(merged_bar, shimmer_updater),
            FadeIn(no_work, shift=UP * 0.1),
            run_time=3.0,
        )

        # Stage D (1.0s): hold — brief continued shimmer, then settle to a
        # close on the merged, motionless-looking bar and the text.
        self.play(
            UpdateFromAlphaFunc(merged_bar, shimmer_updater),
            run_time=1.0,
        )
        # Beat 3 total: 1.5 + 2.0 + 0.5 + 3.0 + 1.0 = 8.0s

        # Scene total: 7.0 + 3.0 + 8.0 = 18.0s
