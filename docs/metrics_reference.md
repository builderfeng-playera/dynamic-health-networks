# Oura Ring Metrics Reference

> For each metric: Calculation (how Oura computes it), Definition (what it means), Health Interpretation (what it tells you about your health).

---

## 1. Daily Activity

### Core Metrics

| Metric | Unit | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `score` | 0–100 | Weighted composite of 6 contributor sub-scores | Overall daily activity score — reflects how active, balanced, and consistent your movement was | **85–100**: Optimal, well-balanced. **70–84**: Good, minor room to improve. **<70**: Needs more movement or better distribution |
| `steps` | count | 3D accelerometer; proprietary algorithm distinguishes hand movement from actual walking/running steps | Total steps taken during the day | **<5,000**: Sedentary. **5,000–7,499**: Low active. **7,500–9,999**: Somewhat active. **10,000–12,499**: Active. **>12,500**: Highly active. Every +1,000 steps/day associated with reduced mortality |
| `active_calories` | kcal | Accelerometer + skin temperature sensor + metabolic algorithm; uses body metrics (age, weight, height, sex) and MET values | Calories burned through physical activity above basal metabolic rate (BMR) | Varies by individual. Active person: 300–500+ kcal/day. Track trends, not absolutes. Consistently very low = sedentary lifestyle |
| `total_calories` | kcal | BMR (Harris-Benedict equation from age/sex/height/weight) + active_calories | Total energy expenditure for the day (resting + activity) | Useful for nutrition planning. Represents your Total Daily Energy Expenditure (TDEE) |
| `target_calories` | kcal | Personalized daily active calorie goal based on recent activity patterns, readiness, and personal settings | Oura's recommended active calorie goal for the day | Dynamically adjusts — lower targets on recovery days is expected and healthy |

### Distance Metrics

| Metric | Unit | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `equivalent_walking_distance` | meters | Converts all activity (including non-step) into equivalent walking distance using accelerometer data | Total daily activity normalized to walking distance | **5,000–8,000m**: Moderate. **>10,000m**: Very active. Better for trend tracking |
| `target_meters` | meters | Personalized daily distance goal based on recent activity and readiness | Your daily distance target | Adjusts dynamically based on readiness |
| `meters_to_target` | meters | `target_meters - equivalent_walking_distance` (negative = exceeded goal) | How far you are from your daily goal | Negative = exceeded goal. Consistently hitting targets = good adherence |

### Time-by-Intensity Metrics

| Metric | Unit | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `high_activity_time` | seconds | Accelerometer; MET ≥ 5 (running, HIIT, etc.) | Time in vigorous activity | WHO recommends 75–150 min/week (~11–21 min/day). Any amount is beneficial |
| `medium_activity_time` | seconds | Accelerometer; MET 3–5 (brisk walking, cycling) | Time in moderate activity | WHO recommends 150–300 min/week (~21–43 min/day) |
| `low_activity_time` | seconds | Accelerometer; MET 1.5–3 (slow walking, housework) | Time in light activity | Still healthier than sedentary time. Important for metabolic health |
| `sedentary_time` | seconds | MET < 1.5 while awake; minimal movement | Awake time with very little physical activity | **>8 hours/day**: Associated with increased health risks regardless of exercise. Break up every 30–60 min |
| `resting_time` | seconds | Time in sleep or prolonged rest | Time sleeping or resting | Overlaps with sleep data |
| `non_wear_time` | seconds | No sensor data detected | Time the ring was not worn | High values = missing data, reduced accuracy |

### MET Metrics

| Metric | Unit | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `average_met_minutes` | MET | Average of all 1,440 per-minute MET values across the day | Average metabolic rate as a multiple of resting rate (1 MET = at rest) | **1.0**: Complete rest. **1.2–1.4**: Lightly active (desk worker). **1.5–1.7**: Moderately active. **1.8+**: Very active |
| `high_activity_met_minutes` | MET·min | Sum of per-minute MET values during high-intensity periods | Cumulative "exercise dose" at vigorous intensity | WHO recommends 500–1,000 MET-minutes/week total moderate+vigorous |
| `medium_activity_met_minutes` | MET·min | Sum of per-minute MET values during moderate-intensity periods | Cumulative exercise dose at moderate intensity | MET-minutes capture "dose" better than time alone (10 min running > 10 min walking) |
| `low_activity_met_minutes` | MET·min | Sum of per-minute MET values during light-intensity periods | Cumulative dose at light intensity | Contributes to overall health even if not vigorous |
| `sedentary_met_minutes` | MET·min | Sum of per-minute MET values during sedentary periods | Very low intensity cumulative dose | Minimal contribution to health |

### Other Fields

| Metric | Type | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `inactivity_alerts` | count | Counts ~50+ continuous minutes of sitting during daytime | Number of prolonged inactivity bouts detected | **0**: Great. **1–2**: Normal for desk work. **3+**: High sedentary behavior |
| `class_5_min` | string (288 chars) | Each character = 5-min block classified by accelerometer intensity | Activity classification per 5-min block: 0=rest, 1=sedentary, 2=light, 3=moderate, 4=high, 5=non-wear | Ideally shows distributed movement throughout day, not long sedentary blocks |
| `met.items` | list[1440] | Per-minute MET from accelerometer | Time series of metabolic intensity for every minute of the day | MET 1.0=rest, 3.0=walking, 6.0+=vigorous. Ideal: regular movement, not one burst |

### Activity Score Contributors

| Contributor | Calculation | Definition | Health Interpretation |
|-------------|-------------|------------|----------------------|
| `meet_daily_targets` | % of personalized daily goals achieved | How close you came to your activity goals | Consistently >80 = sustainable habits |
| `move_every_hour` | Counts waking hours with at least some movement | How evenly distributed your movement is throughout the day | **>85**: Avoiding prolonged sitting. Light movement every hour significantly reduces sedentary risks |
| `recovery_time` | Compares activity to recent recovery needs | Whether you balanced intense activity with appropriate rest | **>90**: Good recovery habits. Low = possible overtraining |
| `stay_active` | Total daily movement time and intensity vs. recommendations | Overall daily activity level | Aim for >70. Captures total activity "dose" |
| `training_frequency` | Days with moderate-to-vigorous exercise in recent period | How consistently you've been exercising | **>85**: Consistent training. WHO recommends activity on most days |
| `training_volume` | Total training load (duration × intensity) over recent days | Total recent training combining duration and intensity | **80–100**: Optimal. Very high = overtraining risk. Very low = insufficient |

---

## 2. Daily Readiness

### Core Metrics

| Metric | Unit | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `score` | 0–100 | Weighted composite of 9 contributor sub-scores; combines sleep quality, HRV, resting HR, body temperature, recent activity | How recovered your body is and how ready for physical/mental demands | **85–100**: Well-recovered, good for challenging workouts. **70–84**: Adequate, normal activity fine. **<70**: Body needs rest. Consistently low may indicate chronic stress, overtraining, or illness onset |
| `temperature_deviation` | °C | NTC thermistor on ring's inner surface; measures palmar skin temperature during sleep; reports deviation from 2-week personal baseline | How much nighttime skin temperature deviates from your personal baseline | **±0.0–0.5°C**: Normal fluctuation. **+0.5–1.0°C**: Mild elevation (illness onset, menstrual cycle, alcohol). **>+1.0°C**: Significant — often illness/inflammation. Can predict COVID symptoms up to 3 days early. Negative = cold room or caloric restriction |
| `temperature_trend_deviation` | °C | Smoothed moving average of temperature_deviation over several days; highlights meaningful shifts vs. noise | Temperature deviation from recent trend (not absolute baseline) | Sustained upward trend over 2–3 days is more significant than single-day spike. Returning to zero suggests recovery |

### Readiness Contributors

| Contributor | Calculation | Definition | Health Interpretation |
|-------------|-------------|------------|----------------------|
| `activity_balance` | Compares 5–7 day activity level against long-term average | Whether recent activity is sustainable vs. your norm | **>85**: Well-balanced. **<60**: Significant imbalance — overtraining or sudden drop. Helps prevent overtraining syndrome |
| `body_temperature` | Derived from temperature_deviation; closer to baseline = higher score | How close nighttime temperature is to your baseline | **>90**: Normal. **70–90**: Slight change (environment, mild stress). **<70**: Notable deviation (illness, hormonal changes) |
| `hrv_balance` | Compares current sleep HRV (RMSSD via PPG) against 2-week rolling average | How your current HRV compares to your recent personal average | **>85**: At/above average, well-recovered. **<60**: Significantly below — stress, illness, overtraining, alcohol. HRV is highly individual — only compare to your own baseline |
| `previous_day_activity` | Evaluates yesterday's MET-minutes relative to optimal recovery level | Whether yesterday's activity set you up for recovery | **>85**: Appropriate. **<60**: Yesterday was likely too intense, impeding recovery |
| `previous_night` | Based on total sleep duration, efficiency, sleep stages, timing | How well you slept the previous night | **>85**: Good sleep supporting recovery. **<60**: Poor sleep significantly impacting readiness |
| `recovery_index` | Measures how quickly resting HR reaches its lowest point during sleep; early = high score | How efficiently your cardiovascular system recovered during sleep | **>85**: HR dropped quickly — efficient recovery. **<60**: HR stayed elevated — common causes: late exercise, alcohol, late heavy meals, high stress. One of the most actionable metrics |
| `resting_heart_rate` | Compares nighttime lowest sustained HR (PPG) against personal baseline | How your sleep resting HR compares to your average | **>85**: At/below average — good recovery. **<60**: Notably elevated — illness, stress, alcohol, dehydration. Long-term decreasing trend = improving fitness |
| `sleep_balance` | 2-week rolling average of sleep duration vs. sleep need (7–9h); weights recent nights more | Whether you've been getting enough sleep over 2 weeks | **>85**: Meeting sleep needs consistently. **<60**: Significant cumulative sleep debt. Performance, mood, immunity may be impaired |
| `sleep_regularity` | Standard deviation of bedtime/wake times over 2 weeks | How consistent your sleep schedule has been | **>85**: Very consistent, supports circadian rhythm. **<70**: Irregular — risk of social jet lag and cardiometabolic issues |

---

## 3. Daily SpO2

| Metric | Unit | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `spo2_percentage.average` | % | PPG with red and infrared LEDs; ratio of oxygenated to deoxygenated hemoglobin via Beer-Lambert law; measured during sleep | Average blood oxygen saturation during sleep | **96–100%**: Normal. **94–95%**: Below average — may indicate mild sleep-disordered breathing. **<94%**: Abnormal — consult healthcare provider (sleep apnea, respiratory issues). SpO2 naturally dips slightly during sleep |
| `breathing_disturbance_index` | events/hour | PPG signal analysis + accelerometer motion during sleep; detects pauses, shallow breathing, respiratory effort-related arousals | Average breathing disturbances per hour of sleep (similar to clinical AHI but NOT diagnostic) | **<5**: Normal. **5–15**: Mild, may not be clinically significant. **15–30**: Moderate — consider discussing with doctor. **>30**: Severe — strongly recommend medical evaluation for sleep apnea. Factors: sleeping on back, alcohol, nasal congestion, obesity, aging. NOT a medical diagnosis — needs polysomnography for confirmation |

---

## 4. Daily Stress

| Metric | Unit | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `stress_high` | seconds | Continuous daytime HRV via PPG; frequency-domain analysis (LF/HF ratio); high sympathetic dominance = stress | Total time in high-stress physiological state (sympathetic nervous system dominance) | **<3,600s (<1h)**: Low stress. **3,600–7,200s (1–2h)**: Moderate, normal for active days. **>7,200s (>2h)**: High — consider stress management. Note: workouts also trigger sympathetic activation. Chronic high = burnout risk |
| `recovery_high` | seconds | Same HRV analysis; identifies parasympathetic (rest & digest) dominance — high HRV, low LF/HF | Total time in high-recovery state (parasympathetic dominant) | **>5,400s (>1.5h)**: Good daily recovery. **1,800–5,400s (0.5–1.5h)**: Moderate. **<1,800s (<30min)**: Low — body spent little time restoring. The stress/recovery balance matters more than absolute values |
| `day_summary` | category | Classified by ratio of stress_high vs. recovery_high | Categorical day summary | **"restored"**: Recovery >> stress (parasympathetic dominant). **"normal"**: Balanced. **"stressful"**: Stress >> recovery. **null**: Insufficient data. Ideal week: mostly normal, some restored, occasional stressful. Consistently stressful (>50% of week) suggests chronic stress |

---

## 5. Heartrate

| Metric | Unit | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `bpm` | beats/min | PPG (green + red LEDs); detects blood volume changes per heartbeat via light absorption; continuous sampling, reported every ~5 min at rest, more frequently during workouts | Instantaneous heart rate | **Resting (awake)**: 60–100 normal. <60 may indicate athletic fitness or bradycardia. >100 may indicate tachycardia, stress, caffeine. **Sleep**: 40–70 typical. Lower = better fitness/recovery. **Exercise**: Varies by intensity. Max HR ≈ 220 minus age |
| `source` | category | Context-classified by Oura: `rest` (during sleep), `awake` (daytime non-exercise), `workout` (exercise sessions), `live` (user-requested real-time) | The context in which HR was measured | `rest` readings most important for recovery tracking. `workout` informs training intensity. `awake` provides daytime baseline. Comparing across sources builds complete cardiovascular picture |
| `timestamp` | ISO 8601 | Recorded at moment of measurement with timezone | Exact time of HR reading | Enables temporal analysis — tracking patterns across day, sleep, exercise, and long-term trends |

---

## 6. Sleep

### Duration Metrics

| Metric | Unit | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `total_sleep_duration` | seconds | Sum of all time in any sleep stage (light + deep + REM); detected via PPG, accelerometer, temperature sensor | Total time actually asleep (excludes awake time) | **7–9h (25,200–32,400s)**: Recommended (NSF). **6–7h**: Borderline. **<6h**: Insufficient — impaired cognition, weakened immunity, cardiovascular risk. **>9h**: May indicate illness or depression if chronic |
| `deep_sleep_duration` | seconds | Time in NREM Stage 3 (slow-wave sleep); identified via very low HR, minimal movement, characteristic autonomic patterns | Duration of deepest, most restorative sleep stage | **1–2h (3,600–7,200s)**: Normal/optimal. **<1h**: Below average — alcohol, aging, late caffeine, or environment. Critical for: physical recovery, immune function, growth hormone, memory consolidation. Mostly occurs in first half of night |
| `light_sleep_duration` | seconds | Time in NREM Stages 1–2; intermediate HR, some movement, moderate HRV | Duration of lighter sleep stages | Typically 50–60% of total sleep (**3–5h**). Not "bad" — necessary for memory and motor skill processing |
| `rem_sleep_duration` | seconds | Time in REM; identified via increased/variable HR, irregular HRV, muscle atonia | Duration of REM sleep (dreaming, emotional processing) | **1.5–2.5h (5,400–9,000s)**: Normal (~20–25% of total). **<1h**: Low — alcohol, medications (antidepressants suppress REM), or fragmented sleep. Critical for: emotional regulation, creativity, learning. Cutting sleep short disproportionately reduces REM |
| `awake_time` | seconds | Total time awake during sleep period; detected via accelerometer + HR/HRV patterns | Cumulative time awake between bedtime_start and bedtime_end | **<30 min (1,800s)**: Normal. **30–60 min**: Moderate. **>60 min**: High — may indicate sleep maintenance insomnia, sleep apnea, or environmental disturbances |
| `time_in_bed` | seconds | Duration from bedtime_start to bedtime_end | Entire time in bed including awake time | Should be close to total_sleep_duration + reasonable latency. Large gap = poor efficiency. Excessive time in bed awake can paradoxically worsen insomnia (CBT-I) |
| `latency` | seconds | Time from bedtime_start to first detected sleep epoch | How long it took to fall asleep | **5–20 min (300–1,200s)**: Optimal. **<5 min**: May indicate sleep deprivation. **>20 min**: Caffeine, stress, poor sleep hygiene. **>45 min**: Clinically significant — may warrant insomnia evaluation |

### Quality Metrics

| Metric | Unit | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `efficiency` | % | `(total_sleep_duration / time_in_bed) × 100` | Percentage of time in bed actually spent sleeping | **>90%**: Excellent. **85–90%**: Good (normal). **75–85%**: Below average. **<75%**: Poor — may indicate insomnia or fragmentation. Clinical threshold: 85% |
| `restless_periods` | count | Distinct clusters of movements detected by accelerometer indicating partial awakenings | Number of restless episodes during sleep | Fewer = more consolidated, higher-quality sleep. High counts may indicate: discomfort, pain, sleep apnea, stress. Track trends |

### Physiological Metrics During Sleep

| Metric | Unit | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `average_heart_rate` | BPM | Mean of PPG-measured HR at 5-min intervals during sleep | Average heart rate during sleep | Typically 8–15 BPM below daytime resting HR. **<60**: Common for fit individuals. **60–70**: Normal. **>70**: Elevated — poor recovery, illness, stress, alcohol, late exercise. Rising trend = declining fitness or increasing stress |
| `lowest_heart_rate` | BPM | Minimum HR value from heart_rate.items time series during sleep | Lowest heart rate reached, typically during deep sleep | Represents peak parasympathetic activation. Generally 10–20 BPM below average sleep HR. Lower (vs. personal baseline) = better recovery. Elevated = alcohol, late exercise, illness, stress |
| `average_hrv` | ms | Average RMSSD (Root Mean Square of Successive Differences) from PPG inter-beat intervals at 5-min intervals | Average heart rate variability during sleep | Highly individual (age, fitness, genetics). **Approx by age**: 20s: 40–80ms, 30s: 35–65ms, 40s: 25–55ms, 50+: 20–45ms. Higher than personal baseline = good recovery. Lower = stress, illness, overtraining, alcohol. One of the most sensitive recovery indicators |
| `average_breath` | breaths/min | Extracted from respiratory modulation of PPG waveform | Average breathing rate during sleep | **12–20**: Normal. **<12**: Fine for fit individuals. **>20**: Elevated — respiratory issues, anxiety, illness. Sudden changes from baseline are most informative |

### Time Series Data

| Metric | Type | Calculation | Definition | Health Interpretation |
|--------|------|-------------|------------|----------------------|
| `heart_rate.items` | list (5-min intervals) | PPG-derived HR sampled every 5 min through sleep | HR time series throughout the night | Should show "hammock" pattern: drops in first half, reaches minimum in deep sleep, gradually rises toward morning. Late-night spikes indicate poor recovery events |
| `hrv.items` | list (5-min intervals) | RMSSD from PPG at 5-min intervals | HRV time series throughout the night | Inverse of HR: should rise in first half, peak during deep sleep. Disruptions (dips) indicate alcohol, late meals, stress |
| `movement_30_sec` | string | Each char = 30-sec epoch from accelerometer | Movement intensity per 30 seconds: 1=still, 2=minor, 3=moderate/restless, 4=significant/likely awake | Long stretches of `1` = consolidated sleep. Clusters of `3`–`4` = restless or awakenings |
| `sleep_phase_5_min` | string | Each char = sleep stage per 5-min epoch from HR/HRV/movement/temperature algorithm | Sleep stage classification: 1=deep, 2=light, 3=REM, 4=awake | Healthy architecture: deep sleep early in night, REM lengthening in second half. 4–6 complete cycles (~90 min each) is typical |
| `sleep_phase_30_sec` | string | Same as above but at 30-sec granularity | Granular sleep stage classification | Same encoding as 5-min version. Provides more detailed view |

### Metadata Fields

| Metric | Type | Definition | Notes |
|--------|------|------------|-------|
| `type` | string | `long_sleep` (primary, >3h), `sleep` (naps, <3h), `late_nap` (after ~6 PM) | Most records should be long_sleep. Late naps can disrupt nighttime sleep |
| `period` | int | Index (0-based) for multiple sleep periods in one day | Multiple periods = polyphasic sleep or napping |
| `bedtime_start` / `bedtime_end` | ISO 8601 | Detected bed and wake times with timezone | Consistency matters — >1h variation between days disrupts circadian rhythm. Earlier bedtimes generally = more deep sleep |
| `readiness` | object | Embedded readiness score + 9 contributors for this sleep period | Same interpretation as Daily Readiness |
| `sleep_score_delta` / `readiness_score_delta` | int | Score adjustments from algorithmic refinements | Usually 0. Non-zero = minor adjustments |
| `sleep_algorithm_version` | string | Algorithm version (e.g., "v2") | Scores most comparable within same version |
| `low_battery_alert` | bool | Ring battery was low during sleep | If true, data may be incomplete or less accurate |
| `app_sleep_phase_5_min` | string | App-displayed sleep phases (may differ from raw) | May include app-side corrections |

---

## 7. VO2 Max

**Status: No data available.** API returned `{"detail": "Not Found"}`.

VO2 Max is the maximum rate of oxygen consumption during exercise. Oura estimates it from walking/running activities using HR response, but requires sufficient workout data to compute. This dataset is empty — likely insufficient qualifying workouts were recorded.
