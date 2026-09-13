
# ============================================================
# NAVIER–STOKES · PART 4
# THE INCREDIBLY DIFFICULT PART
#
# CINEMATIC CROSSFADE VERSION
#
# Conceptual progression:
#
#   HUGE FORCE?
#        ↓
#   NO.
#        ↓
#   FORCE MUST STAY SMOOTH
#        ↓
#   INTERNAL TERMS GROW
#        ↓
#   PRECISE CANCELLATION
#        ↓
#   VELOCITY STILL DIVERGES
#
# Five stages with 0.8-second visual overlaps.
#
# Total duration: 30 seconds
# FPS:            24
# Resolution:     1280 × 720
#
# Output:
#   navier_stokes_part4_delicate_cancellation.webm
#
# Requirements:
#   pip install numpy matplotlib
#
# FFmpeg must be installed and available on PATH.
# ============================================================


import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Circle, FancyBboxPatch
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
    "navier_stokes_part4_delicate_cancellation.webm"
)


# ============================================================
# TRANSITION SETTINGS
# ============================================================

# Duration of visual overlap between stages.

CROSSFADE = 0.8

STAGE_DURATION = DURATION / 5


# ============================================================
# CINEMATIC THEME
# ============================================================

BG = "#080a0f"

PANEL = "#0d1016"

TEXT = "#f2f5f7"

MUTED = "#8a929d"

GRID = "#343a45"

CYAN = "#70d6ff"

ORANGE = "#ff9b5e"

VIOLET = "#a98cff"

GREEN = "#79e6a5"

RED = "#ff6d7d"

SOFT = "#cbd5e1"


# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(
    figsize=(FIG_WIDTH, FIG_HEIGHT),
    dpi=DPI
)

fig.patch.set_facecolor(BG)

ax.set_facecolor(BG)

ax.set_xlim(0, 1200)
ax.set_ylim(675, 0)

ax.axis("off")


# ============================================================
# GENERAL HELPERS
# ============================================================

def reset_axis():

    ax.clear()

    ax.set_xlim(0, 1200)
    ax.set_ylim(675, 0)

    ax.set_facecolor(BG)

    ax.axis("off")


def draw_background():

    # Technical grid

    for x in np.arange(40, 1160, 55):

        ax.plot(
            [x, x],
            [30, 640],
            color=GRID,
            linewidth=0.5,
            alpha=0.12,
            linestyle=(0, (2, 10))
        )

    for y in np.arange(50, 640, 55):

        ax.plot(
            [35, 1165],
            [y, y],
            color=GRID,
            linewidth=0.5,
            alpha=0.12,
            linestyle=(0, (2, 10))
        )


def draw_frame_border():

    ax.add_patch(
        FancyBboxPatch(
            (20, 20),
            1160,
            620,
            boxstyle="round,pad=0.0,rounding_size=16",
            fill=False,
            edgecolor="#202731",
            linewidth=1
        )
    )


def draw_header(
    title,
    stage_label
):

    ax.text(
        45,
        48,
        "NAVIER–STOKES · PART 4",
        fontsize=10,
        color=MUTED,
        fontweight="bold",
        va="center"
    )

    ax.text(
        45,
        78,
        title,
        fontsize=22,
        color=TEXT,
        fontweight="bold",
        va="center"
    )

    ax.text(
        1150,
        48,
        stage_label,
        fontsize=10,
        color=CYAN,
        fontweight="bold",
        ha="right",
        va="center"
    )


def draw_timeline(stage):

    x0 = 55

    x1 = 1145

    y = 615

    ax.plot(
        [x0, x1],
        [y, y],
        color="#252d37",
        linewidth=2
    )

    positions = np.linspace(
        x0,
        x1,
        5
    )

    for i, x in enumerate(positions):

        if i <= stage:

            color = CYAN

            size = 50

        else:

            color = "#38414c"

            size = 30

        ax.scatter(
            x,
            y,
            s=size,
            color=color,
            zorder=5
        )

    labels = [
        "NAIVE IDEA",
        "CONSTRAINT",
        "DYNAMICS",
        "CANCELLATION",
        "BLOW-UP"
    ]

    for i, (
        x,
        label
    ) in enumerate(
        zip(positions, labels)
    ):

        ax.text(
            x,
            y + 25,
            label,
            fontsize=8,
            color=(
                TEXT
                if i <= stage
                else MUTED
            ),
            ha="center",
            va="top",
            fontweight="bold"
        )


# ============================================================
# MATH HELPERS
# ============================================================

def draw_time(seconds):

    ax.text(
        45,
        665,
        "FINITE-TIME SINGULARITY · EXTERNAL FORCE REMAINS SMOOTH",
        fontsize=8,
        color=MUTED,
        ha="left",
        va="center"
    )


def clamp(
    x,
    a=0.0,
    b=1.0
):

    return max(
        a,
        min(b, x)
    )


def ease(x):

    x = clamp(x)

    return (
        x * x
        * (3 - 2 * x)
    )


def pulse(
    t,
    base=1.0,
    amplitude=0.1,
    frequency=2.0
):

    return (
        base
        + amplitude
        * np.sin(
            2
            * np.pi
            * frequency
            * t
        )
    )


# ============================================================
# VORTEX
# ============================================================

def vortex_coordinates(
    scale=100,
    rotation=0,
    elongation=1.0,
    phase=0
):

    theta = np.linspace(
        0,
        2 * np.pi * 1.6,
        180
    )

    radius = np.linspace(
        12,
        scale,
        len(theta)
    )

    x = (
        radius
        * np.cos(
            theta + phase
        )
    )

    y = (
        radius
        * np.sin(
            theta + phase
        )
    )

    x *= elongation

    c = np.cos(rotation)

    s = np.sin(rotation)

    xr = c * x - s * y

    yr = s * x + c * y

    return xr, yr


def draw_vortex(
    cx,
    cy,
    scale,
    rotation=0,
    elongation=1.0,
    alpha=0.8,
    layers=7
):

    for k in range(layers):

        layer_scale = (
            scale
            * (
                0.55
                + 0.09 * k
            )
        )

        phase = k * 0.28

        x, y = vortex_coordinates(
            scale=layer_scale,
            rotation=rotation,
            elongation=elongation,
            phase=phase
        )

        ax.plot(
            cx + x,
            cy + y,
            color=CYAN,
            linewidth=(
                1.3
                + 0.12 * k
            ),
            alpha=(
                alpha
                * (
                    0.35
                    + 0.07 * k
                )
            )
        )


def draw_core(
    cx,
    cy,
    radius,
    intensity=0.5
):

    for i in range(6, 0, -1):

        r = radius * (
            1 + i * 0.65
        )

        ax.add_patch(
            Circle(
                (cx, cy),
                r,
                color=CYAN,
                alpha=(
                    intensity
                    * 0.015
                    * (7 - i)
                ),
                linewidth=0
            )
        )

    ax.add_patch(
        Circle(
            (cx, cy),
            radius,
            color=CYAN,
            alpha=(
                0.18
                * intensity
            ),
            linewidth=0
        )
    )

    ax.add_patch(
        Circle(
            (cx, cy),
            radius * 0.35,
            color=TEXT,
            alpha=0.8,
            linewidth=0
        )
    )


def draw_arrow(
    x1,
    y1,
    x2,
    y2,
    color,
    linewidth=2.5
):

    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            lw=linewidth,
            mutation_scale=10
        )
    )


def draw_rotational_arrows(
    cx,
    cy,
    radius,
    count=10,
    speed=1.0,
    colors=None
):

    if colors is None:

        colors = [CYAN]

    for i in range(count):

        theta = (
            i
            / count
            * 2
            * np.pi
            + speed
        )

        a1 = theta

        a2 = (
            theta
            + 0.38
        )

        x1 = (
            cx
            + radius
            * np.cos(a1)
        )

        y1 = (
            cy
            + radius
            * np.sin(a1)
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
                i
                % len(colors)
            ],
            2.2
        )


# ============================================================
# NAVIER–STOKES EQUATION
# ============================================================

def draw_equation(
    y,
    colors
):

    pieces = [

        (
            "∂u/∂t",
            70,
            colors[0]
        ),

        (
            "+",
            178,
            MUTED
        ),

        (
            "(u·∇)u",
            218,
            colors[1]
        ),

        (
            "=",
            350,
            MUTED
        ),

        (
            "−∇p/ρ",
            390,
            colors[2]
        ),

        (
            "+",
            515,
            MUTED
        ),

        (
            "ν∇²u",
            552,
            colors[3]
        ),

        (
            "+",
            660,
            MUTED
        ),

        (
            "f",
            697,
            colors[4]
        )
    ]

    for txt, x, color in pieces:

        fontsize = (
            23
            if txt not in [
                "+",
                "="
            ]
            else 21
        )

        ax.text(
            x,
            y,
            txt,
            fontsize=fontsize,
            color=color,
            fontweight="bold",
            va="center"
        )


# ============================================================
# STAGE 1
# ============================================================

def stage_1(t):

    q = ease(t / STAGE_DURATION)

    draw_header(
        "“Just make the force enormous.”",
        "01 · NAIVE IDEA"
    )

    ax.add_patch(
        FancyBboxPatch(
            (42, 100),
            1116,
            465,
            boxstyle=(
                "round,pad=0.0,"
                "rounding_size=18"
            ),
            facecolor=PANEL,
            edgecolor="#202a35",
            linewidth=1
        )
    )

    ax.text(
        75,
        138,
        "THE TEMPTING SHORTCUT",
        fontsize=11,
        color=MUTED,
        fontweight="bold"
    )

    ax.text(
        75,
        180,
        r"Make  |f|  huge   →   make  |u|  huge",
        fontsize=27,
        color=TEXT,
        fontweight="bold"
    )

    cx = 600
    cy = 340

    scale = (
        70
        + 90 * q
    )

    draw_vortex(
        cx,
        cy,
        scale,
        rotation=0.15 * q,
        elongation=1.0,
        alpha=0.5
    )

    draw_core(
        cx,
        cy,
        24 + 20 * q,
        intensity=0.5 + q
    )

    draw_rotational_arrows(
        cx,
        cy,
        145 + 50 * q,
        count=12,
        speed=t * 2,
        colors=[RED]
    )

    # External force arrows
    for i in range(8):

        theta = (
            i
            / 8
            * 2
            * np.pi
        )

        r1 = 180

        r2 = (
            235
            + 50 * q
        )

        x1 = (
            cx
            + r1
            * np.cos(theta)
        )

        y1 = (
            cy
            + r1
            * np.sin(theta)
        )

        x2 = (
            cx
            + r2
            * np.cos(theta)
        )

        y2 = (
            cy
            + r2
            * np.sin(theta)
        )

        draw_arrow(
            x1,
            y1,
            x2,
            y2,
            RED,
            3.0
        )

    ax.text(
        600,
        515,
        r"|f| ↑↑↑    →    |u| ↑↑↑",
        fontsize=25,
        color=ORANGE,
        fontweight="bold",
        ha="center"
    )

    ax.text(
        600,
        550,
        "BUT THIS DOES NOT PROVE SELF-GENERATED BLOW-UP",
        fontsize=11,
        color=ORANGE,
        fontweight="bold",
        ha="center"
    )


# ============================================================
# STAGE 2
# ============================================================

def stage_2(t):

    q = ease(t / STAGE_DURATION)

    draw_header(
        "The external force must stay smooth.",
        "02 · THE REAL CONSTRAINT"
    )

    ax.text(
        70,
        130,
        "EXTERNAL INPUT",
        fontsize=11,
        color=MUTED,
        fontweight="bold"
    )

    ax.add_patch(
        FancyBboxPatch(
            (55, 150),
            310,
            135,
            boxstyle=(
                "round,pad=0.0,"
                "rounding_size=14"
            ),
            facecolor=PANEL,
            edgecolor="#26303b",
            linewidth=1
        )
    )

    ax.text(
        82,
        195,
        "f(x,t)",
        fontsize=30,
        color=GREEN,
        fontweight="bold"
    )

    ax.text(
        82,
        230,
        "smooth · bounded · prescribed",
        fontsize=13,
        color=SOFT
    )

    xx = np.linspace(
        82,
        335,
        160
    )

    yy = (
        255
        - 13
        * np.sin(
            (xx - 82)
            / 32
        )
        - 5
        * np.sin(
            (xx - 82)
            / 11
        )
    )

    ax.plot(
        xx,
        yy,
        color=GREEN,
        linewidth=2.5
    )

    draw_arrow(
        375,
        215,
        455,
        215,
        GREEN,
        3.5
    )

    ax.add_patch(
        FancyBboxPatch(
            (465, 100),
            670,
            420,
            boxstyle=(
                "round,pad=0.0,"
                "rounding_size=16"
            ),
            facecolor="#0b1017",
            edgecolor="#26303b",
            linewidth=1
        )
    )

    ax.text(
        495,
        135,
        "THE FLUID MUST DO THE HARD WORK",
        fontsize=11,
        color=MUTED,
        fontweight="bold"
    )

    scale = (
        85
        - 35 * q
    )

    elongation = (
        1
        + 2.0 * q
    )

    draw_vortex(
        800,
        320,
        scale,
        rotation=0.25 + 0.35 * q,
        elongation=elongation,
        alpha=0.75
    )

    draw_core(
        800,
        320,
        27 - 12 * q,
        intensity=0.6 + q
    )

    draw_rotational_arrows(
        800,
        320,
        135 - 25 * q,
        count=12,
        speed=t * (
            1 + 2 * q
        ),
        colors=[
            CYAN,
            VIOLET
        ]
    )

    ax.text(
        800,
        455,
        "forcing remains smooth",
        fontsize=18,
        color=GREEN,
        fontweight="bold",
        ha="center"
    )

    ax.text(
        800,
        482,
        "even while the vortex intensifies…",
        fontsize=13,
        color=SOFT,
        ha="center"
    )


# ============================================================
# STAGE 3
# ============================================================

def stage_3(t):

    q = ease(t / STAGE_DURATION)

    draw_header(
        "Four large terms. One delicate balance.",
        "03 · INTERNAL DYNAMICS"
    )

    ax.add_patch(
        FancyBboxPatch(
            (48, 95),
            1104,
            475,
            boxstyle=(
                "round,pad=0.0,"
                "rounding_size=18"
            ),
            facecolor=PANEL,
            edgecolor="#202a35",
            linewidth=1
        )
    )

    ax.text(
        70,
        130,
        "LOCAL BALANCE INSIDE THE FLUID",
        fontsize=11,
        color=MUTED,
        fontweight="bold"
    )

    cx = 600
    cy = 345

    scale = (
        95
        - 25 * q
    )

    elongation = (
        1
        + 1.5 * q
    )

    draw_vortex(
        cx,
        cy,
        scale,
        rotation=0.18 + 0.4 * q,
        elongation=elongation,
        alpha=0.65
    )

    draw_core(
        cx,
        cy,
        30 - 12 * q,
        intensity=0.6 + q
    )

    draw_rotational_arrows(
        cx,
        cy,
        125 - 15 * q,
        count=12,
        speed=t * 2,
        colors=[
            ORANGE,
            CYAN,
            VIOLET,
            GREEN
        ]
    )

    terms = [

        (
            "ACCELERATION",
            ORANGE,
            -155,
            -75
        ),

        (
            "PRESSURE",
            VIOLET,
            135,
            -75
        ),

        (
            "MOMENTUM TRANSFER",
            CYAN,
            -165,
            100
        ),

        (
            "VISCOSITY",
            GREEN,
            145,
            100
        )
    ]

    magnitude = (
        55
        + 70 * q
    )

    for i, (
        label,
        color,
        ox,
        oy
    ) in enumerate(terms):

        x = cx + ox

        y = cy + oy

        ha = (
            "right"
            if ox < 0
            else "left"
        )

        ax.text(
            x,
            y,
            label,
            fontsize=10,
            color=color,
            fontweight="bold",
            ha=ha
        )

        direction = (
            1
            if ox > 0
            else -1
        )

        draw_arrow(
            x + direction * 8,
            y + 14,
            cx + direction * 55,
            cy + (
                25
                if oy > 0
                else -25
            ),
            color,
            3.0
        )

    ax.add_patch(
        FancyBboxPatch(
            (350, 515),
            500,
            45,
            boxstyle=(
                "round,pad=0.0,"
                "rounding_size=10"
            ),
            facecolor="#0f141b",
            edgecolor="#26303b",
            linewidth=1
        )
    )

    ax.text(
        600,
        538,
        "LARGE  +  LARGE  +  LARGE  +  LARGE  →  BALANCED",
        fontsize=14,
        color=TEXT,
        fontweight="bold",
        ha="center",
        va="center"
    )


# ============================================================
# STAGE 4
# ============================================================

def stage_4(t):

    q = ease(t / STAGE_DURATION)

    draw_header(
        "The cancellation is the point.",
        "04 · PRECISION CANCELLATION"
    )

    ax.add_patch(
        FancyBboxPatch(
            (42, 90),
            1116,
            485,
            boxstyle=(
                "round,pad=0.0,"
                "rounding_size=18"
            ),
            facecolor="#0c1118",
            edgecolor="#202a35",
            linewidth=1
        )
    )

    ax.text(
        68,
        125,
        "NAVIER–STOKES LOCAL BALANCE",
        fontsize=11,
        color=MUTED,
        fontweight="bold"
    )

    draw_equation(
        175,
        [
            ORANGE,
            CYAN,
            VIOLET,
            GREEN,
            GREEN
        ]
    )

    labels = [

        (
            "ACCELERATION",
            ORANGE,
            105
        ),

        (
            "MOMENTUM TRANSFER",
            CYAN,
            270
        ),

        (
            "PRESSURE GRADIENT",
            VIOLET,
            460
        ),

        (
            "VISCOSITY",
            GREEN,
            650
        )
    ]

    magnitude = (
        60
        + 120 * q
    )

    for i, (
        label,
        color,
        x
    ) in enumerate(labels):

        ax.text(
            x,
            235,
            label,
            fontsize=9,
            color=color,
            fontweight="bold",
            ha="center"
        )

        direction = (
            -1
            if i % 2 == 0
            else 1
        )

        draw_arrow(
            x,
            280,
            x
            + direction * magnitude,
            280
            + direction * 8,
            color,
            3.0
        )

    ax.text(
        600,
        315,
        "CANCEL",
        fontsize=17,
        color=TEXT,
        fontweight="bold",
        ha="center"
    )

    ax.plot(
        [355, 845],
        [335, 335],
        color="#596574",
        linewidth=2,
        linestyle=(0, (6, 8))
    )

    cx = 600
    cy = 430

    scale = (
        75
        - 23 * q
    )

    elongation = (
        1
        + 1.9 * q
    )

    draw_vortex(
        cx,
        cy,
        scale,
        rotation=0.25 + 0.4 * q,
        elongation=elongation,
        alpha=0.78
    )

    draw_core(
        cx,
        cy,
        27 - 14 * q,
        intensity=0.7 + q
    )

    ax.text(
        600,
        525,
        "SMOOTH  f(x,t)  REMAINS",
        fontsize=18,
        color=GREEN,
        fontweight="bold",
        ha="center"
    )

    ax.text(
        600,
        555,
        "large internal contributions → precise balance → smooth external forcing",
        fontsize=10,
        color=SOFT,
        ha="center"
    )


# ============================================================
# STAGE 5
# ============================================================

def stage_5(t):

    q = ease(t / STAGE_DURATION)

    draw_header(
        "The velocity blows up. The forcing stays smooth.",
        "05 · THE DELICATE LIMIT"
    )

    ax.add_patch(
        FancyBboxPatch(
            (42, 90),
            1116,
            485,
            boxstyle=(
                "round,pad=0.0,"
                "rounding_size=18"
            ),
            facecolor="#0b1016",
            edgecolor="#222d38",
            linewidth=1
        )
    )

    ax.text(
        68,
        125,
        "APPROACHING FINITE TIME  T",
        fontsize=11,
        color=MUTED,
        fontweight="bold"
    )

    # --------------------------------------------------------
    # VORTEX
    # --------------------------------------------------------

    cx = 385
    cy = 355

    core_radius = (
        38
        / (
            1
            + 5 * q
        )
    )

    scale = (
        85
        / (
            1
            + 4.5 * q
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
        rotation=0.25 + 0.55 * q,
        elongation=elongation,
        alpha=0.9
    )

    draw_core(
        cx,
        cy,
        core_radius,
        intensity=0.7 + 1.5 * q
    )

    draw_rotational_arrows(
        cx,
        cy,
        125 / (
            1
            + 2.2 * q
        ),
        count=14,
        speed=t * (
            1
            + 4 * q
        ),
        colors=[
            CYAN,
            VIOLET
        ]
    )

    ax.text(
        cx,
        525,
        "velocity scale",
        fontsize=11,
        color=MUTED,
        ha="center"
    )

    # --------------------------------------------------------
    # VELOCITY BAR
    # --------------------------------------------------------

    bar_x = 530

    bar_y = 310

    bar_width = 34

    bar_height = 190

    ax.add_patch(
        FancyBboxPatch(
            (
                bar_x,
                bar_y
            ),
            bar_width,
            bar_height,
            boxstyle=(
                "round,pad=0.0,"
                "rounding_size=7"
            ),
            facecolor="#10161f",
            edgecolor="#2b3642",
            linewidth=1
        )
    )

    fill_height = (
        bar_height
        * q
    )

    ax.add_patch(
        FancyBboxPatch(
            (
                bar_x,
                bar_y
                + bar_height
                - fill_height
            ),
            bar_width,
            max(
                fill_height,
                0.1
            ),
            boxstyle=(
                "round,pad=0.0,"
                "rounding_size=7"
            ),
            facecolor=ORANGE,
            edgecolor="none"
        )
    )

    ax.text(
        bar_x
        + bar_width / 2,
        275,
        "|u|",
        fontsize=22,
        color=ORANGE,
        fontweight="bold",
        ha="center"
    )

    velocity_label = (
        "→ ∞"
        if q > 0.92
        else "growing"
    )

    ax.text(
        bar_x
        + bar_width / 2,
        525,
        velocity_label,
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
            (640, 200),
            415,
            175,
            boxstyle=(
                "round,pad=0.0,"
                "rounding_size=14"
            ),
            facecolor="#0f141b",
            edgecolor="#27323d",
            linewidth=1
        )
    )

    ax.text(
        670,
        235,
        "EXTERNAL FORCE",
        fontsize=10,
        color=MUTED,
        fontweight="bold"
    )

    xx = np.linspace(
        675,
        1025,
        180
    )

    yy = (
        305
        - 17
        * np.sin(
            (xx - 675)
            / 35
        )
        - 5
        * np.sin(
            (xx - 675)
            / 12
        )
    )

    ax.plot(
        xx,
        yy,
        color=GREEN,
        linewidth=2.7
    )

    ax.text(
        850,
        350,
        "smooth",
        fontsize=17,
        color=GREEN,
        fontweight="bold",
        ha="center"
    )

    # --------------------------------------------------------
    # LIMIT EQUATION
    # --------------------------------------------------------

    ax.add_patch(
        FancyBboxPatch(
            (640, 400),
            415,
            105,
            boxstyle=(
                "round,pad=0.0,"
                "rounding_size=14"
            ),
            facecolor="#11161e",
            edgecolor="#27323d",
            linewidth=1
        )
    )

    ax.text(
        670,
        435,
        r"AS  t → T⁻",
        fontsize=17,
        color=TEXT,
        fontweight="bold"
    )

    ax.text(
        670,
        480,
        r"|u| → ∞",
        fontsize=27,
        color=ORANGE,
        fontweight="bold"
    )

    ax.text(
        1025,
        480,
        r"T < ∞",
        fontsize=17,
        color=TEXT,
        fontweight="bold",
        ha="right"
    )

    if q > 0.55:

        alpha = clamp(
            (q - 0.55) * 3
        )

        ax.text(
            600,
            550,
            "THE BLOW-UP IS GENERATED BY THE FLUID DYNAMICS",
            fontsize=11,
            color=ORANGE,
            fontweight="bold",
            ha="center",
            alpha=alpha
        )


# ============================================================
# STAGE RENDERER
# ============================================================

def render_stage(
    stage,
    local_t
):

    reset_axis()

    draw_background()

    if stage == 0:

        stage_1(local_t)

    elif stage == 1:

        stage_2(local_t)

    elif stage == 2:

        stage_3(local_t)

    elif stage == 3:

        stage_4(local_t)

    elif stage == 4:

        stage_5(local_t)


# ============================================================
# CROSSFADE LOGIC
# ============================================================
#
# Instead of hard cuts:
#
# Stage A
# █████████████████
#            ↓
#          overlap
#          █████████████████
#                 Stage B
#
# We use an overlap region near every stage boundary.
#
# The outgoing stage fades out while the incoming stage
# fades in.
#
# Matplotlib does not have a simple "scene opacity" mechanism,
# so we create both scenes on separate figures, convert their
# rendered buffers to RGBA, and alpha blend them.
#
# This gives an actual cinematic crossfade.
# ============================================================


def render_scene_to_array(
    stage,
    local_t
):

    # Create temporary figure.

    temp_fig, temp_ax = plt.subplots(
        figsize=(
            FIG_WIDTH,
            FIG_HEIGHT
        ),
        dpi=DPI
    )

    temp_fig.patch.set_facecolor(BG)

    temp_ax.set_facecolor(BG)

    temp_ax.set_xlim(
        0,
        1200
    )

    temp_ax.set_ylim(
        675,
        0
    )

    temp_ax.axis("off")

    # Temporarily switch globals.

    global ax

    original_ax = ax

    ax = temp_ax

    render_stage(
        stage,
        local_t
    )

    temp_fig.canvas.draw()

    width, height = (
        temp_fig.canvas
        .get_width_height()
    )

    buffer = np.frombuffer(
        temp_fig.canvas.buffer_rgba(),
        dtype=np.uint8
    )

    buffer = buffer.reshape(
        height,
        width,
        4
    )

    image = buffer.copy()

    plt.close(
        temp_fig
    )

    ax = original_ax

    return image


# ============================================================
# IMPORTANT PERFORMANCE OPTIMIZATION
# ============================================================
#
# Rendering a complete temporary figure for every frame would
# be unnecessarily expensive.
#
# Therefore we only use true crossfades for the short overlap
# regions and render normal scenes elsewhere.
#
# The transition itself uses a visual "ghost" layer:
#
#   outgoing scene opacity ↓
#   incoming scene opacity ↑
#
# This preserves the cinematic overlap without requiring
# multiple full-size Matplotlib figures to remain alive.
# ============================================================


def crossfade_strength(local_t):

    # Crossfade happens during final CROSSFADE seconds
    # of every stage except the last.

    start = (
        STAGE_DURATION
        - CROSSFADE
    )

    if local_t < start:

        return 0.0

    return clamp(
        (
            local_t
            - start
        )
        / CROSSFADE
    )


# ============================================================
# CINEMATIC STAGE FRAME
# ============================================================

def draw_frame(frame):

    seconds = (
        frame
        / FPS
    )

    # --------------------------------------------------------
    # Determine stage
    # --------------------------------------------------------

    stage_float = (
        seconds
        / STAGE_DURATION
    )

    stage = min(
        4,
        int(stage_float)
    )

    local_t = (
        seconds
        - stage
        * STAGE_DURATION
    )

    # --------------------------------------------------------
    # Determine whether we are inside a transition
    # --------------------------------------------------------

    transition = (
        stage < 4
        and local_t
        >= STAGE_DURATION
        - CROSSFADE
    )

    # --------------------------------------------------------
    # Normal stage
    # --------------------------------------------------------

    if not transition:

        render_stage(
            stage,
            local_t
        )

    # --------------------------------------------------------
    # Crossfade
    # --------------------------------------------------------

    else:

        # ----------------------------------------------------
        # Instead of alpha blending raster images, create
        # the visual transition using synchronized scaling,
        # fading panels and moving elements.
        #
        # This is substantially faster than creating two
        # temporary Matplotlib figures every frame.
        # ----------------------------------------------------

        q = crossfade_strength(
            local_t
        )

        outgoing_q = clamp(
            local_t
            / STAGE_DURATION
        )

        incoming_q = 0.0

        # Start incoming stage slightly before the cut.

        incoming_q = clamp(
            (
                local_t
                - (
                    STAGE_DURATION
                    - CROSSFADE
                )
            )
            / CROSSFADE
        )

        # Draw incoming scene as the primary scene.

        render_stage(
            stage + 1,
            incoming_q
        )

        # ----------------------------------------------------
        # Dark cinematic transition veil.
        #
        # Rather than simply cutting, briefly darken the
        # transition while the next structure emerges.
        # ----------------------------------------------------

        veil_alpha = (
            0.22
            * np.sin(
                np.pi
                * q
            )
        )

        ax.add_patch(
            FancyBboxPatch(
                (20, 20),
                1160,
                620,
                boxstyle=(
                    "round,pad=0.0,"
                    "rounding_size=16"
                ),
                facecolor=BG,
                edgecolor="none",
                alpha=veil_alpha
            )
        )

        # ----------------------------------------------------
        # Transition marker
        # ----------------------------------------------------

        ax.text(
            600,
            595,
            "→",
            fontsize=22,
            color=CYAN,
            alpha=0.45
            + 0.55 * q,
            ha="center",
            va="center",
            fontweight="bold"
        )

    # --------------------------------------------------------
    # Timeline
    # --------------------------------------------------------

    draw_timeline(
        stage
    )

    draw_frame_border()

    draw_time(
        seconds
    )


# ============================================================
# ANIMATION
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
# WEBM WRITER
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
        "-crf", "24",
        "-b:v", "0"
    ]
)


# ============================================================
# RENDER
# ============================================================

print()
print("=" * 64)
print("NAVIER–STOKES · PART 4")
print("THE DELICATE CANCELLATION")
print("=" * 64)

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
    f"Crossfade:        {CROSSFADE:.1f} seconds"
)

print(
    f"Stage duration:   {STAGE_DURATION:.1f} seconds"
)

print(
    f"Output:           {OUTPUT}"
)

print("=" * 64)

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


print()
print("=" * 64)
print("RENDER COMPLETE")
print("=" * 64)

print(
    f"Saved to: {OUTPUT.resolve()}"
)

print("=" * 64)
