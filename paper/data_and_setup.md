# 2. Data & Setup

## 2.1 Data Source

We analyze 7 months of continuous data (September 8, 2025 – April 13, 2026) collected from an Oura Ring Generation 3 worn by a single healthy female participant (age 33). The ring captures sleep architecture, nocturnal heart rate and HRV, daily activity, skin temperature, blood oxygen saturation, and autonomic stress/recovery states via photoplethysmography (PPG), accelerometer, and NTC thermistor sensors. Of 217 calendar days, 168 are classified as usable after excluding a 29-day data gap (travel without charger), a 14-day cold-start calibration period, and 7 low-wear days. The dataset is not publicly released; our contribution is the analytical method, not the data.

## 2.2 Network Nodes

We model the body as a 6-node network, where each node represents a physiological dimension aggregated from multiple raw metrics. Three nodes use Oura's built-in composite scores, proprietary weighted aggregates computed by the device firmware and presented to all Oura users globally. This grounds our analysis in the signals that consumers actually see and act on. Three nodes without built-in scores are constructed from raw metrics:

| Node | Dimension | Time Series Construction |
|------|-----------|------------------------|
| **A** | Sleep quality | Oura **sleep score** (0–100), incorporating total duration, efficiency, deep/REM ratios, latency, and timing |
| **B** | Daily activity | Oura **activity score** (0–100), incorporating steps, active calories, training frequency/volume, and inactivity alerts |
| **C** | Recovery & stress | Oura **readiness score** (0–100), incorporating HRV balance, resting HR, body temperature, recovery index, sleep balance, and previous day activity |
| **D** | Blood oxygen & breathing | Mean of z-scored SpO₂ and breathing disturbance index (inverted, so higher = healthier) |
| **E** | Menstrual cycle | Skin temperature deviation from personal baseline (°C), used as a continuous cycle phase proxy, validated by Alzueta et al. (2022) and Goodale et al. (2019) as tracking the biphasic luteal temperature rise |
| **F** | Tennis load | Composite of match-day binary indicator, workout peak HR (z-scored), and active calories (z-scored), capturing acute exercise load from competitive play |

As a robustness check, we also construct all six nodes via PCA (first principal component over standardized raw metrics per cluster) and report comparative results in the appendix.

## 2.3 Body States

We partition the 168 usable days into three physiological states based on biological markers and known events:

| State | Definition | N days | Identification method |
|-------|-----------|--------|----------------------|
| **Baseline (Follicular)** | Normal days during follicular phase (low temperature deviation) | ~70 | Temperature deviation ≤ 0°C, no match/post-match flag |
| **Luteal phase** | Post-ovulation days with elevated temperature | ~55 | Temperature deviation > 0°C sustained ≥ 3 days, consistent with ~28-day autocorrelation (lag-14 r = −0.33, lag-28 r = +0.33) |
| **Post-tennis match** | Match day + 1 day after | 8 | Known match dates from tournament records (4 matches × 2 days) |

States are mutually exclusive; days falling into multiple categories are assigned by priority: post-tennis match > luteal > baseline. Days surrounding the 29-day data gap (travel absence, Feb 26 – Mar 26) are excluded from analysis due to insufficient sample size for reliable network estimation. The partition yields sufficient samples per state for bootstrap significance testing of network edges.

---

### References (for this section)

- Alzueta E, de Zambotti M, Javitz H, et al. (2022). Tracking sleep, temperature, heart rate, and daily symptoms across the menstrual cycle with the Oura Ring in healthy women. *International Journal of Women's Health*, 14, 579–591.
- Goodale BM, Shilaih M, Falco L, et al. (2019). Wearable sensors reveal menses-driven changes in physiology and enable prediction of the fertile window. *Journal of Medical Internet Research*, 21(4), e13404.
