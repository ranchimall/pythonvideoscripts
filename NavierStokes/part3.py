import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch
from pathlib import Path


# ============================================================
# NAVIER–STOKES — PART 3
#
# THE KEY IDEA:
# BUILD A VORTEX THAT DESTROYS ITS OWN SMOOTHNESS
#
# 30-second cinematic scientific animation
#
# Timeline:
#
# 0–6 s    Initial smooth vortex
# 6–12 s   Spiral inward
# 12–18 s  Stretching / "like spaghetti"
# 18–24 s  Faster rotation + concentration
# 24–30 s  Finite-time singularity
#
# Output:
#   navier_stokes_part3_vortex.webm
#
# Requirements:
#   numpy
#   matplotlib
#   ffmpeg with libvpx-vp9
# ============================================================


# ============================================================
# CONFIGURATION
# ============================================================

FPS = 24
DURATION = 30
TOTAL_FRAMES = FPS * DURATION

FIG_WIDTH = 16
FIG_HEIGHT = 9
DPI = 150

OUTPUT = Path("navier_stokes_part3_vortex.webm")


# ============================================================
# COLORS
# ============================================================

BG = "#080a0f"
PANEL = "#0d1016"

TEXT = "#f2f5f7"
MUTED = "#8a929d"
GRID = "#343a45"

ACCENT = "#7dd3fc"

SOFT = "#cbd5e1"


# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(
    figsize=(FIG_WIDTH, FIG_HEIGHT),
    dpi=DPI
)

fig.patch.set_facecolor(BG)

ax.set_facecolor(PANEL)

ax.set_xlim(0, 1200)
ax.set_ylim(0, 675)

ax.set_aspect("equal")

ax.axis("off")


# ============================================================
# RANDOM GENERATOR
# ============================================================

rng = np.random.default_rng(42)


# ============================================================
# STAGE INFORMATION
# ============================================================

STAGE_NAMES = [
    "STAGE 1 · INITIAL STATE",
    "STAGE 2 · INWARD SPIRAL",
    "STAGE 3 · STRETCHING",
    "STAGE 4 · CONCENTRATION",
    "STAGE 5 · FINITE-TIME SINGULARITY"
]


STAGE_HEADLINES = [
    "Start with a smooth vortex.",
    "The flow spirals inward.",
    "The vortex stretches — like spaghetti.",
    "The core narrows while velocity increases.",
    "At finite time T, |u| → ∞."
]


STAGE_DESCRIPTIONS = [
    "Nothing is singular yet. The velocity field is smooth.",
    "The active region concentrates toward a smaller core.",
    "The vortex becomes increasingly elongated and thin.",
    "Smaller spatial scale + faster rotation produces stronger concentration.",
    "The construction reaches a finite-time singularity."
]


# ============================================================
# GLOBAL HELPERS
# ============================================================

def reset_axis():

    ax.cla()

    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 675)

    ax.set_aspect("equal")

    ax.axis("off")

    ax.set_facecolor(PANEL)


def draw_background():

    # Horizontal grid
    for y in [100, 200, 300, 400, 500, 600]:

        ax.plot(
            [0, 1200],
            [y, y],
            color=GRID,
            linewidth=0.5,
            alpha=0.08
        )

    # Vertical grid
    for x in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]:

        ax.plot(
            [x, x],
            [0, 675],
            color=GRID,
            linewidth=0.5,
            alpha=0.08
        )


def draw_header(stage):

    ax.text(
        600,
        628,
        STAGE_NAMES[stage],
        color=MUTED,
        fontsize=10,
        ha="center",
        va="center",
        fontweight="bold",
        alpha=0.95
    )

    ax.text(
        600,
        596,
        STAGE_HEADLINES[stage],
        color=TEXT,
        fontsize=19,
        ha="center",
        va="center",
        fontweight="bold"
    )

    ax.text(
        600,
        570,
        STAGE_DESCRIPTIONS[stage],
        color=MUTED,
        fontsize=10,
        ha="center",
        va="center"
    )


def draw_timeline(stage):

    start_x = 45
    width = 210
    gap = 12

    for i in range(5):

        x0 = start_x + i * (width + gap)

        if i == stage:

            color = ACCENT
            alpha = 1.0

        else:

            color = GRID
            alpha = 0.5

        ax.plot(
            [x0, x0 + width],
            [25, 25],
            color=color,
            linewidth=4,
            solid_capstyle="round",
            alpha=alpha
        )


def draw_frame_border():

    ax.plot(
        [10, 1190],
        [650, 650],
        color=GRID,
        linewidth=.6,
        alpha=.5
    )

    ax.plot(
        [10, 1190],
        [28, 28],
        color=GRID,
        linewidth=.6,
        alpha=.5
    )


def pulse(t, base, amplitude, frequency):

    return base + amplitude * (
        0.5
        + 0.5 * np.sin(
            2 * np.pi * frequency * t
        )
    )


# ============================================================
# VORTEX FIELD
# ============================================================

def vortex_coordinates(
    cx,
    cy,
    radius,
    turns,
    stretch_y=1.0,
    rotation=0.0,
    points=500
):

    theta = np.linspace(
        0,
        turns * 2 * np.pi,
        points
    )

    # logarithmic-ish spiral
    r = radius * (
        1
        - 0.82 * theta / (
            turns * 2 * np.pi
        )
    )

    r = np.maximum(
        r,
        radius * 0.035
    )

    x = r * np.cos(theta)
    y = r * np.sin(theta) * stretch_y

    # rotate
    xr = (
        x * np.cos(rotation)
        - y * np.sin(rotation)
    )

    yr = (
        x * np.sin(rotation)
        + y * np.cos(rotation)
    )

    return (
        cx + xr,
        cy + yr
    )


# ============================================================
# STREAMLINES
# ============================================================

def draw_streamline_family(
    cx,
    cy,
    scale,
    stretch_y,
    rotation,
    count=12,
    alpha=0.35,
    linewidth=1
):

    for i in range(count):

        radius = (
            scale
            * (0.30 + i * 0.07)
        )

        theta = np.linspace(
            0,
            2.2 * np.pi,
            450
        )

        # swirl
        rr = radius * (
            1
            + 0.025 * np.sin(
                theta * 3 + i
            )
        )

        x = rr * np.cos(theta)

        y = (
            rr
            * np.sin(theta)
            * stretch_y
        )

        # rotation
        xr = (
            x * np.cos(rotation)
            - y * np.sin(rotation)
        )

        yr = (
            x * np.sin(rotation)
            + y * np.cos(rotation)
        )

        ax.plot(
            cx + xr,
            cy + yr,
            color=ACCENT if i == 0 else GRID,
            linewidth=linewidth,
            alpha=alpha if i != 0 else alpha * 1.5
        )


# ============================================================
# STAGE 1
#
# INITIAL SMOOTH VORTEX
# ============================================================

def stage_1(t):

    draw_background()
    draw_header(0)

    cx = 600
    cy = 335

    rotation = t * 0.4

    # --------------------------------------------------------
    # Main vortex
    # --------------------------------------------------------

    draw_streamline_family(
        cx=cx,
        cy=cy,
        scale=270,
        stretch_y=0.52,
        rotation=rotation,
        count=13,
        alpha=0.30,
        linewidth=1
    )

    # --------------------------------------------------------
    # Core glow
    # --------------------------------------------------------

    glow_radius = pulse(
        t,
        65,
        15,
        0.5
    )

    ax.add_patch(
        Circle(
            (cx, cy),
            glow_radius,
            color=ACCENT,
            alpha=0.055
        )
    )

    ax.scatter(
        cx,
        cy,
        s=100,
        color=ACCENT,
        alpha=0.9
    )

    # --------------------------------------------------------
    # Rotation arrows
    # --------------------------------------------------------

    arrow_angles = [
        0,
        np.pi / 2,
        np.pi,
        3 * np.pi / 2
    ]

    for angle in arrow_angles:

        r = 185

        x = cx + r * np.cos(angle)
        y = cy + r * 0.52 * np.sin(angle)

        dx = -45 * np.sin(angle)
        dy = 45 * 0.52 * np.cos(angle)

        ax.arrow(
            x,
            y,
            dx,
            dy,
            color=TEXT,
            alpha=0.35,
            width=0.8,
            head_width=7,
            head_length=10,
            length_includes_head=True
        )

    # --------------------------------------------------------
    # Scientific annotation
    # --------------------------------------------------------

    ax.text(
        cx,
        475,
        "SMOOTH VELOCITY FIELD",
        color=TEXT,
        fontsize=13,
        ha="center",
        fontweight="bold"
    )

    ax.text(
        cx,
        450,
        "finite velocity · finite spatial scale",
        color=MUTED,
        fontsize=10,
        ha="center"
    )

    ax.text(
        600,
        80,
        "A vortex exists — but nothing has blown up.",
        color=MUTED,
        fontsize=12,
        ha="center"
    )


# ============================================================
# STAGE 2
#
# SPIRAL INWARD
# ============================================================

def stage_2(t):

    draw_background()
    draw_header(1)

    cx = 600
    cy = 335

    # normalized progress
    p = min(
        1,
        t / 6
    )

    # concentration
    scale = (
        300
        * (1 - 0.55 * p)
    )

    rotation = (
        t * 0.8
    )

    draw_streamline_family(
        cx=cx,
        cy=cy,
        scale=scale,
        stretch_y=0.55,
        rotation=rotation,
        count=14,
        alpha=0.32,
        linewidth=1
    )

    # --------------------------------------------------------
    # Spiral trajectories
    # --------------------------------------------------------

    for i in range(7):

        radius = (
            260
            - i * 28
        )

        theta = np.linspace(
            0,
            2.6 * np.pi,
            400
        )

        inward = (
            1
            - 0.82
            * theta
            / (2.6 * np.pi)
        )

        rr = radius * inward

        x = rr * np.cos(
            theta + rotation
        )

        y = (
            rr
            * np.sin(theta + rotation)
            * 0.55
        )

        ax.plot(
            cx + x,
            cy + y,
            color=TEXT if i == 0 else GRID,
            alpha=0.45 if i == 0 else 0.22,
            linewidth=1.3
        )

    # --------------------------------------------------------
    # Inward arrows
    # --------------------------------------------------------

    arrow_angles = np.linspace(
        0,
        2 * np.pi,
        8,
        endpoint=False
    )

    for angle in arrow_angles:

        r1 = 260

        r2 = 195

        x1 = cx + r1 * np.cos(angle)
        y1 = cy + r1 * 0.55 * np.sin(angle)

        x2 = cx + r2 * np.cos(angle + 0.25)
        y2 = cy + r2 * 0.55 * np.sin(angle + 0.25)

        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                color=TEXT,
                alpha=0.38,
                linewidth=1.2
            )
        )

    # --------------------------------------------------------
    # Core
    # --------------------------------------------------------

    core_size = (
        65
        * (1 - 0.55 * p)
    )

    ax.add_patch(
        Circle(
            (cx, cy),
            core_size * 2,
            color=ACCENT,
            alpha=0.035
        )
    )

    ax.scatter(
        cx,
        cy,
        s=80,
        color=ACCENT,
        alpha=0.95
    )

    # --------------------------------------------------------
    # Labels
    # --------------------------------------------------------

    ax.text(
        600,
        500,
        "SPIRAL INWARD",
        color=TEXT,
        fontsize=14,
        ha="center",
        fontweight="bold"
    )

    ax.text(
        600,
        475,
        "the active region is concentrating",
        color=MUTED,
        fontsize=10,
        ha="center"
    )

    ax.text(
        600,
        80,
        "SPINS  →  SPIRALS INWARD  →  SMALLER ACTIVE REGION",
        color=TEXT,
        fontsize=12,
        ha="center",
        fontweight="bold"
    )


# ============================================================
# STAGE 3
#
# STRETCHING
# ============================================================

def stage_3(t):

    draw_background()
    draw_header(2)

    cx = 600
    cy = 335

    p = min(
        1,
        t / 6
    )

    # --------------------------------------------------------
    # Stretch increases over time
    # --------------------------------------------------------

    stretch_y = (
        0.7
        + 1.8 * p
    )

    horizontal_scale = (
        150
        - 50 * p
    )

    # --------------------------------------------------------
    # Background flow
    # --------------------------------------------------------

    for i in range(8):

        rx = (
            300
            + i * 35
        )

        ry = (
            100
            + i * 18
        )

        ellipse = Ellipse(
            (cx, cy),
            2 * rx,
            2 * ry,
            fill=False,
            edgecolor=GRID,
            linewidth=1,
            alpha=0.25
        )

        ax.add_patch(ellipse)

    # --------------------------------------------------------
    # Elongated vortex
    # --------------------------------------------------------

    ellipse = Ellipse(
        (cx, cy),
        2 * horizontal_scale,
        2 * 250 * stretch_y,
        fill=False,
        edgecolor=ACCENT,
        linewidth=2.5,
        alpha=0.65
    )

    ax.add_patch(ellipse)

    ellipse2 = Ellipse(
        (cx, cy),
        2 * horizontal_scale * 0.55,
        2 * 220 * stretch_y,
        fill=False,
        edgecolor=TEXT,
        linewidth=1.2,
        alpha=0.42
    )

    ax.add_patch(ellipse2)

    # --------------------------------------------------------
    # Internal helical lines
    # --------------------------------------------------------

    for i in range(8):

        phase = (
            i
            * 2
            * np.pi
            / 8
        )

        y = np.linspace(
            -220 * stretch_y,
            220 * stretch_y,
            500
        )

        x = (
            horizontal_scale
            * 0.8
            * np.sin(
                y / 75
                + phase
                + t
            )
        )

        ax.plot(
            cx + x,
            cy + y,
            color=TEXT,
            alpha=0.18,
            linewidth=0.8
        )

    # --------------------------------------------------------
    # Stretch arrows
    # --------------------------------------------------------

    top = cy + 220 * stretch_y

    bottom = cy - 220 * stretch_y

    ax.annotate(
        "",
        xy=(cx, top + 50),
        xytext=(cx, top - 10),
        arrowprops=dict(
            arrowstyle="-|>",
            color=TEXT,
            alpha=0.55,
            linewidth=1.5
        )
    )

    ax.annotate(
        "",
        xy=(cx, bottom - 50),
        xytext=(cx, bottom + 10),
        arrowprops=dict(
            arrowstyle="-|>",
            color=TEXT,
            alpha=0.55,
            linewidth=1.5
        )
    )

    # --------------------------------------------------------
    # Labels
    # --------------------------------------------------------

    ax.text(
        600,
        105,
        "STRETCH",
        color=TEXT,
        fontsize=14,
        ha="center",
        fontweight="bold"
    )

    ax.text(
        600,
        82,
        "longer  +  thinner",
        color=MUTED,
        fontsize=10,
        ha="center"
    )

    ax.text(
        850,
        355,
        "“LIKE SPAGHETTI”",
        color=TEXT,
        fontsize=13,
        fontweight="bold",
        ha="center"
    )

    ax.text(
        850,
        330,
        "increasingly elongated vortex",
        color=MUTED,
        fontsize=10,
        ha="center"
    )


# ============================================================
# STAGE 4
#
# FASTER ROTATION + CONCENTRATION
# ============================================================

def stage_4(t):

    draw_background()
    draw_header(3)

    cx = 600
    cy = 335

    p = min(
        1,
        t / 6
    )

    # --------------------------------------------------------
    # Narrowing core
    # --------------------------------------------------------

    width = (
        95
        - 65 * p
    )

    height = 230

    # --------------------------------------------------------
    # Outer vortex
    # --------------------------------------------------------

    for i in range(5):

        rx = (
            width
            * (1 + i * 0.55)
        )

        ry = (
            height
            * (1 - i * 0.06)
        )

        ellipse = Ellipse(
            (cx, cy),
            2 * rx,
            2 * ry,
            fill=False,
            edgecolor=GRID,
            linewidth=1,
            alpha=0.28
        )

        ax.add_patch(ellipse)

    # --------------------------------------------------------
    # Fast rotating inner vortex
    # --------------------------------------------------------

    rotation = (
        t * 3.5
    )

    for i in range(7):

        rx = (
            width
            * (0.25 + i * 0.16)
        )

        ry = (
            height
            * (0.45 + i * 0.07)
        )

        theta = np.linspace(
            0,
            2 * np.pi,
            500
        )

        # Rotating ellipse
        x = rx * np.cos(theta)

        y = ry * np.sin(theta)

        xr = (
            x * np.cos(rotation)
            - y * np.sin(rotation)
        )

        yr = (
            x * np.sin(rotation)
            + y * np.cos(rotation)
        )

        ax.plot(
            cx + xr,
            cy + yr,
            color=ACCENT if i == 0 else TEXT,
            alpha=0.75 if i == 0 else 0.22,
            linewidth=2 if i == 0 else .8
        )

    # --------------------------------------------------------
    # Center
    # --------------------------------------------------------

    ax.scatter(
        cx,
        cy,
        s=130,
        color=ACCENT,
        alpha=0.95
    )

    ax.add_patch(
        Circle(
            (cx, cy),
            65,
            color=ACCENT,
            alpha=0.045
        )
    )

    # --------------------------------------------------------
    # Velocity indicator
    # --------------------------------------------------------

    ax.text(
        875,
        455,
        "LOCAL VELOCITY",
        color=MUTED,
        fontsize=9,
        ha="center"
    )

    velocity_level = (
        0.25
        + 0.7 * p
    )

    bar_x = 800
    bar_y = 420
    bar_width = 150

    ax.plot(
        [bar_x, bar_x + bar_width],
        [bar_y, bar_y],
        color=GRID,
        linewidth=7,
        solid_capstyle="round"
    )

    ax.plot(
        [
            bar_x,
            bar_x
            + bar_width
            * velocity_level
        ],
        [bar_y, bar_y],
        color=ACCENT,
        linewidth=7,
        solid_capstyle="round"
    )

    ax.text(
        875,
        390,
        "INCREASING",
        color=TEXT,
        fontsize=12,
        ha="center",
        fontweight="bold"
    )

    # --------------------------------------------------------
    # Core width
    # --------------------------------------------------------

    ax.text(
        325,
        455,
        "CORE WIDTH",
        color=MUTED,
        fontsize=9,
        ha="center"
    )

    ax.text(
        325,
        425,
        "↓ SHRINKING",
        color=TEXT,
        fontsize=13,
        ha="center",
        fontweight="bold"
    )

    ax.plot(
        [
            325 - width,
            325 + width
        ],
        [390, 390],
        color=ACCENT,
        linewidth=2,
        alpha=0.7
    )

    # --------------------------------------------------------
    # Rotation arrows
    # --------------------------------------------------------

    arrow_radius = 125

    for angle in [
        0,
        np.pi / 2,
        np.pi,
        3 * np.pi / 2
    ]:

        x = (
            cx
            + arrow_radius
            * np.cos(angle)
        )

        y = (
            cy
            + arrow_radius
            * np.sin(angle)
        )

        dx = (
            -55
            * np.sin(angle)
        )

        dy = (
            55
            * np.cos(angle)
        )

        ax.arrow(
            x,
            y,
            dx,
            dy,
            color=ACCENT,
            alpha=0.55,
            width=1.0,
            head_width=8,
            head_length=10,
            length_includes_head=True
        )

    # --------------------------------------------------------
    # Bottom explanation
    # --------------------------------------------------------

    ax.text(
        600,
        78,
        "NARROWER CORE  +  FASTER ROTATION  →  STRONGER CONCENTRATION",
        color=TEXT,
        fontsize=12,
        ha="center",
        fontweight="bold"
    )


# ============================================================
# STAGE 5
#
# FINITE-TIME SINGULARITY
# ============================================================

def stage_5(t):

    draw_background()
    draw_header(4)

    cx = 600
    cy = 335

    p = min(
        1,
        t / 6
    )

    # --------------------------------------------------------
    # Extremely elongated vortex
    # --------------------------------------------------------

    width = (
        48
        - 34 * p
    )

    height = 250

    rotation = (
        t * 6
    )

    # Outer structure
    for i in range(4):

        rx = (
            width
            * (1 + i * .6)
        )

        ry = (
            height
            * (1 - i * .05)
        )

        theta = np.linspace(
            0,
            2 * np.pi,
            500
        )

        x = rx * np.cos(theta)

        y = ry * np.sin(theta)

        xr = (
            x * np.cos(rotation)
            - y * np.sin(rotation)
        )

        yr = (
            x * np.sin(rotation)
            + y * np.cos(rotation)
        )

        ax.plot(
            cx + xr,
            cy + yr,
            color=ACCENT if i == 0 else GRID,
            linewidth=2 if i == 0 else 1,
            alpha=0.65 if i == 0 else 0.28
        )

    # --------------------------------------------------------
    # Inner singular core
    # --------------------------------------------------------

    core_radius = (
        18
        * (1 - 0.72 * p)
    )

    glow_radius = (
        55
        + 12
        * np.sin(
            t * 8
        )
    )

    ax.add_patch(
        Circle(
            (cx, cy),
            glow_radius,
            color=ACCENT,
            alpha=0.045
        )
    )

    ax.scatter(
        cx,
        cy,
        s=(
            90
            + 110 * p
        ),
        color=ACCENT,
        alpha=0.95
    )

    # --------------------------------------------------------
    # Rotational rays
    # --------------------------------------------------------

    n_rays = 18

    for i in range(n_rays):

        angle = (
            2 * np.pi * i / n_rays
            + rotation
        )

        r1 = 30
        r2 = 90 + 45 * p

        x1 = (
            cx
            + r1
            * np.cos(angle)
        )

        y1 = (
            cy
            + r1
            * np.sin(angle)
        )

        x2 = (
            cx
            + r2
            * np.cos(angle)
        )

        y2 = (
            cy
            + r2
            * np.sin(angle)
        )

        ax.plot(
            [x1, x2],
            [y1, y2],
            color=TEXT,
            alpha=0.12 + 0.22 * p,
            linewidth=.8
        )

    # --------------------------------------------------------
    # Singularity label
    # --------------------------------------------------------

    ax.text(
        cx,
        510,
        "SINGULARITY",
        color=TEXT,
        fontsize=22,
        ha="center",
        fontweight="bold"
    )

    ax.text(
        cx,
        480,
        "the velocity becomes unbounded",
        color=MUTED,
        fontsize=11,
        ha="center"
    )

    # --------------------------------------------------------
    # Equation panel
    # --------------------------------------------------------

    box = FancyBboxPatch(
        (400, 125),
        400,
        90,
        boxstyle="round,pad=0.02,rounding_size=12",
        facecolor="#10141b",
        edgecolor=GRID,
        linewidth=1
    )

    ax.add_patch(box)

    ax.text(
        600,
        180,
        r"$|u| \rightarrow \infty$",
        color=TEXT,
        fontsize=25,
        ha="center",
        va="center"
    )

    ax.text(
        600,
        150,
        r"as $t \rightarrow T^{-}$, with $T < \infty$",
        color=MUTED,
        fontsize=11,
        ha="center",
        va="center"
    )

    # --------------------------------------------------------
    # Time indicator
    # --------------------------------------------------------

    time_progress = (
        0.2
        + 0.8 * p
    )

    ax.text(
        925,
        300,
        "TIME",
        color=MUTED,
        fontsize=9,
        ha="center"
    )

    ax.plot(
        [850, 1000],
        [275, 275],
        color=GRID,
        linewidth=5,
        solid_capstyle="round"
    )

    ax.plot(
        [
            850,
            850
            + 150
            * time_progress
        ],
        [275, 275],
        color=ACCENT,
        linewidth=5,
        solid_capstyle="round"
    )

    ax.text(
        925,
        245,
        "T",
        color=TEXT,
        fontsize=17,
        fontweight="bold",
        ha="center"
    )

    # --------------------------------------------------------
    # Final statement
    # --------------------------------------------------------

    ax.text(
        600,
        75,
        "SPINS  →  SPIRALS INWARD  →  STRETCHES  →  NARROWS  →  SPINS FASTER  →  CONCENTRATES",
        color=TEXT,
        fontsize=10.5,
        ha="center",
        fontweight="bold"
    )


# ============================================================
# MASTER FRAME FUNCTION
# ============================================================

def draw_frame(frame):

    # Global time
    t = frame / FPS

    # Determine stage
    stage = min(
        4,
        int(t // 6)
    )

    # Local time within stage
    local_t = t - stage * 6

    # Clear
    reset_axis()

    # Draw appropriate stage
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

    # Timeline
    draw_timeline(stage)

    # Border
    draw_frame_border()

    # Timestamp
    ax.text(
        1150,
        645,
        f"{t:05.1f}s",
        color=MUTED,
        fontsize=8,
        ha="right"
    )

    # Project identifier
    ax.text(
        45,
        645,
        "NAVIER–STOKES · PART 3",
        color=MUTED,
        fontsize=8,
        ha="left",
        fontweight="bold"
    )


# ============================================================
# INITIAL FRAME
# ============================================================

draw_frame(0)


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
# VIDEO ENCODER
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

print("=" * 60)
print("NAVIER–STOKES PART 3")
print("THE VORTEX")
print("=" * 60)

print()
print(f"FPS:       {FPS}")
print(f"Duration:  {DURATION} seconds")
print(f"Frames:    {TOTAL_FRAMES}")
print(f"Resolution: {FIG_WIDTH * DPI} × {FIG_HEIGHT * DPI}")
print()
print(f"Output:    {OUTPUT.resolve()}")
print()
print("Rendering...")
print()


animation.save(
    OUTPUT,
    writer=writer,
    dpi=DPI
)


# ============================================================
# FINISH
# ============================================================

plt.close(fig)

print()
print("=" * 60)
print("RENDER COMPLETE")
print("=" * 60)
print()
print(f"Saved to:")
print(OUTPUT.resolve())
print()