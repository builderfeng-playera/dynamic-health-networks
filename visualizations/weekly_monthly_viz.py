"""
Weekly and Monthly aggregated visualizations for Oura Ring data.
Reads from processed_data/daily_merged.csv.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch

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

# Only use normal confidence data for aggregation
df_clean = df[df["data_confidence"] == "normal"].copy()

TENNIS_WEEKS = pd.to_datetime(["2025-10-13", "2025-10-20", "2025-11-10"])

# =========================================================================
# Aggregation helpers
# =========================================================================

def weekly_agg(data):
    data = data.copy()
    data["week"] = data["day"].dt.to_period("W").apply(lambda r: r.start_time)

    agg = {}
    # Count valid days per week
    agg["days_with_data"] = ("day", "count")

    # Sleep
    for c in ["total_sleep_duration_hours", "deep_sleep_duration_hours",
              "light_sleep_duration_hours", "rem_sleep_duration_hours",
              "efficiency", "latency_minutes", "sleep_lowest_hr",
              "sleep_avg_hrv", "sleep_hrv_peak", "sleep_hrv_min", "sleep_hrv_range",
              "sleep_avg_breath", "awake_time_hours"]:
        if c in data.columns:
            agg[c] = (c, "mean")

    # Activity
    for c in ["steps", "active_calories", "activity_score",
              "sedentary_time", "high_activity_time", "medium_activity_time",
              "low_activity_time"]:
        if c in data.columns:
            agg[c] = (c, "mean")

    # HR
    for c in ["hr_awake_avg", "hr_workout_avg", "hr_workout_max"]:
        if c in data.columns:
            agg[c] = (c, "mean")

    # Recovery & stress
    for c in ["readiness_score", "temperature_deviation",
              "stress_high_hours", "recovery_high_hours"]:
        if c in data.columns:
            agg[c] = (c, "mean")

    # SpO2
    for c in ["spo2_avg", "breathing_disturbance_index"]:
        if c in data.columns:
            agg[c] = (c, "mean")

    # Naps
    agg["nap_days"] = ("has_nap", "sum")

    # Tennis
    agg["tennis_matches"] = ("is_tennis_match", "sum")

    result = data.groupby("week").agg(**agg).reset_index()
    return result


def monthly_agg(data):
    data = data.copy()
    data["month"] = data["day"].dt.to_period("M").apply(lambda r: r.start_time)

    agg = {}
    agg["days_with_data"] = ("day", "count")

    for c in ["total_sleep_duration_hours", "deep_sleep_duration_hours",
              "light_sleep_duration_hours", "rem_sleep_duration_hours",
              "efficiency", "latency_minutes", "sleep_lowest_hr",
              "sleep_avg_hrv", "sleep_hrv_peak", "sleep_hrv_min", "sleep_hrv_range",
              "sleep_avg_breath", "awake_time_hours",
              "steps", "active_calories", "activity_score",
              "sedentary_time", "high_activity_time", "medium_activity_time",
              "low_activity_time",
              "hr_awake_avg", "hr_workout_avg", "hr_workout_max",
              "readiness_score", "temperature_deviation",
              "stress_high_hours", "recovery_high_hours",
              "spo2_avg", "breathing_disturbance_index"]:
        if c in data.columns:
            agg[c] = (c, "mean")

    # Stress day_summary counts
    agg["tennis_matches"] = ("is_tennis_match", "sum")
    agg["nap_days"] = ("has_nap", "sum")

    result = data.groupby("month").agg(**agg).reset_index()
    return result


wk = weekly_agg(df_clean)
mo = monthly_agg(df_clean)

print(f"Weekly: {len(wk)} weeks")
print(f"Monthly: {len(mo)} months")


def add_tennis_week_markers(ax, weeks=TENNIS_WEEKS):
    for w in weeks:
        ax.axvline(w, color='#ff6b6b', alpha=0.6, linewidth=1.5, linestyle='--', zorder=5)


# =========================================================================
# WEEKLY VISUALIZATIONS
# =========================================================================

# ── W1: Sleep ──
fig, axes = plt.subplots(5, 1, figsize=(18, 16), sharex=True)
fig.suptitle('WEEKLY AVERAGES — Sleep Quality', fontsize=14, fontweight='bold', y=0.98, color='#4fc3f7')

ax = axes[0]
ax.bar(wk["week"], wk["deep_sleep_duration_hours"], color='#1a237e', label='Deep', width=5)
ax.bar(wk["week"], wk["light_sleep_duration_hours"], bottom=wk["deep_sleep_duration_hours"], color='#42a5f5', label='Light', width=5)
bottom2 = wk["deep_sleep_duration_hours"] + wk["light_sleep_duration_hours"]
ax.bar(wk["week"], wk["rem_sleep_duration_hours"], bottom=bottom2, color='#ab47bc', label='REM', width=5)
bottom3 = bottom2 + wk["rem_sleep_duration_hours"]
ax.bar(wk["week"], wk["awake_time_hours"], bottom=bottom3, color='#ef5350', alpha=0.6, label='Awake', width=5)
ax.axhline(7, color='#66bb6a', alpha=0.4, linestyle=':', linewidth=1)
ax.axhline(9, color='#66bb6a', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Hours')
ax.set_title('Avg Total Sleep Duration (stacked)')
ax.legend(loc='upper right', ncol=4, fontsize=8)
ax.set_ylim(0, 10)
add_tennis_week_markers(ax)

ax = axes[1]
ax.plot(wk["week"], wk["efficiency"], color='#4fc3f7', linewidth=2, marker='o', markersize=5)
ax.fill_between(wk["week"], 70, wk["efficiency"], alpha=0.1, color='#4fc3f7')
ax.axhline(85, color='#ffa726', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('%')
ax.set_title('Avg Sleep Efficiency')
ax.set_ylim(65, 100)
add_tennis_week_markers(ax)

ax = axes[2]
ax.plot(wk["week"], wk["sleep_lowest_hr"], color='#ef5350', linewidth=2, marker='o', markersize=5)
ax.set_ylabel('BPM')
ax.set_title('Avg Lowest Heart Rate During Sleep')
add_tennis_week_markers(ax)

ax = axes[3]
ax.fill_between(wk["week"], wk["sleep_hrv_min"], wk["sleep_hrv_peak"], alpha=0.2, color='#4fc3f7')
ax.plot(wk["week"], wk["sleep_hrv_peak"], color='#66bb6a', linewidth=1.5, marker='o', markersize=4, label='Peak')
ax.plot(wk["week"], wk["sleep_avg_hrv"], color='#4fc3f7', linewidth=2, marker='o', markersize=5, label='Avg')
ax.plot(wk["week"], wk["sleep_hrv_min"], color='#ef5350', linewidth=1.5, marker='o', markersize=4, label='Min')
ax.legend(loc='upper right', fontsize=8, ncol=3)
ax.set_ylabel('ms')
ax.set_title('Avg Sleep HRV (Peak / Avg / Min)')
add_tennis_week_markers(ax)

ax = axes[4]
ax.bar(wk["week"], wk["latency_minutes"], color='#7e57c2', alpha=0.7, width=5)
ax.axhline(20, color='#66bb6a', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Minutes')
ax.set_title('Avg Sleep Latency')
ax.set_ylim(0, 30)
add_tennis_week_markers(ax)

axes[-1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(OUT, 'W1_weekly_sleep.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print("✓ W1_weekly_sleep.png")


# ── W2: Activity ──
fig, axes = plt.subplots(5, 1, figsize=(18, 16), sharex=True)
fig.suptitle('WEEKLY AVERAGES — Daily Activity', fontsize=14, fontweight='bold', y=0.98, color='#ffa726')

ax = axes[0]
colors = wk["steps"].apply(lambda x: '#66bb6a' if x >= 10000 else '#ffa726' if x >= 7000 else '#ef5350')
ax.bar(wk["week"], wk["steps"], color=colors, alpha=0.8, width=5)
ax.axhline(7000, color='#ffa726', alpha=0.4, linestyle=':', linewidth=1)
ax.axhline(10000, color='#66bb6a', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Steps')
ax.set_title('Avg Daily Steps')
add_tennis_week_markers(ax)

ax = axes[1]
ax.bar(wk["week"], wk["active_calories"], color='#ff7043', alpha=0.7, width=5)
ax.axhline(300, color='#ffa726', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('kcal')
ax.set_title('Avg Active Calories')
add_tennis_week_markers(ax)

ax = axes[2]
ax.plot(wk["week"], wk["activity_score"], color='#ffa726', linewidth=2, marker='o', markersize=5)
ax.fill_between(wk["week"], 50, wk["activity_score"], alpha=0.1, color='#ffa726')
ax.axhline(85, color='#66bb6a', alpha=0.3, linestyle=':', linewidth=1)
ax.axhline(70, color='#ef5350', alpha=0.3, linestyle=':', linewidth=1)
ax.set_ylabel('Score')
ax.set_title('Avg Activity Score')
ax.set_ylim(55, 100)
add_tennis_week_markers(ax)

ax = axes[3]
sed_h = wk["sedentary_time"] / 3600
ax.bar(wk["week"], sed_h, color='#78909c', alpha=0.7, width=5)
ax.axhline(8, color='#ef5350', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Hours')
ax.set_title('Avg Sedentary Time')
add_tennis_week_markers(ax)

ax = axes[4]
if "hr_awake_avg" in wk.columns:
    ax.plot(wk["week"], wk["hr_awake_avg"], color='#4fc3f7', linewidth=2, marker='o', markersize=4, label='Awake Avg')
if "hr_workout_avg" in wk.columns:
    ax.plot(wk["week"], wk["hr_workout_avg"], color='#ffa726', linewidth=2, marker='o', markersize=4, label='Workout Avg')
if "hr_workout_max" in wk.columns:
    ax.plot(wk["week"], wk["hr_workout_max"], color='#ef5350', linewidth=2, marker='o', markersize=4, label='Workout Max')
ax.legend(loc='upper right', fontsize=8, ncol=3)
ax.set_ylabel('BPM')
ax.set_title('Avg Heart Rate by Context')
add_tennis_week_markers(ax)

axes[-1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(OUT, 'W2_weekly_activity.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print("✓ W2_weekly_activity.png")


# ── W3: Recovery & Stress ──
fig, axes = plt.subplots(4, 1, figsize=(18, 14), sharex=True)
fig.suptitle('WEEKLY AVERAGES — Recovery & Stress', fontsize=14, fontweight='bold', y=0.98, color='#66bb6a')

ax = axes[0]
ax.plot(wk["week"], wk["readiness_score"], color='#66bb6a', linewidth=2, marker='o', markersize=5)
ax.fill_between(wk["week"], 50, wk["readiness_score"], alpha=0.1, color='#66bb6a')
ax.axhline(85, color='#66bb6a', alpha=0.3, linestyle=':', linewidth=1)
ax.axhline(70, color='#ef5350', alpha=0.3, linestyle=':', linewidth=1)
ax.set_ylabel('Score')
ax.set_title('Avg Readiness Score')
ax.set_ylim(55, 95)
add_tennis_week_markers(ax)

ax = axes[1]
colors = wk["temperature_deviation"].apply(
    lambda x: '#ef5350' if x > 0.2 else '#4fc3f7' if x < -0.1 else '#78909c'
)
ax.bar(wk["week"], wk["temperature_deviation"], color=colors, alpha=0.7, width=5)
ax.axhline(0, color='#888888', alpha=0.5, linewidth=0.8)
ax.set_ylabel('°C')
ax.set_title('Avg Temperature Deviation')
add_tennis_week_markers(ax)

ax = axes[2]
width = 2.5
ax.bar(wk["week"] - pd.Timedelta(days=1.5), wk["stress_high_hours"], width=width, color='#ef5350', alpha=0.7, label='Stress')
ax.bar(wk["week"] + pd.Timedelta(days=1.5), wk["recovery_high_hours"], width=width, color='#66bb6a', alpha=0.7, label='Recovery')
ax.legend(loc='upper right', fontsize=8)
ax.set_ylabel('Hours')
ax.set_title('Avg Stress vs Recovery Time')
add_tennis_week_markers(ax)

ax = axes[3]
# Stress-to-recovery ratio
ratio = wk["stress_high_hours"] / wk["recovery_high_hours"].replace(0, np.nan)
colors = ratio.apply(lambda x: '#ef5350' if x > 2 else '#ffa726' if x > 1 else '#66bb6a')
ax.bar(wk["week"], ratio, color=colors, alpha=0.7, width=5)
ax.axhline(1, color='#888888', alpha=0.5, linewidth=1, linestyle='--')
ax.set_ylabel('Ratio')
ax.set_title('Stress / Recovery Ratio (< 1 = more recovery, > 1 = more stress)')
add_tennis_week_markers(ax)

axes[-1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(OUT, 'W3_weekly_recovery.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print("✓ W3_weekly_recovery.png")


# ── W4: SpO2 + Breathing ──
fig, axes = plt.subplots(2, 1, figsize=(18, 7), sharex=True)
fig.suptitle('WEEKLY AVERAGES — Blood Oxygen & Breathing', fontsize=14, fontweight='bold', y=0.98, color='#4fc3f7')

ax = axes[0]
ax.plot(wk["week"], wk["spo2_avg"], color='#4fc3f7', linewidth=2, marker='o', markersize=5)
ax.axhline(96, color='#66bb6a', alpha=0.3, linestyle=':', linewidth=1)
ax.set_ylabel('SpO2 %')
ax.set_title('Avg Blood Oxygen')
ax.set_ylim(94, 99)
add_tennis_week_markers(ax)

ax = axes[1]
colors = wk["breathing_disturbance_index"].apply(
    lambda x: '#66bb6a' if x < 5 else '#ffa726' if x < 15 else '#ef5350'
)
ax.bar(wk["week"], wk["breathing_disturbance_index"], color=colors, alpha=0.7, width=5)
ax.axhline(5, color='#66bb6a', alpha=0.4, linestyle=':', linewidth=1)
ax.axhline(15, color='#ef5350', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Events/hour')
ax.set_title('Avg Breathing Disturbance Index')
add_tennis_week_markers(ax)

axes[-1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(OUT, 'W4_weekly_spo2.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print("✓ W4_weekly_spo2.png")


# =========================================================================
# MONTHLY VISUALIZATIONS
# =========================================================================

# ── M1: Monthly Overview Dashboard ──
fig, axes = plt.subplots(4, 2, figsize=(20, 16))
fig.suptitle('MONTHLY AVERAGES — Health Dashboard', fontsize=16, fontweight='bold', y=0.98, color='#e0e0e0')

month_labels = mo["month"].dt.strftime("%Y\n%b")

# M1a: Sleep Duration
ax = axes[0, 0]
ax.bar(month_labels, mo["deep_sleep_duration_hours"], color='#1a237e', label='Deep')
ax.bar(month_labels, mo["light_sleep_duration_hours"], bottom=mo["deep_sleep_duration_hours"], color='#42a5f5', label='Light')
b2 = mo["deep_sleep_duration_hours"] + mo["light_sleep_duration_hours"]
ax.bar(month_labels, mo["rem_sleep_duration_hours"], bottom=b2, color='#ab47bc', label='REM')
ax.axhline(7, color='#66bb6a', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Hours')
ax.set_title('Avg Sleep Duration')
ax.legend(fontsize=7, ncol=3)
ax.set_ylim(0, 9)

# M1b: Sleep Efficiency
ax = axes[0, 1]
colors = mo["efficiency"].apply(lambda x: '#66bb6a' if x >= 85 else '#ffa726' if x >= 75 else '#ef5350')
ax.bar(month_labels, mo["efficiency"], color=colors, alpha=0.8)
ax.axhline(85, color='#ffa726', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('%')
ax.set_title('Avg Sleep Efficiency')
ax.set_ylim(70, 100)

# M1c: Steps
ax = axes[1, 0]
colors = mo["steps"].apply(lambda x: '#66bb6a' if x >= 10000 else '#ffa726' if x >= 7000 else '#ef5350')
ax.bar(month_labels, mo["steps"], color=colors, alpha=0.8)
ax.axhline(7000, color='#ffa726', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Steps')
ax.set_title('Avg Daily Steps')

# M1d: Active Calories
ax = axes[1, 1]
ax.bar(month_labels, mo["active_calories"], color='#ff7043', alpha=0.7)
ax.axhline(300, color='#ffa726', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('kcal')
ax.set_title('Avg Active Calories')

# M1e: Readiness Score
ax = axes[2, 0]
ax.bar(month_labels, mo["readiness_score"], color='#66bb6a', alpha=0.8)
ax.axhline(70, color='#ef5350', alpha=0.3, linestyle=':', linewidth=1)
ax.axhline(85, color='#66bb6a', alpha=0.3, linestyle=':', linewidth=1)
ax.set_ylabel('Score')
ax.set_title('Avg Readiness Score')
ax.set_ylim(60, 90)

# M1f: HRV
ax = axes[2, 1]
ax.bar(month_labels, mo["sleep_hrv_peak"], color='#66bb6a', alpha=0.4, label='Peak')
ax.bar(month_labels, mo["sleep_avg_hrv"], color='#4fc3f7', alpha=0.8, label='Avg')
ax.bar(month_labels, mo["sleep_hrv_min"], color='#ef5350', alpha=0.4, label='Min')
ax.legend(fontsize=7, ncol=3)
ax.set_ylabel('ms')
ax.set_title('Avg Sleep HRV')

# M1g: Stress vs Recovery
ax = axes[3, 0]
x_pos = np.arange(len(month_labels))
w = 0.35
ax.bar(x_pos - w/2, mo["stress_high_hours"], width=w, color='#ef5350', alpha=0.7, label='Stress')
ax.bar(x_pos + w/2, mo["recovery_high_hours"], width=w, color='#66bb6a', alpha=0.7, label='Recovery')
ax.set_xticks(x_pos)
ax.set_xticklabels(month_labels)
ax.legend(fontsize=7)
ax.set_ylabel('Hours')
ax.set_title('Avg Stress vs Recovery')

# M1h: Temperature + SpO2
ax = axes[3, 1]
ax.bar(month_labels, mo["temperature_deviation"],
       color=mo["temperature_deviation"].apply(
           lambda x: '#ef5350' if x > 0.1 else '#4fc3f7' if x < -0.1 else '#78909c'
       ), alpha=0.7, label='Temp Dev (°C)')
ax_twin = ax.twinx()
ax_twin.plot(month_labels, mo["spo2_avg"], color='#4fc3f7', linewidth=2, marker='o', markersize=6, label='SpO2 %')
ax_twin.set_ylabel('SpO2 %', color='#4fc3f7')
ax_twin.tick_params(axis='y', labelcolor='#4fc3f7')
ax_twin.set_ylim(95, 98)
ax.set_ylabel('°C')
ax.set_title('Avg Temp Deviation + SpO2')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax_twin.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, fontsize=7, loc='upper left')

fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(OUT, 'M1_monthly_dashboard.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print("✓ M1_monthly_dashboard.png")


# ── M2: Monthly Trends (line charts for trend visibility) ──
fig, axes = plt.subplots(4, 1, figsize=(16, 14), sharex=True)
fig.suptitle('MONTHLY TRENDS — Key Health Indicators', fontsize=14, fontweight='bold', y=0.98, color='#e0e0e0')

ax = axes[0]
ax.plot(mo["month"], mo["total_sleep_duration_hours"], color='#4fc3f7', linewidth=2.5, marker='s', markersize=8, label='Total Sleep')
ax.plot(mo["month"], mo["deep_sleep_duration_hours"], color='#1a237e', linewidth=2, marker='o', markersize=6, label='Deep')
ax.plot(mo["month"], mo["rem_sleep_duration_hours"], color='#ab47bc', linewidth=2, marker='o', markersize=6, label='REM')
ax.axhline(7, color='#66bb6a', alpha=0.3, linestyle=':', linewidth=1)
ax.legend(fontsize=8, ncol=3)
ax.set_ylabel('Hours')
ax.set_title('Sleep Duration Trends')

ax = axes[1]
ax.plot(mo["month"], mo["steps"], color='#ffa726', linewidth=2.5, marker='s', markersize=8, label='Steps')
ax_cal = ax.twinx()
ax_cal.plot(mo["month"], mo["active_calories"], color='#ff7043', linewidth=2, marker='o', markersize=6, label='Active Cal')
ax_cal.set_ylabel('kcal', color='#ff7043')
ax_cal.tick_params(axis='y', labelcolor='#ff7043')
ax.set_ylabel('Steps')
ax.set_title('Activity Trends')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax_cal.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc='upper left')

ax = axes[2]
ax.plot(mo["month"], mo["readiness_score"], color='#66bb6a', linewidth=2.5, marker='s', markersize=8, label='Readiness')
ax.plot(mo["month"], mo["activity_score"], color='#ffa726', linewidth=2, marker='o', markersize=6, label='Activity Score')
ax.axhline(70, color='#ef5350', alpha=0.3, linestyle=':', linewidth=1)
ax.legend(fontsize=8)
ax.set_ylabel('Score')
ax.set_title('Readiness & Activity Score Trends')
ax.set_ylim(60, 90)

ax = axes[3]
ax.plot(mo["month"], mo["sleep_avg_hrv"], color='#4fc3f7', linewidth=2.5, marker='s', markersize=8, label='HRV Avg')
ax_hr = ax.twinx()
ax_hr.plot(mo["month"], mo["sleep_lowest_hr"], color='#ef5350', linewidth=2, marker='o', markersize=6, label='Lowest HR')
ax_hr.set_ylabel('BPM', color='#ef5350')
ax_hr.tick_params(axis='y', labelcolor='#ef5350')
ax.set_ylabel('ms')
ax.set_title('HRV & Lowest Heart Rate Trends')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax_hr.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc='upper left')

axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b'))
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join(OUT, 'M2_monthly_trends.png'), dpi=150, bbox_inches='tight')
plt.close(fig)
print("✓ M2_monthly_trends.png")

print("\n✅ All weekly & monthly visualizations saved.")
