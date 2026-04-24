"""
State-conditional dynamic network analysis for the paper.
Computes L1 (lag cross-correlation), L2 (Granger causality), L3 (state-conditional networks).
"""

import json
import warnings
import numpy as np
import pandas as pd
from scipy import stats
from itertools import combinations

warnings.filterwarnings("ignore")

DATA = "/Users/shipeifeng/Oura ring_Structuredataset_modeling/processed_data/daily_merged.csv"
df = pd.read_csv(DATA, parse_dates=["day"])

# Only normal confidence days
df = df[df["data_confidence"] == "normal"].copy().reset_index(drop=True)
print(f"Usable days: {len(df)}")

# =========================================================================
# NODE CONSTRUCTION
# =========================================================================

# A: Sleep — Oura doesn't export sleep_score in our data, so construct from components
# Use efficiency as primary (it's the closest to a composite)
# Actually, let's check what scores we have
print("\nAvailable scores:")
for col in ["activity_score", "readiness_score", "efficiency"]:
    print(f"  {col}: {df[col].notna().sum()} valid")

# Node A: Sleep quality — use efficiency (0-100 scale, composite of sleep metrics)
df["node_A"] = df["efficiency"]

# Node B: Daily activity — use activity_score
df["node_B"] = df["activity_score"]

# Node C: Recovery & stress — use readiness_score
df["node_C"] = df["readiness_score"]

# Node D: Blood oxygen & breathing — z-score mean of SpO2 and inverted BDI
spo2_z = (df["spo2_avg"] - df["spo2_avg"].mean()) / df["spo2_avg"].std()
bdi_inv_z = -(df["breathing_disturbance_index"] - df["breathing_disturbance_index"].mean()) / df["breathing_disturbance_index"].std()
df["node_D"] = (spo2_z + bdi_inv_z) / 2

# Node E: Menstrual cycle — temperature deviation
df["node_E"] = df["temperature_deviation"]

# Node F: Tennis load — composite of match indicator + workout HR peak + active calories
match_binary = (df["is_tennis_match"] | df["is_post_match"]).astype(float)
hr_peak_z = (df["hr_workout_max"].fillna(df["hr_workout_max"].median()) - df["hr_workout_max"].mean()) / df["hr_workout_max"].std()
cal_z = (df["active_calories"].fillna(df["active_calories"].median()) - df["active_calories"].mean()) / df["active_calories"].std()
df["node_F"] = (match_binary + hr_peak_z + cal_z) / 3

nodes = ["node_A", "node_B", "node_C", "node_D", "node_E", "node_F"]
node_labels = {"node_A": "A (Sleep)", "node_B": "B (Activity)", "node_C": "C (Recovery)",
               "node_D": "D (SpO2/Breath)", "node_E": "E (Cycle)", "node_F": "F (Tennis)"}

# =========================================================================
# STATE PARTITIONING
# =========================================================================

# Post-tennis: match day + day after (highest priority)
is_post_tennis = df["is_tennis_match"] | df["is_post_match"]

# Travel disruption: 7 days before and after the gap (Feb 26 - Mar 26)
gap_start = pd.Timestamp("2026-02-26")
gap_end = pd.Timestamp("2026-03-26")
is_travel = ((df["day"] >= gap_start - pd.Timedelta(days=7)) & (df["day"] < gap_start)) | \
            ((df["day"] > gap_end) & (df["day"] <= gap_end + pd.Timedelta(days=7)))

# Luteal: temperature deviation > 0 sustained (simplified: temp_dev > 0 and not in other states)
is_luteal = df["temperature_deviation"] > 0

# Apply priority: post-tennis > travel > luteal > baseline
df["state"] = "baseline"
df.loc[is_luteal, "state"] = "luteal"
df.loc[is_travel, "state"] = "travel"
df.loc[is_post_tennis, "state"] = "post_tennis"

print("\nState partition:")
for s, count in df["state"].value_counts().items():
    print(f"  {s:15s}: {count} days")

# =========================================================================
# L1: LAGGED CROSS-CORRELATION
# =========================================================================

def lag_crosscorr(x, y, max_lag=7):
    """Compute cross-correlation at lags 0..max_lag. Returns (best_r, best_lag)."""
    x_clean = x.dropna()
    y_clean = y.dropna()
    common = x_clean.index.intersection(y_clean.index)
    if len(common) < 20:
        return np.nan, 0

    best_r, best_lag = 0, 0
    for lag in range(max_lag + 1):
        if lag == 0:
            idx = common
            r, _ = stats.pearsonr(x.loc[idx], y.loc[idx])
        else:
            idx_x = common[common.isin(x_clean.index)]
            idx_y = [i + lag for i in idx_x if (i + lag) in y_clean.index]
            idx_x = [i for i in idx_x if (i + lag) in y_clean.index]
            if len(idx_x) < 20:
                continue
            r, _ = stats.pearsonr(x.loc[idx_x].values, y.loc[idx_y].values)
        if abs(r) > abs(best_r):
            best_r, best_lag = r, lag
    return best_r, best_lag

def permutation_threshold(x, y, n_perm=1000, max_lag=7):
    """95th percentile of |r| under permutation null."""
    null_rs = []
    for _ in range(n_perm):
        y_shuf = y.sample(frac=1, replace=False).reset_index(drop=True)
        y_shuf.index = y.index
        r, _ = lag_crosscorr(x, y_shuf, max_lag)
        null_rs.append(abs(r))
    return np.percentile(null_rs, 95)

print("\n" + "=" * 60)
print("L1: LAGGED CROSS-CORRELATION (full dataset)")
print("=" * 60)

# Compute global threshold from a few representative pairs
print("Computing permutation threshold...")
thresholds = []
for i, j in [(0, 2), (1, 2), (0, 4)]:
    t = permutation_threshold(df[nodes[i]], df[nodes[j]], n_perm=500)
    thresholds.append(t)
r_thresh = np.mean(thresholds)
print(f"Significance threshold: |r| > {r_thresh:.3f}")

l1_results = []
pairs = list(combinations(range(6), 2))
for i, j in pairs:
    r, lag = lag_crosscorr(df[nodes[i]], df[nodes[j]])
    sig = abs(r) > r_thresh
    l1_results.append({
        "node_i": node_labels[nodes[i]], "node_j": node_labels[nodes[j]],
        "r": round(r, 3), "lag": lag, "significant": sig
    })
    if sig:
        print(f"  {node_labels[nodes[i]]:18s} ↔ {node_labels[nodes[j]]:18s}: r={r:+.3f} (lag {lag}d) ***")
    else:
        print(f"  {node_labels[nodes[i]]:18s} ↔ {node_labels[nodes[j]]:18s}: r={r:+.3f} (lag {lag}d)")

sig_edges = sum(1 for r in l1_results if r["significant"])
print(f"\nGlobal network density: {sig_edges}/15 = {sig_edges/15:.2f}")

# =========================================================================
# L2: GRANGER CAUSALITY (baseline + luteal only, need >=30 days)
# =========================================================================

print("\n" + "=" * 60)
print("L2: GRANGER CAUSALITY")
print("=" * 60)

def granger_test(x, y, max_lag=7):
    """Simple Granger causality test: does x's past help predict y?"""
    from numpy.linalg import lstsq

    common = x.dropna().index.intersection(y.dropna().index)
    x_vals = x.loc[common].values
    y_vals = y.loc[common].values

    if len(x_vals) < 30:
        return np.nan, np.nan

    # Select lag order by BIC
    best_bic, best_p = np.inf, 1
    for p in range(1, min(max_lag + 1, len(x_vals) // 5)):
        n = len(y_vals) - p
        Y = y_vals[p:]
        X_r = np.column_stack([y_vals[p-k-1:-(k+1) if k+1 < len(y_vals) else None] for k in range(p)])
        if X_r.shape[0] != n:
            X_r = X_r[:n]
        residuals = Y - X_r @ lstsq(X_r, Y, rcond=None)[0]
        bic = n * np.log(np.var(residuals)) + p * np.log(n)
        if bic < best_bic:
            best_bic, best_p = bic, p

    p = best_p
    n = len(y_vals) - p
    Y = y_vals[p:]

    # Restricted model: y ~ y_lags
    X_r = np.column_stack([y_vals[p-k-1:-(k+1) if k+1 < len(y_vals) else None] for k in range(p)])[:n]
    X_r = np.column_stack([X_r, np.ones(n)])
    beta_r = lstsq(X_r, Y, rcond=None)[0]
    rss_r = np.sum((Y - X_r @ beta_r) ** 2)

    # Unrestricted model: y ~ y_lags + x_lags
    X_x = np.column_stack([x_vals[p-k-1:-(k+1) if k+1 < len(x_vals) else None] for k in range(p)])[:n]
    X_u = np.column_stack([X_r, X_x])
    beta_u = lstsq(X_u, Y, rcond=None)[0]
    rss_u = np.sum((Y - X_u @ beta_u) ** 2)

    # F-test
    df1 = p
    df2 = n - 2 * p - 1
    if df2 <= 0 or rss_u == 0:
        return np.nan, np.nan
    f_stat = ((rss_r - rss_u) / df1) / (rss_u / df2)
    p_value = 1 - stats.f.cdf(f_stat, df1, df2)

    return f_stat, p_value

n_tests = 30  # 6*5 directed pairs
bonferroni = 0.05 / n_tests

for state_name in ["baseline", "luteal"]:
    sub = df[df["state"] == state_name].copy().reset_index(drop=True)
    print(f"\n--- {state_name.upper()} ({len(sub)} days) ---")

    for i in range(6):
        for j in range(6):
            if i == j:
                continue
            f_stat, p_val = granger_test(sub[nodes[i]], sub[nodes[j]])
            if np.isnan(f_stat):
                continue
            sig = "***" if p_val < bonferroni else ""
            if p_val < 0.1:
                print(f"  {node_labels[nodes[i]]:18s} → {node_labels[nodes[j]]:18s}: F={f_stat:.2f}, p={p_val:.4f} {sig}")

# =========================================================================
# L3: STATE-CONDITIONAL NETWORKS
# =========================================================================

print("\n" + "=" * 60)
print("L3: STATE-CONDITIONAL NETWORKS")
print("=" * 60)

state_networks = {}

for state_name in ["baseline", "luteal", "post_tennis", "travel"]:
    sub = df[df["state"] == state_name][nodes].copy()
    n_days = len(sub)

    # Correlation matrix
    C = sub.corr().values

    # Bootstrap significance
    n_boot = 2000
    block_size = 3
    sig_matrix = np.zeros((6, 6))

    for b in range(n_boot):
        # Block bootstrap
        n_blocks = int(np.ceil(n_days / block_size))
        boot_idx = []
        for _ in range(n_blocks):
            start = np.random.randint(0, max(1, n_days - block_size))
            boot_idx.extend(range(start, min(start + block_size, n_days)))
        boot_idx = boot_idx[:n_days]
        boot_data = sub.iloc[boot_idx]
        C_boot = boot_data.corr().values
        sig_matrix += (np.sign(C_boot) == np.sign(C)).astype(float)

    sig_matrix /= n_boot
    significant = sig_matrix > 0.975  # 95% CI excludes zero
    np.fill_diagonal(significant, False)

    # Metrics
    n_sig_edges = significant[np.triu_indices(6, k=1)].sum()
    density = n_sig_edges / 15

    degree = significant.sum(axis=1)  # count significant edges per node
    hub_centrality = degree / 5  # normalized
    dominant_hub_idx = np.argmax(hub_centrality)

    state_networks[state_name] = {
        "n_days": n_days,
        "C": C,
        "significant": significant,
        "density": float(density),
        "hub_centrality": {node_labels[nodes[i]]: float(round(hub_centrality[i], 2)) for i in range(6)},
        "dominant_hub": node_labels[nodes[dominant_hub_idx]],
        "n_significant_edges": int(n_sig_edges),
    }

    print(f"\n--- {state_name.upper()} ({n_days} days) ---")
    print(f"  Density: {n_sig_edges}/15 = {density:.2f}")
    print(f"  Dominant hub: {node_labels[nodes[dominant_hub_idx]]} (centrality = {hub_centrality[dominant_hub_idx]:.2f})")
    print(f"  Hub centrality: {', '.join(f'{node_labels[nodes[i]]}={hub_centrality[i]:.2f}' for i in range(6))}")

    # Print significant edges with r values
    print(f"  Significant edges:")
    for i, j in combinations(range(6), 2):
        if significant[i, j] or significant[j, i]:
            print(f"    {node_labels[nodes[i]]:18s} ↔ {node_labels[nodes[j]]:18s}: r={C[i,j]:+.3f}")

# Frobenius divergence from baseline
print("\n--- NETWORK DIVERGENCE FROM BASELINE ---")
C_base = state_networks["baseline"]["C"]
for state_name in ["luteal", "post_tennis", "travel"]:
    C_s = state_networks[state_name]["C"]
    # Handle NaN in correlation matrices
    C_base_clean = np.nan_to_num(C_base, nan=0)
    C_s_clean = np.nan_to_num(C_s, nan=0)
    frob = np.linalg.norm(C_s_clean - C_base_clean, 'fro')
    state_networks[state_name]["frobenius_divergence"] = float(round(frob, 3))
    print(f"  ||C_{state_name} - C_baseline||_F = {frob:.3f}")

# Summary table
print("\n" + "=" * 60)
print("SUMMARY TABLE")
print("=" * 60)
print(f"{'State':<15} {'N':>4} {'Density':>8} {'Dom. Hub':<18} {'ΔC (Frob)':>10}")
print("-" * 60)
for s in ["baseline", "luteal", "post_tennis", "travel"]:
    net = state_networks[s]
    frob = net.get("frobenius_divergence", 0.0)
    print(f"{s:<15} {net['n_days']:>4} {net['density']:>8.2f} {net['dominant_hub']:<18} {frob:>10.3f}")

# Save results
out = "/Users/shipeifeng/Oura ring_Structuredataset_modeling/analysis/network_results.json"
# Convert numpy arrays for JSON
for s in state_networks:
    state_networks[s]["C"] = state_networks[s]["C"].tolist()
    state_networks[s]["significant"] = state_networks[s]["significant"].tolist()

with open(out, "w") as f:
    json.dump(state_networks, f, indent=2)
print(f"\nResults saved to {out}")
