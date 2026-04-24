# Paper Proposal v3: SD4H @ ICML 2026

## Title

**Deep N-of-1: A Methodology Framework for Discovering the Temporal Architecture of Personal Health Through Long-Duration Consumer Wearable Monitoring**

---

## Abstract (~150 words)

Most wearable health research begins with population-level data and applies findings to individuals. We invert this pipeline with a Natural Observer methodology: the researcher serves as both subject and analyst, using 7 months of continuous consumer wearable data (Oura Ring, September 2025 – April 2026) supplemented by rich contextual annotations spanning four dimensions: athletic training, travel, subjective stress, and menstrual cycle phase. We present a replicable end-to-end framework — from API data collection and contextual annotation schema to multi-resolution temporal analysis and context-conditional modeling — that any individual can apply to their own wearable data. Through this framework, we uncover the layered temporal architecture of one person's health dynamics: daily recovery rhythms, weekly periodicity driven by training load, monthly regime shifts corresponding to life transitions, and cycle-phase-modulated physiological baselines. We demonstrate that context-conditional analysis reveals patterns invisible to context-free methods, and discuss implications for personal health infrastructure that prioritizes individual signal fidelity over population-level generalization.

---

## 1. Introduction

### The limits of population-first health research

Wearable health research overwhelmingly follows a population-first paradigm: recruit N participants, collect standardized data, compute aggregate statistics, and apply findings to individuals. This approach is powerful for identifying universal biological patterns, but it systematically discards the very thing that makes health data meaningful to the person who generated it — context.

When a researcher analyzes 50 participants' HRV trends, they cannot know that Participant 23's dip on Day 12 followed a sleepless night before a job interview, or that Participant 7's anomalous recovery pattern reflects a weekend tennis tournament. These contextual details are not noise — they are the signal. Population averaging treats them as variance to be smoothed away.

### What N-of-1 uniquely reveals

A deep N-of-1 study inverts the epistemic relationship between researcher and data. When the researcher is the subject, every data point carries a story: why sleep was disrupted, what the body was recovering from, what life event triggered a regime shift. This contextual layer transforms wearable data from an opaque time series into an interpretable narrative of physiological adaptation.

Moreover, long-duration single-subject monitoring (7 months vs. the typical 2–4 weeks of population studies) enables analysis of temporal structures that short studies cannot access: seasonal physiological variation, multi-week adaptation cycles, and the long-tail effects of significant life events.

### The Natural Observer methodology

We formalize this approach as the Natural Observer methodology:

1. **Live it** — Generate data through authentic daily life, not controlled protocols
2. **Observe it** — Record contextual annotations alongside physiological signals
3. **Analyze it** — Discover temporal patterns through multi-resolution, context-conditional analysis
4. **Articulate it** — Identify which patterns require personal context to interpret vs. which are context-independent

This methodology does not replace population research — it complements it by identifying the questions that population research should ask and the individual variation it should expect.

---

## 2. Contributions

1. **A replicable N-of-1 methodology framework**: a complete pipeline from Oura Ring API data collection through contextual annotation schema design, multi-resolution temporal analysis, and context-conditional modeling. The framework is released as open-source code so that any individual with a consumer wearable device can apply it to their own data without sharing personal health information.

2. **A four-dimensional contextual annotation schema**: a structured vocabulary for annotating athletic training, travel disruptions, subjective stress, and menstrual cycle phase alongside physiological time series — demonstrating what becomes interpretable when lived experience is paired with sensor data.

3. **Multi-resolution temporal analysis** revealing the layered architecture of personal health: daily recovery rhythms, weekly training periodicity, monthly regime shifts, and seasonal trends — each operating at a different time scale and requiring different analytical methods.

4. **Context-conditional pattern discovery**: empirical demonstration that partitioning physiological time series by life context (e.g., training days vs. rest days, travel vs. home, cycle phase) reveals dynamics invisible to context-free analysis.

5. **Discussion of design implications** for personal health infrastructure that preserves individual signal fidelity rather than optimizing for population-level aggregation.

---

## 3. Dataset

### 3.1 Physiological data: Oura Ring (7 months)

Data collected via Oura Ring API v2, September 7, 2025 – April 13, 2026 (~220 days).

**Daily summary signals:**

| Signal | Source endpoint | Key features |
|--------|----------------|--------------|
| Sleep | `sleep` | total duration, deep/REM/light sleep, efficiency, latency, restfulness, timing, HRV (nightly rMSSD), lowest HR |
| Readiness | `daily_readiness` | readiness score, resting HR, HRV balance, body temperature deviation (δT), recovery index, sleep balance, activity balance |
| Activity | `daily_activity` | steps, active calories, total burn, activity score, low/medium/high activity minutes, MET |
| SpO₂ | `daily_spo2` | blood oxygen percentage, breathing disturbance index |
| Stress | `daily_stress` | daytime stress level, recovery level, day summary |

**Continuous signals:**

| Signal | Resolution | Volume |
|--------|-----------|--------|
| Heart rate | ~5-minute intervals | 219,224 readings across ~200 wear days |

**Temporal characteristics:**
- ~180 daily observations per summary feature (after excluding non-wear days)
- Natural missing data: a 24-day non-wear gap (March 2–25, 2026) due to travel without charger — treated as annotated context, not data error
- Nighttime HR at 5-min resolution → ~200–2,700 observations per day depending on wear

### 3.2 Contextual annotations (the key differentiator)

The author maintained structured contextual records throughout the observation period across four dimensions:

| Context dimension | Key fields | Frequency |
|-------------------|-----------|-----------|
| Athletic training | date, type (match/practice), intensity (1–5), duration (min) | 3–5× per week |
| Travel | start/end date, destination, timezone delta (hours), routine disruption score (1–3) | As occurred |
| Subjective stress | date, level (low/medium/high), source (work/social/health/other) | Daily |
| Menstrual cycle | start/end date, flow intensity (light/medium/heavy) | Monthly |

This contextual layer is what makes N-of-1 analysis fundamentally different from population analysis: every anomaly in the physiological data has an explanation available. The 24-day non-wear gap, for example, is not missing data in the traditional sense — it is annotated context (travel without charger) that can itself be analyzed as a disruption event.

### 3.3 Data availability and privacy

In keeping with the principle that personal health data belongs to the individual, raw physiological data and contextual annotations are not published. Instead, we release:
- The complete data collection pipeline (Oura Ring API scripts)
- The contextual annotation schema (CSV templates)
- The full analysis and modeling codebase

This approach enables full methodological reproducibility: any individual with an Oura Ring can run the identical pipeline on their own data.

---

## 4. Methodology

### 4.1 Data pipeline

```
Oura Ring API (JSON)
        ↓  parsers/
Structured DataFrames (per modality)
        ↓  features/
Master DataFrame (daily granularity)
        ↑
Contextual Annotations (4 CSV files)
        ↓  analysis/
Multi-resolution Analysis
        ↓  models/
Context-conditional Modeling
        ↓  viz/
Visualizations + Notebooks
```

### 4.2 Multi-resolution temporal decomposition

We analyze the 7-month time series at four nested time scales:

**Daily (circadian):** Within-day HR and HRV dynamics. How does the nighttime HR recovery curve differ on training days vs. rest days? What is the shape of a high-quality recovery night?

**Weekly (mesocycle):** 7-day rolling patterns driven by training load periodicity. Does HRV follow a predictable weekly cycle? How many rest days does recovery require after high-intensity training weeks?

**Monthly (macrocycle):** Regime detection across the 7-month span. Are there distinct physiological "phases" of baseline HRV, sleep efficiency, or readiness? What events trigger transitions between regimes?

**Seasonal (7-month arc):** Trends spanning the full observation window. How does body temperature baseline drift across seasons? How do menstrual cycle-phase effects interact with training load effects over multiple cycles?

### 4.3 Context-conditional analysis

The central methodological contribution: partition the same time series by contextual category and compare dynamics.

**Planned comparisons:**

| Partition | Question |
|-----------|---------|
| Tennis match vs. practice vs. rest day | What is the post-match recovery trajectory? How long until HRV returns to baseline? |
| Travel (non-wear gap + timezone disruption) vs. home | How does sleep architecture change during travel disruption? What is the recovery timeline? |
| High-stress vs. low-stress weeks | How does subjective stress propagate through sleep → HRV → readiness over subsequent days? |
| Menstrual cycle phase (follicular vs. luteal) | How does δT align with cycle phase? Do HRV, sleep efficiency, and readiness score differ systematically by phase? |

**Methods:**
- Conditional lag-correlation functions: cross-correlation between features computed separately per context category
- Change-point detection (PELT / BOCPD) on the full series, followed by mapping detected change-points to contextual events
- Predictive models (XGBoost): predict next-day readiness/sleep quality using (a) physiological features only vs. (b) physiological + contextual features — the performance gap quantifies the information value of context

### 4.4 Pattern taxonomy

Discovered patterns are categorized into:

- **Universal candidates:** patterns likely to generalize (e.g., HRV rebound after exertion follows a consistent time course)
- **Context-dependent:** patterns that only appear when data is partitioned by context (e.g., travel-induced sleep disruption has a different recovery profile than training-induced disruption)
- **Idiosyncratic:** patterns likely unique to this individual's physiology, training history, or lifestyle

This taxonomy provides structured outputs that future population-level studies can use as hypotheses to test.

---

## 5. Expected Results

### 5.1 The temporal architecture is layered

Personal health dynamics operate simultaneously at multiple time scales, and patterns at different scales can be partially independent. A person can have excellent daily recovery (circadian level) while undergoing a slow negative regime shift (monthly level) that is invisible in daily metrics until a tipping point.

### 5.2 Context transforms the signal

Context-conditional analysis will substantially change the interpretation of physiological patterns:
- A "low HRV" day following intense tennis is a sign of appropriate physiological load; the same reading on a rest day may signal illness or stress
- The same sleep duration may correspond to very different readiness outcomes depending on prior-day context
- Menstrual cycle phase will emerge as a systematic modulator of δT, HRV, and readiness, invisible in context-free analysis
- Predictive models with contextual features will meaningfully outperform context-free baselines

### 5.3 Long duration reveals what short studies miss

The 7-month window will reveal:
- Cycle-phase-aligned body temperature baseline drift
- Multi-week adaptation to training load changes
- Regime shifts that align with major life transitions (including the non-wear travel gap as a natural disruption experiment)

### 5.4 The methodology framework is replicable

Any individual with an Oura Ring and a willingness to maintain contextual annotations can apply this pipeline to their own data. The framework's value is not the specific patterns discovered, but the analytical infrastructure that makes personal pattern discovery possible.

---

## 6. Limitations

- **Single subject, by design.** Generalization is not the goal. The contribution is the methodology; the patterns found are hypotheses for future multi-participant validation.
- **Self-observation bias.** The researcher-as-subject may unconsciously alter behavior after noticing physiological signals. This is acknowledged as inherent to the methodology and discussed as a feature of real-world personal health monitoring.
- **Consumer device limitations.** Oura Ring provides processed summaries; proprietary algorithms between sensor and output are opaque. We work with data as available to any consumer user.
- **Contextual annotation is manual and subjective.** Annotation richness depends on the observer's diligence. Scaling this approach requires semi-automated context capture (calendar integration, location-based inference).
- **No causal claims.** All temporal patterns are correlational. Context-conditional analysis suggests mechanisms but does not prove causation.
- **Non-wear gap.** The 24-day non-wear period (March 2–25, 2026) interrupts time series continuity and limits seasonal analysis. We treat it as an annotated disruption event rather than imputed data.

---

## 7. Further Discussion

### Personal health infrastructure

Current consumer health platforms optimize for population-level insights: "people like you sleep X hours." The Natural Observer methodology argues for a complementary paradigm: infrastructure that learns the individual's personal baselines, context-response patterns, and recovery signatures — and interprets new data against that personal model, not a population average.

### Scaling the methodology

The annotation burden is real. Future directions include:
- Semi-automated annotation from calendar, location, and app usage data
- Prompting frameworks that reduce annotation to minimal daily inputs
- Transfer of personal models: can patterns discovered in one individual inform priors for another?

### N-of-1 as hypothesis generation for population research

Every data point in a large-scale study was once a moment in someone's life — and that moment had a context that mattered. N-of-1 studies grounded in rich context can generate the specific, testable hypotheses that population studies should then validate. This is not a replacement for large-scale research; it is a necessary complement.

---

## 8. Positioning for SD4H @ ICML 2026

**Workshop topics addressed:**

| Topic | How this paper addresses it |
|-------|----------------------------|
| Irregular & Missing Data | Natural missingness in consumer wearables (non-wear gap as annotated context) |
| Clinical Applications | Personal health pattern discovery from consumer wearables |
| Complex Signals | Multi-resolution temporal decomposition of physiological time series |
| Trust & Reliability | Explainability through contextual grounding |
| Deployment & Implementation | Real-world single-user consumer wearable case study |

**Why this matters for the SD4H community:**

Most submissions will approach "structured data for health" from the population side. This paper approaches it from the individual side — arguing that real-world health impact begins with understanding what health data means to the person who generated it. The Natural Observer methodology offers a complementary paradigm: start from the individual, discover grounded patterns, and use these as hypotheses for population-level validation.

The framework's open-source release means any conference attendee with a consumer wearable can immediately apply the methodology to their own data.
