# 4. Results

## 4.1 Global Network Structure (L1)

Across all 168 usable days, the lag cross-correlation network reveals 4 significant edges out of 15 possible (density = 0.27, permutation threshold |r| > 0.217). The strongest global connections are:

| Edge | r | Lag | Interpretation |
|------|---|-----|---------------|
| B (Activity) ↔ E (Cycle) | +0.420 | 1d | Activity levels co-vary with cycle phase |
| B (Activity) ↔ F (Tennis) | +0.337 | 0d | Tennis drives same-day activity |
| C (Recovery) ↔ E (Cycle) | −0.312 | 0d | Luteal phase suppresses recovery |
| C (Recovery) ↔ F (Tennis) | +0.219 | 6d | Recovery improves ~6 days after match |

Notably, the sleep node (A) has no significant global edges; its connections are state-dependent and wash out in the aggregate, motivating the state-conditional analysis.

## 4.2 Directed Influences (L2)

Granger causality analysis on the two states with sufficient sample size (baseline: 65 days, luteal: 81 days) reveals sparse but interpretable directed edges. In the baseline state, Recovery Granger-causes Blood Oxygen (C → D, F = 9.21, p = 0.004, significant after Bonferroni correction), suggesting that autonomic recovery status predicts next-day breathing quality. Tennis load Granger-causes Activity in baseline (F → B, F = 4.26, p = 0.019), reflecting match-driven activity spikes. In the luteal state, the directed structure shifts: Activity Granger-causes Tennis load (B → F, F = 4.41, p = 0.039), **reversing** the baseline direction (F → B). This reversal carries a physiologically meaningful interpretation: during the follicular phase, exercise choice drives activity ("I play tennis, therefore I'm active"), while during the luteal phase, the body's general capacity constrains exercise output ("my activity level determines whether I can play tennis"). Combined with the Sleep–Activity sign reversal reported in Section 4.4, this points to a broader pattern: the luteal phase shifts the body's mode from volitional ("I choose what to do") to capacity-limited ("my body determines what I can do"), consistent with progesterone-mediated fatigue and reduced exercise tolerance (McNulty et al., 2020).

## 4.3 State-Conditional Networks (L3)

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

## 4.4 Edge-Level State Transitions

Examining how specific edges change across states reveals the mechanism behind hub rotation:

| Edge | Baseline | Luteal | Post-Tennis | Interpretation |
|------|----------|--------|-------------|---------------|
| A ↔ B (Sleep–Activity) | +0.245 ✓ | −0.171 ✓ | n.s. | **Sign reversal** in luteal: sleep and activity become anti-correlated |
| A ↔ C (Sleep–Recovery) | +0.274 ✓ | n.s. | +0.658 ✓ | Coupling **strengthens 2.4×** under exercise stress |
| B ↔ F (Activity–Tennis) | +0.383 ✓ | +0.468 ✓ | n.s. | Persistent but disappears post-match (ceiling effect) |
| C ↔ E (Recovery–Cycle) | n.s. | −0.310 ✓ | −0.473 ✓ | **Emerges only in hormonally active states** |
| C ↔ F (Recovery–Tennis) | n.s. | n.s. | +0.848 ✓ | **Strongest edge in any state**, exclusive to post-match |

The Sleep–Activity sign reversal (A ↔ B: +0.245 → −0.171) between follicular and luteal phases is particularly notable. During the follicular phase, better sleep aligns with higher activity (both systems in a "high-functioning" mode). During the luteal phase, the relationship inverts: the body appears to trade off between sleep quality and activity output, consistent with progesterone-mediated fatigue competing with daytime demands.

---

### References (for this section)

- Bartsch RP, Liu KKL, Bashan A, Ivanov PCh. (2015). Network Physiology: How organ systems dynamically interact. *PLoS ONE*, 10(11), e0142143.
- Granger CWJ. (1969). Investigating causal relations by econometric models and cross-spectral methods. *Econometrica*, 37(3), 424–438.
- McNulty KL, Elliott-Sale KJ, Dolan E, et al. (2020). The effects of menstrual cycle phase on exercise performance in eumenorrheic women: A systematic review and meta-analysis. *Sports Medicine*, 50(10), 1813–1827.
