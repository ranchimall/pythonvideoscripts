import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Circle, FancyBboxPatch, Ellipse
from matplotlib.collections import LineCollection
from pathlib import Path


# ============================================================
# NAVIER–STOKES PART 2
# THE MULTI-AGENT ATTACK
#
# 25-second cinematic scientific visualization
#
# Stages:
#   1. Launch       — one problem
#   2. Diverge      — different attacks
#   3. Explore      — thousands of trajectories
#   4. Communicate  — discoveries move between groups
#   5. Converge     — promising structure emerges
#
# Output:
#   navier_stokes_part2_multi_agent.webm
# ============================================================


# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

FPS = 24
DURATION = 25
TOTAL_FRAMES = FPS * DURATION

WIDTH = 16
HEIGHT = 9
DPI = 150

OUTPUT = Path("navier_stokes_part2_multi_agent.webm")


# ------------------------------------------------------------
# VISUAL STYLE
# ------------------------------------------------------------

BG = "#080a0f"
PANEL = "#0d1016"
TEXT = "#f2f5f7"
MUTED = "#8a929d"
GRID = "#343a45"

ACCENT = "#7dd3fc"

SMOOTH = "#86efac"
BLOWUP = "#fb7185"
SIMPLIFIED = "#c4b5fd"
ESTIMATE = "#fbbf24"
COMPUTE = "#67e8f9"


# ------------------------------------------------------------
# FIGURE
# ------------------------------------------------------------

fig, ax = plt.subplots(
    figsize=(WIDTH, HEIGHT),
    dpi=DPI
)

fig.patch.set_facecolor(BG)
ax.set_facecolor(PANEL)

ax.set_xlim(0, 1200)
ax.set_ylim(0, 675)

ax.set_aspect("equal")
ax.axis("off")


# ------------------------------------------------------------
# DETERMINISTIC RANDOM GENERATOR
# ------------------------------------------------------------

rng = np.random.default_rng(42)


# ------------------------------------------------------------
# TITLE / DESCRIPTION
# ------------------------------------------------------------

subtitle_text = fig.text(
    0.055,
    0.915,
    "",
    color=MUTED,
    fontsize=10,
    ha="left",
    va="top"
)


# ------------------------------------------------------------
# STAGE INFORMATION
# ------------------------------------------------------------

STAGE_TITLES = [
    "1 · LAUNCH",
    "2 · DIVERGE",
    "3 · EXPLORE",
    "4 · COMMUNICATE",
    "5 · CONVERGE"
]

STAGE_HEADLINES = [
    "Don't ask one AI to solve Navier–Stokes.",
    "Give different groups different attacks.",
    "Let thousands of agents explore the space.",
    "Let discoveries travel between groups.",
    "Concentrate effort on the strongest structure."
]

STAGE_DESCRIPTIONS = [
    "One mathematical problem becomes thousands of independent research trajectories.",
    "Some agents pursue global smoothness. Others pursue finite-time blow-up or simplified formulations.",
    "Agents calculate, test hypotheses, search for estimates, find contradictions, and revise.",
    "Useful intermediate discoveries can move between research groups.",
    "OpenAI says Codex helped consolidate useful ideas and feed them into subsequent research."
]


# ------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------

def clear_axis():
    """
    Remove all dynamic artists from the axis.
    """
    ax.cla()

    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 675)

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_facecolor(PANEL)


def add_grid():
    """
    Subtle cinematic background grid.
    """

    # Horizontal grid
    for y in [100, 200, 300, 400, 500, 600]:
        ax.plot(
            [0, 1200],
            [y, y],
            color=GRID,
            alpha=0.08,
            linewidth=0.6
        )

    # Vertical grid
    for x in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]:
        ax.plot(
            [x, x],
            [0, 675],
            color=GRID,
            alpha=0.08,
            linewidth=0.6
        )


def add_stage_bar(stage_index):
    """
    Timeline indicator at bottom.
    """

    start_x = 45
    width = 210
    gap = 12

    for i in range(5):

        x0 = start_x + i * (width + gap)

        color = ACCENT if i == stage_index else GRID
        alpha = 0.95 if i == stage_index else 0.45

        ax.plot(
            [x0, x0 + width],
            [22, 22],
            color=color,
            linewidth=4,
            solid_capstyle="round",
            alpha=alpha
        )


def add_stage_header(stage_index):

    ax.text(
        600,
        630,
        STAGE_TITLES[stage_index],
        color=MUTED,
        fontsize=10,
        ha="center",
        va="center",
        fontweight="bold",
        alpha=0.95
    )

    ax.text(
        600,
        598,
        STAGE_HEADLINES[stage_index],
        color=TEXT,
        fontsize=18,
        ha="center",
        va="center",
        fontweight="bold"
    )

    ax.text(
        600,
        571,
        STAGE_DESCRIPTIONS[stage_index],
        color=MUTED,
        fontsize=10,
        ha="center",
        va="center"
    )


def add_footer(text, y=50, fontsize=10, color=MUTED, weight="normal"):

    ax.text(
        600,
        y,
        text,
        color=color,
        fontsize=fontsize,
        ha="center",
        va="center",
        fontweight=weight
    )


def pulse_radius(t, base=50, amplitude=15, period=2.0):

    return base + amplitude * (
        0.5 + 0.5 * np.sin(2 * np.pi * t / period)
    )


# ------------------------------------------------------------
# STAGE 1
# ONE PROBLEM → MANY DIRECTIONS
# ------------------------------------------------------------

def draw_stage_1(t):

    add_grid()
    add_stage_header(0)

    cx = 600
    cy = 335

    # --------------------------------------------------------
    # Central mathematical problem
    # --------------------------------------------------------

    glow = plt.Circle(
        (cx, cy),
        pulse_radius(t, 70, 20),
        color=ACCENT,
        alpha=0.055
    )
    ax.add_patch(glow)

    ax.add_patch(
        Circle(
            (cx, cy),
            110,
            fill=False,
            edgecolor=GRID,
            linewidth=1,
            linestyle=(0, (3, 8)),
            alpha=0.8
        )
    )

    ax.add_patch(
        Circle(
            (cx, cy),
            35,
            color=ACCENT,
            alpha=0.08
        )
    )

    ax.text(
        cx,
        cy + 8,
        "NAVIER–STOKES",
        color=TEXT,
        fontsize=22,
        fontweight="bold",
        ha="center",
        va="center"
    )

    ax.text(
        cx,
        cy - 24,
        "one mathematical question",
        color=MUTED,
        fontsize=10,
        ha="center"
    )

    # --------------------------------------------------------
    # Branches
    # --------------------------------------------------------

    targets = [
        (125, 545, "SMOOTHNESS"),
        (105, 440, "BLOW-UP"),
        (105, 225, "EULER"),
        (140, 105, "ENERGY"),
        (1075, 545, "FORCING"),
        (1100, 440, "VORTEX"),
        (1100, 225, "ESTIMATES"),
        (1060, 105, "FORMALIZE"),
    ]

    for i, (tx, ty, label) in enumerate(targets):

        side = -1 if tx < cx else 1

        # Control points for curved branches
        cp1x = cx + side * 130
        cp1y = cy

        cp2x = tx - side * 160
        cp2y = ty

        u = np.linspace(0, 1, 100)

        # Cubic Bezier
        x = (
            (1-u)**3 * cx
            + 3*(1-u)**2*u * cp1x
            + 3*(1-u)*u**2 * cp2x
            + u**3 * tx
        )

        y = (
            (1-u)**3 * cy
            + 3*(1-u)**2*u * cp1y
            + 3*(1-u)*u**2 * cp2y
            + u**3 * ty
        )

        ax.plot(
            x,
            y,
            color=GRID,
            linewidth=1,
            alpha=0.55
        )

        # Moving particle
        p = (t * 0.22 + i * 0.12) % 1

        idx = min(
            len(x) - 1,
            int(p * (len(x) - 1))
        )

        ax.scatter(
            x[idx],
            y[idx],
            s=22,
            color=ACCENT,
            alpha=0.85
        )

        # Research node
        ax.scatter(
            tx,
            ty,
            s=1100,
            color="#11151c",
            edgecolors=GRID,
            linewidths=1
        )

        ax.text(
            tx,
            ty,
            label,
            color=TEXT,
            fontsize=7.5,
            fontweight="bold",
            ha="center",
            va="center"
        )

    add_footer(
        "The strategy begins by refusing to search for one answer."
    )


# ------------------------------------------------------------
# STAGE 2
# DIFFERENT GROUPS → DIFFERENT ATTACKS
# ------------------------------------------------------------

def draw_stage_2(t):

    add_grid()
    add_stage_header(1)

    origin_x = 125
    origin_y = 335

    lane_y = [
        535,
        435,
        335,
        235,
        135
    ]

    lane_labels = [
        ("GLOBAL SMOOTHNESS", SMOOTH),
        ("FINITE-TIME BLOW-UP", BLOWUP),
        ("SIMPLIFIED PROBLEMS", SIMPLIFIED),
        ("ALTERNATIVE ESTIMATES", ESTIMATE),
        ("COMPUTATIONAL TESTS", COMPUTE)
    ]

    ax.text(
        95,
        origin_y + 5,
        "10,000",
        color=TEXT,
        fontsize=17,
        ha="right",
        fontweight="bold"
    )

    ax.text(
        95,
        origin_y - 18,
        "CONCURRENT\nAGENTS",
        color=MUTED,
        fontsize=8,
        ha="right",
        linespacing=1.1
    )

    for i, (y, (label, color)) in enumerate(
        zip(lane_y, lane_labels)
    ):

        # Curved path
        end_x = 1070

        u = np.linspace(0, 1, 250)

        if y == origin_y:

            x = origin_x + u * (end_x - origin_x)
            yy = np.full_like(x, origin_y)

        else:

            bend = 170

            control1_x = origin_x + 150
            control2_x = 330

            control1_y = origin_y
            control2_y = y

            x = (
                (1-u)**3 * origin_x
                + 3*(1-u)**2*u * control1_x
                + 3*(1-u)*u**2 * control2_x
                + u**3 * end_x
            )

            yy = (
                (1-u)**3 * origin_y
                + 3*(1-u)**2*u * control1_y
                + 3*(1-u)*u**2 * control2_y
                + u**3 * y
            )

        ax.plot(
            x,
            yy,
            color=color,
            linewidth=1.6,
            alpha=0.7
        )

        # Dotted moving particles
        for j in range(5):

            p = (
                t * 0.14
                + j * 0.2
                + i * 0.08
            ) % 1

            idx = int(
                p * (len(x) - 1)
            )

            ax.scatter(
                x[idx],
                yy[idx],
                s=12 + j * 3,
                color=color,
                alpha=0.75
            )

        ax.text(
            455,
            y + 6,
            label,
            color=color,
            fontsize=12,
            ha="left",
            fontweight="bold"
        )

    add_footer(
        "Some agents search for a proof. Others search for a counterexample.",
        y=66
    )


# ------------------------------------------------------------
# STAGE 3
# MASSIVE EXPLORATION
# ------------------------------------------------------------

def draw_stage_3(t):

    add_grid()
    add_stage_header(2)

    # --------------------------------------------------------
    # Research trajectory waves
    # --------------------------------------------------------

    lane_base = [
        510,
        410,
        310,
        210,
        110
    ]

    for lane_id, base_y in enumerate(lane_base):

        u = np.linspace(0, 1, 300)

        x = 30 + u * 1140

        y = (
            base_y
            + 35 * np.sin(
                2 * np.pi * (u * 1.4)
                + lane_id
            )
        )

        ax.plot(
            x,
            y,
            color=GRID,
            linewidth=1,
            alpha=0.38
        )

        # moving stream markers
        for j in range(8):

            p = (
                t * 0.18
                + j * 0.12
                + lane_id * 0.09
            ) % 1

            idx = int(
                p * (len(x) - 1)
            )

            color = (
                ACCENT
                if j == 0
                else TEXT
            )

            ax.scatter(
                x[idx],
                y[idx],
                s=6 + (j == 0) * 7,
                color=color,
                alpha=0.25 + 0.55 * (j == 0)
            )

    # --------------------------------------------------------
    # Research operation cards
    # --------------------------------------------------------

    cards = [
        (185, 70, "HYPOTHESIS"),
        (400, 70, "ESTIMATE"),
        (615, 70, "COUNTEREXAMPLE"),
        (830, 70, "REVISE")
    ]

    for i, (x, y, label) in enumerate(cards):

        box = FancyBboxPatch(
            (x, y),
            170,
            45,
            boxstyle="round,pad=0.02,rounding_size=8",
            facecolor="#11151c",
            edgecolor=GRID,
            linewidth=1
        )

        ax.add_patch(box)

        ax.text(
            x + 85,
            y + 22,
            label,
            color=TEXT,
            fontsize=9,
            fontweight="bold",
            ha="center",
            va="center"
        )

        # Pulsing operation indicator
        pulse = (
            0.35
            + 0.35 * np.sin(
                t * 3 + i
            )
        )

        ax.scatter(
            x + 18,
            y + 22,
            s=22,
            color=ACCENT,
            alpha=pulse
        )

    # --------------------------------------------------------
    # Particle field
    # --------------------------------------------------------

    n = 320

    # deterministic field
    rng_local = np.random.default_rng(100)

    px = rng_local.uniform(50, 1150, n)
    py = rng_local.uniform(95, 550, n)

    # subtle motion
    px2 = px + 25 * np.sin(
        t * 0.9
        + py * 0.02
    )

    py2 = py + 18 * np.cos(
        t * 0.75
        + px * 0.01
    )

    alpha = (
        0.12
        + 0.32
        * (
            0.5
            + 0.5
            * np.sin(
                t * 1.7
                + px * 0.015
            )
        )
    )

    ax.scatter(
        px2,
        py2,
        s=5,
        color=TEXT,
        alpha=alpha
    )

    # Selected promising particles
    idx = np.array(
        [8, 38, 91, 117, 164, 215, 270]
    )

    ax.scatter(
        px2[idx],
        py2[idx],
        s=20,
        color=ACCENT,
        alpha=0.85
    )

    # --------------------------------------------------------
    # Text
    # --------------------------------------------------------

    ax.text(
        600,
        600,
        "HYPOTHESIZE  →  CALCULATE  →  TEST  →  REJECT  →  REVISE",
        color=MUTED,
        fontsize=10,
        ha="center",
        va="center",
        fontweight="bold"
    )

    ax.text(
        600,
        55,
        "2.7 MILLION MESSAGES   ·   ~130 BILLION OUTPUT TOKENS",
        color=TEXT,
        fontsize=13,
        ha="center",
        va="center",
        fontweight="bold"
    )


# ------------------------------------------------------------
# STAGE 4
# COMMUNICATION BETWEEN GROUPS
# ------------------------------------------------------------

def draw_stage_4(t):

    add_grid()
    add_stage_header(3)

    cx = 600
    cy = 330

    # --------------------------------------------------------
    # Network nodes
    # --------------------------------------------------------

    nodes = np.array([
        [140, 510],
        [390, 405],
        [235, 170],
        [610, 265],
        [1000, 490],
        [850, 120],
        [940, 320]
    ])

    # Connections
    edges = [
        (0,1),
        (1,2),
        (2,3),
        (3,4),
        (4,6),
        (6,1),
        (1,5),
        (2,5),
        (0,4),
        (3,6)
    ]

    for a, b in edges:

        x1, y1 = nodes[a]
        x2, y2 = nodes[b]

        ax.plot(
            [x1, x2],
            [y1, y2],
            color=GRID,
            linewidth=1,
            alpha=0.4
        )

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------

    for i, (x, y) in enumerate(nodes):

        pulse = (
            0.35
            + 0.4 * (
                0.5
                + 0.5 * np.sin(
                    t * 3 + i
                )
            )
        )

        ax.scatter(
            x,
            y,
            s=80,
            color=ACCENT if i == 3 else TEXT,
            alpha=pulse,
            zorder=4
        )

    # --------------------------------------------------------
    # Moving information packets
    # --------------------------------------------------------

    packet_routes = [
        (0, 1),
        (2, 3),
        (1, 6)
    ]

    for route_id, (a, b) in enumerate(packet_routes):

        x1, y1 = nodes[a]
        x2, y2 = nodes[b]

        p = (
            t * 0.35
            + route_id * 0.33
        ) % 1

        # ease in/out
        pe = 0.5 - 0.5 * np.cos(
            np.pi * p
        )

        x = x1 + (x2 - x1) * pe
        y = y1 + (y2 - y1) * pe

        ax.scatter(
            x,
            y,
            s=55,
            color=ACCENT,
            alpha=0.95,
            zorder=10
        )

    # --------------------------------------------------------
    # Central shared discovery
    # --------------------------------------------------------

    glow_radius = (
        55
        + 12 * np.sin(t * 3)
    )

    ax.add_patch(
        Circle(
            (cx, cy),
            glow_radius,
            color=ACCENT,
            alpha=0.035
        )
    )

    ax.add_patch(
        Circle(
            (cx, cy),
            12,
            color=ACCENT,
            alpha=0.95
        )
    )

    ax.text(
        cx,
        cy + 62,
        "SHARED DISCOVERY",
        color=TEXT,
        fontsize=15,
        ha="center",
        fontweight="bold"
    )

    ax.text(
        cx,
        cy + 35,
        "a clue from one group",
        color=MUTED,
        fontsize=10,
        ha="center"
    )

    ax.text(
        cx,
        cy + 18,
        "becomes another group's",
        color=MUTED,
        fontsize=10,
        ha="center"
    )

    ax.text(
        cx,
        cy + 1,
        "starting point",
        color=MUTED,
        fontsize=10,
        ha="center"
    )

    add_footer(
        "Intermediate results can move between groups instead of dying inside isolated conversations.",
        y=65
    )

    ax.text(
        600,
        98,
        "SEARCH BECOMES COLLECTIVE",
        color=TEXT,
        fontsize=15,
        ha="center",
        fontweight="bold"
    )


# ------------------------------------------------------------
# STAGE 5
# CONVERGENCE
# ------------------------------------------------------------

def draw_stage_5(t):

    add_grid()
    add_stage_header(4)

    cx = 600
    cy = 335

    # --------------------------------------------------------
    # Shrinking search space
    # --------------------------------------------------------

    progress = 0.5 + 0.5 * np.sin(
        2 * np.pi * t / 5
    )

    rings = [
        (440, 220),
        (345, 172),
        (250, 125),
        (165, 82)
    ]

    for i, (rx, ry) in enumerate(rings):

        # The inner ring becomes dominant
        alpha = (
            0.15 + 0.06 * i
        )

        if i == len(rings) - 1:
            alpha = 0.45

        ellipse = Ellipse(
            (cx, cy),
            2 * rx,
            2 * ry,
            fill=False,
            edgecolor=ACCENT if i == 3 else GRID,
            linewidth=2 if i == 3 else 1,
            alpha=alpha
        )

        ax.add_patch(ellipse)

    # --------------------------------------------------------
    # Orbiting surviving research paths
    # --------------------------------------------------------

    n_paths = 80

    for i in range(n_paths):

        phase = (
            2 * np.pi * i / n_paths
        )

        radius = (
            180
            + 180 * (i / n_paths)
        )

        angle = (
            phase
            + t * 0.75
            + i * 0.01
        )

        x = (
            cx
            + np.cos(angle)
            * radius
        )

        y = (
            cy
            + np.sin(angle)
            * radius
            * 0.48
        )

        # gradually fade outer paths
        path_alpha = (
            0.08
            + 0.35
            * (
                1
                - i / n_paths
            )
        )

        ax.scatter(
            x,
            y,
            s=8,
            color=TEXT,
            alpha=path_alpha
        )

    # --------------------------------------------------------
    # Central promising structure
    # --------------------------------------------------------

    glow = (
        55
        + 20 * np.sin(
            t * 2.4
        )
    )

    ax.add_patch(
        Circle(
            (cx, cy),
            glow,
            color=ACCENT,
            alpha=0.06
        )
    )

    ax.add_patch(
        Circle(
            (cx, cy),
            30,
            color=ACCENT,
            alpha=0.08
        )
    )

    ax.scatter(
        cx,
        cy,
        s=150,
        color=ACCENT,
        alpha=0.95
    )

    ax.text(
        cx,
        cy + 72,
        "PROMISING STRUCTURE",
        color=TEXT,
        fontsize=17,
        ha="center",
        fontweight="bold"
    )

    ax.text(
        cx,
        cy + 43,
        "useful ideas are consolidated",
        color=MUTED,
        fontsize=10,
        ha="center"
    )

    ax.text(
        cx,
        cy + 25,
        "and fed into subsequent research",
        color=MUTED,
        fontsize=10,
        ha="center"
    )

    # --------------------------------------------------------
    # Codex label
    # --------------------------------------------------------

    codex_box = FancyBboxPatch(
        (80, 80),
        220,
        60,
        boxstyle="round,pad=0.02,rounding_size=10",
        facecolor="#10141b",
        edgecolor=GRID,
        linewidth=1
    )

    ax.add_patch(codex_box)

    ax.text(
        190,
        115,
        "CODEX",
        color=ACCENT,
        fontsize=14,
        fontweight="bold",
        ha="center"
    )

    ax.text(
        190,
        94,
        "consolidate useful ideas",
        color=MUTED,
        fontsize=9,
        ha="center"
    )

    # --------------------------------------------------------
    # Bottom statement
    # --------------------------------------------------------

    ax.text(
        600,
        82,
        "THOUSANDS OF PATHS  →  FEWER PROMISING PATHS  →  FOCUSED ATTACK",
        color=TEXT,
        fontsize=13,
        ha="center",
        fontweight="bold"
    )


# ------------------------------------------------------------
# MASTER DRAW FUNCTION
# ------------------------------------------------------------

def draw_frame(frame):

    # Time in seconds
    t = frame / FPS

    # stage
    stage = min(
        4,
        int(t // 5)
    )

    # local stage time
    local_t = t - stage * 5

    clear_axis()

    # Background
    ax.set_facecolor(PANEL)

    # Draw stage
    if stage == 0:
        draw_stage_1(local_t)

    elif stage == 1:
        draw_stage_2(local_t)

    elif stage == 2:
        draw_stage_3(local_t)

    elif stage == 3:
        draw_stage_4(local_t)

    elif stage == 4:
        draw_stage_5(local_t)

    # --------------------------------------------------------
    # Stage timeline
    # --------------------------------------------------------

    add_stage_bar(stage)

    # --------------------------------------------------------
    # Outer cinematic border
    # --------------------------------------------------------

    ax.plot(
        [10, 1190],
        [650, 650],
        color=GRID,
        linewidth=.5,
        alpha=.4
    )

    ax.plot(
        [10, 1190],
        [28, 28],
        color=GRID,
        linewidth=.5,
        alpha=.4
    )

    # --------------------------------------------------------
    # Time indicator
    # --------------------------------------------------------

    ax.text(
        1150,
        645,
        f"{t:05.1f}s",
        color=MUTED,
        fontsize=8,
        ha="right"
    )

    # --------------------------------------------------------
    # Top-left identifier
    # --------------------------------------------------------

    ax.text(
        45,
        645,
        "NAVIER–STOKES · PART 2",
        color=MUTED,
        fontsize=8,
        ha="left",
        fontweight="bold",
        alpha=.8
    )


# ------------------------------------------------------------
# INITIAL FRAME
# ------------------------------------------------------------

draw_frame(0)


# ------------------------------------------------------------
# ANIMATION
# ------------------------------------------------------------

anim = FuncAnimation(
    fig,
    draw_frame,
    frames=TOTAL_FRAMES,
    interval=1000 / FPS,
    blit=False,
    repeat=True
)


# ------------------------------------------------------------
# EXPORT WEBM
# ------------------------------------------------------------

print("Rendering...")
print(f"Duration: {DURATION}s")
print(f"FPS:      {FPS}")
print(f"Frames:   {TOTAL_FRAMES}")
print(f"Output:   {OUTPUT.resolve()}")


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


anim.save(
    OUTPUT,
    writer=writer,
    dpi=DPI
)


# ------------------------------------------------------------
# CLEANUP
# ------------------------------------------------------------

plt.close(fig)

print()
print("Done.")
print(f"Saved to: {OUTPUT.resolve()}")