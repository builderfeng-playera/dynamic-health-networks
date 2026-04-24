"""
Oura Ring Data Processing Pipeline

Loads raw JSON → cleans → annotates → joins into a single daily dataset.

Output:
  processed_data/daily_merged.csv   — one row per day, all metrics + annotations
  processed_data/daily_merged.json  — same data in JSON
"""

import json
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from annotations import (
    COLD_START_DAYS,
    MIN_STEPS_THRESHOLD,
    NON_WEAR_THRESHOLD_HOURS,
    get_absence_mask,
    get_absence_reason,
    get_tennis_df,
    get_tennis_match_days,
)

BASE = os.path.join(os.path.dirname(__file__), "..", "raw_data")
OUT = os.path.join(os.path.dirname(__file__), "..", "processed_data")


def load_raw(name):
    with open(os.path.join(BASE, name)) as f:
        d = json.load(f)
    return d.get("data", [])


# =========================================================================
# STEP 1: Load & extract each dataset
# =========================================================================

def process_activity():
    """Daily activity → flat columns."""
    df = pd.DataFrame(load_raw("daily_activity.json"))
    df["day"] = pd.to_datetime(df["day"])

    contrib = pd.json_normalize(df["contributors"]).add_prefix("act_contrib_")
    df = pd.concat([df.drop(columns=["contributors"]), contrib], axis=1)

    keep = [
        "day", "score", "steps", "active_calories", "total_calories",
        "target_calories", "equivalent_walking_distance", "target_meters",
        "meters_to_target", "high_activity_time", "medium_activity_time",
        "low_activity_time", "sedentary_time", "resting_time", "non_wear_time",
        "high_activity_met_minutes", "medium_activity_met_minutes",
        "low_activity_met_minutes", "sedentary_met_minutes",
        "average_met_minutes", "inactivity_alerts",
        "act_contrib_meet_daily_targets", "act_contrib_move_every_hour",
        "act_contrib_recovery_time", "act_contrib_stay_active",
        "act_contrib_training_frequency", "act_contrib_training_volume",
    ]
    df = df[[c for c in keep if c in df.columns]]
    df = df.rename(columns={"score": "activity_score"})
    return df


def process_readiness():
    """Daily readiness → flat columns."""
    df = pd.DataFrame(load_raw("daily_readiness.json"))
    df["day"] = pd.to_datetime(df["day"])

    contrib = pd.json_normalize(df["contributors"]).add_prefix("rd_contrib_")
    df = pd.concat([df.drop(columns=["contributors"]), contrib], axis=1)

    keep = [
        "day", "score", "temperature_deviation", "temperature_trend_deviation",
        "rd_contrib_activity_balance", "rd_contrib_body_temperature",
        "rd_contrib_hrv_balance", "rd_contrib_previous_day_activity",
        "rd_contrib_previous_night", "rd_contrib_recovery_index",
        "rd_contrib_resting_heart_rate", "rd_contrib_sleep_balance",
        "rd_contrib_sleep_regularity",
    ]
    df = df[[c for c in keep if c in df.columns]]
    df = df.rename(columns={"score": "readiness_score"})
    return df


def process_spo2():
    """Daily SpO2 → flat columns."""
    df = pd.DataFrame(load_raw("daily_spo2.json"))
    df["day"] = pd.to_datetime(df["day"])
    df["spo2_avg"] = df["spo2_percentage"].apply(
        lambda x: x.get("average") if isinstance(x, dict) else None
    )
    return df[["day", "spo2_avg", "breathing_disturbance_index"]]


def process_stress():
    """Daily stress → clean zero-means-no-data."""
    df = pd.DataFrame(load_raw("daily_stress.json"))
    df["day"] = pd.to_datetime(df["day"])
    df = df[["day", "stress_high", "recovery_high", "day_summary"]]

    # Rule: both stress_high=0 AND recovery_high=0 means no data, not "zero stress"
    no_data_mask = (df["stress_high"] == 0) & (df["recovery_high"] == 0)
    df.loc[no_data_mask, "stress_high"] = np.nan
    df.loc[no_data_mask, "recovery_high"] = np.nan
    df.loc[no_data_mask, "day_summary"] = np.nan

    # Convert seconds to hours for readability
    df["stress_high_hours"] = df["stress_high"] / 3600
    df["recovery_high_hours"] = df["recovery_high"] / 3600
    df = df.drop(columns=["stress_high", "recovery_high"])

    return df


def process_sleep():
    """Sleep → one row per day. Only long_sleep for main metrics; naps as features."""
    raw = load_raw("sleep.json")
    df = pd.DataFrame(raw)
    df["day"] = pd.to_datetime(df["day"])

    # ── Nap feature: did the person nap today, and for how long? ──
    naps = df[df["type"] != "long_sleep"].groupby("day").agg(
        nap_count=("total_sleep_duration", "count"),
        nap_total_seconds=("total_sleep_duration", "sum"),
    ).reset_index()
    naps["has_nap"] = True

    # ── Main sleep: only long_sleep ──
    main = df[df["type"] == "long_sleep"].copy()

    # If multiple long_sleep on same day (rare), keep the longest
    main = main.sort_values("total_sleep_duration", ascending=False).drop_duplicates(
        subset=["day"], keep="first"
    )

    # Extract HRV stats from hrv.items time series
    hrv_records = []
    for _, row in main.iterrows():
        hrv_data = row.get("hrv")
        if hrv_data and isinstance(hrv_data, dict) and hrv_data.get("items"):
            items = [x for x in hrv_data["items"] if x is not None]
            if items:
                hrv_records.append({
                    "day": row["day"],
                    "sleep_hrv_peak": max(items),
                    "sleep_hrv_min": min(items),
                    "sleep_hrv_range": max(items) - min(items),
                })
    hrv_df = pd.DataFrame(hrv_records)

    # Convert durations from seconds to hours
    duration_cols = [
        "total_sleep_duration", "deep_sleep_duration", "light_sleep_duration",
        "rem_sleep_duration", "awake_time", "time_in_bed",
    ]
    for col in duration_cols:
        main[f"{col}_hours"] = main[col] / 3600

    main["latency_minutes"] = main["latency"] / 60

    keep = [
        "day",
        "total_sleep_duration_hours", "deep_sleep_duration_hours",
        "light_sleep_duration_hours", "rem_sleep_duration_hours",
        "awake_time_hours", "time_in_bed_hours", "latency_minutes",
        "efficiency", "average_heart_rate", "lowest_heart_rate",
        "average_hrv", "average_breath", "restless_periods",
        "bedtime_start", "bedtime_end",
    ]
    main = main[[c for c in keep if c in main.columns]]

    # Rename for clarity
    rename_map = {
        "average_heart_rate": "sleep_avg_hr",
        "lowest_heart_rate": "sleep_lowest_hr",
        "average_hrv": "sleep_avg_hrv",
        "average_breath": "sleep_avg_breath",
    }
    main = main.rename(columns=rename_map)

    # Merge HRV stats
    if not hrv_df.empty:
        main = main.merge(hrv_df, on="day", how="left")

    # Merge nap info
    main = main.merge(naps, on="day", how="left")
    main["has_nap"] = main["has_nap"].fillna(False)
    main["nap_count"] = main["nap_count"].fillna(0).astype(int)
    main["nap_total_seconds"] = main["nap_total_seconds"].fillna(0)
    main["nap_total_hours"] = main["nap_total_seconds"] / 3600
    main = main.drop(columns=["nap_total_seconds"])

    return main


def process_heartrate():
    """Heartrate → daily aggregates by source."""
    raw = load_raw("heartrate.json")
    df = pd.DataFrame(raw)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["day"] = df["timestamp"].dt.normalize()

    df["day"] = df["day"].dt.tz_localize(None)
    agg = df.groupby(["day", "source"])["bpm"].agg(["mean", "max", "min", "count"]).reset_index()

    all_days = pd.DataFrame({"day": df["day"].unique()}).sort_values("day").reset_index(drop=True)

    result = all_days.copy()
    for source in ["awake", "workout", "rest"]:
        src = agg[agg["source"] == source].copy()
        src = src.rename(columns={
            "mean": f"hr_{source}_avg",
            "max": f"hr_{source}_max",
            "min": f"hr_{source}_min",
            "count": f"hr_{source}_count",
        })
        src = src[["day"] + [c for c in src.columns if c.startswith(f"hr_{source}")]]
        result = result.merge(src, on="day", how="left")

    return result


# =========================================================================
# STEP 2: Merge all datasets
# =========================================================================

def merge_all():
    print("Loading and processing datasets...")
    dfs = {
        "activity": process_activity(),
        "readiness": process_readiness(),
        "spo2": process_spo2(),
        "stress": process_stress(),
        "sleep": process_sleep(),
        "heartrate": process_heartrate(),
    }

    for name, df in dfs.items():
        print(f"  {name:12s}: {len(df)} rows, {len(df.columns)} columns")

    # Outer join on day — keep all days from any dataset
    merged = dfs["activity"]
    for name in ["readiness", "spo2", "stress", "sleep", "heartrate"]:
        merged = merged.merge(dfs[name], on="day", how="outer")

    merged = merged.sort_values("day").reset_index(drop=True)

    # Deduplicate: if outer join produces multiple rows for the same day, keep first
    before = len(merged)
    merged = merged.drop_duplicates(subset=["day"], keep="first").reset_index(drop=True)
    if len(merged) < before:
        print(f"  Deduped: {before} → {len(merged)} rows ({before - len(merged)} duplicates removed)")

    print(f"\nMerged: {len(merged)} days, {len(merged.columns)} columns")
    return merged


# =========================================================================
# STEP 3: Annotate
# =========================================================================

def annotate(df):
    print("Annotating...")
    first_day = df["day"].min()

    # ── 3a: Data confidence flags ──
    df["is_known_absence"] = get_absence_mask(df["day"])
    df["absence_reason"] = df["day"].apply(get_absence_reason)

    df["is_cold_start"] = df["day"] < (first_day + pd.Timedelta(days=COLD_START_DAYS))

    df["is_low_wear"] = (
        (df["non_wear_time"].fillna(0) > NON_WEAR_THRESHOLD_HOURS * 3600) |
        (df["steps"].fillna(0) < MIN_STEPS_THRESHOLD)
    )

    df["data_confidence"] = "normal"
    df.loc[df["is_cold_start"], "data_confidence"] = "cold_start"
    df.loc[df["is_low_wear"], "data_confidence"] = "low_wear"
    df.loc[df["is_known_absence"], "data_confidence"] = "known_absence"

    # ── 3b: Tennis match annotations ──
    tennis_days = get_tennis_match_days()
    tennis_df = get_tennis_df()
    df["is_tennis_match"] = df["day"].isin(tennis_days)

    df = df.merge(
        tennis_df[["day", "opponent", "result", "sets"]].rename(columns={
            "opponent": "tennis_opponent",
            "result": "tennis_result",
            "sets": "tennis_sets",
        }),
        on="day",
        how="left",
    )

    # Pre/post match flags (day before and day after a match)
    for offset, label in [(1, "post_match"), (-1, "pre_match")]:
        offset_days = {d + pd.Timedelta(days=offset) for d in tennis_days}
        df[f"is_{label}"] = df["day"].isin(offset_days)

    # ── 3c: Day of week ──
    df["day_of_week"] = df["day"].dt.day_name()
    df["is_weekend"] = df["day"].dt.dayofweek >= 5

    # ── 3d: Reorder columns ──
    # Put annotation columns at the end
    annotation_cols = [
        "data_confidence", "is_known_absence", "absence_reason",
        "is_cold_start", "is_low_wear",
        "is_tennis_match", "tennis_opponent", "tennis_result", "tennis_sets",
        "is_pre_match", "is_post_match",
        "day_of_week", "is_weekend",
    ]
    metric_cols = [c for c in df.columns if c not in annotation_cols and c != "day"]
    df = df[["day"] + metric_cols + annotation_cols]

    return df


# =========================================================================
# STEP 4: Summary report
# =========================================================================

def print_summary(df):
    print("\n" + "=" * 60)
    print("PROCESSED DATASET SUMMARY")
    print("=" * 60)
    print(f"Date range: {df['day'].min().date()} → {df['day'].max().date()}")
    print(f"Total days: {len(df)}")
    print(f"\nData confidence breakdown:")
    for val, count in df["data_confidence"].value_counts().items():
        print(f"  {val:20s}: {count:3d} days ({count/len(df)*100:.1f}%)")

    usable = df[df["data_confidence"] == "normal"]
    print(f"\nUsable days (normal confidence): {len(usable)}")

    print(f"\nTennis matches: {df['is_tennis_match'].sum()} days")
    print(f"Post-match days: {df['is_post_match'].sum()} days")

    print(f"\nColumn count: {len(df.columns)}")
    print(f"\nNull rates for key metrics (normal days only):")
    key_metrics = [
        "activity_score", "steps", "readiness_score",
        "total_sleep_duration_hours", "sleep_avg_hrv", "sleep_hrv_peak",
        "spo2_avg", "stress_high_hours", "temperature_deviation",
        "hr_awake_avg", "hr_workout_avg",
    ]
    for col in key_metrics:
        if col in usable.columns:
            null_pct = usable[col].isna().mean() * 100
            valid = usable[col].notna().sum()
            print(f"  {col:35s}: {valid:3d} valid / {len(usable)} ({null_pct:4.1f}% null)")


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    merged = merge_all()
    annotated = annotate(merged)
    print_summary(annotated)

    # Save
    os.makedirs(OUT, exist_ok=True)

    csv_path = os.path.join(OUT, "daily_merged.csv")
    annotated.to_csv(csv_path, index=False)
    print(f"\nSaved: {csv_path}")

    json_path = os.path.join(OUT, "daily_merged.json")
    annotated.to_json(json_path, orient="records", date_format="iso", indent=2)
    print(f"Saved: {json_path}")

    print("\n✅ Pipeline complete.")
