# 5. Discussion

## 5.1 Physiological Interpretation

The hub rotation phenomenon admits direct physiological explanations for each state.

**Luteal phase.** Progesterone, which peaks during the luteal phase, increases basal metabolic rate, elevates core body temperature by 0.2–0.5°C, and shifts autonomic balance toward sympathetic dominance (Baker & Driver, 2007). This explains why the menstrual cycle node (E) forms a new inhibitory edge to Recovery (C → E, r = −0.31): elevated progesterone suppresses parasympathetic recovery. The simultaneous sign reversal in the Sleep–Activity edge (A ↔ B: +0.25 → −0.17) and the Granger causality direction reversal (F → B becomes B → F) together suggest a mode shift from volitional to capacity-limited physiology, where the body constrains what activities are feasible rather than responding to chosen activities.

**Post-tennis.** Acute high-intensity exercise triggers a well-characterized recovery cascade: elevated cortisol, suppressed HRV, glycogen depletion, and inflammatory signaling (Halson, 2014). The network densification (density 0.20 → 0.40) and the emergence of Recovery (C) as dominant hub (centrality 0.60) reflect this whole-body mobilization. The exceptionally strong C ↔ F edge (r = +0.85) indicates tight coupling between exercise load and recovery demand, a relationship absent in baseline, where exercise is too mild to trigger measurable recovery costs. Notably, the Cycle–Recovery edge (E ↔ C, r = −0.47) also activates post-match, suggesting that menstrual cycle phase modulates recovery capacity even under acute exercise stress.

## 5.2 Framework Applicability

The three-level framework is designed to be portable across consumer wearable platforms and user populations. The input is a daily multivariate time series with a state partition; the output is a set of state-conditional networks with formal significance testing. The node construction step (Section 2.2) is the only component that requires device-specific adaptation: different wearables expose different raw metrics, but the analytical levels (L1–L3) operate on any set of continuous daily time series. We release the full pipeline as open-source code so that researchers can apply it to their own Oura, Whoop, Garmin, or Apple Watch data without sharing personal health information.

The framework also extends naturally to richer state partitions. In this study we used three states defined by biological markers and known events; in principle, any contextual annotation (shift work schedules, medication changes, seasonal variation) can serve as the conditioning variable. This makes the framework a general-purpose tool for structured health time series analysis, not specific to the N-of-1 design or the particular states we examined.

## 5.3 Limitations

**Sample size.** This is an N-of-1 study with 168 usable days. The post-tennis state (8 days) has a limited sample, reducing statistical power and precluding Granger analysis. The observed effects in this state should be interpreted as hypothesis-generating rather than confirmatory.

**Node construction.** Three nodes (A, B, C) rely on Oura's proprietary composite scores, whose internal weighting is not publicly documented. While this choice maximizes ecological validity (these are the scores users actually see), it introduces a dependency on vendor-specific algorithms.

**State partitioning.** The luteal/follicular classification uses a simple threshold on temperature deviation (> 0) as a proxy. Without hormonal assays, the exact ovulation timing is approximate. Days near phase transitions may be misclassified, and isolated days with slightly positive temperature deviation may be noise rather than true luteal phase. A more robust approach would require consecutive runs of elevated temperature (e.g., $\geq$ 3 days) to confirm phase assignment.

**Causality.** Granger causality tests temporal precedence, not true causal mechanisms. The directed edges we report should be interpreted as predictive relationships, not confirmed causal pathways.

**Equity considerations.** The menstrual cycle findings highlight that current wearable platforms report readiness and recovery scores without conditioning on cycle phase, potentially introducing systematic bias for female users. Extending the framework to diverse populations would help quantify whether such biases are consistent across individuals.

## 5.4 Future Work

The three-level framework presented here can be extended in two directions:

**Level 4: Information-theoretic networks.** Transfer entropy (Schreiber, 2000) captures non-linear, directional information flow between nodes. This would replace the linear Granger test with a model-free measure, potentially revealing non-linear dependencies (e.g., threshold effects where HRV only drops after exercise intensity exceeds a critical level).

**Level 5: State-space dynamic models.** Modeling the 6-node system as a vector autoregressive process with regime-switching transition matrices (Hamilton, 1989) would allow the body states to be inferred from data rather than predefined, and would capture smooth transitions between states rather than discrete partitions.

Beyond methodology, the immediate next step is multi-subject validation: applying this framework to a cohort of wearable users to test whether the hub rotation phenomenon generalizes across individuals or reflects idiosyncratic physiology.

---

### References (for this section)

- Baker FC, Driver HS. (2007). Circadian rhythms, sleep, and the menstrual cycle. *Sleep Medicine*, 8(6), 613–622.
- Carmichael MA, Perry K, Roberts AH, Klass V, Clarke AC. (2025). Menstrual cycle monitoring in applied sport settings: A scoping review. *International Journal of Sports Science & Coaching*, online first.
- Halson SL. (2014). Monitoring training load to understand fatigue in athletes. *Sports Medicine*, 44(Suppl 2), S139–S147.
- Hamilton JD. (1989). A new approach to the economic analysis of nonstationary time series and the business cycle. *Econometrica*, 57(2), 357–384.
- Schreiber T. (2000). Measuring information transfer. *Physical Review Letters*, 85(2), 461–464.
