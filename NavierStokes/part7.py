import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch


# ============================================================
# NAVIER–STOKES — PART 7
#
# "THEN THEY FORMALLY VERIFIED THE PROOF"
#
# Cinematic + scientifically explicit
#
# 30 seconds
# 24 FPS
# 16:9
#
# Visual language continues from Parts 5 and 6:
# dark background, technical grid, clean typography,
# cyan / orange / violet / green accents.
#
# IMPORTANT DESIGN PRINCIPLE:
# NO TEXT IS PLACED ON TOP OF OTHER TEXT.
#
# Every stage has:
#   1. A fixed title area
#   2. A dedicated visualization area
#   3. A dedicated bottom narration panel
#
# Output:
#   navier_stokes_part7_formal_verification.webm
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

OUTPUT_FILE = "navier_stokes_part7_formal_verification.webm"

STAGE_DURATION = 5.0


# ============================================================
# CINEMATIC THEME
# ============================================================

BG = "#080a0f"
PANEL = "#0d1016"
CARD = "#111720"

TEXT = "#f2f5f7"
SOFT = "#cbd5e1"
MUTED = "#8a929d"

GRID = "#343a45"
BORDER = "#29313c"

CYAN = "#70d6ff"
ORANGE = "#ff9b5e"
VIOLET = "#a98cff"
GREEN = "#79e6a5"
RED = "#ff6d7d"


# ============================================================
# FIGURE
# ============================================================

fig = plt.figure(
    figsize=(FIG_WIDTH, FIG_HEIGHT),
    dpi=DPI,
    facecolor=BG
)


# ------------------------------------------------------------
# MAIN VISUALIZATION AREA
# ------------------------------------------------------------

ax = fig.add_axes(
    [0.045, 0.215, 0.91, 0.665]
)

ax.set_xlim(0, 16)
ax.set_ylim(0, 9)

ax.set_aspect("equal")
ax.axis("off")

ax.set_facecolor(BG)


# ------------------------------------------------------------
# BOTTOM NARRATION AREA
# ------------------------------------------------------------

text_ax = fig.add_axes(
    [0.055, 0.045, 0.89, 0.115]
)

text_ax.set_xlim(0, 1)
text_ax.set_ylim(0, 1)
text_ax.axis("off")
text_ax.set_facecolor(PANEL)


narration_box = FancyBboxPatch(
    (0, 0),
    1,
    1,
    boxstyle="round,pad=0.015,rounding_size=0.025",
    facecolor=PANEL,
    edgecolor="#242b35",
    linewidth=0.8,
    transform=text_ax.transAxes
)

text_ax.add_patch(narration_box)


narration = text_ax.text(
    0.025,
    0.50,
    "",
    color=SOFT,
    fontsize=12,
    ha="left",
    va="center",
    linespacing=1.45,
    transform=text_ax.transAxes
)


# ============================================================
# TOP HUD
# ============================================================

fig.text(
    0.055,
    0.955,
    "PART 07  ·  FORMAL VERIFICATION",
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
# BASIC HELPERS
# ============================================================

def clamp(x):
    return np.clip(x, 0.0, 1.0)


def smoothstep(x):

    x = clamp(x)

    return x * x * (3.0 - 2.0 * x)


def fade_in(q):

    return smoothstep(
        clamp(q / 0.20)
    )


def fade_out(q):

    return smoothstep(
        clamp((1.0 - q) / 0.20)
    )


def stage_progress(q, start, end):

    return smoothstep(
        clamp(
            (q - start) /
            (end - start)
        )
    )


# ============================================================
# GRID
# ============================================================

def draw_grid():

    for x in np.arange(
        0.5,
        16.0,
        1.0
    ):

        ax.plot(
            [x, x],
            [0.25, 8.65],
            color=GRID,
            linewidth=0.7,
            alpha=0.10,
            zorder=0
        )


    for y in np.arange(
        0.5,
        8.6,
        0.75
    ):

        ax.plot(
            [0.25, 15.75],
            [y, y],
            color=GRID,
            linewidth=0.7,
            alpha=0.10,
            zorder=0
        )


# ============================================================
# CARD
# ============================================================

def draw_card(
    x,
    y,
    w,
    h,
    title,
    subtitle=None,
    accent=CYAN,
    alpha=1.0,
    title_size=12
):

    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.025,rounding_size=0.12",
        facecolor=CARD,
        edgecolor=BORDER,
        linewidth=0.9,
        alpha=alpha,
        zorder=10
    )

    ax.add_patch(box)


    # Accent strip

    strip = FancyBboxPatch(
        (x, y),
        0.06,
        h,
        boxstyle="round,pad=0.005,rounding_size=0.04",
        facecolor=accent,
        edgecolor="none",
        alpha=alpha,
        zorder=11
    )

    ax.add_patch(strip)


    ax.text(
        x + w / 2,
        y + h * 0.60,
        title,
        color=TEXT if alpha > 0.5 else MUTED,
        fontsize=title_size,
        fontweight="bold",
        ha="center",
        va="center",
        alpha=alpha,
        zorder=12
    )


    if subtitle:

        ax.text(
            x + w / 2,
            y + h * 0.31,
            subtitle,
            color=SOFT if alpha > 0.5 else MUTED,
            fontsize=8.5,
            ha="center",
            va="center",
            alpha=alpha,
            zorder=12
        )


# ============================================================
# ARROW
# ============================================================

def draw_arrow(
    x1,
    y1,
    x2,
    y2,
    color=CYAN,
    alpha=1.0,
    linewidth=1.8
):

    arrow = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=linewidth,
        color=color,
        alpha=alpha,
        zorder=8
    )

    ax.add_patch(arrow)


# ============================================================
# NODE DOT
# ============================================================

def draw_node(
    x,
    y,
    color,
    radius=0.07,
    alpha=1.0
):

    circle = Circle(
        (x, y),
        radius,
        facecolor=color,
        edgecolor="none",
        alpha=alpha,
        zorder=15
    )

    ax.add_patch(circle)


# ============================================================
# VORTEX ICON
# ============================================================

def draw_vortex_icon(
    cx,
    cy,
    scale=1.0,
    alpha=1.0
):

    theta = np.linspace(
        0,
        4.8 * np.pi,
        240
    )

    for i in range(8):

        r0 = (
            0.35
            + i * 0.13
        )

        r = (
            r0
            * (1.0 - theta / (6.0 * np.pi))
        )

        x = (
            cx
            + scale
            * r
            * np.cos(theta + i * 0.3)
        )

        y = (
            cy
            + scale
            * r
            * np.sin(theta + i * 0.3)
            * 0.65
        )

        color = (
            ORANGE
            if i < 3
            else CYAN
        )

        ax.plot(
            x,
            y,
            color=color,
            linewidth=1.2,
            alpha=alpha * (
                0.35
                + 0.08 * i
            ),
            zorder=5
        )


# ============================================================
# CHECKMARK
# ============================================================

def draw_checkmark(
    x,
    y,
    scale=1.0,
    alpha=1.0
):

    # Outer circle

    circle = Circle(
        (x, y),
        0.42 * scale,
        facecolor="none",
        edgecolor=GREEN,
        linewidth=2.0,
        alpha=alpha,
        zorder=20
    )

    ax.add_patch(circle)


    # Check

    ax.plot(
        [
            x - 0.18 * scale,
            x - 0.04 * scale,
            x + 0.20 * scale
        ],
        [
            y,
            y - 0.14 * scale,
            y + 0.18 * scale
        ],
        color=GREEN,
        linewidth=3.0,
        solid_capstyle="round",
        alpha=alpha,
        zorder=21
    )


# ============================================================
# STAGE 1
#
# SEARCH
# ============================================================

def stage_1(q):

    title_text.set_text(
        "Finding the idea is not the same as proving every step."
    )


    narration.set_text(
        "The agents first have to discover a mathematical construction "
        "that could resolve the problem. A plausible route is not yet a proof."
    )


    # Main problem

    draw_card(
        5.0,
        5.9,
        6.0,
        1.15,
        "NAVIER–STOKES PROBLEM",
        "existence + smoothness",
        CYAN
    )


    # Four branches

    labels = [
        (
            0.9,
            "PROVE SMOOTHNESS",
            "regularity route",
            VIOLET
        ),
        (
            4.45,
            "FIND SINGULARITY",
            "blow-up route",
            ORANGE
        ),
        (
            8.0,
            "SIMPLIFY",
            "reduce structure",
            CYAN
        ),
        (
            11.55,
            "EXPLORE",
            "many constructions",
            VIOLET
        )
    ]


    for x, label, sub, color in labels:

        draw_card(
            x,
            2.65,
            2.65,
            1.0,
            label,
            sub,
            color
        )

        draw_arrow(
            8.0,
            5.9,
            x + 1.325,
            3.65,
            GRID,
            0.55
        )


    # Small search activity

    progress = stage_progress(
        q,
        0.25,
        0.80
    )


    for i in range(20):

        angle = (
            i * 2.399
            + q * 2.0
        )

        radius = (
            0.4
            + (i % 5) * 0.16
        )

        x = (
            8.0
            + np.cos(angle)
            * radius
        )

        y = (
            4.8
            + np.sin(angle)
            * radius
        )

        draw_node(
            x,
            y,
            CYAN,
            0.035,
            0.25 * progress
        )


# ============================================================
# STAGE 2
#
# EULER → VORTEX
# ============================================================

def stage_2(q):

    title_text.set_text(
        "One route begins to survive: Euler first, then Navier–Stokes."
    )


    narration.set_text(
        "The search narrows toward a useful blow-up mechanism. "
        "An Euler insight points toward a concrete vortex construction."
    )


    # Left

    draw_card(
        1.0,
        3.35,
        3.5,
        1.25,
        "EULER BLOW-UP INSIGHT",
        "a useful mechanism",
        ORANGE
    )


    # Center

    draw_arrow(
        4.5,
        3.98,
        6.0,
        3.98,
        ORANGE,
        2.2
    )


    # Vortex

    draw_card(
        6.0,
        3.35,
        3.5,
        1.25,
        "VORTEX CONSTRUCTION",
        "a specific candidate",
        CYAN
    )


    # Right endpoint

    draw_arrow(
        9.5,
        3.98,
        11.0,
        3.98,
        CYAN,
        2.2
    )


    draw_card(
        11.0,
        3.35,
        3.5,
        1.25,
        "SINGULAR STRUCTURE",
        "the target",
        RED
    )


    # Vortex graphic

    draw_vortex_icon(
        7.75,
        2.0,
        scale=1.2,
        alpha=fade_in(q)
    )


    ax.text(
        8.0,
        6.4,
        "THE SEARCH SPACE COLLAPSES",
        color=MUTED,
        fontsize=10,
        fontweight="bold",
        family="monospace",
        ha="center",
        va="center"
    )


    ax.text(
        8.0,
        5.95,
        "many possibilities  →  one structured construction",
        color=SOFT,
        fontsize=10,
        ha="center",
        va="center"
    )


# ============================================================
# STAGE 3
#
# VORTEX CONSEQUENCES
# ============================================================

def stage_3(q):

    title_text.set_text(
        "The construction must satisfy several conditions at once."
    )


    narration.set_text(
        "The vortex develops inward spiral and stretching. "
        "The velocity becomes unbounded, yet the energy remains finite "
        "and the external forcing stays smooth."
    )


    # Central vortex

    draw_vortex_icon(
        8.0,
        4.55,
        scale=2.15,
        alpha=0.90
    )


    # Three clean consequence cards

    draw_card(
        0.75,
        5.95,
        3.45,
        1.15,
        "VELOCITY",
        r"$|u| \rightarrow \infty$",
        RED
    )


    draw_card(
        6.275,
        6.85,
        3.45,
        1.15,
        "ENERGY",
        r"$E(t) < \infty$",
        GREEN
    )


    draw_card(
        11.80,
        5.95,
        3.45,
        1.15,
        "FORCING",
        "smooth external force",
        VIOLET
    )


    # Geometry labels

    ax.text(
        4.2,
        3.15,
        "INWARD SPIRAL",
        color=CYAN,
        fontsize=9,
        fontweight="bold",
        family="monospace",
        ha="center",
        va="center"
    )


    draw_arrow(
        4.2,
        3.45,
        5.75,
        4.15,
        CYAN,
        1.4,
        0.75
    )


    ax.text(
        11.8,
        3.15,
        "AXIAL STRETCHING",
        color=ORANGE,
        fontsize=9,
        fontweight="bold",
        family="monospace",
        ha="center",
        va="center"
    )


    draw_arrow(
        11.8,
        3.45,
        10.15,
        4.15,
        ORANGE,
        1.4,
        0.75
    )


    # Central singularity

    core_alpha = 0.4 + 0.5 * smoothstep(q)

    core = Circle(
        (8.0, 4.55),
        0.12 + 0.04 * np.sin(q * 4 * np.pi),
        facecolor=RED,
        edgecolor=ORANGE,
        linewidth=1.5,
        alpha=core_alpha,
        zorder=30
    )

    ax.add_patch(core)


# ============================================================
# STAGE 4
#
# ANALYTICAL PROOF
# ============================================================

def stage_4(q):

    title_text.set_text(
        "Now the pieces have to become one analytical proof."
    )


    narration.set_text(
        "A proof must establish the entire chain simultaneously: "
        "finite-time blow-up, finite energy, and smooth external forcing."
    )


    # Three evidence boxes

    draw_card(
        0.85,
        5.65,
        3.55,
        1.20,
        "UNBOUNDED VELOCITY",
        r"$|u| \rightarrow \infty$",
        RED
    )


    draw_card(
        0.85,
        3.35,
        3.55,
        1.20,
        "FINITE ENERGY",
        r"$E(t) < \infty$",
        GREEN
    )


    draw_card(
        0.85,
        1.05,
        3.55,
        1.20,
        "SMOOTH FORCING",
        r"$f(x,t)$ remains smooth",
        VIOLET
    )


    # Central convergence point

    convergence_alpha = stage_progress(
        q,
        0.15,
        0.60
    )


    for y, color in [
        (6.25, RED),
        (3.95, GREEN),
        (1.65, VIOLET)
    ]:

        draw_arrow(
            4.4,
            y,
            6.25,
            4.15,
            color,
            1.8,
            convergence_alpha
        )


    # Central box

    draw_card(
        6.25,
        3.35,
        3.65,
        1.60,
        "ANALYTICAL PROOF",
        "all conditions established together",
        GREEN,
        alpha=0.4 + 0.6 * convergence_alpha,
        title_size=13
    )


    # Checkmark

    if q > 0.45:

        check_alpha = stage_progress(
            q,
            0.45,
            0.75
        )

        draw_checkmark(
            8.05,
            2.25,
            scale=0.75,
            alpha=check_alpha
        )


    # Right side

    draw_arrow(
        9.9,
        4.15,
        11.45,
        4.15,
        GREEN,
        2.4,
        convergence_alpha
    )


    draw_card(
        11.45,
        3.35,
        3.65,
        1.60,
        "RESOLUTION",
        "mathematical argument complete",
        GREEN,
        alpha=0.45 + 0.55 * convergence_alpha,
        title_size=13
    )


# ============================================================
# STAGE 5
#
# LEAN FORMALIZATION
# ============================================================

def stage_5(q):

    title_text.set_text(
        "Then they formally verified the proof in Lean."
    )


    narration.set_text(
        "OpenAI says the initial resolution arrived around September 5, "
        "about 88 hours after the effort began. Lean formalization and "
        "verification took another 17 hours, using GPT-6 Astra."
    )


    # --------------------------------------------------------
    # ANALYTICAL PROOF
    # --------------------------------------------------------

    draw_card(
        1.25,
        4.65,
        4.0,
        1.45,
        "ANALYTICAL PROOF",
        "human-readable mathematical argument",
        GREEN,
        title_size=13
    )


    # --------------------------------------------------------
    # ARROW
    # --------------------------------------------------------

    arrow_alpha = stage_progress(
        q,
        0.15,
        0.55
    )


    draw_arrow(
        5.25,
        5.375,
        6.75,
        5.375,
        CYAN,
        2.4,
        arrow_alpha
    )


    ax.text(
        6.0,
        5.75,
        "FORMALIZE",
        color=MUTED,
        fontsize=8.5,
        family="monospace",
        fontweight="bold",
        ha="center",
        va="center",
        alpha=arrow_alpha
    )


    # --------------------------------------------------------
    # LEAN
    # --------------------------------------------------------

    lean_alpha = stage_progress(
        q,
        0.35,
        0.75
    )


    draw_card(
        6.75,
        4.65,
        4.0,
        1.45,
        "LEAN FORMALIZATION",
        "machine-checkable proof",
        CYAN,
        alpha=lean_alpha,
        title_size=13
    )


    # --------------------------------------------------------
    # VERIFIED
    # --------------------------------------------------------

    verified_alpha = stage_progress(
        q,
        0.65,
        0.90
    )


    if verified_alpha > 0:

        draw_checkmark(
            12.45,
            5.38,
            scale=1.0,
            alpha=verified_alpha
        )


        ax.text(
            12.45,
            4.62,
            "FORMALLY",
            color=GREEN,
            fontsize=9,
            family="monospace",
            fontweight="bold",
            ha="center",
            va="center",
            alpha=verified_alpha
        )


        ax.text(
            12.45,
            4.28,
            "VERIFIED",
            color=GREEN,
            fontsize=13,
            fontweight="bold",
            ha="center",
            va="center",
            alpha=verified_alpha
        )


    # --------------------------------------------------------
    # TIMELINE
    # --------------------------------------------------------

    ax.plot(
        [2.0, 14.0],
        [2.35, 2.35],
        color=GRID,
        linewidth=2.0,
        alpha=0.7,
        zorder=2
    )


    # 88 hours

    ax.scatter(
        4.0,
        2.35,
        s=80,
        color=ORANGE,
        alpha=0.95,
        zorder=5
    )


    ax.text(
        4.0,
        2.85,
        "≈ 88 HOURS",
        color=ORANGE,
        fontsize=11,
        fontweight="bold",
        family="monospace",
        ha="center",
        va="center"
    )


    ax.text(
        4.0,
        1.90,
        "initial resolution",
        color=MUTED,
        fontsize=9,
        ha="center",
        va="center"
    )


    # 17 hours

    ax.scatter(
        10.0,
        2.35,
        s=80,
        color=CYAN,
        alpha=0.95,
        zorder=5
    )


    ax.text(
        10.0,
        2.85,
        "+ 17 HOURS",
        color=CYAN,
        fontsize=11,
        fontweight="bold",
        family="monospace",
        ha="center",
        va="center"
    )


    ax.text(
        10.0,
        1.90,
        "Lean formalization + verification",
        color=MUTED,
        fontsize=9,
        ha="center",
        va="center"
    )


    # Final statement

    final_alpha = stage_progress(
        q,
        0.72,
        0.96
    )


    ax.text(
        8.0,
        7.35,
        "ANALYTICAL ARGUMENT",
        color=SOFT,
        fontsize=10,
        family="monospace",
        fontweight="bold",
        ha="center",
        va="center",
        alpha=final_alpha
    )


    ax.text(
        8.0,
        7.78,
        "↓",
        color=CYAN,
        fontsize=15,
        ha="center",
        va="center",
        alpha=final_alpha
    )


    ax.text(
        8.0,
        8.20,
        "FORMALLY CHECKED",
        color=GREEN,
        fontsize=15,
        fontweight="bold",
        family="monospace",
        ha="center",
        va="center",
        alpha=final_alpha
    )


# ============================================================
# CLEAR DYNAMIC SCENE
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


    # Remove axis text

    for artist in list(
        ax.texts
    ):

        artist.remove()


    # Restore grid

    draw_grid()


# ============================================================
# MAIN UPDATE
# ============================================================

def update(frame):

    # Current time

    t = frame / FPS

    t = min(
        t,
        DURATION - 1e-6
    )


    # Six-second stages

    stage = int(
        t // STAGE_DURATION
    )

    # Since DURATION is 30 seconds:
    # stages are 0–5

    # Each stage is 5 seconds

    stage = min(
        stage,
        5
    )


    local_t = (
        t
        - stage * STAGE_DURATION
    )

    q = local_t / STAGE_DURATION


    # Clear previous frame

    clear_scene()


    # --------------------------------------------------------
    # DRAW CURRENT STAGE
    # --------------------------------------------------------

    if stage == 0:

        stage_1(q)

    elif stage == 1:

        stage_2(q)

    elif stage == 2:

        stage_3(q)

    elif stage == 3:

        stage_4(q)

    elif stage == 4:

        # Repeat analytical proof briefly
        stage_4(q)

    else:

        stage_5(q)


    # --------------------------------------------------------
    # TIME DISPLAY
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
            0.4,
            0.4 + 15.2 * progress
        ],
        [
            0.20,
            0.20
        ],
        color=CYAN,
        linewidth=2.0,
        solid_capstyle="round",
        alpha=0.75,
        zorder=100
    )


    ax.plot(
        [
            0.4 + 15.2 * progress,
            15.6
        ],
        [
            0.20,
            0.20
        ],
        color=GRID,
        linewidth=2.0,
        solid_capstyle="round",
        alpha=0.55,
        zorder=99
    )


    # --------------------------------------------------------
    # STAGE COUNTER
    # --------------------------------------------------------

    ax.text(
        15.55,
        0.43,
        f"{stage + 1} / 6",
        color=MUTED,
        fontsize=8.5,
        family="monospace",
        ha="right",
        va="bottom",
        zorder=100
    )


    return []


# ============================================================
# CREATE ANIMATION
# ============================================================

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

print()
print("==============================================")
print(" NAVIER–STOKES — PART 7")
print(" FORMAL VERIFICATION")
print("==============================================")
print()

print(f"Duration : {DURATION} seconds")
print(f"FPS      : {FPS}")
print(f"Frames   : {TOTAL_FRAMES}")
print(f"Output   : {OUTPUT_FILE}")

print()
print("Rendering...")
print()


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