import pandas as pd


KNOCKOUT_STAGE_ORDER = [
    "LAST_32",
    "LAST_16",
    "QUARTER_FINALS",
    "SEMI_FINALS",
    "FINAL",
]


KNOCKOUT_STAGE_LABELS = {
    "LAST_32": "Round of 32",
    "LAST_16": "Round of 16",
    "QUARTER_FINALS": "Quarter-Finals",
    "SEMI_FINALS": "Semi-Finals",
    "FINAL": "Final",
}


def get_knockout_matches(matches_df: pd.DataFrame) -> pd.DataFrame:
    df = matches_df.copy()

    if "stage" not in df.columns:
        return pd.DataFrame()

    df = df[df["stage"].isin(KNOCKOUT_STAGE_ORDER)].copy()

    if df.empty:
        return df

    df["stage_order"] = df["stage"].apply(KNOCKOUT_STAGE_ORDER.index)

    return df.sort_values(
        by=["stage_order", "utc_date"],
        ascending=[True, True],
    ).reset_index(drop=True)


def get_stage_matches(knockout_df: pd.DataFrame, stage: str) -> pd.DataFrame:
    if knockout_df.empty:
        return pd.DataFrame()

    return knockout_df[knockout_df["stage"] == stage].copy()


def get_match_winner(row) -> str | None:
    winner = row.get("winner")

    if winner is None or pd.isna(winner):
        return None

    if winner == "HOME_TEAM":
        return row.get("home_team")

    if winner == "AWAY_TEAM":
        return row.get("away_team")

    if winner == "DRAW":
        return "Penalty winner TBC"

    return None