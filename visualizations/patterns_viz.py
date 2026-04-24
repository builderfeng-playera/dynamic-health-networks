"""
Pattern & disruption visualizations — phase shifts, cycles, correlations, outliers.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch

plt.rcParams.update({
    'figure.facecolor': '#0e1117',
    'axes.facecolor': '#1a1d23',
    'axes.edgecolor': '#2d3139',
    'axes.labelcolor': '#e0e0e0',
    'text.color': '#e0e0e0',
    'xtick.color': '#888888',
    'ytick.color': '#888888',
    'grid.color': '#2d3139',
    'grid.alpha': 0.5,
    'font.size': 9,
    'axes.titlesize': 11,
    'axes.titleweight': 'bold',
})

BASE = os.path.dirname(__file__)
OUT = BASE
df = pd.read_csv(os.path.join(BASE, "..", "processed_data", "daily_merged.csv"))
df["day"] = pd.to_datetime(df["day"])
df_clean = df[df["data_confidence"] == "normal"].copy().sort_values("day").reset_index(drop=True)

TENNIS = [pd.Timestamp(d) for d in ["2025-10-15", "2025-10-23", "2025-10-25", "2025-11-10"]]
TRAVEL_START = pd.Timestamp("2026-02-26")
TRAVEL_END = pd.Timestamp("2026-03-26")

def add_context(ax):
    for d in TENNIS:
        ax.axvline(d, color='#ff6b6b', alpha=0.5, linewidth=1, linestyle='--')
    ax.axvspan(TRAVEL_START, TRAVEL_END, alpha=0.08, color='#ffa726')


# =========================================================================
# P1: Phase Shifts — 7-day vs 30-day rolling with phase labels
# =========================================================================
fig, axes = plt.subplots(5, 1, figsize=(20, 20), sharex=True)
fig.suptitle('PHASE SHIFTS — 7-Day vs 30-Day Rolling Mean', fontsize=14, fontweight='bold', y=0.99, color='#e0e0e0')

phase_metrics = [
    ("readiness_score", "Readiness Score", '#66bb6a'),
    ("sleep_avg_hrv", "Sleep HRV (ms)", '#4fc3f7'),
    ("steps", "Daily Steps", '#ffa726'),
    ("sleep_lowest_hr", "Lowest HR (BPM)", '#ef5350'),
    ("stress_high_hours", "Stress (hours)", '#ce93d8'),
]

for i, (col, label, color) in enumerate(phase_metrics):
    ax = axes[i]
    s = df_clean[["day", col]].dropna().copy()
    s["r7"] = s[col].rolling(7, min_periods=3).mean()
    s["r30"] = s[col].rolling(30, min_periods=10).mean()

    ax.plot(s["day"], s[col], color=color, alpha=0.15, linewidth=0.5)
    ax.plot(s["day"], s["r7"], color=color, linewidth=1.5, label='7-day', alpha=0.9)
    ax.plot(s["day"], s["r30"], color='#ffffff', linewidth=2, label='30-day', alpha=0.7)

    # Shade when 7d < 30d (decline phase)
    valid = s.dropna(subset=["r7", "r30"])
    if len(valid) > 1:
        ax.fill_between(valid["day"], valid["r7"], valid["r30"],
                         where=valid["r7"] < valid["r30"],
                         alpha=0.15, color='#ef5350', label='Decline phase')
        ax.fill_between(valid["day"], valid["r7"], valid["r30"],
                         where=valid["r7"] >= valid["r30"],
                         alpha=0.15, color='#66bb6a', label='Rise phase')

    ax.legend(loc='upper right', fontsize=7, ncol=4)
    ax.set_ylabel(label)
    add_context(ax)

axes[-1].xaxis.set_major_locator(mdates.MonthLocator())
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
fig.tight_layout(rect=[0, 0, 1, 0.97])
fig.savefig(os.path.join(OUT, 'P1_phase_shifts.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print("✓ P1_phase_shifts.png")


# =========================================================================
# P2: The December Crisis — multi-metric disruption convergence
# =========================================================================
fig, axes = plt.subplots(5, 1, figsize=(18, 16), sharex=True)
fig.suptitle('DISRUPTION CONVERGENCE — Dec 2025 "Low Point"', fontsize=14, fontweight='bold', y=0.98, color='#ef5350')

crisis_start = pd.Timestamp("2025-11-15")
crisis_end = pd.Timestamp("2026-01-15")
dc = df_clean[(df_clean["day"] >= crisis_start) & (df_clean["day"] <= crisis_end)]

# Readiness
ax = axes[0]
ax.plot(dc["day"], dc["readiness_score"], color='#66bb6a', linewidth=2, marker='o', markersize=4)
ax.axhline(df_clean["readiness_score"].mean(), color='#66bb6a', alpha=0.3, linestyle=':', linewidth=1)
# Mark outliers
outlier_days = ["2025-11-27", "2025-12-13", "2025-12-20", "2025-12-21", "2025-12-30"]
for od in outlier_days:
    od_t = pd.Timestamp(od)
    row = dc[dc["day"] == od_t]
    if len(row) > 0:
        ax.scatter([od_t], row["readiness_score"].values, color='#ef5350', s=80, zorder=10, edgecolors='white')
        ax.annotate(f'{row["readiness_score"].values[0]:.0f}', (od_t, row["readiness_score"].values[0]),
                    textcoords="offset points", xytext=(0, 10), fontsize=8, color='#ef5350', ha='center')
ax.set_ylabel('Score')
ax.set_title('Readiness Score (red dots = >2σ disruptions)')

# HRV
ax = axes[1]
ax.plot(dc["day"], dc["sleep_avg_hrv"], color='#4fc3f7', linewidth=2, marker='o', markersize=4)
ax.axhline(df_clean["sleep_avg_hrv"].mean(), color='#4fc3f7', alpha=0.3, linestyle=':', linewidth=1)
for od in ["2025-11-27", "2025-12-21"]:
    od_t = pd.Timestamp(od)
    row = dc[dc["day"] == od_t]
    if len(row) > 0:
        ax.scatter([od_t], row["sleep_avg_hrv"].values, color='#ef5350', s=80, zorder=10, edgecolors='white')
        ax.annotate(f'{row["sleep_avg_hrv"].values[0]:.0f}ms', (od_t, row["sleep_avg_hrv"].values[0]),
                    textcoords="offset points", xytext=(0, -15), fontsize=8, color='#ef5350', ha='center')
ax.set_ylabel('ms')
ax.set_title('Sleep HRV')

# Lowest HR
ax = axes[2]
ax.plot(dc["day"], dc["sleep_lowest_hr"], color='#ef5350', linewidth=2, marker='o', markersize=4)
ax.axhline(df_clean["sleep_lowest_hr"].mean(), color='#ef5350', alpha=0.3, linestyle=':', linewidth=1)
for od in ["2025-11-27", "2025-11-29", "2025-12-13", "2025-12-20", "2025-12-21", "2025-12-22"]:
    od_t = pd.Timestamp(od)
    row = dc[dc["day"] == od_t]
    if len(row) > 0:
        ax.scatter([od_t], row["sleep_lowest_hr"].values, color='#ffa726', s=80, zorder=10, edgecolors='white')
ax.set_ylabel('BPM')
ax.set_title('Lowest Heart Rate During Sleep (orange = elevated)')

# Stress
ax = axes[3]
ax.bar(dc["day"], dc["stress_high_hours"], color='#ef5350', alpha=0.6, width=0.8, label='Stress')
ax.bar(dc["day"], dc["recovery_high_hours"], color='#66bb6a', alpha=0.6, width=0.8, bottom=0, label='Recovery')
ax.axhline(df_clean["stress_high_hours"].mean(), color='#ef5350', alpha=0.3, linestyle=':', linewidth=1)
ax.legend(loc='upper right', fontsize=8)
ax.set_ylabel('Hours')
ax.set_title('Stress vs Recovery')

# Temperature
ax = axes[4]
ax.bar(dc["day"], dc["temperature_deviation"],
       color=dc["temperature_deviation"].apply(
           lambda x: '#ef5350' if x > 0.3 else '#4fc3f7' if x < -0.2 else '#78909c'
       ), alpha=0.7, width=0.8)
ax.axhline(0, color='#888888', alpha=0.5, linewidth=0.8)
ax.set_ylabel('°C')
ax.set_title('Temperature Deviation')

# Annotate Dec 21 as the single worst day
for ax in axes:
    ax.axvline(pd.Timestamp("2025-12-21"), color='#ff6b6b', alpha=0.8, linewidth=2, linestyle='-')

axes[-1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(OUT, 'P2_december_crisis.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print("✓ P2_december_crisis.png")


# =========================================================================
# P3: Menstrual Cycle — autocorrelation proof + overlay
# =========================================================================
fig, axes = plt.subplots(3, 1, figsize=(18, 12), sharex=False)
fig.suptitle('CYCLICAL PATTERN — ~28-Day Menstrual Cycle Signal', fontsize=14, fontweight='bold', y=0.98, color='#f48fb1')

# 3a: Autocorrelation function for temperature
ax = axes[0]
temp = df_clean["temperature_deviation"].dropna()
lags = range(1, 60)
acf = [temp.autocorr(lag=l) for l in lags]
colors = ['#f48fb1' if abs(a) > 0.2 else '#555555' for a in acf]
ax.bar(lags, acf, color=colors, alpha=0.8)
ax.axhline(0, color='#888888', linewidth=0.5)
ax.axhline(0.2, color='#ffa726', alpha=0.4, linestyle=':', linewidth=1)
ax.axhline(-0.2, color='#ffa726', alpha=0.4, linestyle=':', linewidth=1)
# Mark 14 and 28 day lags
ax.axvline(14, color='#f48fb1', alpha=0.5, linestyle='--', linewidth=1)
ax.axvline(28, color='#f48fb1', alpha=0.5, linestyle='--', linewidth=1)
ax.annotate('lag 14\n(anti-phase)', xy=(14, acf[13]), fontsize=8, color='#f48fb1', ha='center',
            xytext=(14, 0.45), arrowprops=dict(arrowstyle='->', color='#f48fb1', alpha=0.5))
ax.annotate('lag 28\n(full cycle)', xy=(28, acf[27]), fontsize=8, color='#f48fb1', ha='center',
            xytext=(28, 0.45), arrowprops=dict(arrowstyle='->', color='#f48fb1', alpha=0.5))
ax.set_xlabel('Lag (days)')
ax.set_ylabel('Autocorrelation')
ax.set_title('Temperature Deviation Autocorrelation — confirms ~28-day periodicity')
ax.set_ylim(-0.5, 0.6)

# 3b: Temperature with 28-day cycle overlay
ax = axes[1]
t = df_clean[["day", "temperature_deviation"]].dropna()
ax.plot(t["day"], t["temperature_deviation"], color='#f48fb1', linewidth=1, alpha=0.6)
# 7-day smoothed
t["smooth"] = t["temperature_deviation"].rolling(7, min_periods=3, center=True).mean()
ax.plot(t["day"], t["smooth"], color='#f48fb1', linewidth=2.5)
ax.axhline(0, color='#888888', linewidth=0.5)
ax.set_ylabel('°C')
ax.set_title('Temperature Deviation (7-day smoothed) — visual cycle confirmation')
add_context(ax)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))

# 3c: Temperature vs HRV (inverse relationship)
ax = axes[2]
merged = df_clean[["day", "temperature_deviation", "sleep_avg_hrv"]].dropna()
m_smooth = merged.copy()
m_smooth["temp_s"] = m_smooth["temperature_deviation"].rolling(7, min_periods=3, center=True).mean()
m_smooth["hrv_s"] = m_smooth["sleep_avg_hrv"].rolling(7, min_periods=3, center=True).mean()

ax.plot(m_smooth["day"], m_smooth["temp_s"], color='#f48fb1', linewidth=2, label='Temp Dev (°C)')
ax2 = ax.twinx()
ax2.plot(m_smooth["day"], m_smooth["hrv_s"], color='#4fc3f7', linewidth=2, label='HRV (ms)')
ax2.invert_yaxis()
ax2.set_ylabel('HRV ms (inverted)', color='#4fc3f7')
ax2.tick_params(axis='y', labelcolor='#4fc3f7')
ax.set_ylabel('Temp °C', color='#f48fb1')
ax.tick_params(axis='y', labelcolor='#f48fb1')
ax.set_title('Temperature vs HRV — inverse relationship (HRV axis inverted)')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc='upper left')
add_context(ax)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))

fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(OUT, 'P3_menstrual_cycle_proof.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print("✓ P3_menstrual_cycle_proof.png")


# =========================================================================
# P4: Key Correlations scatter plots
# =========================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle('KEY CORRELATIONS', fontsize=14, fontweight='bold', y=0.98, color='#e0e0e0')

# 4a: HRV → Readiness (strongest same-day)
ax = axes[0, 0]
valid = df_clean[["sleep_avg_hrv", "readiness_score"]].dropna()
ax.scatter(valid["sleep_avg_hrv"], valid["readiness_score"], c='#4fc3f7', alpha=0.5, s=20)
z = np.polyfit(valid["sleep_avg_hrv"], valid["readiness_score"], 1)
p = np.poly1d(z)
x_line = np.linspace(valid["sleep_avg_hrv"].min(), valid["sleep_avg_hrv"].max(), 100)
ax.plot(x_line, p(x_line), color='#ffa726', linewidth=2)
r = valid["sleep_avg_hrv"].corr(valid["readiness_score"])
ax.set_xlabel('Sleep HRV (ms)')
ax.set_ylabel('Readiness Score')
ax.set_title(f'HRV → Readiness  (r = {r:.3f})')

# 4b: Stress today → HRV tonight (strongest lagged)
ax = axes[0, 1]
temp = df_clean[["day", "stress_high_hours", "sleep_avg_hrv"]].copy()
temp["hrv_next"] = temp["sleep_avg_hrv"].shift(-1)
valid = temp[["stress_high_hours", "hrv_next"]].dropna()
ax.scatter(valid["stress_high_hours"], valid["hrv_next"], c='#ce93d8', alpha=0.5, s=20)
z = np.polyfit(valid["stress_high_hours"], valid["hrv_next"], 1)
p = np.poly1d(z)
x_line = np.linspace(valid["stress_high_hours"].min(), valid["stress_high_hours"].max(), 100)
ax.plot(x_line, p(x_line), color='#ffa726', linewidth=2)
r = valid["stress_high_hours"].corr(valid["hrv_next"])
ax.set_xlabel('Stress Today (hours)')
ax.set_ylabel('HRV Tonight (ms)')
ax.set_title(f'Stress → Next Night HRV  (r = {r:.3f})')

# 4c: Temperature → Readiness
ax = axes[1, 0]
valid = df_clean[["temperature_deviation", "readiness_score"]].dropna()
ax.scatter(valid["temperature_deviation"], valid["readiness_score"], c='#f48fb1', alpha=0.5, s=20)
z = np.polyfit(valid["temperature_deviation"], valid["readiness_score"], 1)
p = np.poly1d(z)
x_line = np.linspace(valid["temperature_deviation"].min(), valid["temperature_deviation"].max(), 100)
ax.plot(x_line, p(x_line), color='#ffa726', linewidth=2)
r = valid["temperature_deviation"].corr(valid["readiness_score"])
ax.set_xlabel('Temperature Deviation (°C)')
ax.set_ylabel('Readiness Score')
ax.set_title(f'Temp Dev → Readiness  (r = {r:.3f})')

# 4d: Volatility over time (rolling 14-day std)
ax = axes[1, 1]
for col, label, color in [
    ("readiness_score", "Readiness", "#66bb6a"),
    ("sleep_avg_hrv", "HRV", "#4fc3f7"),
]:
    s = df_clean[["day", col]].dropna()
    s["vol"] = s[col].rolling(14, min_periods=7).std()
    # Normalize to CV%
    s["cv"] = s["vol"] / s[col].rolling(14, min_periods=7).mean() * 100
    ax.plot(s["day"], s["cv"], color=color, linewidth=1.5, label=label, alpha=0.8)
ax.legend(fontsize=8)
ax.set_ylabel('Coefficient of Variation %')
ax.set_title('Rolling 14-Day Volatility (lower = more stable)')
add_context(ax)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(OUT, 'P4_correlations.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print("✓ P4_correlations.png")


# =========================================================================
# P5: Comprehensive Timeline — all signals on one page
# =========================================================================
fig, axes = plt.subplots(7, 1, figsize=(22, 22), sharex=True)
fig.suptitle('7-MONTH BODY TIMELINE — Patterns, Phases & Disruptions', fontsize=16, fontweight='bold', y=0.99, color='#e0e0e0')

d = df_clean

# Phase labels
phases = [
    ("2025-09-08", "2025-10-31", "ACTIVE\nSEASON", '#66bb6a'),
    ("2025-11-01", "2025-12-31", "DECELERATION\n& LOW POINT", '#ef5350'),
    ("2026-01-01", "2026-02-25", "STABILIZATION\n& RECOVERY", '#4fc3f7'),
    ("2026-02-26", "2026-03-26", "SF\nTRIP", '#ffa726'),
    ("2026-03-27", "2026-04-13", "RETURN", '#ce93d8'),
]

for ax in axes:
    for start, end, label, color in phases:
        ax.axvspan(pd.Timestamp(start), pd.Timestamp(end), alpha=0.04, color=color)
    for d_t in TENNIS:
        ax.axvline(d_t, color='#ff6b6b', alpha=0.4, linewidth=1, linestyle='--')

# Row 0: Readiness
ax = axes[0]
s = d[["day", "readiness_score"]].dropna()
ax.plot(s["day"], s["readiness_score"], color='#66bb6a', alpha=0.3, linewidth=0.5)
ax.plot(s["day"], s["readiness_score"].rolling(7, min_periods=3).mean(), color='#66bb6a', linewidth=2)
ax.set_ylabel('Score')
ax.set_title('Readiness Score (7-day smoothed)')
ax.set_ylim(45, 100)
# Phase labels
for start, end, label, color in phases:
    mid = pd.Timestamp(start) + (pd.Timestamp(end) - pd.Timestamp(start)) / 2
    ax.text(mid, 97, label, ha='center', va='top', fontsize=7, color=color, fontweight='bold')

# Row 1: HRV
ax = axes[1]
s = d[["day", "sleep_avg_hrv", "sleep_hrv_peak", "sleep_hrv_min"]].dropna()
ax.fill_between(s["day"],
                s["sleep_hrv_min"].rolling(7, min_periods=3).mean(),
                s["sleep_hrv_peak"].rolling(7, min_periods=3).mean(),
                alpha=0.15, color='#4fc3f7')
ax.plot(s["day"], s["sleep_avg_hrv"].rolling(7, min_periods=3).mean(), color='#4fc3f7', linewidth=2)
ax.set_ylabel('ms')
ax.set_title('Sleep HRV (7-day smoothed, band = peak/min)')

# Row 2: Lowest HR
ax = axes[2]
s = d[["day", "sleep_lowest_hr"]].dropna()
ax.plot(s["day"], s["sleep_lowest_hr"], color='#ef5350', alpha=0.3, linewidth=0.5)
ax.plot(s["day"], s["sleep_lowest_hr"].rolling(7, min_periods=3).mean(), color='#ef5350', linewidth=2)
ax.set_ylabel('BPM')
ax.set_title('Lowest Heart Rate During Sleep')

# Row 3: Steps
ax = axes[3]
s = d[["day", "steps"]].dropna()
ax.bar(s["day"], s["steps"], color='#ffa726', alpha=0.3, width=0.8)
ax.plot(s["day"], s["steps"].rolling(14, min_periods=5).mean(), color='#ffa726', linewidth=2)
ax.set_ylabel('Steps')
ax.set_title('Daily Steps (14-day trend)')

# Row 4: Temperature (cycle signal)
ax = axes[4]
s = d[["day", "temperature_deviation"]].dropna()
ax.plot(s["day"], s["temperature_deviation"], color='#f48fb1', alpha=0.3, linewidth=0.5)
ax.plot(s["day"], s["temperature_deviation"].rolling(7, min_periods=3, center=True).mean(),
        color='#f48fb1', linewidth=2)
ax.axhline(0, color='#888888', linewidth=0.5)
ax.set_ylabel('°C')
ax.set_title('Temperature Deviation (menstrual cycle signal)')

# Row 5: Stress/Recovery ratio
ax = axes[5]
s = d[["day", "stress_high_hours", "recovery_high_hours"]].dropna()
ratio = s["stress_high_hours"] / s["recovery_high_hours"].replace(0, np.nan)
ax.bar(s["day"], ratio, color=ratio.apply(
    lambda x: '#ef5350' if x > 2 else '#ffa726' if x > 1 else '#66bb6a'
), alpha=0.5, width=0.8)
ax.plot(s["day"], ratio.rolling(14, min_periods=5).mean(), color='#ffffff', linewidth=2)
ax.axhline(1, color='#888888', linewidth=1, linestyle='--')
ax.set_ylabel('Ratio')
ax.set_title('Stress / Recovery Ratio (14-day trend, <1 = net recovery)')
ax.set_ylim(0, 8)

# Row 6: Breathing Disturbance
ax = axes[6]
s = d[["day", "breathing_disturbance_index"]].dropna()
ax.bar(s["day"], s["breathing_disturbance_index"], color='#ffa726', alpha=0.4, width=0.8)
ax.plot(s["day"], s["breathing_disturbance_index"].rolling(14, min_periods=5).mean(),
        color='#ffa726', linewidth=2)
ax.axhline(5, color='#66bb6a', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Events/h')
ax.set_title('Breathing Disturbance Index (14-day trend — note sustained improvement)')

axes[-1].xaxis.set_major_locator(mdates.MonthLocator())
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
fig.tight_layout(rect=[0, 0, 1, 0.97])
fig.savefig(os.path.join(OUT, 'P5_timeline.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print("✓ P5_timeline.png")

print("\n✅ All pattern visualizations saved.")
