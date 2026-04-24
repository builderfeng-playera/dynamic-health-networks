"""
Metadata annotations for the Oura Ring dataset.
Contains known context that cannot be derived from the data itself.
"""

from typing import Optional

import pandas as pd

# ── Travel / Non-Wear Periods ──
# Periods where data is missing or unreliable due to known external reasons.
KNOWN_ABSENCE_PERIODS = [
    {
        "start": "2026-02-26",
        "end": "2026-03-26",
        "reason": "travel_no_charger",
        "description": "San Francisco trip, no ring charger brought",
    },
]

# ── Tennis Matches ──
TENNIS_MATCHES = [
    {"day": "2025-10-15", "round": "R2", "opponent": "Shushan Dai",  "score": "1-6, 7⁷-6⁵, 1¹⁰-0⁶", "result": "W", "sets": 3, "start_time": "18:55"},
    {"day": "2025-10-23", "round": "R4", "opponent": "Robert Mireles","score": "6-4, 6-2",             "result": "W", "sets": 2, "start_time": "17:46"},
    {"day": "2025-10-25", "round": "R1", "opponent": "Nicholas Best", "score": "3-6, 2-6",             "result": "L", "sets": 2, "start_time": "08:30"},
    {"day": "2025-11-10", "round": "R3", "opponent": "Yingshan Zhao", "score": "6-1, 2-6, 1¹⁰-0⁷",   "result": "W", "sets": 3, "start_time": "21:52"},
]

# ── Oura Cold-Start Window ──
# Oura needs ~14 days to establish personal baselines for HRV, temperature, sleep balance.
# Contributors like hrv_balance, sleep_balance, sleep_regularity will be null during this period.
COLD_START_DAYS = 14

# ── Non-Wear Threshold ──
# If non_wear_time exceeds this fraction of the day, mark as low confidence.
NON_WEAR_THRESHOLD_HOURS = 12

# ── Minimum Steps Threshold ──
# Days below this are almost certainly non-wear or device-off days.
MIN_STEPS_THRESHOLD = 100


def get_absence_mask(dates: pd.Series) -> pd.Series:
    """Returns a boolean mask: True if the date falls within a known absence period."""
    mask = pd.Series(False, index=dates.index)
    for period in KNOWN_ABSENCE_PERIODS:
        start = pd.Timestamp(period["start"])
        end = pd.Timestamp(period["end"])
        mask |= (dates >= start) & (dates <= end)
    return mask


def get_absence_reason(date: pd.Timestamp) -> Optional[str]:
    """Returns the reason string for a known absence, or None."""
    for period in KNOWN_ABSENCE_PERIODS:
        if pd.Timestamp(period["start"]) <= date <= pd.Timestamp(period["end"]):
            return period["reason"]
    return None


def get_tennis_match_days() -> set:
    return {pd.Timestamp(m["day"]) for m in TENNIS_MATCHES}


def get_tennis_df() -> pd.DataFrame:
    df = pd.DataFrame(TENNIS_MATCHES)
    df["day"] = pd.to_datetime(df["day"])
    return df
