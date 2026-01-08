# === Iowa FSM — PANEL of 20 donuts with bottom horizontal legend ===
# Output: iowa_fsm_donuts_panel.png (800 dpi)

import re, difflib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib import colors as mcolors
from google.colab import files

# -------- Top-20 order --------
COUNTY_ORDER = [
    "Louisa","Black Hawk","Des Moines","Henry","Muscatine",
    "Washington","Monona","Fremont","Linn","Polk",
    "Van Buren","Greene","Clinton","Scott","Jefferson",
    "Marshall","Butler","Bremer","Johnson","Jasper"
]

# ======== knobs ========
PANEL_ROWS, PANEL_COLS = 5, 4
SAVE_DPI      = 800
CELL_INCH     = 2.8
WEDGE_WIDTH   = 0.50
LABEL_MIN     = 2.5
PCT_MIN, PCT_MAX = 7.5, 11.5
NAME_FS       = 11
EDGE_LW       = 1.3
# =======================

# -------- Upload & read --------
print("➡️ Upload your Excel file")
up = files.upload()
fname = next(iter(up.keys()))

xls = pd.ExcelFile(fname)
sheet_to_use = "LGBM_FSM" if "LGBM_FSM" in xls.sheet_names else xls.sheet_names[0]
df = pd.read_excel(fname, sheet_name=sheet_to_use)
df.columns = [str(c).strip() for c in df.columns]

# -------- Column detection --------
norm = lambda s: re.sub(r'[^a-z0-9]+','', str(s).lower().strip())
def find_col(cands):
    m = {norm(c): c for c in df.columns}
    for cand in cands:
        if norm(cand) in m:
            return m[norm(cand)]
    raise ValueError(f"Missing column from {cands}")

county = find_col(["NAME_2","County","NAME"])

pct_cols = {
    "vl": find_col(["VL_Perc"]),
    "l" : find_col(["L_Perc"]),
    "m" : find_col(["M_Perc"]),
    "h" : find_col(["H_Perc"]),
    "vh": find_col(["VH_Perc"]),
}

for c in pct_cols.values():
    df[c] = pd.to_numeric(df[c].astype(str).str.replace('%',''), errors="coerce").fillna(0.0)

# -------- Filter counties --------
df[county] = df[county].astype(str).str.strip()
want = [w.lower() for w in COUNTY_ORDER]

use = df[df[county].str.lower().isin(want)].copy()
use["__ord"] = use[county].str.lower().apply(lambda x: want.index(x))
use = use.sort_values("__ord").reset_index(drop=True)

# -------- COLORS (ONLY GREEN & YELLOW REPLACED) --------
COLOR_VL = "#1F6F1F"   # Dark green (reference)
COLOR_L  = "#F2F21C"   # Yellow (reference)
COLOR_M  = "#FB8C00"
COLOR_H  = "#F4511E"
COLOR_VH = "#E53935"
COLORS   = [COLOR_VL, COLOR_L, COLOR_M, COLOR_H, COLOR_VH]

VAL_COLS = [pct_cols[k] for k in ["vl","l","m","h","vh"]]

INNER = 1 - WEDGE_WIDTH
MID_R = INNER + WEDGE_WIDTH/2
YL_RGB = mcolors.to_rgb(COLOR_L)

def pct_fontsize(p):
    p = max(0, min(30, p))
    return PCT_MIN + (PCT_MAX - PCT_MIN) * (p / 30.0)

def draw_donut_on(ax, vals, name):
    vals = np.nan_to_num(vals, nan=0.0)
    pct  = 100*vals/max(vals.sum(), 1e-12)

    wedges, _ = ax.pie(
        vals, colors=COLORS, startangle=90, counterclock=False,
        wedgeprops=dict(width=WEDGE_WIDTH, edgecolor="black", linewidth=EDGE_LW)
    )

    for w, p in zip(wedges, pct):
        if p < LABEL_MIN:
            continue

        ang = 0.5*(w.theta1 + w.theta2)
        x = MID_R*np.cos(np.deg2rad(ang))
        y = MID_R*np.sin(np.deg2rad(ang))
        rot = ang - 90
        if 90 < ang < 270:
            rot += 180

        text_color = "#666666" if np.allclose(w.get_facecolor()[:3], YL_RGB) else "white"

        ax.text(
            x, y, f"{p:.1f}%",
            ha="center", va="center",
            rotation=rot, rotation_mode="anchor",
            fontsize=pct_fontsize(p),
            color=text_color
        )

    ax.text(0, 0, name, ha="center", va="center",
            fontsize=NAME_FS, color="black")

    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(-1.06, 1.06); ax.set_ylim(-1.06, 1.06)

# -------- Build panel --------
fig_w, fig_h = CELL_INCH * PANEL_COLS, CELL_INCH * PANEL_ROWS
fig, axes = plt.subplots(PANEL_ROWS, PANEL_COLS, figsize=(fig_w, fig_h), dpi=SAVE_DPI)
axes = axes.flatten()

for ax, (_, row) in zip(axes, use.iterrows()):
    draw_donut_on(ax, row[VAL_COLS].to_numpy(float), row[county])

# -------- Bottom horizontal legend --------
legend_handles = [
    Patch(facecolor=COLOR_VL, edgecolor="black", label="Very Low"),
    Patch(facecolor=COLOR_L , edgecolor="black", label="Low"),
    Patch(facecolor=COLOR_M , edgecolor="black", label="Moderate"),
    Patch(facecolor=COLOR_H , edgecolor="black", label="High"),
    Patch(facecolor=COLOR_VH, edgecolor="black", label="Very High"),
]

fig.legend(
    handles=legend_handles,
    loc="lower center",
    ncol=5,
    frameon=False,
    fontsize=11,
    bbox_to_anchor=(0.5, 0.01)
)

plt.tight_layout(rect=[0, 0.05, 1, 1])
fig.savefig("iowa_fsm_donuts_panel.png", dpi=SAVE_DPI, bbox_inches="tight")
plt.show()

print("Saved: iowa_fsm_donuts_panel.png")
