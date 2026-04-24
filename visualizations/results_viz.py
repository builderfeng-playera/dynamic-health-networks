"""
Paper results visualizations (light theme):
  Figure 1: State-conditional networks (4 panels)
  Figure 2: Hub centrality comparison
  Figure 3: Edge transition heatmap
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from matplotlib.colors import TwoSlopeNorm
from itertools import combinations
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "paper", "figures")
os.makedirs(OUT, exist_ok=True)

with open(os.path.join(os.path.dirname(__file__), "..", "analysis", "network_results.json")) as f:
    results = json.load(f)

NODES = ["A", "B", "C", "D", "E", "F"]
NODE_FULL = {
    "A": "Sleep", "B": "Activity", "C": "Recovery",
    "D": "SpO\u2082/Breath", "E": "Cycle", "F": "Tennis"
}
NODE_COLORS = {
    "A": "#388E3C", "B": "#1565C0", "C": "#7B1FA2",
    "D": "#00897B", "E": "#C2185B", "F": "#E64A19"
}

POSITIONS = {
    "A": (0.0, 1.0),
    "B": (0.87, 0.5),
    "C": (0.87, -0.5),
    "D": (0.0, -1.0),
    "E": (-0.87, -0.5),
    "F": (-0.87, 0.5),
}

STATES = ["baseline", "luteal", "post_tennis"]
STATE_LABELS = {
    "baseline": "Baseline\n(Follicular)",
    "luteal": "Luteal\nPhase",
    "post_tennis": "Post-Tennis\nMatch",
}
STATE_BG = {
    "baseline": "#E8F5E9",
    "luteal": "#FCE4EC",
    "post_tennis": "#FFF3E0",
}

BG = "#FAFAFA"
TEXT = "#222222"
TEXT_LIGHT = "#666666"
GRID = "#DDDDDD"

EDGE_POS = "#2E7D32"
EDGE_NEG = "#C62828"
EDGE_NONE = "#CCCCCC"

# =========================================================================
# FIGURE 1: State-conditional networks (4 panels)
# =========================================================================

fig, axes = plt.subplots(1, 3, figsize=(21, 8), facecolor=BG)
fig.suptitle("State-Conditional Health Networks", fontsize=20, fontweight="bold",
             color=TEXT, y=1.02)
fig.text(0.5, 0.97,
         "Edge thickness \u221d |r|.   Green = positive.   Red = negative.   Gray dashed = not significant.",
         ha="center", fontsize=10, color=TEXT_LIGHT)

for idx, (state, ax) in enumerate(zip(STATES, axes.flat)):
    ax.set_facecolor(STATE_BG[state])
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.55, 1.55)
    ax.set_aspect("equal")
    ax.axis("off")

    net = results[state]
    C = np.array(net["C"])
    sig = np.array(net["significant"])

    # State label
    ax.text(0, 1.45, STATE_LABELS[state], ha="center", va="center",
            fontsize=14, fontweight="bold", color=TEXT,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor="#999999", linewidth=0.8))

    # Metrics annotation
    density = net["density"]
    hub = net["dominant_hub"].split(" ")[0] if net["n_significant_edges"] > 0 else "\u2014"
    frob = net.get("frobenius_divergence", 0.0)
    if state != "baseline":
        metrics_text = f"\u03c1 = {density:.2f}     Hub: {hub}     \u0394C = {frob:.2f}"
    else:
        metrics_text = f"\u03c1 = {density:.2f}     Hub: {hub}"
    ax.text(0, -1.45, metrics_text, ha="center", va="center",
            fontsize=10, color=TEXT_LIGHT, fontstyle="italic")

    # Draw edges
    for i, j in combinations(range(6), 2):
        x1, y1 = POSITIONS[NODES[i]]
        x2, y2 = POSITIONS[NODES[j]]

        r_val = C[i][j]
        is_sig = sig[i][j] or sig[j][i]

        if is_sig:
            width = max(2.0, min(9, abs(r_val) * 12))
            color = EDGE_POS if r_val > 0 else EDGE_NEG
            alpha = min(1.0, 0.5 + abs(r_val) * 0.5)
            linestyle = "-"
            zorder = 2
        else:
            width = 0.6
            color = EDGE_NONE
            alpha = 0.4
            linestyle = "--"
            zorder = 1

        ax.plot([x1, x2], [y1, y2], color=color, linewidth=width,
                alpha=alpha, linestyle=linestyle, zorder=zorder, solid_capstyle="round")

        if is_sig:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            dx, dy = x2 - x1, y2 - y1
            length = np.sqrt(dx**2 + dy**2)
            nx, ny = -dy / length * 0.14, dx / length * 0.14
            ax.text(mx + nx, my + ny, f"{r_val:+.2f}", fontsize=9,
                    color=color, ha="center", va="center", fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                              edgecolor=color, linewidth=0.5, alpha=0.9))

    # Draw nodes
    hub_nodes = []
    if net["n_significant_edges"] > 0:
        centralities = net["hub_centrality"]
        max_cent = max(centralities.values())
        hub_nodes = [k.split(" ")[0] for k, v in centralities.items() if v == max_cent]

    for node in NODES:
        x, y = POSITIONS[node]
        is_hub = node in hub_nodes
        node_size = 0.22 if is_hub else 0.17
        edge_width = 3.5 if is_hub else 1.5
        edge_color = "#FFD600" if is_hub else "#888888"

        circle = plt.Circle((x, y), node_size, facecolor=NODE_COLORS[node],
                             edgecolor=edge_color, linewidth=edge_width, zorder=10)
        ax.add_patch(circle)
        ax.text(x, y + 0.02, node, ha="center", va="center", fontsize=15,
                fontweight="bold", color="white", zorder=11)
        ax.text(x, y - 0.35, NODE_FULL[node], ha="center", va="center",
                fontsize=9, color=TEXT, fontweight="medium", zorder=11)

plt.tight_layout(rect=[0, 0, 1, 0.94])
fig.savefig(os.path.join(OUT, "fig1_state_networks.png"), dpi=200, bbox_inches="tight",
            facecolor=BG)
print("Saved: fig1_state_networks.png")
plt.close()

# =========================================================================
# FIGURE 2: Hub centrality comparison
# =========================================================================

fig, ax = plt.subplots(figsize=(13, 6), facecolor=BG)
ax.set_facecolor(BG)

bar_width = 0.25
x = np.arange(len(NODES))
state_bar_colors = ["#66BB6A", "#F48FB1", "#FFB74D"]

for s_idx, state in enumerate(STATES):
    centralities = results[state]["hub_centrality"]
    values = []
    for node in NODES:
        key = [k for k in centralities if k.startswith(node)][0]
        values.append(centralities[key])

    bars = ax.bar(x + s_idx * bar_width, values, bar_width,
                  label=STATE_LABELS[state].replace("\n", " "),
                  color=state_bar_colors[s_idx],
                  edgecolor="white", linewidth=0.8)

    max_val = max(values)
    if max_val > 0:
        for i, v in enumerate(values):
            if v == max_val:
                ax.text(x[i] + s_idx * bar_width, v + 0.02, "\u2605",
                        color="#E65100", fontsize=16, ha="center", va="bottom", zorder=10)

ax.set_xticks(x + bar_width * 1.0)
ax.set_xticklabels([f"{n}\n{NODE_FULL[n]}" for n in NODES], fontsize=11, color=TEXT)
ax.set_ylabel("Hub Centrality (degree / 5)", fontsize=12, color=TEXT)
ax.set_title("Hub Rotation Across Body States", fontsize=17, fontweight="bold", color=TEXT)
ax.set_ylim(0, 0.82)
ax.tick_params(colors=TEXT)
ax.spines["bottom"].set_color(GRID)
ax.spines["left"].set_color(GRID)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.yaxis.grid(True, color=GRID, linewidth=0.5, alpha=0.7)
ax.set_axisbelow(True)

handles = [mpatches.Patch(facecolor=state_bar_colors[i], edgecolor="white",
                          label=STATE_LABELS[s].replace("\n", " "))
           for i, s in enumerate(STATES)]
ax.legend(handles=handles, loc="upper right", fontsize=10,
          facecolor="white", edgecolor=GRID, labelcolor=TEXT)

ax.text(0.5, -0.12, "\u2605 = dominant hub in that state",
        transform=ax.transAxes, ha="center", fontsize=11, color="#E65100", fontweight="bold")

plt.tight_layout()
fig.savefig(os.path.join(OUT, "fig2_hub_rotation.png"), dpi=200, bbox_inches="tight",
            facecolor=BG)
print("Saved: fig2_hub_rotation.png")
plt.close()

# =========================================================================
# FIGURE 3: Edge transition heatmap
# =========================================================================

edge_keys = [
    ("A \u2194 B", "Sleep \u2013 Activity", 0, 1),
    ("A \u2194 C", "Sleep \u2013 Recovery", 0, 2),
    ("A \u2194 F", "Sleep \u2013 Tennis", 0, 5),
    ("B \u2194 F", "Activity \u2013 Tennis", 1, 5),
    ("C \u2194 E", "Recovery \u2013 Cycle", 2, 4),
    ("C \u2194 F", "Recovery \u2013 Tennis", 2, 5),
    ("D \u2194 E", "SpO\u2082 \u2013 Cycle", 3, 4),
    ("E \u2194 F", "Cycle \u2013 Tennis", 4, 5),
]

fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
ax.set_facecolor(BG)

heatmap_data = np.zeros((len(edge_keys), len(STATES)))
sig_mask = np.zeros_like(heatmap_data, dtype=bool)

for col, state in enumerate(STATES):
    C = np.array(results[state]["C"])
    sig_arr = np.array(results[state]["significant"])
    for row, (label, desc, i, j) in enumerate(edge_keys):
        heatmap_data[row, col] = C[i][j]
        sig_mask[row, col] = sig_arr[i][j] or sig_arr[j][i]

norm = TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1)
im = ax.imshow(heatmap_data, cmap="RdYlGn", norm=norm, aspect="auto")

for row in range(len(edge_keys)):
    for col in range(len(STATES)):
        val = heatmap_data[row, col]
        is_sig = sig_mask[row, col]
        text = f"{val:+.2f}" if not np.isnan(val) else "\u2014"
        if is_sig:
            text += "\n\u2605"
        text_color = "white" if abs(val) > 0.55 else "#222222"
        weight = "bold" if is_sig else "normal"
        ax.text(col, row, text, ha="center", va="center",
                fontsize=10, color=text_color, fontweight=weight)

ax.set_xticks(range(len(STATES)))
ax.set_xticklabels([STATE_LABELS[s].replace("\n", " ") for s in STATES],
                   fontsize=11, color=TEXT)
ax.set_yticks(range(len(edge_keys)))
ax.set_yticklabels([f"{e[0]}  ({e[1]})" for e in edge_keys],
                   fontsize=10, color=TEXT)

ax.set_title("Edge Correlation Values Across Body States", fontsize=17,
             fontweight="bold", color=TEXT, pad=15)

cbar = plt.colorbar(im, ax=ax, shrink=0.8, pad=0.02)
cbar.set_label("Pearson r", fontsize=11, color=TEXT)
cbar.ax.tick_params(colors=TEXT)

ax.text(0.5, -0.08,
        "\u2605 = statistically significant (bootstrap p < 0.05).   Green = positive.   Red = negative.",
        transform=ax.transAxes, ha="center", fontsize=9, color=TEXT_LIGHT)

# Sign reversal highlight
rect = Rectangle((-0.5, -0.5), 2, 1, linewidth=2.5, edgecolor="#E65100",
                 facecolor="none", linestyle="--", zorder=10)
ax.add_patch(rect)
ax.text(0.5, -0.72, "sign reversal", ha="center", va="top",
        fontsize=9, color="#E65100", fontweight="bold")

plt.tight_layout()
fig.savefig(os.path.join(OUT, "fig3_edge_heatmap.png"), dpi=200, bbox_inches="tight",
            facecolor=BG)
print("Saved: fig3_edge_heatmap.png")
plt.close()

print("\nAll figures saved to paper/figures/")
