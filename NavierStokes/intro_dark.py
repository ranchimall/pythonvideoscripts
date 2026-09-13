import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from PIL import Image
import os

# ============================================================
# OPENAI x NAVIER-STOKES
# Seamless-loop, dark-background version (light-colored animation)
# ============================================================

# -----------------------------
# SETTINGS
# -----------------------------
FPS = 24
DURATION = 8                 # length of ONE loop cycle, in seconds
TOTAL_FRAMES = FPS * DURATION

OUTPUT = "openai_navier_stokes_loop_dark.webm"

# Resolve the logo path relative to THIS script's folder, not the
# current working directory, so it's found no matter where you run
# the script from.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_FILE = os.path.join(SCRIPT_DIR, "openai_white.png")

# 16:9
FIG_W = 12.8
FIG_H = 7.2

# Particle count
N_PARTICLES = 1800

# -----------------------------
# COLORS (dark background, light-colored animation - inverse of the
# light version. Same brightness contrast, just flipped.)
# -----------------------------
BG = "#0b0e14"                       # deep near-black navy

PARTICLE_COLOR = (0.82, 0.90, 0.98)  # pale ice blue
FLOW_COLOR = (0.55, 0.68, 0.82)      # soft steel blue
CORE_COLOR = (0.92, 0.96, 1.0)       # near-white, for contrast at the core

# ============================================================
# FIGURE
# ============================================================

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=100)

fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")

plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

# ============================================================
# LOAD OPENAI LOGO
# ============================================================

logo_artist = None

if os.path.exists(LOGO_FILE):
    logo_img = Image.open(LOGO_FILE).convert("RGBA")
    logo_img.thumbnail((420, 420), Image.Resampling.LANCZOS)
    logo_array = np.asarray(logo_img)

    logo_artist = ax.imshow(
        logo_array,
        extent=(0.43, 0.57, 0.43, 0.57),
        alpha=0,
        zorder=20
    )
    print(f"Logo loaded from: {LOGO_FILE}")
else:
    print(f"WARNING: logo not found at {LOGO_FILE} - continuing without it.")

# ============================================================
# PARTICLE INITIALIZATION
# ============================================================

rng = np.random.default_rng(42)

angles = rng.uniform(0, 2 * np.pi, N_PARTICLES)
radii = np.sqrt(rng.uniform(0, 1, N_PARTICLES)) * 0.47

initial_x = 0.5 + np.cos(angles) * radii
initial_y = 0.5 + np.sin(angles) * radii * 0.62

# Distance from center / base angle, precomputed once
dx0 = initial_x - 0.5
dy0 = (initial_y - 0.5) / 0.62
r0 = np.sqrt(dx0 ** 2 + dy0 ** 2)
base_angle = np.arctan2(dy0, dx0)

# Per-particle random spin-rate MULTIPLIER, then rounded to a whole
# number of full turns per loop below -> guarantees every particle
# lands back on its exact starting angle after TOTAL_FRAMES frames,
# which is what makes the rotation loop seamlessly.
speed_jitter = rng.uniform(0.75, 1.25, N_PARTICLES)

# Inner particles spin faster than outer ones (same idea as before),
# but expressed as a whole number of turns per loop.
r_norm = np.clip(r0 / 0.48, 0, 1)
raw_turns = (1.0 + 5.0 * (1 - r_norm)) * speed_jitter
n_turns = np.maximum(1, np.round(raw_turns)).astype(int)

sizes = rng.uniform(1.0, 4.0, N_PARTICLES)

particles = ax.scatter(
    initial_x, initial_y,
    s=sizes,
    c=[PARTICLE_COLOR],
    alpha=0,
    linewidths=0,
    zorder=5
)

# ============================================================
# FLOW LINES
# ============================================================

FLOW_COUNT = 36
FLOW_POINTS = 150
FLOW_TURNS = 2  # whole number of turns per loop -> seamless

flow_lines = []
for i in range(FLOW_COUNT):
    line, = ax.plot([], [], linewidth=0.55, color=FLOW_COLOR, alpha=0, zorder=2)
    flow_lines.append(line)

# ============================================================
# CORE
# ============================================================

core_scatter = ax.scatter(
    [0.5], [0.5],
    s=[0],
    c=[CORE_COLOR],
    alpha=0,
    linewidths=0,
    zorder=10
)

# ============================================================
# HELPERS
# ============================================================

def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


# ============================================================
# ANIMATION
# ============================================================

def update(frame):

    # ------------------------------------------------------------
    # LOOP-SAFE TIME BASE
    #
    # frac goes 0 -> just-under-1 across the clip, and the very
    # next frame after the last one IS frame 0 again, so using
    # `frame / TOTAL_FRAMES` (not TOTAL_FRAMES - 1) keeps the step
    # between last-frame and first-frame the same size as every
    # other step -> no visible jump when the video repeats.
    #
    # `phase` is a smooth breathing envelope: 0 -> 1 -> 0 across
    # the clip, with zero velocity at both ends, so anything driven
    # by `phase` automatically loops with no seam.
    # ------------------------------------------------------------

    frac = frame / TOTAL_FRAMES
    phase = (1 - np.cos(2 * np.pi * frac)) / 2  # 0 -> 1 -> 0, smooth

    ax.set_facecolor(BG)

    # ========================================================
    # OPENAI LOGO
    # Tied to the same breathing envelope: it grows in as the
    # vortex intensifies and recedes as it relaxes, every cycle.
    # ========================================================

    if logo_artist is not None:
        logo_alpha = 0.9 * smoothstep(phase * 1.3)
        logo_artist.set_alpha(logo_alpha)

        scale = 0.92 + 0.10 * phase
        half = 0.075 * scale
        logo_artist.set_extent((0.5 - half, 0.5 + half, 0.5 - half, 0.5 + half))

    # ========================================================
    # VORTEX / CONVERGENCE STRENGTH (both = breathing envelope)
    # ========================================================

    vortex = phase
    convergence = phase

    # ========================================================
    # PARTICLE POSITIONS
    # ========================================================

    r = r0
    # Constant-rate spin: a whole number of turns per particle,
    # so angle(frame=TOTAL_FRAMES) == angle(frame=0) exactly.
    angle = base_angle + 2 * np.pi * n_turns * frac

    # Extra spiral twist that breathes in and out with `phase`
    # (function of phase only -> loop safe, no accumulation).
    spiral_strength = vortex * (0.35 + 1.6 * (1 - r_norm))
    angle = angle + spiral_strength * (1 - r_norm)

    collapse_strength = 0.02 + 0.86 * convergence
    radius = r * (1 - collapse_strength)

    elongation = 1 - 0.28 * vortex * np.clip(1 - r / 0.48, 0, 1)

    x = 0.5 + np.cos(angle) * radius
    y = 0.5 + np.sin(angle) * radius * 0.62 * elongation

    # --------------------------------------------------------
    # APPEARANCE
    # --------------------------------------------------------

    alpha = 0.62  # always fully "emerged" - no one-time fade in/out
    core_weight = np.exp(-(r / 0.22) ** 2)
    alpha *= (0.72 + 0.28 * core_weight)

    particles.set_offsets(np.column_stack((x, y)))
    particles.set_alpha(alpha)

    # ========================================================
    # FLOW LINES
    # ========================================================

    for k, line in enumerate(flow_lines):
        base = k / FLOW_COUNT * 2 * np.pi
        rr = np.linspace(0.035, 0.47, FLOW_POINTS)

        twist = 0.45 + 2.7 * vortex * (1 - rr / 0.47) ** 1.7

        # Whole number of turns over the loop (FLOW_TURNS) keeps
        # this seamless too.
        ang = base + rr * twist + 2 * np.pi * FLOW_TURNS * frac

        rr2 = rr * (1 - 0.58 * convergence * (1 - rr / 0.47))

        xx = 0.5 + np.cos(ang) * rr2
        yy = 0.5 + np.sin(ang) * rr2 * 0.62

        line_alpha = (0.05 + 0.14 * vortex)

        line.set_data(xx, yy)
        line.set_alpha(line_alpha)

    # ========================================================
    # SINGULAR CORE
    # ========================================================

    core_size = 4 + 130 * vortex ** 3
    core_alpha = 0.05 + 0.35 * vortex ** 2

    # This pulse already loops seamlessly: sin(pi*18*frac) completes
    # exactly 9 full periods between frac=0 and frac=1.
    pulse = np.sin(frac * np.pi * 18) * 0.5 + 0.5
    pulse_size = 3 + pulse * vortex * 30

    core_scatter.set_sizes([core_size + pulse_size])
    core_scatter.set_alpha(core_alpha)

    # ========================================================
    # RETURN ARTISTS
    # ========================================================

    artists = [particles, core_scatter]
    artists.extend(flow_lines)
    if logo_artist is not None:
        artists.append(logo_artist)

    return artists


# ============================================================
# CREATE ANIMATION
# ============================================================

anim = FuncAnimation(
    fig,
    update,
    frames=TOTAL_FRAMES,
    interval=1000 / FPS,
    blit=True
)

# ============================================================
# SAVE
# ============================================================

print("Rendering animation...")

writer = FFMpegWriter(
    fps=FPS,
    codec="libvpx-vp9",
    bitrate=4000,
    extra_args=[
        "-pix_fmt", "yuv420p",
        "-deadline", "good",
        "-cpu-used", "2",
        "-crf", "24",
        "-b:v", "0"
    ]
)

anim.save(OUTPUT, writer=writer, dpi=150)

plt.close(fig)

print()
print("Done.")
print(f"Saved to: {OUTPUT}")
print("This clip is a seamless loop - set your player/video tag to loop it.")
