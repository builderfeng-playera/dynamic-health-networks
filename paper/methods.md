# 3. Methods

We analyze inter-node dependencies at three levels of increasing complexity. Each level builds on the previous, progressively adding directionality and state-conditioning to the network.

## 3.1 Level 1: Lagged Cross-Correlation Network

For each pair of nodes $(X_i, X_j)$, we compute the Pearson cross-correlation at lags $\tau = 0, 1, \ldots, 7$ days:

$$r_{ij}(\tau) = \text{Corr}(X_i(t),\ X_j(t + \tau))$$

The **optimal lag** $\tau^*_{ij} = \arg\max_\tau |r_{ij}(\tau)|$ identifies the strongest coupling and its temporal offset. An edge is drawn from $X_i$ to $X_j$ if $|r_{ij}(\tau^*)| > r_{\text{thresh}}$, with thickness proportional to $|r_{ij}|$ and direction indicating which node leads. We set $r_{\text{thresh}}$ via a permutation test: shuffling one series 1,000 times and taking the 95th percentile of the resulting $|r|$ distribution as the significance cutoff.

This yields an undirected-with-lead network where edge weight encodes correlation strength and the optimal lag encodes temporal precedence.

## 3.2 Level 2: Granger Causality Network

To test whether the past of $X_i$ improves prediction of $X_j$ beyond $X_j$'s own past, we fit two vector autoregressive (VAR) models of order $p$:

$$\text{Restricted:} \quad X_j(t) = \sum_{k=1}^{p} \alpha_k\, X_j(t-k) + \epsilon_t$$

$$\text{Unrestricted:} \quad X_j(t) = \sum_{k=1}^{p} \alpha_k\, X_j(t-k) + \sum_{k=1}^{p} \beta_k\, X_i(t-k) + \eta_t$$

A standard F-test compares the residual sum of squares: if the unrestricted model explains significantly more variance ($p < 0.05$, Bonferroni-corrected for 30 pairwise tests), we draw a **directed edge** $X_i \to X_j$, indicating Granger-causal influence. Model order $p$ is selected by BIC over $p \in \{1, \ldots, 7\}$. Stationarity is ensured by first-differencing any node series that fails the augmented Dickey–Fuller test.

This upgrades the network from correlational to directional: edges now carry causal interpretation (in the Granger sense) with statistical control for autocorrelation. Granger analysis requires sufficient time series length for reliable VAR estimation; for states with fewer than 30 days (post-tennis match), we report only L1 correlation results.

## 3.3 Level 3: State-Conditional Dynamic Network

We compute separate networks for each body state $s \in \{\text{baseline, luteal, post-match}\}$ defined in Section 2.3. For each state, we extract the corresponding daily subsequences and compute the pairwise correlation matrix $\mathbf{C}^{(s)} \in \mathbb{R}^{6 \times 6}$.

Edge significance within each state is assessed via block bootstrap (resampling contiguous blocks of 3 days to preserve local autocorrelation, 2,000 iterations). An edge is retained if the bootstrap 95% confidence interval for $|r_{ij}|$ excludes zero.

**Network comparison metrics.** We quantify structural differences across states using three measures:

1. **Network density** $\rho^{(s)}$: fraction of the 15 possible edges that are significant in state $s$.

$$\rho^{(s)} = \frac{|\{(i,j) : |r^{(s)}_{ij}| \text{ is significant}\}|}{15}$$

2. **Hub centrality** $h^{(s)}_i$: degree centrality of node $i$ in state $s$ (number of significant edges incident to $i$, normalized by 5). The **dominant hub** in each state is $\arg\max_i\, h^{(s)}_i$.

3. **Network divergence** $\Delta^{(s)}$: Frobenius norm of the difference between the state-conditional and baseline correlation matrices, measuring how far each state deviates from the default topology.

$$\Delta^{(s)} = \|\mathbf{C}^{(s)} - \mathbf{C}^{(\text{baseline})}\|_F$$

Together, these metrics allow us to quantitatively characterize the **hub rotation** phenomenon: whether different physiological states produce networks with different dominant hubs, different densities, and measurably different topologies. In the next section, we report these metrics across all three states and visualize the resulting state-conditional networks.

---

### References (for this section)

- Granger CWJ. (1969). Investigating causal relations by econometric models and cross-spectral methods. *Econometrica*, 37(3), 424–438.
- Bartsch RP, Liu KKL, Bashan A, Ivanov PCh. (2015). Network Physiology: How organ systems dynamically interact. *PLoS ONE*, 10(11), e0142143.
