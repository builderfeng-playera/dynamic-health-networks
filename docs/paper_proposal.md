# Paper Proposal — SD4H @ ICML 2026

**Deadline:** April 28, 2026 | **Format:** 4 pages + refs, ICML template, double-blind

---

## Title (working)

**Dynamic Health Networks: How Physiological Dependencies Reorganize Across Body States in Longitudinal Wearable Data**

---

## Core Thesis

The dependency structure among health metrics captured by a wearable device is not static — it dynamically reorganizes depending on the body's current physiological state. We show this by constructing state-conditional correlation networks from 7 months of Oura Ring data across 6 health dimensions, and demonstrate that different states produce qualitatively different network topologies with distinct hub nodes.

---

## Motivation

Most wearable health analyses treat metrics independently (e.g., "is my HRV good?") or compute fixed pairwise correlations across the entire observation period. This misses a key phenomenon: **the relationships between metrics change depending on what the body is doing.** During the luteal phase, hormonal signals dominate the network; after a tennis match, exercise load dominates; during travel disruption, the network destabilizes. A single static correlation matrix cannot capture this.

**Academic anchor:** Network Physiology has shown that organ-level interactions reorganize across sleep stages (Bartsch et al., 2015). We extend this approach to consumer wearable data and demonstrate analogous reorganization across biological and behavioral states in daily life.

---

## Data

- 7 months of Oura Ring data (Sep 2025 – Apr 2026), 168 usable days
- 6 metric clusters as network nodes:
  - **A** Sleep quality (duration, efficiency, HRV, deep/REM ratios)
  - **B** Daily activity (steps, sedentary time, intensity distribution)
  - **C** Recovery & stress (readiness, stress/recovery ratio, temperature)
  - **D** Blood oxygen & breathing (SpO2, breathing disturbance index)
  - **E** Menstrual cycle (temperature deviation as cycle proxy)
  - **F** Tennis load (match days, active calories, workout HR)
- Each node is a composite of multiple raw metrics within its cluster
- **Node construction:** Each node's time series is derived via PCA (first principal component) over the standardized raw metrics in its cluster, preserving the dominant variance axis. Alternative: use Oura's built-in composite scores (activity_score, readiness_score) where available, with raw metrics for clusters without scores (D, E, F). The choice affects interpretability — PCA is data-driven but less clinically transparent; scores are interpretable but vendor-specific. We report results for both and compare.
- Data is not publicly released; the contribution is the method, not the dataset

---

## Methods (3 levels)

| Level | Method | What it reveals | Math required |
|-------|--------|----------------|---------------|
| **L1** | Lag cross-correlation (0–7 day lags) | Which clusters lead/follow, strength & direction | Statistics, linear algebra |
| **L2** | Granger causality | Directed causal edges — does X's past predict Y's future? | + Autoregressive models, F-test |
| **L3** | State-conditional network | Separate networks per body state; compare topology changes | + Information theory, bootstrap testing |

**Body states for L3:**
- Baseline (normal days, follicular phase)
- Luteal phase (post-ovulation, elevated temperature)
- Post-tennis match (day of + day after competitive match)
- Travel disruption (data edges around the 29-day absence)

---

## Expected Results

| State | Network signature |
|-------|-------------------|
| **Baseline / Follicular** | Balanced topology, no single dominant hub — the "optimal training window" |
| **Luteal phase** | E (menstrual cycle) becomes hub: E→A (sleep disruption), E→C (recovery cost) edges strengthen |
| **Post-tennis match** | F (tennis load) becomes hub: F→C (recovery demand), F→B (activity spike) edges strongest |
| **Travel disruption** | A↔C (sleep↔recovery) tightly coupled, B and F edges weaken, D→A (SpO2→sleep) strengthens |

Key finding: **the hub node rotates** across states — cycle, exercise, or sleep takes control of the network depending on context.

**Quantification:** Each state-conditional network is compared using: (1) **network density** — fraction of edges passing significance threshold (bootstrap p < 0.05); (2) **hub centrality** — degree centrality or eigenvector centrality of each node per state; (3) **network difference** — Frobenius norm ‖ΔC‖_F between state-conditional and baseline correlation matrices, measuring how far each state deviates from the default topology.

---

## Contribution

1. **Network perspective on wearable health data** — shifting from "is metric X normal?" to "how do metrics interact, and how does that interaction change?"
2. **State-conditional dynamic networks** — a concrete method (L1–L3) for constructing and comparing physiological dependency networks across body states
3. **Clinically interpretable findings** — the rotating hub structure has direct implications for personalized health recommendations (e.g., training periodization around menstrual cycle phases)
4. **Female health gap** — the finding that menstrual cycle phase becomes the dominant network hub during the luteal phase has direct implications for female athletes and highlights a systematic gap in current wearable health analytics, which typically do not condition interpretations on cycle phase

---

## Paper Outline (4 pages)

| Section | ~Length | Content |
|---------|--------|---------|
| 1. Introduction | 0.75p | Static vs dynamic view of wearable data; Network Physiology anchor (Bartsch & Ivanov 2015); why networks matter |
| 2. Data & Setup | 0.5p | 6 nodes (A–F), body states, data period; no dataset release |
| 3. Methods | 1.0p | L1 → L2 → L3 progression with formulation |
| 4. Results | 1.25p | State-conditional networks, hub rotation, key edges |
| 5. Discussion | 0.5p | Physiological interpretation, limitations, future work (L4–L5) |

---

## Future Work (not in this paper)

- **L4: Information-theoretic network** — transfer entropy for non-linear, directed information flow
- **L5: State-space dynamic model** — model the 6-node system as a dynamical system with regime-switching transition matrices
