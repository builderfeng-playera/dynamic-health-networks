# Patterns & Observations — 7-Month Oura Ring Analysis

> Data period: Sep 8, 2025 → Apr 13, 2026 (217 days, 168 usable "normal confidence" days)

---

## A. Sleep Quality

### Observations

- Sleep duration fluctuates significantly, with a majority of nights falling below the 7-hour recommendation
- Sleep efficiency is generally good (85%+) with occasional dips
- HRV peak/min band is clearly visible, with a slight upward trend in recent months

### Supporting Metrics

| Metric | Value |
|--------|-------|
| Mean total sleep | **6.76h** (std = 1.00h) |
| Nights below 7h | **56.2%** |
| Nights below 6h | **25.3%** |
| Nights above 8h | **10.5%** |
| Mean deep sleep | **1.19h** (17.9% of total) |
| Mean REM sleep | **1.85h** (27.3% of total) |
| Mean sleep efficiency | **89.6%** |
| Efficiency below 85% | **11.7%** of nights |
| Efficiency below 75% | **1.2%** of nights |
| Mean sleep latency | **11.6 min** |
| Latency above 20 min | **7.4%** of nights |
| Mean lowest HR | **57.6 BPM** (std = 3.5) |
| Mean HRV (rMSSD) | **31.3 ms** (std = 6.3) |
| Mean HRV peak | **53.7 ms** |
| Mean HRV min | **16.6 ms** |
| Mean HRV range (peak − min) | **37.0 ms** |
| HRV trend: first half avg | **31.8 ms** |
| HRV trend: second half avg | **30.8 ms** |
| Nap frequency | **35.2%** of days |
| Mean nap duration | **0.68h** (41 min) |

### Key Patterns

1. **More than half of nights are below 7 hours** — this is the single most consistent deficit. Deep sleep (17.9%) is slightly below the 20% optimal target; REM (27.3%) is above the 20-25% range, suggesting adequate cognitive recovery even on shorter nights.

2. **HRV range averaging 37 ms** (peak 54, min 17) indicates substantial within-night autonomic variability. This is normal but the wide band suggests some nights have significantly suppressed HRV troughs.

3. **Napping on 35% of days** with average 41 min — this supplements the short primary sleep. November had the highest nap rate (54%), coinciding with the post-competition deceleration.

---

## B. Daily Activity

### Observations

- Step distribution is uneven: few days above 10k, many below 7k
- Heart rate data is concentrated on workout days with clear intensity peaks
- Sedentary time exceeds 8 hours on nearly all days

### Supporting Metrics

| Metric | Value |
|--------|-------|
| Mean daily steps | **7,056** (median = 6,585, std = 3,566) |
| Days < 5,000 steps | **32.1%** |
| Days 5,000–7,000 | **20.8%** |
| Days 7,000–10,000 | **26.8%** |
| Days > 10,000 | **20.2%** |
| Mean active calories | **318 kcal** |
| Mean activity score | **78.8 / 100** |
| Activity score below 70 | **15.5%** of days |
| Mean sedentary time | **11.2 hours** |
| Days with sedentary > 8h | **94.6%** |
| Mean high-intensity time | **4.8 min/day** |
| Mean moderate-intensity time | **44.1 min/day** |
| Mean awake HR | **76.8 BPM** |
| Mean workout HR | **99.2 BPM** |
| Mean workout max HR | **124.2 BPM** |
| Days with workout data | **95.2%** |

### Key Patterns

1. **Steps follow a bimodal distribution** — roughly one-third of days are sedentary (<5k) and one-fifth are highly active (>10k), with relatively few "moderate" days. The coefficient of variation (51%) is very high, indicating an inconsistent activity pattern.

2. **94.6% of days exceed 8 hours sedentary** — this is the most persistent health risk signal in the entire dataset. Average sedentary time of 11.2h means the majority of waking hours are spent sitting.

3. **High-intensity activity averages only 4.8 min/day** — well below WHO's recommendation of 11-21 min/day of vigorous activity. Moderate activity (44 min) meets the guideline floor of 21-43 min/day.

---

## C. Recovery & Stress

### Observations

- Readiness score mostly ranges 70-85, relatively stable
- Temperature deviation shows cyclical fluctuation (menstrual cycle signal)
- Day Summary color band reveals stressful day clusters

### Supporting Metrics

| Metric | Value |
|--------|-------|
| Mean readiness score | **77.8** (std = 7.4) |
| Readiness ≥ 85 | **21.0%** of days |
| Readiness < 70 | **12.4%** of days |
| Mean temperature deviation | **+0.05°C** (std = 0.26) |
| Mean stress time | **2.07 hours/day** |
| Mean recovery time | **1.66 hours/day** |
| Mean stress/recovery ratio | **2.22** (stress-dominant) |
| Day summary: normal | **75.0%** |
| Day summary: stressful | **17.5%** |
| Day summary: restored | **7.5%** |
| Mean recovery index (contributor) | **65.8 / 100** |

**Stress/Recovery ratio by month:**

| Month | Stress (h) | Recovery (h) | Ratio |
|-------|-----------|-------------|-------|
| Sep 2025 | 2.1 | 0.8 | **2.64** |
| Oct 2025 | 1.6 | 2.1 | **0.75** ← only recovery-dominant month |
| Nov 2025 | 2.2 | 1.7 | 1.32 |
| Dec 2025 | 2.4 | 1.4 | 1.63 |
| Jan 2026 | 2.1 | 1.8 | 1.19 |
| Feb 2026 | 1.8 | 1.7 | **1.01** ← near-balance |
| Apr 2026 | 3.2 | 1.1 | **2.89** ← highest |

### Key Patterns

1. **Chronic stress dominance** — 6 of 7 months had stress > recovery. The only exception was October (competition month), when structured physical exertion may have activated parasympathetic recovery more effectively than non-competition days.

2. **Recovery index is the weakest readiness contributor** at 65.8/100 — this measures how quickly resting HR stabilizes during sleep. It suggests evening behaviors (late meals, exercise, or screen time) are delaying cardiovascular recovery.

3. **December 21st was the single worst day in 7 months** — a multi-system convergence:

| Metric | Dec 21 | 7-Month Mean | Deviation |
|--------|--------|-------------|-----------|
| Readiness | **50** | 77.8 | **3.7σ** below |
| HRV | **13 ms** | 31.3 | **2.9σ** below |
| Lowest HR | **76 BPM** | 57.6 | **5.3σ** above |
| Stress | **6.75h** | 2.07 | **3.2σ** above |

---

## D. Blood Oxygen & Breathing

### Observations

- SpO2 is stable at 95-98%, very healthy
- Breathing disturbance index mostly falls in the 5-15 range (mild)

### Supporting Metrics

| Metric | Value |
|--------|-------|
| Mean SpO2 | **96.5%** (std = 0.64) |
| SpO2 below 95% | **0.0%** of nights |
| Mean breathing disturbance index | **8.6 events/h** (std = 4.6) |
| BDI < 5 (normal) | **23.4%** of nights |
| BDI 5-15 (mild) | **64.6%** |
| BDI > 15 (moderate+) | **12.0%** |
| BDI first half (Sep-Dec) | **10.8 events/h** |
| BDI second half (Jan-Apr) | **6.4 events/h** |
| BDI improvement | **−40.5%** |

### Key Patterns

1. **SpO2 is clinically normal** with zero nights below 95%. No respiratory concern signals.

2. **Breathing disturbance index improved 40.5%** — from 10.8 to 6.4 events/hour. This is the most significant sustained improvement across all metrics. The shift moved the distribution from predominantly "mild" toward "normal." Possible contributing factors: change in sleep position, nasal breathing practice, weight change, or reduced alcohol intake.

---

## E. Menstrual Cycle Signals

### Observations

- Temperature deviation shows a clear cyclical waveform with ~28-day periodicity
- HRV and lowest HR show expected inverse/same-direction relationships with temperature
- Breathing rate also shows mild cyclical variation

### Supporting Metrics

| Metric | Value |
|--------|-------|
| Temp autocorrelation at lag 14 | **r = −0.33** (anti-phase: opposite half of cycle) |
| Temp autocorrelation at lag 28 | **r = +0.33** (full cycle: signal repeats) |
| Temp ↔ HRV correlation | **r = −0.32** (inverse: temp↑ = HRV↓) |
| Temp ↔ Lowest HR correlation | **r = +0.42** (same direction: temp↑ = HR↑) |
| Temp ↔ Breathing rate correlation | **r = +0.42** (same direction: temp↑ = breath↑) |

### Key Patterns

1. **Autocorrelation confirms ~28-day periodicity** — the negative peak at lag 14 (r = −0.33) and positive peak at lag 28 (r = +0.33) form the classic menstrual cycle signature. Temperature rises ~0.2-0.5°C during the luteal phase (post-ovulation) and returns to baseline during follicular phase.

2. **Three physiological signals co-oscillate with the cycle:**
   - Temperature ↑ → HRV ↓ (r = −0.32): progesterone increases sympathetic tone
   - Temperature ↑ → Resting HR ↑ (r = +0.42): same mechanism
   - Temperature ↑ → Breathing rate ↑ (r = +0.42): progesterone stimulates respiratory drive

3. **The 7-day smoothed temperature line shows 5-6 clear wave cycles** across the data period, visible in the P3 and P5 visualizations. This is consistent with a regular menstrual cycle with minimal disruption.

---

## F. Tennis Tournament (Oct 10 → Nov 15)

### Observations

- Match days show clear spikes in steps and active calories
- Workout max HR reaches peak values (150+ BPM) on match days
- Oct 25 back-to-back match shows readiness decline
- Post-match HRV shows a temporary dip

### Supporting Metrics

**Match day vs post-match vs normal day comparison:**

| Metric | Match Day | Post-Match | Normal Day | Match vs Normal |
|--------|-----------|-----------|------------|-----------------|
| Steps | **11,040** | 6,171 | 7,014 | **+57%** |
| Active calories | **738 kcal** | 361 | 307 | **+140%** |
| Workout avg HR | **108.9 BPM** | 102.5 | 98.9 | +10% |
| Workout max HR | **149.0 BPM** | 124.2 | 123.7 | **+20%** |
| Readiness score | 79.0 | **70.8** | 77.8 | — |
| Sleep HRV | **27.8 ms** | **27.0 ms** | 31.5 | −12% / −14% |
| Lowest HR | 57.5 | **58.8** | 57.6 | — |
| Stress time | **3.19h** | 1.19 | 2.09 | +53% |

**Individual match details:**

| Date | Opponent | Score | Sets | Result | Steps | Active Cal |
|------|----------|-------|------|--------|-------|-----------|
| Oct 15 (6:55 PM) | Shushan Dai | 1-6, 7⁷-6⁵, 1¹⁰-0⁶ | 3 | W | 11,291 | — |
| Oct 23 (5:46 PM) | Robert Mireles | 6-4, 6-2 | 2 | W | 8,603 | — |
| Oct 25 (8:30 AM) | Nicholas Best | 3-6, 2-6 | 2 | L | 12,283 | — |
| Nov 10 (9:52 PM) | Yingshan Zhao | 6-1, 2-6, 1¹⁰-0⁷ | 3 | W | 11,981 | — |

### Key Patterns

1. **Match days generate 2.4x the calorie burn** (738 vs 307 kcal) and 57% more steps than normal days. Workout max HR reaches 149 BPM vs 124 BPM baseline — a clear high-intensity signature.

2. **Post-match recovery cost is real:**
   - Readiness drops to **70.8** (−9% from normal)
   - HRV suppressed to **27.0 ms** (−14% from normal)
   - Lowest HR elevated to **58.8 BPM** (+1.2 above normal)
   - These effects are visible in the day after every match.

3. **The Oct 23 → Oct 25 back-to-back** was physiologically costly — only 36 hours between matches with insufficient recovery. The Oct 25 match was the only loss, played at 8:30 AM morning slot after an evening match two days prior.

4. **Late-night matches show compounded impact** — Oct 15 (6:55 PM) and Nov 10 (9:52 PM) were both 3-set matches ending late. Late exercise delays the recovery index (heart rate takes longer to reach its overnight minimum), which cascades into lower readiness the next day.

---

## Cross-Cutting Patterns

### Strongest Correlations

| Relationship | r | Interpretation |
|-------------|---|----------------|
| HRV → Readiness (same day) | **+0.64** | HRV is the single best predictor of readiness |
| Stress today → HRV tonight | **−0.43** | High-stress days suppress that night's HRV |
| Temperature → Readiness | **−0.31** | Elevated temperature (luteal phase, illness) lowers readiness |

### Decreasing Volatility Over Time

Readiness score coefficient of variation by month:

| Period | CV% | Interpretation |
|--------|-----|----------------|
| Sep 2025 | 10.2% | High variability (new device, establishing baseline) |
| Oct 2025 | 7.7% | Moderate (competition period) |
| Nov 2025 | 11.0% | High (post-competition adjustment) |
| Dec 2025 | 11.0% | High (crisis month) |
| Jan 2026 | 7.2% | Stabilizing |
| Feb 2026 | 6.5% | Stable |
| Mar 2026 | 6.1% | Most stable |
| Apr 2026 | 6.2% | Stable |

**The body's day-to-day autonomic swings halved** from ~11% CV to ~6% CV over 7 months, indicating increasing physiological regulation.

### Five Distinct Phases

| Phase | Period | Defining Characteristics |
|-------|--------|-------------------------|
| **Active Season** | Sep – Oct 2025 | Highest steps (8,400/day), tennis competition, best stress/recovery balance (Oct ratio 0.75) |
| **Deceleration** | Nov – Dec 2025 | Steps dropped 37%, HRV lowest (28.1 ms in Dec), readiness lowest (72.1 in Dec), Dec 21 multi-system crisis |
| **Stabilization** | Jan – Feb 2026 | Gradual HRV recovery (29.7 → 33.0 ms), readiness recovery (78 → 81), Feb highest non-competition steps (9,487/day) |
| **SF Trip** | Late Feb – Late Mar | 29 days no data (travel, no charger) |
| **Return** | Mar – Apr 2026 | Best sleep efficiency (92.6%), best HRV (35.2 ms), but lowest activity (4,273 steps), highest stress ratio (2.89 in Apr) |
