
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Circle, FancyBboxPatch
from PIL import Image


# ============================================================
# NAVIER–STOKES — PART 6
#
# "AND THEN COMES THE SURPRISING PART: FINITE ENERGY"
#
# Cinematic scientific visualization
#
# 30 seconds
# 24 FPS
# 16:9
#
# NEW:
# The uploaded 3D vortex/singularity image is incorporated as
# the visual singularity model in the final stages.
#
# IMPORTANT:
# This image is a visual model of the geometry
# (inward spiral + axial stretching).
# It is NOT itself a numerical solution of Navier–Stokes.
# ============================================================


# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

FPS = 24
DURATION = 30
TOTAL_FRAMES = FPS * DURATION

FIG_WIDTH = 16
FIG_HEIGHT = 9
DPI = 150

OUTPUT_FILE = "navier_stokes_part6_finite_energy.webm"

# Five stages × 6 seconds
STAGE_DURATION = 6.0

# ------------------------------------------------------------
# IMAGE
# ------------------------------------------------------------

# Put the uploaded reference image beside this Python file.
SINGULARITY_IMAGE = "singularity_model.png"


# ------------------------------------------------------------
# DARK CINEMATIC THEME
# ------------------------------------------------------------

BG = "#080a0f"
PANEL = "#0d1016"

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
# LOAD + PREPROCESS SINGULARITY IMAGE
# ============================================================

print("Loading singularity model...")

img = Image.open(SINGULARITY_IMAGE).convert("RGBA")

img_array = np.array(img).astype(np.float32) / 255.0


# ------------------------------------------------------------
# REMOVE WHITE BACKGROUND
#
# The supplied image has a white background.
# Pixels close to white are converted to transparent.
# ------------------------------------------------------------

rgb = img_array[:, :, :3]

brightness = np.mean(rgb, axis=2)

white_mask = (
    (rgb[:, :, 0] > 0.93) &
    (rgb[:, :, 1] > 0.93) &
    (rgb[:, :, 2] > 0.93)
)

# Gradual transparency rather than a hard binary cut.
# This preserves anti-aliased edges.
alpha = np.clip(
    (0.94 - brightness) / 0.18,
    0.0,
    1.0
)

# Completely remove obvious white background
alpha[white_mask] = 0.0

img_array[:, :, 3] = alpha

singularity_rgba = img_array


# ============================================================
# FIGURE
# ============================================================

fig = plt.figure(
    figsize=(FIG_WIDTH, FIG_HEIGHT),
    dpi=DPI,
    facecolor=BG
)

ax = fig.add_axes(
    [0.03, 0.18, 0.94, 0.75]
)

ax.set_xlim(-6.0, 6.0)
ax.set_ylim(-3.35, 3.35)

ax.set_aspect("equal")
ax.axis("off")

fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)


# ============================================================
# BOTTOM NARRATION PANEL
# ============================================================

text_ax = fig.add_axes(
    [0.055, 0.035, 0.89, 0.105]
)

text_ax.set_xlim(0, 1)
text_ax.set_ylim(0, 1)
text_ax.axis("off")
text_ax.set_facecolor(PANEL)


text_box = FancyBboxPatch(
    (0, 0),
    1,
    1,
    boxstyle="round,pad=0.015,rounding_size=0.025",
    linewidth=0.8,
    edgecolor="#242b35",
    facecolor=PANEL,
    transform=text_ax.transAxes
)

text_ax.add_patch(text_box)


narration = text_ax.text(
    0.025,
    0.50,
    "",
    transform=text_ax.transAxes,
    ha="left",
    va="center",
    color=SOFT,
    fontsize=12,
    linespacing=1.45
)


# ============================================================
# TOP LABELS
# ============================================================

part_label = fig.text(
    0.055,
    0.955,
    "PART 06  ·  FINITE ENERGY",
    color=MUTED,
    fontsize=10,
    fontweight="bold",
    ha="left",
    va="top"
)


title_text = fig.text(
    0.055,
    0.915,
    "",
    color=TEXT,
    fontsize=21,
    fontweight="bold",
    ha="left",
    va="top"
)


time_text = fig.text(
    0.945,
    0.955,
    "",
    color=MUTED,
    fontsize=10,
    family="monospace",
    ha="right",
    va="top"
)


# ============================================================
# HELPERS
# ============================================================

def clamp(x, a=0.0, b=1.0):
    return np.clip(x, a, b)


def smoothstep(x):

    x = clamp(x)

    return x * x * (3.0 - 2.0 * x)


def ease_in(x):

    x = clamp(x)

    return x * x


def ease_out(x):

    x = clamp(x)

    return 1.0 - (1.0 - x) ** 2


def get_stage(t):

    t = clamp(
        t,
        0,
        DURATION - 1e-6
    )

    stage = int(
        t // STAGE_DURATION
    )

    local_t = (
        t
        - stage * STAGE_DURATION
    )

    q = local_t / STAGE_DURATION

    return stage, q


# ============================================================
# GRID
# ============================================================

def draw_grid():

    # Vertical grid

    for x in np.arange(
        -5.5,
        5.51,
        1.0
    ):

        ax.plot(
            [x, x],
            [-3.0, 3.0],
            color=GRID,
            alpha=0.12,
            linewidth=0.7,
            zorder=0
        )

    # Horizontal grid

    for y in np.arange(
        -3.0,
        3.01,
        0.75
    ):

        ax.plot(
            [-5.7, 5.7],
            [y, y],
            color=GRID,
            alpha=0.12,
            linewidth=0.7,
            zorder=0
        )


# ============================================================
# 2D VORTEX
# ============================================================

N_STREAMLINES = 44
N_POINTS = 260


def vortex_geometry(stage, q):

    """
    Creates the earlier 2D spiral representation.

    This is intentionally schematic.

    As the animation progresses:

        radius       decreases
        concentration increases
        core shrinks
        local velocity increases
    """

    concentration = smoothstep(q)

    if stage == 0:

        concentration_strength = 0.15

    elif stage == 1:

        concentration_strength = 0.35

    elif stage == 2:

        concentration_strength = 0.60

    elif stage == 3:

        concentration_strength = 0.82

    else:

        concentration_strength = 0.92


    curves = []

    for i in range(N_STREAMLINES):

        normalized = (
            i /
            (N_STREAMLINES - 1)
        )

        base_radius = (
            0.25
            + normalized * 3.0
        )

        theta = np.linspace(
            0,
            4.8 * np.pi,
            N_POINTS
        )

        phase = i * 0.115

        r = base_radius * (
            1.0
            - concentration_strength
            * concentration
            * (1.0 - normalized) ** 1.25
        )

        inward = (
            concentration
            * (1.0 - normalized)
            * 0.85
        )

        radius = np.maximum(
            0.045,
            r - inward
        )

        angle = (
            theta
            + phase
            + concentration
            * 3.4
            * (1.0 - normalized)
        )

        x = (
            radius
            * np.cos(angle)
        )

        y = (
            radius
            * np.sin(angle)
            * 0.62
        )

        # Axial stretching begins later

        if stage >= 2:

            stretch = (
                1.0
                + 0.45
                * concentration
                * (1.0 - normalized)
            )

            y *= stretch

        curves.append(
            np.column_stack(
                [x, y]
            )
        )

    return curves


def draw_vortex(stage, q):

    curves = vortex_geometry(
        stage,
        q
    )

    concentration = smoothstep(q)

    for i, curve in enumerate(curves):

        normalized = (
            i /
            (len(curves) - 1)
        )

        intensity = (
            0.20
            + 0.45
            * (1.0 - normalized)
        )

        if (
            stage >= 3
            and normalized < 0.28
        ):

            color = ORANGE

            alpha = (
                0.18
                + 0.65
                * (1.0 - normalized)
                * concentration
            )

        else:

            color = CYAN
            alpha = intensity

        ax.plot(
            curve[:, 0],
            curve[:, 1],
            color=color,
            linewidth=(
                0.75
                + 0.5
                * (1.0 - normalized)
            ),
            alpha=alpha,
            zorder=2
        )


# ============================================================
# CORE
# ============================================================

def draw_core(stage, q):

    concentration = smoothstep(q)

    if stage == 0:

        radius = 0.62

    elif stage == 1:

        radius = (
            0.62
            - 0.18 * concentration
        )

    elif stage == 2:

        radius = (
            0.44
            - 0.18 * concentration
        )

    elif stage == 3:

        radius = (
            0.28
            - 0.16 * concentration
        )

    else:

        radius = (
            0.14
            - 0.085 * concentration
        )

    radius = max(
        radius,
        0.035
    )


    # Soft glow

    for multiplier, alpha in [

        (3.5, 0.025),
        (2.8, 0.035),
        (2.2, 0.05),
        (1.7, 0.08),

    ]:

        circle = Circle(
            (0, 0),
            radius * multiplier,
            facecolor=ORANGE,
            edgecolor="none",
            alpha=alpha,
            zorder=1
        )

        ax.add_patch(circle)


    # Core

    core = Circle(
        (0, 0),
        radius,
        facecolor=RED,
        edgecolor=ORANGE,
        linewidth=1.2,
        alpha=0.90,
        zorder=5
    )

    ax.add_patch(core)


# ============================================================
# CORE BOUNDARY
# ============================================================

def draw_core_boundary(stage, q):

    concentration = smoothstep(q)

    if stage < 1:
        return

    if stage == 1:

        radius = (
            0.75
            - 0.12 * concentration
        )

    elif stage == 2:

        radius = (
            0.60
            - 0.22 * concentration
        )

    elif stage == 3:

        radius = (
            0.38
            - 0.24 * concentration
        )

    else:

        radius = (
            0.17
            - 0.12 * concentration
        )

    radius = max(
        radius,
        0.025
    )

    theta = np.linspace(
        0,
        2 * np.pi,
        300
    )

    ax.plot(
        radius * np.cos(theta),
        radius * np.sin(theta) * 0.62,
        color=ORANGE,
        linewidth=1.0,
        linestyle="--",
        alpha=0.55,
        zorder=4
    )


# ============================================================
# SINGULARITY IMAGE
# ============================================================

singularity_artist = None


def draw_singularity_model(
    stage,
    q
):

    """
    Displays the uploaded reference image.

    The image becomes increasingly important during
    stages 3 and 4.

    Stage 3:
        image gradually appears.

    Stage 4:
        image dominates and contracts toward the
        singular core.
    """

    global singularity_artist

    concentration = smoothstep(q)


    # --------------------------------------------------------
    # IMAGE OPACITY
    # --------------------------------------------------------

    if stage < 3:

        alpha = 0.0

    elif stage == 3:

        alpha = (
            0.10
            + 0.78 * concentration
        )

    else:

        alpha = (
            0.84
            + 0.12 * concentration
        )

    alpha = clamp(
        alpha,
        0,
        0.96
    )


    # --------------------------------------------------------
    # IMAGE SIZE
    # --------------------------------------------------------

    if stage < 3:

        scale = 0.0

    elif stage == 3:

        # Large introduction
        scale = (
            2.10
            + 0.35 * concentration
        )

    else:

        # The entire singularity contracts.
        #
        # This is the key visual transition:
        #
        # LARGE STRUCTURE
        #       ↓
        # SMALL STRUCTURE
        #       ↓
        # CONCENTRATED CORE

        scale = (
            2.45
            - 1.70 * concentration
        )


    # Image dimensions are square.
    #
    # Center the image around the singularity.

    width = scale * 2.0
    height = scale * 2.0


    extent = [
        -width,
        width,
        -height,
        height
    ]


    singularity_artist = ax.imshow(
        singularity_rgba,
        extent=extent,
        interpolation="bilinear",
        alpha=alpha,
        zorder=6
    )


    return singularity_artist


# ============================================================
# PARTICLES
# ============================================================

N_PARTICLES = 180

particle_r = np.linspace(
    0.35,
    3.1,
    N_PARTICLES
)

particle_phase = np.linspace(
    0,
    2 * np.pi,
    N_PARTICLES,
    endpoint=False
)


def draw_particles(stage, q):

    concentration = smoothstep(q)

    for i in range(N_PARTICLES):

        r0 = particle_r[i]

        if stage == 0:

            shrink = 0.0

        elif stage == 1:

            shrink = (
                0.12
                * concentration
            )

        elif stage == 2:

            shrink = (
                0.32
                * concentration
            )

        elif stage == 3:

            shrink = (
                0.62
                * concentration
            )

        else:

            shrink = (
                0.88
                * concentration
            )

        r = r0 * (
            1.0
            - shrink
            * (1.0 - r0 / 3.2)
        )

        theta = (
            particle_phase[i]
            + q
            * (
                1.0
                + 5.0
                * (1.0 - r0 / 3.2)
            )
        )

        x = (
            r
            * np.cos(theta)
        )

        y = (
            r
            * np.sin(theta)
            * 0.62
        )

        proximity = np.exp(
            -r / 0.75
        )

        if (
            proximity > 0.45
            and stage >= 2
        ):

            color = ORANGE
            alpha = 0.70
            size = 10

        else:

            color = CYAN
            alpha = 0.35
            size = 5

        ax.scatter(
            x,
            y,
            s=size,
            color=color,
            alpha=alpha,
            edgecolors="none",
            zorder=8
        )


# ============================================================
# ENERGY INFLOW ARROWS
# ============================================================

def draw_energy_flow(stage, q):

    if stage < 2:
        return

    concentration = smoothstep(q)

    angles = np.linspace(
        0,
        2 * np.pi,
        12,
        endpoint=False
    )

    radius = (
        2.15
        - 0.8 * concentration
    )

    for angle in angles:

        x = (
            radius
            * np.cos(angle)
        )

        y = (
            radius
            * np.sin(angle)
            * 0.62
        )

        dx = (
            -0.42
            * np.cos(angle)
        )

        dy = (
            -0.42
            * np.sin(angle)
            * 0.62
        )

        ax.arrow(
            x,
            y,
            dx,
            dy,
            color=VIOLET,
            alpha=0.38,
            width=0.006,
            head_width=0.09,
            head_length=0.12,
            length_includes_head=True,
            zorder=3
        )


# ============================================================
# METRIC PANEL
# ============================================================

def draw_metric_panel(
    x,
    y,
    width,
    height,
    label,
    value,
    color,
    progress=None
):

    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle=(
            "round,pad=0.02,"
            "rounding_size=0.08"
        ),
        facecolor=PANEL,
        edgecolor="#29313c",
        linewidth=0.8,
        alpha=0.96,
        zorder=20
    )

    ax.add_patch(box)

    ax.text(
        x + 0.16,
        y + height - 0.20,
        label,
        color=MUTED,
        fontsize=8.5,
        family="monospace",
        ha="left",
        va="top",
        zorder=21
    )

    ax.text(
        x + 0.16,
        y + 0.22,
        value,
        color=color,
        fontsize=13,
        fontweight="bold",
        family="monospace",
        ha="left",
        va="bottom",
        zorder=21
    )

    if progress is not None:

        progress = clamp(progress)

        bar_x = x + 0.16
        bar_y = y + 0.12
        bar_w = width - 0.32

        ax.plot(
            [
                bar_x,
                bar_x + bar_w
            ],
            [bar_y, bar_y],
            color="#252c36",
            linewidth=4,
            solid_capstyle="round",
            zorder=21
        )

        ax.plot(
            [
                bar_x,
                bar_x
                + bar_w * progress
            ],
            [bar_y, bar_y],
            color=color,
            linewidth=4,
            solid_capstyle="round",
            zorder=22
        )


# ============================================================
# VELOCITY + CORE VOLUME
# ============================================================

def draw_energy_comparison(
    stage,
    q
):

    concentration = smoothstep(q)

    # --------------------------------------------------------
    # LOCAL SPEED
    # --------------------------------------------------------

    if stage == 0:

        speed = 0.28

    elif stage == 1:

        speed = (
            0.35
            + 0.20 * concentration
        )

    elif stage == 2:

        speed = (
            0.45
            + 0.35 * concentration
        )

    elif stage == 3:

        speed = (
            0.65
            + 0.30 * concentration
        )

    else:

        speed = (
            0.95
            + 0.05 * concentration
        )


    # --------------------------------------------------------
    # CORE VOLUME
    # --------------------------------------------------------

    if stage == 0:

        volume = 0.82

    elif stage == 1:

        volume = (
            0.62
            - 0.15 * concentration
        )

    elif stage == 2:

        volume = (
            0.43
            - 0.18 * concentration
        )

    elif stage == 3:

        volume = (
            0.20
            - 0.12 * concentration
        )

    else:

        volume = (
            0.055
            - 0.035 * concentration
        )

    volume = max(
        volume,
        0.012
    )


    draw_metric_panel(
        -5.25,
        2.10,
        2.25,
        0.90,
        "LOCAL SPEED  |u|",
        "→ ∞"
        if stage == 4
        else "rising",
        ORANGE,
        min(speed, 1.0)
    )


    draw_metric_panel(
        3.00,
        2.10,
        2.25,
        0.90,
        "CORE VOLUME",
        "→ 0"
        if stage >= 3
        else "shrinking",
        CYAN,
        volume
    )


# ============================================================
# TOTAL ENERGY
# ============================================================

def draw_total_energy(
    stage,
    q
):

    """
    Conceptual visualization of bounded total energy.

    The point is:

        local velocity → ∞

        core volume → 0

        total energy remains finite

    This is schematic rather than a numerical energy integral.
    """

    energy = (
        0.78
        + 0.015
        * np.sin(q * 2 * np.pi)
    )

    if stage == 0:

        energy = 0.78

    x = 2.95
    y = -2.65

    width = 2.30


    ax.text(
        x,
        y + 0.45,
        "TOTAL KINETIC ENERGY",
        color=MUTED,
        fontsize=8.5,
        family="monospace",
        ha="left",
        va="bottom",
        zorder=20
    )


    # Background

    ax.plot(
        [x, x + width],
        [y, y],
        color="#252c36",
        linewidth=8,
        solid_capstyle="round",
        zorder=20
    )


    # Energy

    ax.plot(
        [
            x,
            x + width * energy
        ],
        [y, y],
        color=GREEN,
        linewidth=8,
        solid_capstyle="round",
        zorder=21
    )


    ax.text(
        x + width,
        y - 0.22,
        "FINITE",
        color=GREEN,
        fontsize=10,
        fontweight="bold",
        family="monospace",
        ha="right",
        va="top",
        zorder=22
    )


# ============================================================
# EQUATIONS
# ============================================================

def draw_equation(
    stage,
    q
):

    if stage == 0:

        equation = (
            r"$E(t)=\frac{1}{2}\rho"
            r"\int_{\Omega}|u(x,t)|^2\,dV$"
        )

        ax.text(
            0,
            -2.05,
            equation,
            color=TEXT,
            fontsize=21,
            ha="center",
            va="center",
            zorder=20
        )


    elif stage == 1:

        ax.text(
            0,
            -2.05,
            r"$|u|\rightarrow\infty"
            r"\qquad"
            r"V_{\mathrm{core}}\rightarrow0$",
            color=TEXT,
            fontsize=20,
            ha="center",
            va="center",
            zorder=20
        )


    elif stage == 2:

        ax.text(
            0,
            -1.95,
            r"$|u|^2\quad\times\quad dV$",
            color=TEXT,
            fontsize=21,
            ha="center",
            va="center",
            zorder=20
        )

        ax.text(
            -1.05,
            -2.30,
            "huge",
            color=ORANGE,
            fontsize=10.5,
            fontweight="bold",
            family="monospace",
            ha="center",
            va="center",
            zorder=20
        )

        ax.text(
            1.05,
            -2.30,
            "tiny",
            color=CYAN,
            fontsize=10.5,
            fontweight="bold",
            family="monospace",
            ha="center",
            va="center",
            zorder=20
        )


    elif stage == 3:

        ax.text(
            0,
            -2.05,
            r"$E\sim\frac{1}{2}\rho"
            r"\,|u_{\mathrm{core}}|^2"
            r"V_{\mathrm{core}}$",
            color=TEXT,
            fontsize=21,
            ha="center",
            va="center",
            zorder=20
        )


    else:

        ax.text(
            0,
            -2.05,
            r"$|u|\rightarrow\infty"
            r"\qquad\mathrm{but}\qquad"
            r"E(t)<\infty$",
            color=TEXT,
            fontsize=22,
            fontweight="bold",
            ha="center",
            va="center",
            zorder=20
        )


# ============================================================
# SINGULARITY ANNOTATIONS
# ============================================================

def draw_singularity_annotations(
    stage,
    q
):

    if stage < 3:
        return

    concentration = smoothstep(q)


    # --------------------------------------------------------
    # INWARD SPIRAL
    # --------------------------------------------------------

    if stage == 3:

        alpha = 0.25 + 0.55 * concentration

    else:

        alpha = 0.72


    ax.annotate(
        "INWARD SPIRAL",
        xy=(-1.25, 0.45),
        xytext=(-4.6, 0.55),
        color=SOFT,
        fontsize=10,
        fontweight="bold",
        family="monospace",
        arrowprops=dict(
            arrowstyle="->",
            color=CYAN,
            lw=1.1,
            alpha=alpha
        ),
        alpha=alpha,
        zorder=30
    )


    # --------------------------------------------------------
    # AXIAL STRETCHING
    # --------------------------------------------------------

    ax.annotate(
        "AXIAL STRETCHING",
        xy=(0.75, 1.45),
        xytext=(1.8, 2.35),
        color=SOFT,
        fontsize=10,
        fontweight="bold",
        family="monospace",
        arrowprops=dict(
            arrowstyle="->",
            color=ORANGE,
            lw=1.1,
            alpha=alpha
        ),
        alpha=alpha,
        zorder=30
    )


    # --------------------------------------------------------
    # SHRINKING CORE
    # --------------------------------------------------------

    if stage == 4:

        ax.annotate(
            "CONCENTRATED CORE",
            xy=(0, 0),
            xytext=(2.0, -0.65),
            color=ORANGE,
            fontsize=9.5,
            fontweight="bold",
            family="monospace",
            arrowprops=dict(
                arrowstyle="->",
                color=ORANGE,
                lw=1.1
            ),
            zorder=30
        )


# ============================================================
# FINITE-TIME LABEL
# ============================================================

def draw_finite_time(
    stage,
    q
):

    if stage != 4:
        return

    concentration = smoothstep(q)

    alpha = (
        0.45
        + 0.55 * concentration
    )

    ax.text(
        0,
        1.42,
        r"$t\rightarrow T^{-}$",
        color=RED,
        fontsize=15,
        fontweight="bold",
        family="monospace",
        ha="center",
        va="center",
        alpha=alpha,
        zorder=35
    )

    ax.text(
        0,
        1.05,
        r"$T<\infty$",
        color=TEXT,
        fontsize=11,
        family="monospace",
        ha="center",
        va="center",
        alpha=alpha,
        zorder=35
    )


# ============================================================
# STAGE 0
# ============================================================

def stage_0(q):

    title_text.set_text(
        "Energy is an integral — not the velocity at one point."
    )

    narration.set_text(
        "The dangerous quantity is local velocity. "
        "But kinetic energy is not measured at one point — "
        "it is velocity squared integrated over the entire fluid volume."
    )

    draw_vortex(
        0,
        q
    )

    draw_particles(
        0,
        q
    )

    draw_core(
        0,
        q
    )

    draw_energy_comparison(
        0,
        q
    )

    draw_equation(
        0,
        q
    )

    draw_total_energy(
        0,
        q
    )


# ============================================================
# STAGE 1
# ============================================================

def stage_1(q):

    title_text.set_text(
        "The blow-up is concentrated into a shrinking core."
    )

    narration.set_text(
        "The construction does not make the whole fluid infinitely fast. "
        "Instead, the dangerous velocity becomes concentrated into an "
        "increasingly tiny region around the singularity."
    )

    draw_vortex(
        1,
        q
    )

    draw_particles(
        1,
        q
    )

    draw_core(
        1,
        q
    )

    draw_core_boundary(
        1,
        q
    )

    draw_energy_comparison(
        1,
        q
    )

    draw_equation(
        1,
        q
    )

    draw_total_energy(
        1,
        q
    )


# ============================================================
# STAGE 2
# ============================================================

def stage_2(q):

    title_text.set_text(
        "Huge velocity × extremely tiny volume."
    )

    narration.set_text(
        "As the core shrinks, the local speed rises. "
        "The key tradeoff is geometric: less and less volume "
        "contains more and more velocity."
    )

    draw_vortex(
        2,
        q
    )

    draw_particles(
        2,
        q
    )

    draw_core(
        2,
        q
    )

    draw_core_boundary(
        2,
        q
    )

    draw_energy_flow(
        2,
        q
    )

    draw_energy_comparison(
        2,
        q
    )

    draw_equation(
        2,
        q
    )

    draw_total_energy(
        2,
        q
    )


# ============================================================
# STAGE 3
# ============================================================

def stage_3(q):

    title_text.set_text(
        "The blow-up takes shape in a tiny region."
    )

    narration.set_text(
        "Now the geometry becomes three-dimensional: "
        "an inward spiral and axial stretching concentrate "
        "the intense motion toward a narrow central structure."
    )

    # Existing mathematical schematic

    draw_vortex(
        3,
        q
    )

    draw_particles(
        3,
        q
    )

    draw_core(
        3,
        q
    )

    draw_core_boundary(
        3,
        q
    )

    draw_energy_flow(
        3,
        q
    )

    # NEW: reference singularity model

    draw_singularity_model(
        3,
        q
    )

    draw_singularity_annotations(
        3,
        q
    )

    draw_energy_comparison(
        3,
        q
    )

    draw_equation(
        3,
        q
    )

    draw_total_energy(
        3,
        q
    )


# ============================================================
# STAGE 4
# ============================================================

def stage_4(q):

    title_text.set_text(
        "At the singularity: speed diverges, energy stays finite."
    )

    narration.set_text(
        "The remarkable outcome is not infinite energy everywhere. "
        "The velocity magnitude can diverge as t approaches a finite T, "
        "while the total kinetic energy remains finite because the blow-up "
        "is confined to an ever-smaller region."
    )

    # Keep a subtle mathematical flow underneath
    draw_vortex(
        4,
        q
    )

    # Particles become sparse around the singularity
    draw_particles(
        4,
        q
    )

    draw_core(
        4,
        q
    )

    draw_core_boundary(
        4,
        q
    )

    draw_energy_flow(
        4,
        q
    )

    # Dominant singularity model

    draw_singularity_model(
        4,
        q
    )

    draw_singularity_annotations(
        4,
        q
    )

    draw_energy_comparison(
        4,
        q
    )

    draw_equation(
        4,
        q
    )

    draw_total_energy(
        4,
        q
    )

    draw_finite_time(
        4,
        q
    )


# ============================================================
# SCENE CLEANUP
# ============================================================

def clear_scene():

    # Remove patches

    for artist in list(
        ax.patches
    ):

        artist.remove()


    # Remove lines

    for artist in list(
        ax.lines
    ):

        artist.remove()


    # Remove scatter collections

    for artist in list(
        ax.collections
    ):

        artist.remove()


    # Remove dynamic text

    for artist in list(
        ax.texts
    ):

        artist.remove()


    # Remove previous image

    for artist in list(
        ax.images
    ):

        artist.remove()


    # Restore grid

    draw_grid()


# ============================================================
# MAIN UPDATE
# ============================================================

def update(frame):

    t = frame / FPS

    t = min(
        t,
        DURATION - 1e-6
    )

    stage, q = get_stage(t)

    clear_scene()


    # --------------------------------------------------------
    # CURRENT STAGE
    # --------------------------------------------------------

    if stage == 0:

        stage_0(q)

    elif stage == 1:

        stage_1(q)

    elif stage == 2:

        stage_2(q)

    elif stage == 3:

        stage_3(q)

    else:

        stage_4(q)


    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    time_text.set_text(
        f"t = {t:05.2f} s"
    )


    # --------------------------------------------------------
    # PROGRESS BAR
    # --------------------------------------------------------

    progress = (
        t /
        DURATION
    )

    ax.plot(
        [
            -5.65,
            -5.65
            + 11.3 * progress
        ],
        [
            -3.08,
            -3.08
        ],
        color=CYAN,
        linewidth=2.0,
        solid_capstyle="round",
        alpha=0.75,
        zorder=50
    )

    ax.plot(
        [
            -5.65
            + 11.3 * progress,
            5.65
        ],
        [
            -3.08,
            -3.08
        ],
        color="#252c36",
        linewidth=2.0,
        solid_capstyle="round",
        alpha=0.55,
        zorder=49
    )


    # --------------------------------------------------------
    # STAGE INDICATOR
    # --------------------------------------------------------

    ax.text(
        5.65,
        -2.88,
        f"{stage + 1} / 5",
        color=MUTED,
        fontsize=8.5,
        family="monospace",
        ha="right",
        va="bottom",
        zorder=50
    )


    return []


# ============================================================
# CREATE ANIMATION
# ============================================================

print()
print("==============================================")
print(" NAVIER–STOKES PART 6")
print(" FINITE ENERGY")
print("==============================================")
print()
print(f"Duration : {DURATION} seconds")
print(f"FPS      : {FPS}")
print(f"Frames   : {TOTAL_FRAMES}")
print(f"Image    : {SINGULARITY_IMAGE}")
print(f"Output   : {OUTPUT_FILE}")
print()


anim = FuncAnimation(
    fig,
    update,
    frames=TOTAL_FRAMES,
    interval=1000 / FPS,
    blit=False,
    repeat=False
)


# ============================================================
# EXPORT
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


print("Rendering...")
print()


anim.save(
    OUTPUT_FILE,
    writer=writer,
    dpi=DPI
)


plt.close(fig)


print()
print("==============================================")
print(" DONE")
print("==============================================")
print()
print(f"Saved: {OUTPUT_FILE}")
print()
