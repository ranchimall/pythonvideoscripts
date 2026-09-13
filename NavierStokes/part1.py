import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from pathlib import Path

# ============================================================
# SETTINGS
# ============================================================

OUTPUT_FILE = Path("euler_first_strategy_20s.webm")

FPS = 20
DURATION = 20
TOTAL_FRAMES = FPS * DURATION

# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(
    figsize=(12.8, 7.2),
    dpi=150
)

ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-0.72, 0.72)
ax.set_aspect("equal")
ax.axis("off")


# ============================================================
# TEXT ELEMENTS
# ============================================================

title = fig.text(
    0.5, 0.90, "",
    ha="center",
    fontsize=20,
    weight="bold"
)

subtitle = fig.text(
    0.5, 0.845, "",
    ha="center",
    fontsize=13
)

equation = fig.text(
    0.5, 0.07, "",
    ha="center",
    fontsize=15,
    family="monospace"
)

stage_label = fig.text(
    0.04, 0.97, "",
    ha="left",
    fontsize=11,
    weight="bold"
)

bottom_label = fig.text(
    0.5, 0.15, "",
    ha="center",
    fontsize=15,
    weight="bold"
)


# ============================================================
# BACKGROUND VORTEX RINGS
# ============================================================

theta = np.linspace(0, 2 * np.pi, 300)

for radius in [0.28, 0.45, 0.62, 0.79]:

    ax.plot(
        radius * np.cos(theta),
        0.72 * radius * np.sin(theta),
        linewidth=1,
        alpha=0.25
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
            "∂u/∂t + (u·∇)u = −(1/ρ)∇p + ν∇²u + f",

        "label":
            "Full Navier–Stokes"
    },

    {
        "heading": "SET ν = 0",

        "headline":
            "Remove viscosity and study the simpler Euler equations.",

        "equation":
            "ν = 0   →   ∂u/∂t + (u·∇)u = −(1/ρ)∇p + f",

        "label":
            "Viscosity removed"
    },

    {
        "heading": "ASK WHETHER SMOOTHNESS CAN FAIL",

        "headline":
            "Can a smooth flow develop unbounded velocity in finite time?",

        "equation":
            "smooth at t = 0   →   |u| → ∞ at finite T ?",

        "label":
            "Search for finite-time blow-up"
    },

    {
        "heading":
            "USE THE SIMPLER PROBLEM TO REVEAL STRUCTURE",

        "headline":
            "Explore Euler for a mechanism guiding the harder Navier–Stokes search.",

        "equation":
            "Euler clue   →   candidate mechanism   →   Navier–Stokes",

        "label":
            "≈100 agents  •  ≈50 hours"
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

    # Time within current stage: 0 → 1
    local_time = (
        time - stage * 5
    ) / 5

    # --------------------------------------------------------
    # UPDATE TEXT
    # --------------------------------------------------------

    current = stages[stage]

    stage_label.set_text(
        f"STEP 1  •  {stage + 1}/4"
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

    # VP9 codec → WebM
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