import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

# ============================================================
# SETTINGS
# ============================================================

OUTPUT_FILE = Path("euler_first_strategy_20s.webm")

FPS = 20
DURATION = 20
TOTAL_FRAMES = FPS * DURATION


# ============================================================
# CINEMATIC DARK THEME
#
# Same palette used across parts 5-8 so this part matches
# the rest of the series.
# ============================================================

BG = "#080a0f"
PANEL = "#0d1016"

TEXT = "#f2f5f7"
MUTED = "#8a929d"
SOFT = "#cbd5e1"

GRID = "#343a45"
BORDER = "#202731"

CYAN = "#70d6ff"
ORANGE = "#ff9b5e"
VIOLET = "#a98cff"
GREEN = "#79e6a5"
RED = "#ff6d7d"

# One accent per internal stage, used on the timeline + callout line
STAGE_COLORS = [CYAN, ORANGE, VIOLET, GREEN]


# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(
    figsize=(12.8, 7.2),
    dpi=150
)

fig.patch.set_facecolor(BG)

ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-0.72, 0.72)
ax.set_aspect("equal")
ax.axis("off")

# Transparent so the background grid (drawn in its own axes
# beneath this one) shows through everywhere, including the
# letterboxed margins around the equal-aspect data box.
ax.patch.set_alpha(0)


# ============================================================
# BACKGROUND GRID (own full-bleed axes, drawn first = bottom layer)
# ============================================================

grid_ax = fig.add_axes([0, 0, 1, 1])
grid_ax.set_xlim(0, 1)
grid_ax.set_ylim(0, 1)
grid_ax.axis("off")
grid_ax.patch.set_alpha(0)

for gx in np.linspace(0.05, 0.95, 18):
    grid_ax.plot(
        [gx, gx],
        [0.05, 0.95],
        color=GRID,
        linewidth=0.5,
        alpha=0.12,
        linestyle=(0, (2, 10))
    )

for gy in np.linspace(0.05, 0.95, 12):
    grid_ax.plot(
        [0.05, 0.95],
        [gy, gy],
        color=GRID,
        linewidth=0.5,
        alpha=0.12,
        linestyle=(0, (2, 10))
    )


# ============================================================
# FOREGROUND DECORATION (own full-bleed axes, drawn last = top layer)
#
# Holds the border frame, the bottom panel card, and the
# 4-stage timeline. All in the same 0-1 figure-fraction
# coordinate system that fig.text() already uses, so nothing
# needs converting.
# ============================================================

deco_ax = fig.add_axes([0, 0, 1, 1])
deco_ax.set_xlim(0, 1)
deco_ax.set_ylim(0, 1)
deco_ax.axis("off")
deco_ax.patch.set_alpha(0)


# ------------------------------------------------------------
# Border frame
# ------------------------------------------------------------

deco_ax.add_patch(
    FancyBboxPatch(
        (0.025, 0.03),
        0.95,
        0.935,
        boxstyle="round,pad=0,rounding_size=0.012",
        fill=False,
        edgecolor=BORDER,
        linewidth=1.2
    )
)


# ------------------------------------------------------------
# Bottom panel card (sits behind the equation + bottom_label)
# ------------------------------------------------------------

deco_ax.add_patch(
    FancyBboxPatch(
        (0.15, 0.045),
        0.70,
        0.165,
        boxstyle="round,pad=0,rounding_size=0.018",
        facecolor=PANEL,
        edgecolor="#242b35",
        linewidth=0.8,
        alpha=0.92
    )
)


# ------------------------------------------------------------
# 4-stage timeline
# ------------------------------------------------------------

TIMELINE_Y = 0.275
TIMELINE_X0 = 0.12
TIMELINE_X1 = 0.88

TIMELINE_LABELS = [
    "FULL EQUATION",
    "\u03bd = 0",
    "SMOOTHNESS?",
    "REVEAL STRUCTURE"
]

timeline_positions = np.linspace(TIMELINE_X0, TIMELINE_X1, 4)

deco_ax.plot(
    [TIMELINE_X0, TIMELINE_X1],
    [TIMELINE_Y, TIMELINE_Y],
    color="#252d37",
    linewidth=2,
    zorder=1
)

timeline_dots = []
timeline_dot_labels = []

for i, tx in enumerate(timeline_positions):

    dot = deco_ax.scatter(
        tx,
        TIMELINE_Y,
        s=28,
        color="#38414c",
        zorder=5
    )

    timeline_dots.append(dot)

    label = deco_ax.text(
        tx,
        TIMELINE_Y - 0.028,
        TIMELINE_LABELS[i],
        fontsize=7.5,
        color=MUTED,
        ha="center",
        va="top",
        fontweight="bold"
    )

    timeline_dot_labels.append(label)


# ============================================================
# TEXT ELEMENTS
# ============================================================

title = fig.text(
    0.5, 0.90, "",
    ha="center",
    fontsize=20,
    weight="bold",
    color=TEXT
)

subtitle = fig.text(
    0.5, 0.845, "",
    ha="center",
    fontsize=13,
    color=MUTED
)

equation = fig.text(
    0.5, 0.07, "",
    ha="center",
    fontsize=15,
    family="monospace",
    color=SOFT
)

stage_label = fig.text(
    0.04, 0.97, "",
    ha="left",
    fontsize=11,
    weight="bold",
    color=MUTED
)

bottom_label = fig.text(
    0.5, 0.15, "",
    ha="center",
    fontsize=15,
    weight="bold",
    color=CYAN
)


# ============================================================
# BACKGROUND VORTEX RINGS
# ============================================================

theta = np.linspace(0, 2 * np.pi, 300)

RING_RADII = [0.28, 0.45, 0.62, 0.79]
RING_COLORS = [ORANGE, CYAN, CYAN, CYAN]
RING_ALPHAS = [0.30, 0.26, 0.20, 0.14]

for radius, color, ring_alpha in zip(RING_RADII, RING_COLORS, RING_ALPHAS):

    ax.plot(
        radius * np.cos(theta),
        0.72 * radius * np.sin(theta),
        color=color,
        linewidth=1,
        alpha=ring_alpha
    )


# ============================================================
# FLUID PARTICLES
# ============================================================

rng = np.random.default_rng(3)

NUM_PARTICLES = 65

initial_radius = rng.uniform(
    0.16,
    0.82,
    NUM_PARTICLES
)

initial_angle = rng.uniform(
    0,
    2 * np.pi,
    NUM_PARTICLES
)

particles = ax.scatter(
    [],
    [],
    s=10,
    alpha=0.75
)


# ============================================================
# FOUR STAGES
# ============================================================

stages = [

    {
        "heading": "START WITH THE FULL EQUATION",

        "headline":
            "Don't attack the hardest version first.",

        "equation":
            "\u2202u/\u2202t + (u\u00b7\u2207)u = \u2212(1/\u03c1)\u2207p + \u03bd\u2207\u00b2u + f",

        "label":
            "Full Navier\u2013Stokes"
    },

    {
        "heading": "SET \u03bd = 0",

        "headline":
            "Remove viscosity and study the simpler Euler equations.",

        "equation":
            "\u03bd = 0   \u2192   \u2202u/\u2202t + (u\u00b7\u2207)u = \u2212(1/\u03c1)\u2207p + f",

        "label":
            "Viscosity removed"
    },

    {
        "heading": "ASK WHETHER SMOOTHNESS CAN FAIL",

        "headline":
            "Can a smooth flow develop unbounded velocity in finite time?",

        "equation":
            "smooth at t = 0   \u2192   |u| \u2192 \u221e at finite T ?",

        "label":
            "Search for finite-time blow-up"
    },

    {
        "heading":
            "USE THE SIMPLER PROBLEM TO REVEAL STRUCTURE",

        "headline":
            "Explore Euler for a mechanism guiding the harder Navier\u2013Stokes search.",

        "equation":
            "Euler clue   \u2192   candidate mechanism   \u2192   Navier\u2013Stokes",

        "label":
            "\u2248100 agents  \u2022  \u224850 hours"
    }
]


# ============================================================
# ANIMATION FUNCTION
# ============================================================

def update(frame):

    # Convert frame number to seconds
    time = frame / FPS

    # Each stage lasts 5 seconds
    stage = min(
        3,
        int(time / 5)
    )

    # Time within current stage: 0 -> 1
    local_time = (
        time - stage * 5
    ) / 5

    # --------------------------------------------------------
    # UPDATE TEXT
    # --------------------------------------------------------

    current = stages[stage]
    accent = STAGE_COLORS[stage]

    stage_label.set_text(
        f"STEP 1  \u2022  {stage + 1}/4"
    )

    title.set_text(
        current["headline"]
    )

    subtitle.set_text(
        current["heading"]
    )

    equation.set_text(
        current["equation"]
    )

    bottom_label.set_text(
        current["label"]
    )

    bottom_label.set_color(accent)

    # --------------------------------------------------------
    # UPDATE TIMELINE
    # --------------------------------------------------------

    for i, (dot, label) in enumerate(
        zip(timeline_dots, timeline_dot_labels)
    ):

        active = i <= stage

        dot.set_sizes(
            [48 if i == stage else (28 if not active else 36)]
        )

        dot.set_color(
            STAGE_COLORS[i] if i == stage
            else (SOFT if active else "#38414c")
        )

        label.set_color(
            TEXT if i == stage
            else (SOFT if active else MUTED)
        )

    # --------------------------------------------------------
    # CONTROL VORTEX EVOLUTION
    # --------------------------------------------------------

    if stage == 0:

        # Normal smooth flow
        concentration = 0.0
        squeeze = 0.82
        rotation = 0.5 * local_time

    elif stage == 1:

        # Slight concentration after removing viscosity
        concentration = (
            0.15 +
            0.08 * local_time
        )

        squeeze = 0.82

        rotation = (
            0.6 +
            local_time
        )

    elif stage == 2:

        # Increasing concentration
        concentration = (
            0.23 +
            0.52 * local_time
        )

        squeeze = (
            0.82 -
            0.20 * local_time
        )

        rotation = (
            1.6 +
            2 * local_time
        )

    else:

        # Strong concentration
        concentration = (
            0.72 +
            0.12 * local_time
        )

        squeeze = (
            0.62 -
            0.08 * local_time
        )

        rotation = (
            3.6 +
            2 * local_time
        )

    # --------------------------------------------------------
    # MOVE FLUID PARTICLES
    # --------------------------------------------------------

    # Shrink the radius as the vortex concentrates
    radius = (
        initial_radius *
        (1 - 0.62 * concentration)
    )

    # Rotate particles around the vortex
    angle = (
        initial_angle
        + rotation
        + local_time * (1 - initial_radius)
    )

    # Convert polar coordinates to Cartesian
    x = (
        radius *
        np.cos(angle)
    )

    y = (
        squeeze *
        radius *
        np.sin(angle)
    )

    particles.set_offsets(
        np.c_[x, y]
    )

    # --------------------------------------------------------
    # PARTICLE SIZE
    # --------------------------------------------------------

    # Particles near the center become visually stronger
    sizes = (
        7 +
        26 *
        (1 - radius / 0.85) ** 2
    )

    particles.set_sizes(
        sizes
    )

    # --------------------------------------------------------
    # PARTICLE COLOR
    #
    # Purely a visual reskin, mirroring the proximity-based
    # orange/cyan coloring used for the vortex icon in the
    # other parts of the series. Does not touch the underlying
    # motion, sizing, or timing.
    # --------------------------------------------------------

    proximity = np.exp(-radius / 0.30)

    particle_colors = np.where(
        proximity[:, None] > 0.45,
        np.array(
            [int(ORANGE[1:3], 16), int(ORANGE[3:5], 16), int(ORANGE[5:7], 16)]
        ) / 255,
        np.array(
            [int(CYAN[1:3], 16), int(CYAN[3:5], 16), int(CYAN[5:7], 16)]
        ) / 255
    )

    particles.set_color(particle_colors)

    return particles,


# ============================================================
# CREATE ANIMATION
# ============================================================

animation = FuncAnimation(
    fig,
    update,
    frames=TOTAL_FRAMES,
    interval=1000 / FPS,
    blit=False
)


# ============================================================
# WEBM / VP9 ENCODING
# ============================================================

writer = FFMpegWriter(
    fps=FPS,

    # VP9 codec -> WebM
    codec="libvpx-vp9",

    # Video bitrate
    bitrate=1400,

    # FFmpeg options
    extra_args=[
        "-pix_fmt",
        "yuv420p",

        # Faster encoding
        "-deadline",
        "good",

        "-cpu-used",
        "2",

        "-crf", "24",
        "-b:v", "0"
    ]
)


# ============================================================
# SAVE
# ============================================================

animation.save(
    OUTPUT_FILE,
    writer=writer
)

plt.close(fig)

print(
    f"Animation saved to: {OUTPUT_FILE}"
)
