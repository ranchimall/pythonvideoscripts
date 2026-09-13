import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch


# ============================================================
# NAVIER–STOKES — PART 8
#
# "AND THERE'S AN EVEN MORE INTERESTING TWIST"
#
# Mathematical lineage / related prior work
#
# 30 seconds
# 24 FPS
# 16:9
#
# CLEAN CINEMATIC DESIGN
#
# IMPORTANT:
#   - No overlapping text
#   - Fixed title region
#   - Fixed visualization region
#   - Fixed narration region
#   - One conceptual message per stage
#
# OUTPUT:
#   navier_stokes_part8_mathematical_lineage.webm
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

OUTPUT_FILE = (
    "navier_stokes_part8_mathematical_lineage.webm"
)

STAGE_DURATION = 6.0


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


# ============================================================
# MAIN VISUALIZATION AREA
# ============================================================

ax = fig.add_axes(
    [0.045, 0.215, 0.91, 0.665]
)

ax.set_xlim(0, 16)
ax.set_ylim(0, 9)

ax.set_aspect("equal")
ax.axis("off")

ax.set_facecolor(BG)


# ============================================================
# BOTTOM NARRATION PANEL
# ============================================================

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
    boxstyle=(
        "round,pad=0.015,"
        "rounding_size=0.025"
    ),
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
    "PART 08  ·  MATHEMATICAL LINEAGE",
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
# BASIC FUNCTIONS
# ============================================================

def clamp(x):

    return np.clip(
        x,
        0.0,
        1.0
    )


def smoothstep(x):

    x = clamp(x)

    return (
        x * x *
        (3.0 - 2.0 * x)
    )


def fade_in(q):

    return smoothstep(
        q / 0.20
    )


def fade_out(q):

    return smoothstep(
        (1.0 - q) / 0.20
    )


def local_progress(
    q,
    start,
    end
):

    return smoothstep(
        (q - start) /
        (end - start)
    )


# ============================================================
# GRID
# ============================================================

def draw_grid():

    # Vertical

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


    # Horizontal

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
# CLEAN CARD
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
        boxstyle=(
            "round,pad=0.025,"
            "rounding_size=0.12"
        ),
        facecolor=CARD,
        edgecolor=BORDER,
        linewidth=0.9,
        alpha=alpha,
        zorder=10
    )

    ax.add_patch(box)


    # Accent strip

    ax.plot(
        [x, x],
        [y + 0.12, y + h - 0.12],
        color=accent,
        linewidth=4,
        solid_capstyle="round",
        alpha=alpha,
        zorder=11
    )


    ax.text(
        x + w / 2,
        y + h * 0.61,
        title,
        color=TEXT,
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
            color=SOFT,
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
    linewidth=1.8,
    alpha=1.0
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
# VORTEX GRAPHIC
# ============================================================

def draw_vortex(
    cx,
    cy,
    scale=1.0,
    alpha=1.0
):

    theta = np.linspace(
        0,
        4.8 * np.pi,
        280
    )


    for i in range(10):

        r0 = (
            0.25
            + i * 0.13
        )

        r = (
            r0
            * (
                1.0
                - theta /
                (6.0 * np.pi)
            )
        )


        angle = (
            theta
            + i * 0.28
        )


        x = (
            cx
            + scale
            * r
            * np.cos(angle)
        )


        y = (
            cy
            + scale
            * r
            * np.sin(angle)
            * 0.62
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
            linewidth=1.15,
            alpha=alpha * (
                0.28
                + 0.055 * i
            ),
            zorder=4
        )


    # Core

    core = Circle(
        (cx, cy),
        0.08 * scale,
        facecolor=RED,
        edgecolor=ORANGE,
        linewidth=1.2,
        alpha=alpha,
        zorder=8
    )

    ax.add_patch(core)


# ============================================================
# HIGHLIGHT RING
# ============================================================

def draw_highlight(
    x,
    y,
    w,
    h,
    alpha=1.0,
    color=ORANGE
):

    # Outer glow

    for extra, a in [
        (0.20, 0.08),
        (0.10, 0.14),
        (0.00, 0.85)
    ]:

        box = FancyBboxPatch(
            (
                x - extra,
                y - extra
            ),
            w + 2 * extra,
            h + 2 * extra,
            boxstyle=(
                "round,pad=0.02,"
                "rounding_size=0.14"
            ),
            facecolor="none",
            edgecolor=color,
            linewidth=(
                1.0
                if extra
                else 2.0
            ),
            alpha=alpha * a,
            zorder=25
        )

        ax.add_patch(box)


# ============================================================
# STAGE 1
#
# BROADER CONTEXT
# ============================================================

def stage_1(q):

    title_text.set_text(
        "And there's an even more interesting twist."
    )


    narration.set_text(
        "The underlying mathematical idea wasn't necessarily "
        "something AI invented from nothing. Related mathematical "
        "work already existed."
    )


    # Main central problem

    draw_card(
        4.5,
        5.75,
        7.0,
        1.20,
        "NAVIER–STOKES SINGULARITY",
        "a difficult mathematical target",
        CYAN,
        title_size=14
    )


    # Three paths

    draw_card(
        0.75,
        2.45,
        3.75,
        1.25,
        "EARLIER RELATED WORK",
        "vortex-cascade ideas",
        ORANGE
    )


    draw_card(
        6.10,
        2.45,
        3.75,
        1.25,
        "AI SEARCH",
        "many mathematical constructions",
        CYAN
    )


    draw_card(
        11.45,
        2.45,
        3.75,
        1.25,
        "FORMAL VERIFICATION",
        "analytical proof → Lean",
        GREEN
    )


    # Connections

    draw_arrow(
        8.0,
        5.75,
        2.65,
        3.70,
        ORANGE,
        1.5,
        0.60
    )


    draw_arrow(
        8.0,
        5.75,
        7.98,
        3.70,
        CYAN,
        1.5,
        0.60
    )


    draw_arrow(
        8.0,
        5.75,
        13.33,
        3.70,
        GREEN,
        1.5,
        0.60
    )


    # Small vortex in background

    draw_vortex(
        8.0,
        1.35,
        0.55,
        0.45
    )


# ============================================================
# STAGE 2
#
# ZOOM INTO CÓRDOBA + MARTÍNEZ-ZOROA
# ============================================================

def stage_2(q):

    title_text.set_text(
        "Zoom in: Diego Córdoba and Luis Martínez-Zoroa."
    )


    narration.set_text(
        "Reporting around the announcement highlighted closely "
        "related earlier work by Diego Córdoba and Luis Martínez-Zoroa, "
        "including a vortex-cascade idea related to finite-time "
        "singularity formation."
    )


    z = smoothstep(q)


    # --------------------------------------------------------
    # Background fades away
    # --------------------------------------------------------

    background_alpha = (
        1.0
        - 0.65 * z
    )


    draw_card(
        0.8,
        5.95,
        14.4,
        1.05,
        "RELATED MATHEMATICAL WORK",
        "earlier work connected to the same broad singularity question",
        ORANGE,
        alpha=background_alpha
    )


    # --------------------------------------------------------
    # Main highlighted name panel
    # --------------------------------------------------------

    base_w = 6.2
    base_h = 2.30          # was 2.05 — extra height gives the "and" its own row

    w = (
        base_w
        + 1.15 * z
    )

    h = (
        base_h
        + 0.35 * z
    )


    x = 8.0 - w / 2
    y = 3.05 - 0.15 * z


    draw_card(
        x,
        y,
        w,
        h,
        "DIEGO CÓRDOBA",
        None,               # "and" is now drawn separately below, own row
        ORANGE,
        title_size=17 + 3 * z
    )


    # "and" connector — its own row, well clear of the name above and below
    ax.text(
        8.0,
        y + h * 0.40,
        "and",
        color=SOFT,
        fontsize=10,
        ha="center",
        va="center",
        zorder=13
    )


    ax.text(
        8.0,
        y + h * 0.16,
        "LUIS MARTÍNEZ-ZOROA",
        color=TEXT,
        fontsize=17 + 3 * z,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=13
    )


    # --------------------------------------------------------
    # Highlight
    # --------------------------------------------------------

    draw_highlight(
        x - 0.08,
        y - 0.08,
        w + 0.16,
        h + 0.16,
        alpha=0.25 + 0.65 * z,
        color=ORANGE
    )


    # --------------------------------------------------------
    # Vortex-cascade graphic
    # --------------------------------------------------------

    vortex_alpha = (
        0.20
        + 0.65 * z
    )


    draw_vortex(
        8.0,
        2.10,
        0.48 + 0.12 * z,
        vortex_alpha
    )


    # --------------------------------------------------------
    # Descriptor
    # --------------------------------------------------------

    ax.text(
        8.0,
        1.05,               # was 6.85 — that sat inside the background
                             # card's own box and bled through its title
                             # as the card faded. Moved below the vortex
                             # graphic it's actually captioning instead.
        "VORTEX-CASCADE IDEA",
        color=ORANGE,
        fontsize=10,
        fontweight="bold",
        family="monospace",
        ha="center",
        va="center",
        alpha=0.5 + 0.5 * z,
        zorder=20
    )


# ============================================================
# STAGE 3
#
# RELATED ≠ IDENTICAL
# ============================================================

def stage_3(q):

    title_text.set_text(
        "Related work does not mean identical proof."
    )


    narration.set_text(
        "The important distinction is between a related mathematical "
        "idea and the exact construction used in the reported result."
    )


    # --------------------------------------------------------
    # LEFT — EARLIER WORK
    # --------------------------------------------------------

    draw_card(
        0.9,
        4.15,
        5.15,
        1.45,
        "CÓRDOBA + MARTÍNEZ-ZOROA",
        "related vortex-cascade work",
        ORANGE,
        title_size=12
    )


    # --------------------------------------------------------
    # RIGHT — REPORTED RESULT
    # --------------------------------------------------------

    draw_card(
        9.95,
        4.15,
        5.15,
        1.45,
        "REPORTED AI RESULT",
        "a significantly different proof",
        CYAN,
        title_size=12
    )


    # --------------------------------------------------------
    # CENTER DISTINCTION
    # --------------------------------------------------------

    draw_arrow(
        6.05,
        4.88,
        7.10,
        4.88,
        GRID,
        2.0,
        0.85
    )


    draw_arrow(
        8.90,
        4.88,
        9.95,
        4.88,
        GRID,
        2.0,
        0.85
    )


    # Center symbol

    circle = Circle(
        (8.0, 4.88),
        0.52,
        facecolor="#10161e",
        edgecolor=SOFT,
        linewidth=1.5,
        zorder=15
    )

    ax.add_patch(circle)


    ax.text(
        8.0,
        4.88,
        "≠",
        color=TEXT,
        fontsize=21,
        fontweight="bold",
        ha="center",
        va="center",
        zorder=16
    )


    # --------------------------------------------------------
    # Bottom explanation
    # --------------------------------------------------------

    ax.text(
        8.0,
        2.65,
        "RELATED",
        color=ORANGE,
        fontsize=10,
        fontweight="bold",
        family="monospace",
        ha="center",
        va="center"
    )


    ax.text(
        8.0,
        2.20,
        "does not mean",
        color=MUTED,
        fontsize=10,
        ha="center",
        va="center"
    )


    ax.text(
        8.0,
        1.72,
        "IDENTICAL",
        color=CYAN,
        fontsize=13,
        fontweight="bold",
        family="monospace",
        ha="center",
        va="center"
    )


# ============================================================
# STAGE 4
#
# BUCKMASTER + ALPÖGE
# ============================================================

def stage_4(q):

    title_text.set_text(
        "There was concurrent work on a related Euler problem too."
    )


    narration.set_text(
        "There was also concurrent work by Tristan Buckmaster and "
        "Levent Alpoge on a related Euler problem. OpenAI says its "
        "proof is significantly different and says it did not access "
        "their specific user data."
    )


    # --------------------------------------------------------
    # Left
    # --------------------------------------------------------

    draw_card(
        1.0,
        4.20,
        5.4,
        1.55,
        "TRISTAN BUCKMASTER",
        "concurrent Euler work",
        VIOLET,
        title_size=13
    )


    # --------------------------------------------------------
    # Center
    # --------------------------------------------------------

    draw_card(
        5.9,
        2.85,
        4.2,
        1.35,
        "RELATED EULER PROBLEM",
        "a separate research route",
        VIOLET,
        title_size=12
    )


    # --------------------------------------------------------
    # Right
    # --------------------------------------------------------

    draw_card(
        9.6,
        4.20,
        5.4,
        1.55,
        "LEVENT ALPÖGE",
        "concurrent Euler work",
        VIOLET,
        title_size=13
    )


    # Connections

    draw_arrow(
        6.4,
        4.20,
        7.15,
        4.20,
        VIOLET,
        1.7,
        0.80
    )


    draw_arrow(
        9.6,
        4.20,
        8.85,
        4.20,
        VIOLET,
        1.7,
        0.80
    )


    # --------------------------------------------------------
    # Bottom distinction
    # --------------------------------------------------------

    draw_card(
        3.0,
        0.95,
        10.0,
        1.10,
        "OPENAI'S CLAIM",
        "significantly different proof + no access to their specific user data",
        CYAN,
        title_size=11
    )


# ============================================================
# STAGE 5
#
# THE ACCURATE FRAMING
# ============================================================

def stage_5(q):

    title_text.set_text(
        "So don't say: “AI invented the mathematical idea from scratch.”"
    )


    narration.set_text(
        "A more accurate description is that OpenAI's multi-agent system "
        "searched an enormous mathematical space, found and developed "
        "a viable singularity construction, and then formally verified "
        "the resulting proof."
    )


    # --------------------------------------------------------
    # WRONG CLAIM
    # --------------------------------------------------------

    wrong_alpha = (
        1.0
        - local_progress(
            q,
            0.15,
            0.40
        )
    )


    draw_card(
        0.9,
        5.25,
        6.0,
        1.45,
        "NOT THIS",
        "“AI invented the idea from nothing.”",
        RED,
        alpha=wrong_alpha,
        title_size=13
    )


    if wrong_alpha > 0.05:

        # X

        ax.plot(
            [
                6.15,
                6.55
            ],
            [
                5.60,
                6.30
            ],
            color=RED,
            linewidth=3,
            alpha=wrong_alpha,
            zorder=30
        )


        ax.plot(
            [
                6.55,
                6.15
            ],
            [
                5.60,
                6.30
            ],
            color=RED,
            linewidth=3,
            alpha=wrong_alpha,
            zorder=30
        )


    # --------------------------------------------------------
    # ACCURATE CLAIM
    # --------------------------------------------------------

    correct_alpha = local_progress(
        q,
        0.35,
        0.75
    )


    draw_card(
        9.1,
        5.25,
        6.0,
        1.45,
        "MORE ACCURATE",
        "AI searched → found → developed → verified",
        GREEN,
        alpha=correct_alpha,
        title_size=13
    )


    # --------------------------------------------------------
    # Four-step pipeline
    # --------------------------------------------------------

    steps = [
        (
            1.25,
            "SEARCH",
            "enormous\nmath space",
            CYAN
        ),
        (
            5.05,
            "FIND",
            "viable\nconstruction",
            ORANGE
        ),
        (
            8.85,
            "DEVELOP",
            "analytical\nproof",
            VIOLET
        ),
        (
            12.65,
            "VERIFY",
            "Lean\nformalization",
            GREEN
        )
    ]


    pipeline_alpha = local_progress(
        q,
        0.45,
        0.95
    )


    for i, (
        x,
        label,
        sub,
        color
    ) in enumerate(steps):

        active_alpha = pipeline_alpha


        draw_card(
            x,
            2.25,
            2.15,
            1.15,
            label,
            sub.replace(
                "\n",
                " "
            ),
            color,
            alpha=active_alpha,
            title_size=11
        )


        if i < len(steps) - 1:

            draw_arrow(
                x + 2.15,
                2.82,
                x + 3.80,
                2.82,
                color,
                1.8,
                active_alpha
            )


    # --------------------------------------------------------
    # Final line
    # --------------------------------------------------------

    final_alpha = local_progress(
        q,
        0.72,
        0.98
    )


    ax.text(
        8.0,
        7.75,
        "THAT DISTINCTION MAKES THE STORY MORE INTERESTING.",
        color=GREEN,
        fontsize=11,
        fontweight="bold",
        family="monospace",
        ha="center",
        va="center",
        alpha=final_alpha
    )


    ax.text(
        8.0,
        7.25,
        "SEARCH  ·  DEVELOPMENT  ·  VERIFICATION",
        color=SOFT,
        fontsize=10,
        family="monospace",
        ha="center",
        va="center",
        alpha=final_alpha
    )


# ============================================================
# CLEAR FRAME
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


    # Remove text

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


    # Six stages

    stage = int(
        t // STAGE_DURATION
    )


    stage = min(
        stage,
        4
    )


    local_t = (
        t
        - stage * STAGE_DURATION
    )


    q = (
        local_t /
        STAGE_DURATION
    )


    # Clear

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


    else:

        stage_5(q)


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
        f"{stage + 1} / 5",
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
print(" NAVIER–STOKES — PART 8")
print(" MATHEMATICAL LINEAGE")
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