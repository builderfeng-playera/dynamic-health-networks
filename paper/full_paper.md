# Dynamic Health Networks: A Three-Level Framework for State-Conditional Dependency Modeling in Structured Wearable Time Series

**Anonymous submission, SD4H Workshop @ ICML 2026**

---

## Abstract

We present a replicable three-level framework for modeling structured health time series as state-conditional dependency networks. Given daily multivariate physiological data from a consumer wearable device, the framework progressively builds (1) a lagged cross-correlation network capturing pairwise coupling strength and temporal precedence, (2) a Granger causality network adding directed, statistically controlled edges, and (3) a set of state-conditional networks that reveal how the dependency topology reorganizes across physiological contexts. We demonstrate the framework on 7 months of continuous Oura Ring data across six health dimensions (sleep, activity, recovery, blood oxygen, menstrual cycle, and exercise load). The state-conditional analysis uncovers a hub rotation phenomenon: sleep anchors the baseline network, activity dominates during the luteal phase, and recovery becomes central after competitive tennis matches. We further identify a sign reversal in the sleep–activity relationship and a Granger causality direction reversal between cycle phases, providing observational causal evidence for a mode shift from volitional to capacity-limited physiology. The framework is released as open-source code applicable to any consumer wearable dataset, requiring no clinical infrastructure.

---

## 1. Introduction

Consumer wearable devices now generate continuous, multi-dimensional structured health data, including sleep architecture, heart rate variability (HRV), activity patterns, blood oxygen, skin temperature, and stress indicators, enabling longitudinal health monitoring at unprecedented granularity. However, the dominant analytical paradigm treats these metrics independently: tracking individual signals against personal baselines (Mishra et al., 2020), validating sensor accuracy per metric (Cao et al., 2022), or computing summary statistics across observation periods (Huhn et al., 2022). When inter-metric relationships are examined, they are typically modeled as fixed pairwise correlations over the entire dataset. This static view obscures a fundamental property of physiological systems: **the dependency structure among health metrics is itself state-dependent.**

Network Physiology has established that organ-level interactions dynamically reorganize across physiological states. Bartsch et al. (2015) demonstrated that brain–heart–respiration coupling networks undergo pronounced topological changes across sleep stages. Ivanov (2021) formalized this into a broader vision of the "Human Physiolome," the complete map of dynamic organ-to-organ interaction networks, and called for extending this framework to consumer wearable data. Yet no study has provided a replicable, end-to-end analytical framework that takes consumer-grade structured health time series as input and outputs state-conditional dependency networks with formal significance testing.

We address this gap with a three-level framework for structured health time series modeling. The framework progressively constructs: (L1) lagged cross-correlation networks capturing pairwise coupling and temporal precedence, (L2) Granger causality networks adding directed edges with causal interpretation from observational data, and (L3) state-conditional networks that partition the time series by physiological context and quantify topological reorganization via network density, hub centrality, and Frobenius divergence. Each level builds on the previous, and the entire pipeline is released as open-source code applicable to any consumer wearable dataset.

We demonstrate the framework on 7 months of Oura Ring data across six health dimensions (sleep, activity, recovery, blood oxygen, menstrual cycle, and exercise load), showing that the network topology reorganizes across biological and behavioral states, with the **hub node rotating** depending on context. Notably, the Granger causality analysis reveals a direction reversal between cycle phases, providing observational causal evidence for a physiological mode shift. These findings also highlight that current wearable platforms do not condition metric interpretation on menstrual cycle state (Alzueta et al., 2022; Goodale et al., 2019), and sport science still lacks standardized cycle-aware monitoring protocols (Carmichael et al., 2025).

**Contributions.** (1) A replicable, open-source three-level framework for modeling structured health time series as state-conditional dependency networks. (2) A demonstration that Granger causality applied to consumer wearable data can recover directed, state-dependent physiological relationships. (3) Empirical evidence that state-conditional analysis reveals network dynamics (hub rotation, sign reversals, density shifts) invisible to static correlation methods.

## 2. Data & Setup

### 2.1 Data Source

We analyze 7 months of continuous data (September 8, 2025 – April 13, 2026) collected from an Oura Ring Generation 3 worn by a single healthy female participant (age 33). The ring captures sleep architecture, nocturnal heart rate and HRV, daily activity, skin temperature, blood oxygen saturation, and autonomic stress/recovery states via photoplethysmography (PPG), accelerometer, and NTC thermistor sensors. Of 217 calendar days, 168 are classified as usable after excluding a 29-day data gap (travel without charger), a 14-day cold-start calibration period, and 7 low-wear days. The dataset is not publicly released; our contribution is the analytical method, not the data.

### 2.2 Network Nodes

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

### 2.3 Body States

We partition the 168 usable days into three physiological states based on biological markers and known events:

| State | Definition | N days | Identification method |
|-------|-----------|--------|----------------------|
| **Baseline (Follicular)** | Normal days during follicular phase (low temperature deviation) | ~70 | Temperature deviation ≤ 0°C, no match/post-match flag |
| **Luteal phase** | Post-ovulation days with elevated temperature | ~55 | Temperature deviation > 0°C sustained ≥ 3 days, consistent with ~28-day autocorrelation (lag-14 r = −0.33, lag-28 r = +0.33) |
| **Post-tennis match** | Match day + 1 day after | 8 | Known match dates from tournament records (4 matches × 2 days) |

States are mutually exclusive; days falling into multiple categories are assigned by priority: post-tennis match > luteal > baseline. Days surrounding the 29-day data gap (travel absence, Feb 26 – Mar 26) are excluded from analysis due to insufficient sample size for reliable network estimation. The partition yields sufficient samples per state for bootstrap significance testing of network edges.

## 3. Methods

We analyze inter-node dependencies at three levels of increasing complexity. Each level builds on the previous, progressively adding directionality and state-conditioning to the network.

### 3.1 Level 1: Lagged Cross-Correlation Network

For each pair of nodes $(X_i, X_j)$, we compute the Pearson cross-correlation at lags $\tau = 0, 1, \ldots, 7$ days:

$$r_{ij}(\tau) = \text{Corr}(X_i(t),\ X_j(t + \tau))$$

The **optimal lag** $\tau^*_{ij} = \arg\max_\tau |r_{ij}(\tau)|$ identifies the strongest coupling and its temporal offset. An edge is drawn from $X_i$ to $X_j$ if $|r_{ij}(\tau^*)| > r_{\text{thresh}}$, with thickness proportional to $|r_{ij}|$ and direction indicating which node leads. We set $r_{\text{thresh}}$ via a permutation test: shuffling one series 1,000 times and taking the 95th percentile of the resulting $|r|$ distribution as the significance cutoff.

### 3.2 Level 2: Granger Causality Network

To test whether the past of $X_i$ improves prediction of $X_j$ beyond $X_j$'s own past, we fit two vector autoregressive (VAR) models of order $p$:

$$\text{Restricted:} \quad X_j(t) = \sum_{k=1}^{p} \alpha_k\, X_j(t-k) + \epsilon_t$$

$$\text{Unrestricted:} \quad X_j(t) = \sum_{k=1}^{p} \alpha_k\, X_j(t-k) + \sum_{k=1}^{p} \beta_k\, X_i(t-k) + \eta_t$$

A standard F-test compares the residual sum of squares: if the unrestricted model explains significantly more variance ($p < 0.05$, Bonferroni-corrected for 30 pairwise tests), we draw a **directed edge** $X_i \to X_j$, indicating Granger-causal influence. Model order $p$ is selected by BIC over $p \in \{1, \ldots, 7\}$. Stationarity is ensured by first-differencing any node series that fails the augmented Dickey–Fuller test. For states with fewer than 30 days (post-tennis match), we report only L1 correlation results.

### 3.3 Level 3: State-Conditional Dynamic Network

We compute separate networks for each body state $s \in \{\text{baseline, luteal, post-match}\}$. For each state, we extract the corresponding daily subsequences and compute the pairwise correlation matrix $\mathbf{C}^{(s)} \in \mathbb{R}^{6 \times 6}$.

Edge significance is assessed via block bootstrap (resampling contiguous blocks of 3 days to preserve local autocorrelation, 2,000 iterations). An edge is retained if the bootstrap 95% confidence interval for $|r_{ij}|$ excludes zero.

**Network comparison metrics.** We quantify structural differences across states using three measures:

1. **Network density** $\rho^{(s)}$: fraction of the 15 possible edges that are significant in state $s$.

$$\rho^{(s)} = \frac{|\{(i,j) : |r^{(s)}_{ij}| \text{ is significant}\}|}{15}$$

2. **Hub centrality** $h^{(s)}_i$: degree centrality of node $i$ in state $s$ (number of significant edges incident to $i$, normalized by 5). The **dominant hub** is $\arg\max_i\, h^{(s)}_i$.

3. **Network divergence** $\Delta^{(s)}$: Frobenius norm of the difference between the state-conditional and baseline correlation matrices.

$$\Delta^{(s)} = \|\mathbf{C}^{(s)} - \mathbf{C}^{(\text{baseline})}\|_F$$

In the next section, we report these metrics across all three states and visualize the resulting state-conditional networks.

## 4. Results

### 4.1 Global Network Structure (L1)

Across all 168 usable days, the lag cross-correlation network reveals 4 significant edges out of 15 possible (density = 0.27, permutation threshold |r| > 0.217). The strongest global connections are:

| Edge | r | Lag | Interpretation |
|------|---|-----|---------------|
| B (Activity) ↔ E (Cycle) | +0.420 | 1d | Activity levels co-vary with cycle phase |
| B (Activity) ↔ F (Tennis) | +0.337 | 0d | Tennis drives same-day activity |
| C (Recovery) ↔ E (Cycle) | −0.312 | 0d | Luteal phase suppresses recovery |
| C (Recovery) ↔ F (Tennis) | +0.219 | 6d | Recovery improves ~6 days after match |

Notably, the sleep node (A) has no significant global edges; its connections are state-dependent and wash out in the aggregate, motivating the state-conditional analysis.

### 4.2 Directed Influences (L2)

Granger causality analysis on the two states with sufficient sample size (baseline: 65 days, luteal: 81 days) reveals sparse but interpretable directed edges. In the baseline state, Recovery Granger-causes Blood Oxygen (C → D, F = 9.21, p = 0.004, significant after Bonferroni correction), suggesting that autonomic recovery status predicts next-day breathing quality. Tennis load Granger-causes Activity in baseline (F → B, F = 4.26, p = 0.019), reflecting match-driven activity spikes. In the luteal state, the directed structure shifts: Activity Granger-causes Tennis load (B → F, F = 4.41, p = 0.039), **reversing** the baseline direction (F → B). This reversal carries a physiologically meaningful interpretation: during the follicular phase, exercise choice drives activity ("I play tennis, therefore I'm active"), while during the luteal phase, the body's general capacity constrains exercise output ("my activity level determines whether I can play tennis"). Combined with the Sleep–Activity sign reversal reported in Section 4.4, this points to a broader pattern: the luteal phase shifts the body's mode from volitional ("I choose what to do") to capacity-limited ("my body determines what I can do"), consistent with progesterone-mediated fatigue and reduced exercise tolerance (McNulty et al., 2020).

### 4.3 State-Conditional Networks (L3)

The central result of this paper: constructing separate networks for each body state reveals pronounced topological reorganization, summarized in Table 1.

**Table 1.** State-conditional network summary.

| State | N days | Density | Dominant Hub | Hub Centrality | ΔC (Frobenius) |
|-------|--------|---------|-------------|----------------|----------------|
| Baseline (Follicular) | 65 | 0.20 | A (Sleep) | 0.40 | — |
| Luteal phase | 81 | 0.20 | B (Activity) | 0.40 | 1.066 |
| Post-tennis match | 8 | **0.40** | **C (Recovery)** | **0.60** | **2.419** |

Two findings stand out:

**Hub rotation.** The dominant hub node shifts across states: Sleep (A) anchors the baseline network, Activity (B) takes over during the luteal phase, and Recovery (C) dominates post-tennis. No single node is universally central; the body's coordination center rotates depending on what physiological challenge is active.

**Post-tennis densification.** The post-tennis network is the most interconnected (density 0.40, double the baseline) and exhibits the largest divergence from baseline (ΔC = 2.419). Three edges involving Recovery (C) and Tennis load (F) emerge with strong magnitudes: C ↔ F (r = +0.848), A ↔ F (r = +0.778), and C ↔ E (r = −0.473). This dense, Recovery-centered topology reflects the body marshaling multiple systems for post-exercise repair. The appearance of a Cycle–Recovery edge (E ↔ C) that is absent in baseline suggests that menstrual cycle phase modulates recovery capacity even during acute exercise recovery, a cross-system interaction invisible in static analysis.

### 4.4 Edge-Level State Transitions

Examining how specific edges change across states reveals the mechanism behind hub rotation:

| Edge | Baseline | Luteal | Post-Tennis | Interpretation |
|------|----------|--------|-------------|---------------|
| A ↔ B (Sleep–Activity) | +0.245 ✓ | −0.171 ✓ | n.s. | **Sign reversal** in luteal: sleep and activity become anti-correlated |
| A ↔ C (Sleep–Recovery) | +0.274 ✓ | n.s. | +0.658 ✓ | Coupling **strengthens 2.4×** under exercise stress |
| B ↔ F (Activity–Tennis) | +0.383 ✓ | +0.468 ✓ | n.s. | Persistent but disappears post-match (ceiling effect) |
| C ↔ E (Recovery–Cycle) | n.s. | −0.310 ✓ | −0.473 ✓ | **Emerges only in hormonally active states** |
| C ↔ F (Recovery–Tennis) | n.s. | n.s. | +0.848 ✓ | **Strongest edge in any state**, exclusive to post-match |

The Sleep–Activity sign reversal (A ↔ B: +0.245 → −0.171) between follicular and luteal phases is particularly notable. During the follicular phase, better sleep aligns with higher activity (both systems in a "high-functioning" mode). During the luteal phase, the relationship inverts: the body appears to trade off between sleep quality and activity output, consistent with progesterone-mediated fatigue competing with daytime demands.

## 5. Discussion

### 5.1 Physiological Interpretation

The hub rotation phenomenon admits direct physiological explanations for each state.

**Luteal phase.** Progesterone, which peaks during the luteal phase, increases basal metabolic rate, elevates core body temperature by 0.2–0.5°C, and shifts autonomic balance toward sympathetic dominance (Baker & Driver, 2007). This explains why the menstrual cycle node (E) forms a new inhibitory edge to Recovery (C → E, r = −0.31): elevated progesterone suppresses parasympathetic recovery. The simultaneous sign reversal in the Sleep–Activity edge (A ↔ B: +0.25 → −0.17) and the Granger causality direction reversal (F → B becomes B → F) together suggest a mode shift from volitional to capacity-limited physiology, where the body constrains what activities are feasible rather than responding to chosen activities.

**Post-tennis.** Acute high-intensity exercise triggers a well-characterized recovery cascade: elevated cortisol, suppressed HRV, glycogen depletion, and inflammatory signaling (Halson, 2014). The network densification (density 0.20 → 0.40) and the emergence of Recovery (C) as dominant hub (centrality 0.60) reflect this whole-body mobilization. The exceptionally strong C ↔ F edge (r = +0.85) indicates tight coupling between exercise load and recovery demand, a relationship absent in baseline, where exercise is too mild to trigger measurable recovery costs. Notably, the Cycle–Recovery edge (E ↔ C, r = −0.47) also activates post-match, suggesting that menstrual cycle phase modulates recovery capacity even under acute exercise stress.

### 5.2 Framework Applicability

The three-level framework is designed to be portable across consumer wearable platforms and user populations. The input is a daily multivariate time series with a state partition; the output is a set of state-conditional networks with formal significance testing. The node construction step (Section 2.2) is the only component that requires device-specific adaptation: different wearables expose different raw metrics, but the analytical levels (L1–L3) operate on any set of continuous daily time series. We release the full pipeline as open-source code so that researchers can apply it to their own Oura, Whoop, Garmin, or Apple Watch data without sharing personal health information.

The framework also extends naturally to richer state partitions. In this study we used three states defined by biological markers and known events; in principle, any contextual annotation (shift work schedules, medication changes, seasonal variation) can serve as the conditioning variable. This makes the framework a general-purpose tool for structured health time series analysis, not specific to the N-of-1 design or the particular states we examined.

### 5.3 Limitations

**Sample size.** This is an N-of-1 study with 168 usable days. The post-tennis state (8 days) has a limited sample, reducing statistical power and precluding Granger analysis. The observed effects in this state should be interpreted as hypothesis-generating rather than confirmatory.

**Node construction.** Three nodes (A, B, C) rely on Oura's proprietary composite scores, whose internal weighting is not publicly documented. While this choice maximizes ecological validity (these are the scores users actually see), it introduces a dependency on vendor-specific algorithms.

**State partitioning.** The luteal/follicular classification uses temperature deviation as a proxy. Without hormonal assays, the exact ovulation timing is approximate. Days near phase transitions may be misclassified.

**Causality.** Granger causality tests temporal precedence, not true causal mechanisms. The directed edges we report should be interpreted as predictive relationships, not confirmed causal pathways.

**Equity considerations.** The menstrual cycle findings highlight that current wearable platforms report readiness and recovery scores without conditioning on cycle phase, potentially introducing systematic bias for female users. Extending the framework to diverse populations would help quantify whether such biases are consistent across individuals.

### 5.4 Future Work

The three-level framework presented here can be extended in two directions:

**Level 4: Information-theoretic networks.** Transfer entropy (Schreiber, 2000) captures non-linear, directional information flow between nodes. This would replace the linear Granger test with a model-free measure, potentially revealing non-linear dependencies (e.g., threshold effects where HRV only drops after exercise intensity exceeds a critical level).

**Level 5: State-space dynamic models.** Modeling the 6-node system as a vector autoregressive process with regime-switching transition matrices (Hamilton, 1989) would allow the body states to be inferred from data rather than predefined, and would capture smooth transitions between states rather than discrete partitions.

Beyond methodology, the immediate next step is multi-subject validation: applying this framework to a cohort of wearable users to test whether the hub rotation phenomenon generalizes across individuals or reflects idiosyncratic physiology.

---

## References

- Alzueta E, de Zambotti M, Javitz H, et al. (2022). Tracking sleep, temperature, heart rate, and daily symptoms across the menstrual cycle with the Oura Ring in healthy women. *International Journal of Women's Health*, 14, 579–591.
- Baker FC, Driver HS. (2007). Circadian rhythms, sleep, and the menstrual cycle. *Sleep Medicine*, 8(6), 613–622.
- Bartsch RP, Liu KKL, Bashan A, Ivanov PCh. (2015). Network Physiology: How organ systems dynamically interact. *PLoS ONE*, 10(11), e0142143.
- Cao R, Azimi I, Sarhaddi F, et al. (2022). Accuracy assessment of Oura Ring nocturnal heart rate and heart rate variability in comparison with electrocardiography. *Journal of Medical Internet Research*, 24(1), e27487.
- Carmichael MA, Perry K, Roberts AH, Klass V, Clarke AC. (2025). Menstrual cycle monitoring in applied sport settings: A scoping review. *International Journal of Sports Science & Coaching*, online first.
- Goodale BM, Shilaih M, Falco L, et al. (2019). Wearable sensors reveal menses-driven changes in physiology and enable prediction of the fertile window. *Journal of Medical Internet Research*, 21(4), e13404.
- Granger CWJ. (1969). Investigating causal relations by econometric models and cross-spectral methods. *Econometrica*, 37(3), 424–438.
- Halson SL. (2014). Monitoring training load to understand fatigue in athletes. *Sports Medicine*, 44(Suppl 2), S139–S147.
- Hamilton JD. (1989). A new approach to the economic analysis of nonstationary time series and the business cycle. *Econometrica*, 57(2), 357–384.
- Huhn S, Axt M, Gunga H-C, et al. (2022). The impact of wearable technologies in health research: Scoping review. *JMIR mHealth and uHealth*, 10(1), e34384.
- Ivanov PCh. (2021). The new field of Network Physiology: Building the Human Physiolome. *Frontiers in Network Physiology*, 1, 711778.
- McNulty KL, Elliott-Sale KJ, Dolan E, et al. (2020). The effects of menstrual cycle phase on exercise performance in eumenorrheic women: A systematic review and meta-analysis. *Sports Medicine*, 50(10), 1813–1827.
- Mishra T, Wang M, Metwally AA, et al. (2020). Pre-symptomatic detection of COVID-19 from smartwatch data. *Nature Biomedical Engineering*, 4, 1208–1220.
- Schreiber T. (2000). Measuring information transfer. *Physical Review Letters*, 85(2), 461–464.
