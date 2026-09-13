
# ============================================================
# NAVIER–STOKES · PART 5
# VISCOSITY DOESN'T SIMPLY "LOSE"
#
# CINEMATIC SCIENTIFIC VISUALIZATION
#
# Story:
#
# 01  The tempting story
#     nonlinear effects grow
#          ↓
#     viscosity gets overwhelmed
#          ↓
#     infinity
#
# 02  But viscosity is still present
#
# 03  Several terms become large together
#
# 04  They balance through delicate cancellation
#
# 05  Velocity can still diverge while external forcing
#     remains smooth.
#
# ------------------------------------------------------------
#
# VIDEO
#   Duration:     30 seconds
#   FPS:          24
#   Resolution:   1280 × 720
#   Format:       WebM / VP9
#
# ------------------------------------------------------------
#
# REQUIREMENTS
#
#   pip install numpy matplotlib
#
# FFmpeg must also be installed and available on PATH.
#
# ============================================================


import numpy as np
import matplotlib.pyplot as plt
import textwrap

from matplotlib.animation import (
    FuncAnimation,
    FFMpegWriter
)

from matplotlib.patches import (
    Circle,
    FancyBboxPatch
)

from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

FPS = 24

DURATION = 30

TOTAL_FRAMES = FPS * DURATION

FIG_WIDTH = 16
FIG_HEIGHT = 9

DPI = 150

OUTPUT = Path(
    "navier_stokes_part5_viscosity_balance.webm"
)


# ============================================================
# TIMING
# ============================================================

NUM_STAGES = 5

STAGE_DURATION = DURATION / NUM_STAGES

# 0.8 second cinematic overlap
CROSSFADE = 0.8


# ============================================================
# COLORS
# ============================================================

BG = "#080a0f"

PANEL = "#0d1016"

PANEL_2 = "#0b1017"

TEXT = "#f2f5f7"

MUTED = "#8a929d"

SOFT = "#cbd5e1"

GRID = "#343a45"

CYAN = "#70d6ff"

ORANGE = "#ff9b5e"

VIOLET = "#a98cff"

GREEN = "#79e6a5"

RED = "#ff6d7d"


# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(
    figsize=(
        FIG_WIDTH,
        FIG_HEIGHT
    ),
    dpi=DPI
)

fig.patch.set_facecolor(BG)

ax.set_facecolor(BG)

ax.set_xlim(
    0,
    1200
)

ax.set_ylim(
    675,
    0
)

ax.axis("off")


# ============================================================
# GENERAL HELPERS
# ============================================================

def clamp(
    value,
    minimum=0.0,
    maximum=1.0
):

    return max(
        minimum,
        min(
            maximum,
            value
        )
    )


def ease(
    value
):

    value = clamp(value)

    return (
        value
        * value
        * (3 - 2 * value)
    )


def reset_axis():

    ax.clear()

    ax.set_xlim(
        0,
        1200
    )

    ax.set_ylim(
        675,
        0
    )

    ax.set_facecolor(
        BG
    )

    ax.axis("off")


# ============================================================
# BACKGROUND
# ============================================================

def draw_background():

    # Vertical grid

    for x in np.arange(
        40,
        1160,
        55
    ):

        ax.plot(
            [x, x],
            [30, 640],
            color=GRID,
            linewidth=0.5,
            alpha=0.12,
            linestyle=(
                0,
                (2, 10)
            )
        )

    # Horizontal grid

    for y in np.arange(
        50,
        640,
        55
    ):

        ax.plot(
            [35, 1165],
            [y, y],
            color=GRID,
            linewidth=0.5,
            alpha=0.12,
            linestyle=(
                0,
                (2, 10)
            )
        )


# ============================================================
# FRAME BORDER
# ============================================================

def draw_border():

    ax.add_patch(
        FancyBboxPatch(
            (
                20,
                20
            ),
            1160,
            620,
            boxstyle=(
                "round,pad=0,"
                "rounding_size=16"
            ),
            fill=False,
            edgecolor="#202731",
            linewidth=1
        )
    )


# ============================================================
# HEADER
# ============================================================

def draw_header(
    title,
    stage
):

    ax.text(
        45,
        47,
        "NAVIER–STOKES · PART 5",
        fontsize=10,
        color=MUTED,
        fontweight="bold",
        va="center"
    )

    ax.text(
        45,
        77,
        title,
        fontsize=22,
        color=TEXT,
        fontweight="bold",
        va="center"
    )

    ax.text(
        1150,
        47,
        stage,
        fontsize=10,
        color=CYAN,
        fontweight="bold",
        ha="right",
        va="center"
    )


# ============================================================
# TIMELINE
# ============================================================

def draw_timeline(
    stage
):

    x0 = 55

    x1 = 1145

    y = 612

    ax.plot(
        [x0, x1],
        [y, y],
        color="#252d37",
        linewidth=2
    )

    positions = np.linspace(
        x0,
        x1,
        NUM_STAGES
    )

    labels = [
        "WRONG PICTURE",
        "VISCOSITY",
        "DYNAMICS",
        "CANCELLATION",
        "BLOW-UP"
    ]

    for i, x in enumerate(
        positions
    ):

        active = i <= stage

        ax.scatter(
            x,
            y,
            s=48 if active else 28,
            color=(
                CYAN
                if active
                else "#38414c"
            ),
            zorder=5
        )

        ax.text(
            x,
            y + 24,
            labels[i],
            fontsize=7.5,
            color=(
                TEXT
                if active
                else MUTED
            ),
            ha="center",
            va="top",
            fontweight="bold"
        )


# ============================================================
# TIME
# ============================================================

def draw_time(
    seconds
):

    ax.text(
        45,
        662,
        "INTERNAL BALANCE · SMOOTH EXTERNAL FORCING",
        fontsize=8,
        color=MUTED,
        ha="left",
        va="center"
    )


# ============================================================
# BOTTOM NARRATION PANEL
# ============================================================

def draw_bottom_text(
    text,
    color=SOFT
):

    box_x = 55
    box_y = 520
    box_w = 1090
    pad_x = 23

    # Wrap manually to the panel's actual width, not the figure's.
    # ~95 characters fits comfortably at fontsize 11.5 in this box.
    wrapped_lines = textwrap.wrap(text, width=95)

    line_height = 22
    min_box_h = 72

    box_h = max(
        min_box_h,
        26 + line_height * len(wrapped_lines)
    )

    ax.add_patch(
        FancyBboxPatch(
            (box_x, box_y),
            box_w,
            box_h,
            boxstyle=(
                "round,pad=0,"
                "rounding_size=11"
            ),
            facecolor="#0b1017",
            edgecolor="#202a35",
            linewidth=1
        )
    )

    start_y = (
        box_y
        + box_h / 2
        - (len(wrapped_lines) - 1) * line_height / 2
    )

    for i, line in enumerate(wrapped_lines):

        ax.text(
            box_x + pad_x,
            start_y + i * line_height,
            line,
            fontsize=11.5,
            color=color,
            fontweight="500",
            ha="left",
            va="center"
        )


# ============================================================
# ARROW
# ============================================================

def draw_arrow(
    x1,
    y1,
    x2,
    y2,
    color,
    width=3
):

    ax.annotate(
        "",
        xy=(
            x2,
            y2
        ),
        xytext=(
            x1,
            y1
        ),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=width,
            mutation_scale=11
        )
    )


# ============================================================
# VORTEX
# ============================================================

def vortex_coordinates(
    scale,
    elongation,
    rotation,
    phase
):

    theta = np.linspace(
        0,
        3.2 * np.pi,
        170
    )

    radius = np.linspace(
        10,
        scale,
        len(theta)
    )

    x = (
        radius
        * np.cos(
            theta + phase
        )
        * elongation
    )

    y = (
        radius
        * np.sin(
            theta + phase
        )
    )

    c = np.cos(
        rotation
    )

    s = np.sin(
        rotation
    )

    xr = (
        c * x
        - s * y
    )

    yr = (
        s * x
        + c * y
    )

    return xr, yr


def draw_vortex(
    cx,
    cy,
    scale,
    elongation=1,
    rotation=0,
    alpha=0.75,
    layers=7
):

    for k in range(
        layers
    ):

        x, y = vortex_coordinates(
            scale=(
                scale
                * (
                    0.55
                    + 0.08 * k
                )
            ),
            elongation=elongation,
            rotation=rotation,
            phase=k * 0.27
        )

        ax.plot(
            cx + x,
            cy + y,
            color=CYAN,
            linewidth=(
                1.25
                + 0.1 * k
            ),
            alpha=(
                alpha
                * (
                    0.32
                    + 0.07 * k
                )
            )
        )

    # Core

    ax.add_patch(
        Circle(
            (
                cx,
                cy
            ),
            scale * 0.34,
            color=CYAN,
            alpha=0.09
        )
    )

    ax.add_patch(
        Circle(
            (
                cx,
                cy
            ),
            scale * 0.14,
            color=TEXT,
            alpha=0.75
        )
    )


# ============================================================
# ROTATION ARROWS
# ============================================================

def draw_rotation(
    cx,
    cy,
    radius,
    count,
    speed,
    colors
):

    for i in range(
        count
    ):

        angle = (
            2
            * np.pi
            * i
            / count
            + speed
        )

        a2 = (
            angle
            + 0.30
        )

        x1 = (
            cx
            + radius
            * np.cos(angle)
        )

        y1 = (
            cy
            + radius
            * np.sin(angle)
        )

        x2 = (
            cx
            + radius
            * np.cos(a2)
        )

        y2 = (
            cy
            + radius
            * np.sin(a2)
        )

        draw_arrow(
            x1,
            y1,
            x2,
            y2,
            colors[
                i % len(colors)
            ],
            width=2.1
        )


# ============================================================
# EQUATION
# ============================================================

def draw_equation(
    y
):

    pieces = [

        (
            "∂u/∂t",
            70,
            ORANGE
        ),

        (
            "+",
            177,
            MUTED
        ),

        (
            "(u·∇)u",
            218,
            CYAN
        ),

        (
            "=",
            350,
            MUTED
        ),

        (
            "−∇p/ρ",
            390,
            VIOLET
        ),

        (
            "+",
            515,
            MUTED
        ),

        (
            "ν∇²u",
            552,
            GREEN
        ),

        (
            "+",
            660,
            MUTED
        ),

        (
            "f",
            697,
            GREEN
        )
    ]

    for text, x, color in pieces:

        size = (
            23
            if text not in [
                "+",
                "="
            ]
            else 21
        )

        ax.text(
            x,
            y,
            text,
            fontsize=size,
            color=color,
            fontweight="bold",
            va="center"
        )


# ============================================================
# STAGE 1
# ============================================================

def stage_1(
    t
):

    q = ease(
        t / STAGE_DURATION
    )

    draw_header(
        "Viscosity does not simply “lose.”",
        "01 · THE WRONG PICTURE"
    )

    ax.add_patch(
        FancyBboxPatch(
            (
                42,
                95
            ),
            1116,
            410,
            boxstyle=(
                "round,pad=0,"
                "rounding_size=18"
            ),
            facecolor=PANEL,
            edgecolor="#202a35",
            linewidth=1
        )
    )

    ax.text(
        75,
        130,
        "THE TEMPTING STORY",
        fontsize=11,
        color=MUTED,
        fontweight="bold"
    )

    # Main chain

    ax.text(
        600,
        180,
        "nonlinear effects",
        fontsize=25,
        color=CYAN,
        fontweight="bold",
        ha="center"
    )

    ax.text(
        600,
        215,
        "become stronger",
        fontsize=15,
        color=SOFT,
        ha="center"
    )

    draw_arrow(
        600,
        235,
        600,
        270,
        CYAN,
        3
    )

    ax.text(
        600,
        305,
        "viscosity gets overwhelmed",
        fontsize=24,
        color=ORANGE,
        fontweight="bold",
        ha="center"
    )

    draw_arrow(
        600,
        325,
        600,
        360,
        ORANGE,
        3
    )

    ax.text(
        600,
        405,
        "∞",
        fontsize=54,
        color=RED,
        fontweight="bold",
        ha="center"
    )

    # Moving vortex in background

    draw_vortex(
        250,
        310,
        55 + 15 * q,
        elongation=1 + 0.4 * q,
        rotation=t * 0.5,
        alpha=0.25
    )

    draw_vortex(
        950,
        310,
        55 + 15 * q,
        elongation=1 + 0.4 * q,
        rotation=-t * 0.5,
        alpha=0.25
    )

    # Bottom narration

    draw_bottom_text(
        "The tempting story is: nonlinear effects grow → "
        "viscosity gets overwhelmed → infinity. "
        "That is too simplistic.",
        color=ORANGE
    )


# ============================================================
# STAGE 2
# ============================================================

def stage_2(
    t
):

    q = ease(
        t / STAGE_DURATION
    )

    draw_header(
        "No. Viscosity is still in the equation.",
        "02 · VISCOSITY REMAINS"
    )

    ax.add_patch(
        FancyBboxPatch(
            (
                42,
                95
            ),
            1116,
            410,
            boxstyle=(
                "round,pad=0,"
                "rounding_size=18"
            ),
            facecolor=PANEL_2,
            edgecolor="#202a35",
            linewidth=1
        )
    )

    # Equation

    draw_equation(
        165
    )

    ax.text(
        600,
        220,
        "THE VISCOUS TERM IS STILL ACTIVE",
        fontsize=12,
        color=GREEN,
        fontweight="bold",
        ha="center"
    )

    # Central vortex

    draw_vortex(
        600,
        355,
        75 - 12 * q,
        elongation=1 + 1.2 * q,
        rotation=0.2 + 0.3 * q,
        alpha=0.75
    )

    draw_rotation(
        600,
        355,
        115 - 12 * q,
        12,
        t * 1.5,
        [
            ORANGE,
            CYAN,
            VIOLET,
            GREEN
        ]
    )

    # Four terms

    terms = [

        (
            "ACCELERATION",
            ORANGE,
            300
        ),

        (
            "ADVECTION",
            CYAN,
            485
        ),

        (
            "PRESSURE",
            VIOLET,
            720
        ),

        (
            "VISCOSITY",
            GREEN,
            900
        )
    ]

    for label, color, x in terms:

        ax.text(
            x,
            470,
            label,
            fontsize=10,
            color=color,
            fontweight="bold",
            ha="center"
        )

        ax.add_patch(
            FancyBboxPatch(
                (
                    x - 65,
                    480
                ),
                130,
                10,
                boxstyle=(
                    "round,pad=0,"
                    "rounding_size=5"
                ),
                facecolor="#111722",
                edgecolor="#2a3540",
                linewidth=1
            )
        )

        width = (
            130
            * (
                0.30
                + 0.55 * q
            )
        )

        ax.add_patch(
            FancyBboxPatch(
                (
                    x - 65,
                    480
                ),
                width,
                10,
                boxstyle=(
                    "round,pad=0,"
                    "rounding_size=5"
                ),
                facecolor=color,
                edgecolor="none"
            )
        )

    draw_bottom_text(
        "The construction does not remove the viscous term. "
        "Viscosity remains a large participant in a much "
        "more delicate balance.",
        color=GREEN
    )


# ============================================================
# STAGE 3
# ============================================================

def stage_3(
    t
):

    q = ease(
        t / STAGE_DURATION
    )

    draw_header(
        "The terms become large together.",
        "03 · INTERNAL DYNAMICS"
    )

    ax.add_patch(
        FancyBboxPatch(
            (
                40,
                90
            ),
            1120,
            415,
            boxstyle=(
                "round,pad=0,"
                "rounding_size=18"
            ),
            facecolor="#0c1118",
            edgecolor="#202a35",
            linewidth=1
        )
    )

    draw_equation(
        150
    )

    ax.text(
        600,
        205,
        "THE MAGNITUDES RISE TOGETHER",
        fontsize=12,
        color=MUTED,
        fontweight="bold",
        ha="center"
    )

    # Vortex

    draw_vortex(
        600,
        350,
        82 - 22 * q,
        elongation=1 + 2.0 * q,
        rotation=0.2 + 0.5 * q,
        alpha=0.85
    )

    draw_rotation(
        600,
        350,
        125 - 20 * q,
        16,
        2 + 4 * q,
        [
            ORANGE,
            CYAN,
            VIOLET,
            GREEN
        ]
    )

    # Four term vectors

    terms = [

        (
            "ACCELERATION",
            ORANGE,
            220,
            -1
        ),

        (
            "ADVECTION",
            CYAN,
            445,
            1
        ),

        (
            "PRESSURE",
            VIOLET,
            770,
            -1
        ),

        (
            "VISCOSITY",
            GREEN,
            985,
            1
        )
    ]

    magnitude = (
        50
        + 105 * q
    )

    for label, color, x, direction in terms:

        ax.text(
            x,
            270,
            label,
            fontsize=10,
            color=color,
            fontweight="bold",
            ha="center"
        )

        draw_arrow(
            x,
            305,
            x + direction * magnitude,
            305 + direction * 8,
            color,
            3.2
        )

        # Secondary particle-like indicators

        for j in range(3):

            yy = (
                330
                + j * 25
            )

            draw_arrow(
                x,
                yy,
                x
                + direction
                * (
                    magnitude
                    * (
                        0.45
                        + 0.12 * j
                    )
                ),
                yy,
                color,
                1.7
            )

    ax.text(
        600,
        455,
        "The question is their COMBINED BALANCE.",
        fontsize=16,
        color=TEXT,
        fontweight="bold",
        ha="center"
    )

    draw_bottom_text(
        "As the solution approaches its singular structure, "
        "acceleration, advection, pressure gradients and "
        "viscous effects can all become large. "
        "The question is their combined balance.",
        color=SOFT
    )


# ============================================================
# STAGE 4
# ============================================================

def stage_4(
    t
):

    q = ease(
        t / STAGE_DURATION
    )

    draw_header(
        "The cancellation is the mechanism.",
        "04 · DELICATE CANCELLATION"
    )

    ax.add_patch(
        FancyBboxPatch(
            (
                38,
                88
            ),
            1124,
            417,
            boxstyle=(
                "round,pad=0,"
                "rounding_size=18"
            ),
            facecolor="#0b1017",
            edgecolor="#202a35",
            linewidth=1
        )
    )

    draw_equation(
        145
    )

    # Four opposing terms

    terms = [

        (
            "ACCELERATION",
            ORANGE,
            240,
            1
        ),

        (
            "ADVECTION",
            CYAN,
            455,
            -1
        ),

        (
            "PRESSURE",
            VIOLET,
            750,
            1
        ),

        (
            "VISCOSITY",
            GREEN,
            965,
            -1
        )
    ]

    magnitude = (
        50
        + 120 * q
    )

    for label, color, x, direction in terms:

        ax.text(
            x,
            235,
            label,
            fontsize=10,
            color=color,
            fontweight="bold",
            ha="center"
        )

        # Main opposing vector

        draw_arrow(
            x - direction * 10,
            285,
            x + direction * magnitude,
            285,
            color,
            3.5
        )

        # Small parallel vectors

        for j in range(2):

            yy = (
                310
                + j * 22
            )

            draw_arrow(
                x - direction * 8,
                yy,
                x
                + direction
                * magnitude
                * (
                    0.55
                    + 0.15 * j
                ),
                yy,
                color,
                1.7
            )

    # Balance equation

    ax.text(
        600,
        380,
        "LARGE  +  LARGE",
        fontsize=21,
        color=TEXT,
        fontweight="bold",
        ha="center"
    )

    ax.text(
        600,
        420,
        "≈",
        fontsize=27,
        color=GREEN,
        fontweight="bold",
        ha="center"
    )

    ax.text(
        600,
        460,
        "LARGE  +  LARGE",
        fontsize=21,
        color=TEXT,
        fontweight="bold",
        ha="center"
    )

    # Smooth residual force

    ax.text(
        850,
        470,
        "smooth residual  f(x,t)",
        fontsize=11,
        color=GREEN,
        fontweight="bold",
        ha="center"
    )

    draw_bottom_text(
        "The key is not that viscosity loses. Large contributions "
        "oppose one another with precise structure, leaving a "
        "smooth residual forcing.",
        color=GREEN
    )


# ============================================================
# STAGE 5
# ============================================================

def stage_5(
    t
):

    q = ease(
        t / STAGE_DURATION
    )

    draw_header(
        "Wait… the velocity still diverges.",
        "05 · VELOCITY BLOW-UP"
    )

    ax.add_patch(
        FancyBboxPatch(
            (
                40,
                88
            ),
            1120,
            417,
            boxstyle=(
                "round,pad=0,"
                "rounding_size=18"
            ),
            facecolor="#0b1016",
            edgecolor="#222d38",
            linewidth=1
        )
    )

    ax.text(
        68,
        122,
        "THE FINAL DISTINCTION",
        fontsize=11,
        color=MUTED,
        fontweight="bold"
    )

    # --------------------------------------------------------
    # VORTEX
    # --------------------------------------------------------

    cx = 330

    cy = 345

    core_radius = (
        34
        / (
            1
            + 5 * q
        )
    )

    scale = (
        90
        / (
            1
            + 4 * q
        )
    )

    elongation = (
        1
        + 3.0 * q
    )

    draw_vortex(
        cx,
        cy,
        scale,
        elongation,
        rotation=(
            0.2
            + 0.7 * q
        ),
        alpha=0.9
    )

    # Intensifying rotation

    draw_rotation(
        cx,
        cy,
        120 / (
            1
            + 2.2 * q
        ),
        15,
        3 + 8 * q,
        [
            CYAN,
            VIOLET
        ]
    )

    ax.text(
        cx,
        475,
        "VORTEX CONCENTRATES",
        fontsize=11,
        color=CYAN,
        fontweight="bold",
        ha="center"
    )

    # --------------------------------------------------------
    # VELOCITY BAR
    # --------------------------------------------------------

    bar_x = 480

    bar_y = 190

    bar_h = 285

    bar_w = 34

    ax.add_patch(
        FancyBboxPatch(
            (
                bar_x,
                bar_y
            ),
            bar_w,
            bar_h,
            boxstyle=(
                "round,pad=0,"
                "rounding_size=8"
            ),
            facecolor="#10161f",
            edgecolor="#2a3540",
            linewidth=1
        )
    )

    fill = (
        bar_h
        * q
    )

    ax.add_patch(
        FancyBboxPatch(
            (
                bar_x,
                bar_y
                + bar_h
                - fill
            ),
            bar_w,
            max(
                fill,
                0.1
            ),
            boxstyle=(
                "round,pad=0,"
                "rounding_size=8"
            ),
            facecolor=ORANGE,
            edgecolor="none"
        )
    )

    ax.text(
        bar_x + 17,
        160,
        "|u|",
        fontsize=23,
        color=ORANGE,
        fontweight="bold",
        ha="center"
    )

    ax.text(
        bar_x + 17,
        495,
        (
            "→ ∞"
            if q > 0.9
            else "growing"
        ),
        fontsize=11,
        color=ORANGE,
        fontweight="bold",
        ha="center"
    )

    # --------------------------------------------------------
    # EXTERNAL FORCE
    # --------------------------------------------------------

    ax.add_patch(
        FancyBboxPatch(
            (
                570,
                165
            ),
            520,
            155,
            boxstyle=(
                "round,pad=0,"
                "rounding_size=14"
            ),
            facecolor="#0f141b",
            edgecolor="#27323d",
            linewidth=1
        )
    )

    ax.text(
        600,
        200,
        "EXTERNAL FORCE",
        fontsize=10,
        color=MUTED,
        fontweight="bold"
    )

    xx = np.linspace(
        600,
        1060,
        200
    )

    yy = (
        270
        - 17
        * np.sin(
            (xx - 600)
            / 38
        )
        - 5
        * np.sin(
            (xx - 600)
            / 13
        )
    )

    ax.plot(
        xx,
        yy,
        color=GREEN,
        linewidth=2.8
    )

    ax.text(
        835,
        305,
        "still smooth",
        fontsize=17,
        color=GREEN,
        fontweight="bold",
        ha="center"
    )

    # --------------------------------------------------------
    # LIMIT
    # --------------------------------------------------------

    ax.add_patch(
        FancyBboxPatch(
            (
                570,
                345
            ),
            520,
            145,
            boxstyle=(
                "round,pad=0,"
                "rounding_size=14"
            ),
            facecolor="#11161e",
            edgecolor="#27323d",
            linewidth=1
        )
    )

    ax.text(
        600,
        385,
        r"AS  t → T⁻",
        fontsize=16,
        color=TEXT,
        fontweight="bold"
    )

    ax.text(
        600,
        435,
        r"|u| → ∞",
        fontsize=28,
        color=ORANGE,
        fontweight="bold"
    )

    ax.text(
        1055,
        435,
        r"T < ∞",
        fontsize=17,
        color=TEXT,
        fontweight="bold",
        ha="right"
    )

    # Final statement

    alpha = clamp(
        (q - 0.5)
        * 2
    )

    ax.text(
        830,
        475,
        "NO INFINITE EXTERNAL FORCE IS REQUIRED",
        fontsize=10,
        color=ORANGE,
        fontweight="bold",
        ha="center",
        alpha=alpha
    )

    draw_bottom_text(
        "The remarkable outcome: internal terms balance so "
        "the external forcing remains smooth, yet the velocity "
        "magnitude can still diverge as t approaches a finite T.",
        color=ORANGE
    )


# ============================================================
# STAGE DISPATCH
# ============================================================

def render_stage(
    stage,
    local_time
):

    if stage == 0:

        stage_1(
            local_time
        )

    elif stage == 1:

        stage_2(
            local_time
        )

    elif stage == 2:

        stage_3(
            local_time
        )

    elif stage == 3:

        stage_4(
            local_time
        )

    elif stage == 4:

        stage_5(
            local_time
        )


# ============================================================
# FRAME RENDERER
# ============================================================

def draw_frame(
    frame
):

    seconds = (
        frame
        / FPS
    )

    # --------------------------------------------------------
    # Determine current stage
    # --------------------------------------------------------

    stage = min(
        NUM_STAGES - 1,
        int(
            seconds
            / STAGE_DURATION
        )
    )

    local_time = (
        seconds
        - stage
        * STAGE_DURATION
    )

    # --------------------------------------------------------
    # Determine transition
    # --------------------------------------------------------

    in_transition = (
        stage < NUM_STAGES - 1
        and local_time
        >= (
            STAGE_DURATION
            - CROSSFADE
        )
    )

    # --------------------------------------------------------
    # Normal scene
    # --------------------------------------------------------

    if not in_transition:

        reset_axis()

        draw_background()

        render_stage(
            stage,
            local_time
        )

    # --------------------------------------------------------
    # Cinematic transition
    # --------------------------------------------------------

    else:

        # Progress through overlap

        transition_progress = clamp(
            (
                local_time
                - (
                    STAGE_DURATION
                    - CROSSFADE
                )
            )
            / CROSSFADE
        )

        transition_progress = ease(
            transition_progress
        )

        # Draw the incoming stage.
        #
        # The incoming stage starts slightly early and
        # is visually revealed through a dark cinematic veil.

        reset_axis()

        draw_background()

        render_stage(
            stage + 1,
            transition_progress
        )

        # Dark transition veil

        veil = (
            0.22
            * np.sin(
                np.pi
                * transition_progress
            )
        )

        ax.add_patch(
            FancyBboxPatch(
                (
                    20,
                    20
                ),
                1160,
                620,
                boxstyle=(
                    "round,pad=0,"
                    "rounding_size=16"
                ),
                facecolor=BG,
                edgecolor="none",
                alpha=veil
            )
        )

        # Direction marker

        timeline_x0 = 55
        timeline_x1 = 1145
        timeline_positions = np.linspace(timeline_x0, timeline_x1, NUM_STAGES)

        arrow_x = timeline_positions[stage + 1]

        ax.text(
            arrow_x,
            598,
            "→",
            fontsize=20,
            color=CYAN,
            fontweight="bold",
            ha="center",
            va="center",
            alpha=(
                0.3
                + 0.7
                * transition_progress
            )
        )

    # --------------------------------------------------------
    # Persistent UI
    # --------------------------------------------------------

    draw_timeline(
        stage
    )

    draw_border()

    draw_time(
        seconds
    )


# ============================================================
# CREATE ANIMATION
# ============================================================

animation = FuncAnimation(
    fig,
    draw_frame,
    frames=TOTAL_FRAMES,
    interval=1000 / FPS,
    blit=False,
    repeat=True
)


# ============================================================
# VIDEO WRITER
# ============================================================

writer = FFMpegWriter(
    fps=FPS,
    codec="libvpx-vp9",
    bitrate=4000,
    extra_args=[
        "-pix_fmt",
        "yuv420p",
        "-deadline",
        "good",
        "-cpu-used",
        "2",
        "-crf", "24",          # constant quality (0=lossless, 63=worst); 20-28 is a good HD range
        "-b:v", "0"
    ]
)


# ============================================================
# RENDER
# ============================================================

print()
print("=" * 70)
print("NAVIER–STOKES · PART 5")
print("VISCOSITY DOESN'T SIMPLY 'LOSE'")
print("=" * 70)

print(
    f"FPS:              {FPS}"
)

print(
    f"Duration:         {DURATION} seconds"
)

print(
    f"Frames:           {TOTAL_FRAMES}"
)

print(
    "Resolution:       1280 × 720"
)

print(
    f"Stage duration:   {STAGE_DURATION:.1f} seconds"
)

print(
    f"Crossfade:        {CROSSFADE:.1f} seconds"
)

print(
    f"Output:           {OUTPUT}"
)

print("=" * 70)

print()
print("Rendering...")
print()


animation.save(
    OUTPUT,
    writer=writer,
    dpi=DPI
)


plt.close(
    fig
)


# ============================================================
# DONE
# ============================================================

print()
print("=" * 70)
print("RENDER COMPLETE")
print("=" * 70)

print(
    f"Saved to:\n{OUTPUT.resolve()}"
)

print("=" * 70)
