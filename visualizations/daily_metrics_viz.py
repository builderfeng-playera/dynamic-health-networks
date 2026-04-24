import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch
from datetime import datetime, timedelta

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

BASE = "/Users/shipeifeng/Oura ring_Structuredataset_modeling/raw_data"
OUT = "/Users/shipeifeng/Oura ring_Structuredataset_modeling/visualizations"

TENNIS_MATCHES = [
    ("2025-10-15", "vs Shushan Dai\n1-6, 7⁷-6⁵, 1¹⁰-0⁶ (W)"),
    ("2025-10-23", "vs Robert Mireles\n6-4, 6-2 (W)"),
    ("2025-10-25", "vs Nicholas Best\n3-6, 2-6 (L)"),
    ("2025-11-10", "vs Yingshan Zhao\n6-1, 2-6, 1¹⁰-0⁷ (W)"),
]

def load(name):
    with open(os.path.join(BASE, name)) as f:
        d = json.load(f)
    return d.get('data', [])

def add_tennis_markers(ax, y_pos=None):
    for date_str, label in TENNIS_MATCHES:
        d = pd.Timestamp(date_str)
        ax.axvline(d, color='#ff6b6b', alpha=0.7, linewidth=1.2, linestyle='--', zorder=5)

# ── Load all data ──
activity = pd.DataFrame(load("daily_activity.json"))
activity['day'] = pd.to_datetime(activity['day'])

readiness = pd.DataFrame(load("daily_readiness.json"))
readiness['day'] = pd.to_datetime(readiness['day'])

spo2 = pd.DataFrame(load("daily_spo2.json"))
spo2['day'] = pd.to_datetime(spo2['day'])

stress = pd.DataFrame(load("daily_stress.json"))
stress['day'] = pd.to_datetime(stress['day'])

hr_raw = load("heartrate.json")
hr_df = pd.DataFrame(hr_raw)
hr_df['timestamp'] = pd.to_datetime(hr_df['timestamp'])
hr_df['day'] = hr_df['timestamp'].dt.date

sleep_raw = load("sleep.json")
sleep = pd.DataFrame(sleep_raw)
sleep['day'] = pd.to_datetime(sleep['day'])
sleep_long = sleep[sleep['type'] == 'long_sleep'].copy()

# Extract HRV stats from sleep hrv.items
hrv_stats = []
for _, row in sleep_long.iterrows():
    hrv_data = row.get('hrv')
    if hrv_data and isinstance(hrv_data, dict) and hrv_data.get('items'):
        items = [x for x in hrv_data['items'] if x is not None]
        if items:
            hrv_stats.append({
                'day': row['day'],
                'hrv_peak': max(items),
                'hrv_min': min(items),
                'hrv_range': max(items) - min(items),
                'hrv_avg': np.mean(items),
            })
hrv_df = pd.DataFrame(hrv_stats)

# Aggregate heartrate by day and source
hr_daily = hr_df.groupby(['day', 'source'])['bpm'].agg(['mean', 'max', 'count']).reset_index()
hr_daily['day'] = pd.to_datetime(hr_daily['day'])

hr_awake = hr_daily[hr_daily['source'] == 'awake'][['day', 'mean']].rename(columns={'mean': 'hr_awake_avg'})
hr_workout = hr_daily[hr_daily['source'] == 'workout'][['day', 'mean', 'max']].rename(columns={'mean': 'hr_workout_avg', 'max': 'hr_workout_max'})

# Extract spo2 average
spo2['spo2_avg'] = spo2['spo2_percentage'].apply(
    lambda x: x.get('average') if isinstance(x, dict) else None
)

# Extract readiness contributors
readiness['recovery_index'] = readiness['contributors'].apply(
    lambda x: x.get('recovery_index') if isinstance(x, dict) else None
)

# ── FIGURE 1: Sleep Quality ──
fig1, axes1 = plt.subplots(5, 1, figsize=(20, 16), sharex=True)
fig1.suptitle('A. SLEEP QUALITY  (Day-to-Day)', fontsize=14, fontweight='bold', y=0.98, color='#4fc3f7')

# 1a: Sleep duration stacked
ax = axes1[0]
sl = sleep_long.sort_values('day')
deep_h = sl['deep_sleep_duration'] / 3600
light_h = sl['light_sleep_duration'] / 3600
rem_h = sl['rem_sleep_duration'] / 3600
awake_h = sl['awake_time'] / 3600
ax.bar(sl['day'], deep_h, color='#1a237e', label='Deep', width=0.8)
ax.bar(sl['day'], light_h, bottom=deep_h, color='#42a5f5', label='Light', width=0.8)
ax.bar(sl['day'], rem_h, bottom=deep_h + light_h, color='#ab47bc', label='REM', width=0.8)
ax.bar(sl['day'], awake_h, bottom=deep_h + light_h + rem_h, color='#ef5350', alpha=0.6, label='Awake', width=0.8)
ax.axhline(7, color='#66bb6a', alpha=0.5, linestyle=':', linewidth=1)
ax.axhline(9, color='#66bb6a', alpha=0.5, linestyle=':', linewidth=1)
ax.set_ylabel('Hours')
ax.set_title('Total Sleep Duration (stacked: Deep / Light / REM / Awake)')
ax.legend(loc='upper right', ncol=4, fontsize=8)
ax.set_ylim(0, 12)
add_tennis_markers(ax)

# 1b: Efficiency
ax = axes1[1]
ax.plot(sl['day'], sl['efficiency'], color='#4fc3f7', linewidth=1, alpha=0.5)
ax.scatter(sl['day'], sl['efficiency'], c=sl['efficiency'].apply(
    lambda x: '#66bb6a' if x >= 90 else '#ffa726' if x >= 80 else '#ef5350'
), s=12, zorder=5)
ax.axhline(85, color='#ffa726', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('%')
ax.set_title('Sleep Efficiency')
ax.set_ylim(50, 100)
add_tennis_markers(ax)

# 1c: Lowest HR during sleep
ax = axes1[2]
valid_lr = sl.dropna(subset=['lowest_heart_rate'])
ax.plot(valid_lr['day'], valid_lr['lowest_heart_rate'], color='#ef5350', linewidth=1, alpha=0.6)
ax.scatter(valid_lr['day'], valid_lr['lowest_heart_rate'], color='#ef5350', s=12, zorder=5)
ax.set_ylabel('BPM')
ax.set_title('Lowest Heart Rate During Sleep')
add_tennis_markers(ax)

# 1d: HRV (peak, min, range)
ax = axes1[3]
if not hrv_df.empty:
    ax.fill_between(hrv_df['day'], hrv_df['hrv_min'], hrv_df['hrv_peak'], alpha=0.2, color='#4fc3f7')
    ax.plot(hrv_df['day'], hrv_df['hrv_peak'], color='#66bb6a', linewidth=1, label='HRV Peak', alpha=0.8)
    ax.plot(hrv_df['day'], hrv_df['hrv_min'], color='#ef5350', linewidth=1, label='HRV Min', alpha=0.8)
    ax.plot(hrv_df['day'], hrv_df['hrv_avg'], color='#4fc3f7', linewidth=1.5, label='HRV Avg', alpha=0.9)
    ax.legend(loc='upper right', fontsize=8, ncol=3)
ax.set_ylabel('ms (rMSSD)')
ax.set_title('Sleep HRV (Peak / Avg / Min)')
add_tennis_markers(ax)

# 1e: Latency
ax = axes1[4]
latency_min = sl['latency'] / 60
ax.bar(sl['day'], latency_min, color='#7e57c2', alpha=0.7, width=0.8)
ax.axhline(20, color='#66bb6a', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Minutes')
ax.set_title('Sleep Latency (time to fall asleep)')
ax.set_ylim(0, 45)
add_tennis_markers(ax)

axes1[-1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
axes1[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
fig1.tight_layout(rect=[0, 0, 1, 0.96])
fig1.savefig(os.path.join(OUT, '01_sleep_quality.png'), dpi=150, bbox_inches='tight')
plt.close(fig1)
print("✓ 01_sleep_quality.png")

# ── FIGURE 2: Daily Activity ──
fig2, axes2 = plt.subplots(5, 1, figsize=(20, 16), sharex=True)
fig2.suptitle('B. DAILY ACTIVITY  (Day-to-Day)', fontsize=14, fontweight='bold', y=0.98, color='#ffa726')

act = activity.sort_values('day')

# 2a: Steps
ax = axes2[0]
colors = act['steps'].apply(lambda x: '#66bb6a' if x >= 10000 else '#ffa726' if x >= 7000 else '#ef5350')
ax.bar(act['day'], act['steps'], color=colors, alpha=0.8, width=0.8)
ax.axhline(7000, color='#ffa726', alpha=0.4, linestyle=':', linewidth=1)
ax.axhline(10000, color='#66bb6a', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Steps')
ax.set_title('Daily Steps')
add_tennis_markers(ax)

# 2b: Active Calories
ax = axes2[1]
ax.bar(act['day'], act['active_calories'], color='#ff7043', alpha=0.7, width=0.8)
ax.axhline(300, color='#ffa726', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('kcal')
ax.set_title('Active Calories')
add_tennis_markers(ax)

# 2c: Activity Score
ax = axes2[2]
ax.plot(act['day'], act['score'], color='#ffa726', linewidth=1, alpha=0.6)
ax.scatter(act['day'], act['score'], c=act['score'].apply(
    lambda x: '#66bb6a' if x >= 85 else '#ffa726' if x >= 70 else '#ef5350'
), s=12, zorder=5)
ax.axhline(85, color='#66bb6a', alpha=0.3, linestyle=':', linewidth=1)
ax.axhline(70, color='#ef5350', alpha=0.3, linestyle=':', linewidth=1)
ax.set_ylabel('Score')
ax.set_title('Activity Score')
ax.set_ylim(40, 100)
add_tennis_markers(ax)

# 2d: Sedentary Time
ax = axes2[3]
sed_h = act['sedentary_time'] / 3600
ax.bar(act['day'], sed_h, color='#78909c', alpha=0.7, width=0.8)
ax.axhline(8, color='#ef5350', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Hours')
ax.set_title('Sedentary Time')
add_tennis_markers(ax)

# 2e: Heart Rate (awake avg + workout avg/max)
ax = axes2[4]
if not hr_awake.empty:
    ax.plot(hr_awake['day'], hr_awake['hr_awake_avg'], color='#4fc3f7', linewidth=1, label='Awake Avg HR', alpha=0.8)
if not hr_workout.empty:
    ax.plot(hr_workout['day'], hr_workout['hr_workout_avg'], color='#ffa726', linewidth=1, label='Workout Avg HR', alpha=0.8)
    ax.plot(hr_workout['day'], hr_workout['hr_workout_max'], color='#ef5350', linewidth=1, label='Workout Max HR', alpha=0.6)
ax.legend(loc='upper right', fontsize=8, ncol=3)
ax.set_ylabel('BPM')
ax.set_title('Daily Heart Rate (Awake vs Workout)')
add_tennis_markers(ax)

axes2[-1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
axes2[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
fig2.tight_layout(rect=[0, 0, 1, 0.96])
fig2.savefig(os.path.join(OUT, '02_daily_activity.png'), dpi=150, bbox_inches='tight')
plt.close(fig2)
print("✓ 02_daily_activity.png")

# ── FIGURE 3: Recovery & Stress ──
fig3, axes3 = plt.subplots(4, 1, figsize=(20, 14), sharex=True)
fig3.suptitle('C. RECOVERY & STRESS  (Day-to-Day)', fontsize=14, fontweight='bold', y=0.98, color='#66bb6a')

rd = readiness.sort_values('day')
st = stress.sort_values('day')

# 3a: Readiness Score
ax = axes3[0]
ax.plot(rd['day'], rd['score'], color='#66bb6a', linewidth=1.5, alpha=0.8)
ax.fill_between(rd['day'], 0, rd['score'], alpha=0.1, color='#66bb6a')
ax.axhline(85, color='#66bb6a', alpha=0.3, linestyle=':', linewidth=1)
ax.axhline(70, color='#ef5350', alpha=0.3, linestyle=':', linewidth=1)
ax.set_ylabel('Score')
ax.set_title('Readiness Score')
ax.set_ylim(40, 100)
add_tennis_markers(ax)

# 3b: Temperature Deviation
ax = axes3[1]
ax.bar(rd['day'], rd['temperature_deviation'],
       color=rd['temperature_deviation'].apply(
           lambda x: '#ef5350' if x > 0.5 else '#4fc3f7' if x < -0.3 else '#78909c'
       ), alpha=0.7, width=0.8)
ax.axhline(0, color='#888888', alpha=0.5, linewidth=0.8)
ax.axhline(0.5, color='#ef5350', alpha=0.3, linestyle=':', linewidth=1)
ax.axhline(-0.5, color='#4fc3f7', alpha=0.3, linestyle=':', linewidth=1)
ax.set_ylabel('°C')
ax.set_title('Temperature Deviation from Baseline')
add_tennis_markers(ax)

# 3c: Stress vs Recovery (hours)
ax = axes3[2]
stress_h = st['stress_high'] / 3600
recovery_h = st['recovery_high'] / 3600
width = 0.4
ax.bar(st['day'] - pd.Timedelta(hours=5), stress_h, width=width, color='#ef5350', alpha=0.7, label='Stress High')
ax.bar(st['day'] + pd.Timedelta(hours=5), recovery_h, width=width, color='#66bb6a', alpha=0.7, label='Recovery High')
ax.legend(loc='upper right', fontsize=8)
ax.set_ylabel('Hours')
ax.set_title('Stress vs Recovery Time')
add_tennis_markers(ax)

# 3d: Day Summary as colored bars
ax = axes3[3]
summary_colors = st['day_summary'].map({
    'normal': '#4fc3f7',
    'stressful': '#ef5350',
    'restored': '#66bb6a',
}).fillna('#555555')
ax.bar(st['day'], 1, color=summary_colors, alpha=0.8, width=0.8)
ax.set_yticks([])
ax.set_title('Day Summary (blue=normal, red=stressful, green=restored, gray=N/A)')
add_tennis_markers(ax)

axes3[-1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
axes3[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
fig3.tight_layout(rect=[0, 0, 1, 0.96])
fig3.savefig(os.path.join(OUT, '03_recovery_stress.png'), dpi=150, bbox_inches='tight')
plt.close(fig3)
print("✓ 03_recovery_stress.png")

# ── FIGURE 4: SpO2 & Breathing ──
fig4, axes4 = plt.subplots(2, 1, figsize=(20, 7), sharex=True)
fig4.suptitle('D. BLOOD OXYGEN & BREATHING  (Day-to-Day)', fontsize=14, fontweight='bold', y=0.98, color='#4fc3f7')

sp = spo2.sort_values('day')

# 4a: SpO2
ax = axes4[0]
valid_spo2 = sp.dropna(subset=['spo2_avg'])
ax.plot(valid_spo2['day'], valid_spo2['spo2_avg'], color='#4fc3f7', linewidth=1, alpha=0.6)
ax.scatter(valid_spo2['day'], valid_spo2['spo2_avg'], c=valid_spo2['spo2_avg'].apply(
    lambda x: '#66bb6a' if x >= 96 else '#ffa726' if x >= 94 else '#ef5350'
), s=12, zorder=5)
ax.axhline(96, color='#66bb6a', alpha=0.3, linestyle=':', linewidth=1)
ax.axhline(94, color='#ef5350', alpha=0.3, linestyle=':', linewidth=1)
ax.set_ylabel('SpO2 %')
ax.set_title('Average Blood Oxygen During Sleep')
ax.set_ylim(93, 100)
add_tennis_markers(ax)

# 4b: Breathing Disturbance Index
ax = axes4[1]
valid_bdi = sp.dropna(subset=['breathing_disturbance_index'])
bdi_colors = valid_bdi['breathing_disturbance_index'].apply(
    lambda x: '#66bb6a' if x < 5 else '#ffa726' if x < 15 else '#ef5350'
)
ax.bar(valid_bdi['day'], valid_bdi['breathing_disturbance_index'], color=bdi_colors, alpha=0.7, width=0.8)
ax.axhline(5, color='#66bb6a', alpha=0.4, linestyle=':', linewidth=1)
ax.axhline(15, color='#ef5350', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Events/hour')
ax.set_title('Breathing Disturbance Index')
add_tennis_markers(ax)

axes4[-1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
axes4[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
fig4.tight_layout(rect=[0, 0, 1, 0.96])
fig4.savefig(os.path.join(OUT, '04_spo2_breathing.png'), dpi=150, bbox_inches='tight')
plt.close(fig4)
print("✓ 04_spo2_breathing.png")

# ── FIGURE 5: Menstrual Cycle Signals ──
fig5, axes5 = plt.subplots(5, 1, figsize=(20, 16), sharex=True)
fig5.suptitle('E. MENSTRUAL CYCLE SIGNALS  (Day-to-Day)', fontsize=14, fontweight='bold', y=0.98, color='#f48fb1')

# 5a: Temperature Deviation (primary cycle signal)
ax = axes5[0]
ax.plot(rd['day'], rd['temperature_deviation'], color='#f48fb1', linewidth=1.5, alpha=0.9)
ax.fill_between(rd['day'], 0, rd['temperature_deviation'],
                where=rd['temperature_deviation'] > 0, alpha=0.2, color='#ef5350')
ax.fill_between(rd['day'], 0, rd['temperature_deviation'],
                where=rd['temperature_deviation'] <= 0, alpha=0.2, color='#4fc3f7')
ax.axhline(0, color='#888888', alpha=0.5, linewidth=0.8)
ax.set_ylabel('°C')
ax.set_title('Temperature Deviation (♀ strongest cycle signal: luteal↑ / follicular↓)')
add_tennis_markers(ax)

# 5b: Temperature Trend
ax = axes5[1]
valid_trend = rd.dropna(subset=['temperature_trend_deviation'])
ax.plot(valid_trend['day'], valid_trend['temperature_trend_deviation'], color='#ce93d8', linewidth=1.5)
ax.axhline(0, color='#888888', alpha=0.5, linewidth=0.8)
ax.set_ylabel('°C')
ax.set_title('Temperature Trend Deviation (smoothed cycle pattern)')
add_tennis_markers(ax)

# 5c: HRV avg (inverse of temperature)
ax = axes5[2]
if not hrv_df.empty:
    ax.plot(hrv_df['day'], hrv_df['hrv_avg'], color='#4fc3f7', linewidth=1.5)
    ax.fill_between(hrv_df['day'], hrv_df['hrv_min'], hrv_df['hrv_peak'], alpha=0.15, color='#4fc3f7')
ax.set_ylabel('ms')
ax.set_title('Sleep HRV (♀ inverse of temp: luteal↓ / follicular↑)')
add_tennis_markers(ax)

# 5d: Lowest HR (same direction as temperature)
ax = axes5[3]
valid_lr = sl.dropna(subset=['lowest_heart_rate'])
ax.plot(valid_lr['day'], valid_lr['lowest_heart_rate'], color='#ef5350', linewidth=1.5)
ax.set_ylabel('BPM')
ax.set_title('Lowest Heart Rate During Sleep (♀ same as temp: luteal↑ / follicular↓)')
add_tennis_markers(ax)

# 5e: Deep Sleep + Breath Rate
ax2 = ax  # reuse
ax = axes5[4]
valid_breath = sl.dropna(subset=['average_breath'])
deep_h_valid = valid_breath['deep_sleep_duration'] / 3600
ax.bar(valid_breath['day'], deep_h_valid, color='#1a237e', alpha=0.6, width=0.8, label='Deep Sleep (h)')
ax_twin = ax.twinx()
ax_twin.plot(valid_breath['day'], valid_breath['average_breath'], color='#ffab91', linewidth=1.2, label='Breath Rate')
ax_twin.set_ylabel('breaths/min', color='#ffab91')
ax_twin.tick_params(axis='y', labelcolor='#ffab91')
ax.set_ylabel('Hours')
ax.set_title('Deep Sleep Duration + Breathing Rate')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax_twin.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=8)
add_tennis_markers(ax)

axes5[-1].xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
axes5[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
fig5.tight_layout(rect=[0, 0, 1, 0.96])
fig5.savefig(os.path.join(OUT, '05_menstrual_cycle.png'), dpi=150, bbox_inches='tight')
plt.close(fig5)
print("✓ 05_menstrual_cycle.png")

# ── FIGURE 6: Tennis Match Zoom (Oct 10 - Nov 15) ──
fig6, axes6 = plt.subplots(6, 1, figsize=(18, 18), sharex=True)
fig6.suptitle('F. TENNIS TOURNAMENT PERIOD  (Oct 10 → Nov 15, 2025)', fontsize=14, fontweight='bold', y=0.98, color='#ff6b6b')

t_start = pd.Timestamp('2025-10-10')
t_end = pd.Timestamp('2025-11-15')

act_t = act[(act['day'] >= t_start) & (act['day'] <= t_end)]
sl_t = sl[(sl['day'] >= t_start) & (sl['day'] <= t_end)]
rd_t = rd[(rd['day'] >= t_start) & (rd['day'] <= t_end)]
st_t = st[(st['day'] >= t_start) & (st['day'] <= t_end)]
hrv_t = hrv_df[(hrv_df['day'] >= t_start) & (hrv_df['day'] <= t_end)] if not hrv_df.empty else pd.DataFrame()
hr_aw_t = hr_awake[(hr_awake['day'] >= t_start) & (hr_awake['day'] <= t_end)]
hr_wo_t = hr_workout[(hr_workout['day'] >= t_start) & (hr_workout['day'] <= t_end)]

def add_tennis_full(ax):
    for date_str, label in TENNIS_MATCHES:
        d = pd.Timestamp(date_str)
        if t_start <= d <= t_end:
            ax.axvline(d, color='#ff6b6b', alpha=0.8, linewidth=2, linestyle='-', zorder=10)

# 6a: Steps + Active Calories
ax = axes6[0]
ax.bar(act_t['day'], act_t['steps'], color='#ffa726', alpha=0.7, width=0.8, label='Steps')
ax_cal = ax.twinx()
ax_cal.plot(act_t['day'], act_t['active_calories'], color='#ff7043', linewidth=2, marker='o', markersize=4, label='Active Cal')
ax_cal.set_ylabel('kcal', color='#ff7043')
ax_cal.tick_params(axis='y', labelcolor='#ff7043')
ax.set_ylabel('Steps')
ax.set_title('Steps & Active Calories')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax_cal.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)
add_tennis_full(ax)

# 6b: Heart Rate
ax = axes6[1]
if not hr_aw_t.empty:
    ax.plot(hr_aw_t['day'], hr_aw_t['hr_awake_avg'], color='#4fc3f7', linewidth=1.5, marker='o', markersize=3, label='Awake Avg')
if not hr_wo_t.empty:
    ax.plot(hr_wo_t['day'], hr_wo_t['hr_workout_avg'], color='#ffa726', linewidth=1.5, marker='o', markersize=3, label='Workout Avg')
    ax.plot(hr_wo_t['day'], hr_wo_t['hr_workout_max'], color='#ef5350', linewidth=1.5, marker='o', markersize=3, label='Workout Max')
ax.legend(loc='upper right', fontsize=8)
ax.set_ylabel('BPM')
ax.set_title('Heart Rate by Context')
add_tennis_full(ax)

# 6c: Readiness Score
ax = axes6[2]
ax.plot(rd_t['day'], rd_t['score'], color='#66bb6a', linewidth=2, marker='o', markersize=5)
ax.fill_between(rd_t['day'], 50, rd_t['score'], alpha=0.15, color='#66bb6a')
ax.axhline(70, color='#ef5350', alpha=0.4, linestyle=':', linewidth=1)
ax.set_ylabel('Score')
ax.set_title('Readiness Score')
ax.set_ylim(45, 95)
add_tennis_full(ax)

# 6d: Sleep HRV
ax = axes6[3]
if not hrv_t.empty:
    ax.fill_between(hrv_t['day'], hrv_t['hrv_min'], hrv_t['hrv_peak'], alpha=0.2, color='#4fc3f7')
    ax.plot(hrv_t['day'], hrv_t['hrv_peak'], color='#66bb6a', linewidth=1.5, marker='o', markersize=3, label='Peak')
    ax.plot(hrv_t['day'], hrv_t['hrv_avg'], color='#4fc3f7', linewidth=2, marker='o', markersize=4, label='Avg')
    ax.plot(hrv_t['day'], hrv_t['hrv_min'], color='#ef5350', linewidth=1.5, marker='o', markersize=3, label='Min')
    ax.legend(loc='upper right', fontsize=8, ncol=3)
ax.set_ylabel('ms')
ax.set_title('Sleep HRV (Peak / Avg / Min)')
add_tennis_full(ax)

# 6e: Sleep Duration + Lowest HR
ax = axes6[4]
valid_sl_t = sl_t.dropna(subset=['lowest_heart_rate'])
total_h = valid_sl_t['total_sleep_duration'] / 3600
ax.bar(valid_sl_t['day'], total_h, color='#42a5f5', alpha=0.5, width=0.8, label='Total Sleep (h)')
ax.axhline(7, color='#66bb6a', alpha=0.4, linestyle=':', linewidth=1)
ax_hr = ax.twinx()
ax_hr.plot(valid_sl_t['day'], valid_sl_t['lowest_heart_rate'], color='#ef5350', linewidth=2, marker='o', markersize=4, label='Lowest HR')
ax_hr.set_ylabel('BPM', color='#ef5350')
ax_hr.tick_params(axis='y', labelcolor='#ef5350')
ax.set_ylabel('Hours')
ax.set_title('Sleep Duration + Lowest Heart Rate')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax_hr.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)
add_tennis_full(ax)

# 6f: Stress vs Recovery
ax = axes6[5]
stress_h = st_t['stress_high'] / 3600
recovery_h = st_t['recovery_high'] / 3600
width = 0.35
ax.bar(st_t['day'] - pd.Timedelta(hours=4), stress_h, width=width, color='#ef5350', alpha=0.7, label='Stress')
ax.bar(st_t['day'] + pd.Timedelta(hours=4), recovery_h, width=width, color='#66bb6a', alpha=0.7, label='Recovery')
ax.legend(loc='upper right', fontsize=8)
ax.set_ylabel('Hours')
ax.set_title('Stress vs Recovery')
add_tennis_full(ax)

# Add match labels at top
for date_str, label in TENNIS_MATCHES:
    d = pd.Timestamp(date_str)
    axes6[0].annotate(label.split('\n')[0], xy=(d, axes6[0].get_ylim()[1]),
                      fontsize=7, color='#ff6b6b', ha='center', va='bottom',
                      rotation=0)

axes6[-1].xaxis.set_major_locator(mdates.DayLocator(interval=2))
axes6[-1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.setp(axes6[-1].xaxis.get_majorticklabels(), rotation=45)
fig6.tight_layout(rect=[0, 0, 1, 0.96])
fig6.savefig(os.path.join(OUT, '06_tennis_tournament.png'), dpi=150, bbox_inches='tight')
plt.close(fig6)
print("✓ 06_tennis_tournament.png")

print("\n✅ All 6 visualization files saved to:", OUT)
