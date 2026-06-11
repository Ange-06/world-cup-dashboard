import pandas as pd


def attach_owners(matches_df: pd.DataFrame, teams_df: pd.DataFrame) -> pd.DataFrame:
    team_owner_map = teams_df.set_index("team")["member_name"].to_dict()
    team_group_map = teams_df.set_index("team")["group"].to_dict()

    df = matches_df.copy()

    df["home_owner"] = df["home_team"].map(team_owner_map)
    df["away_owner"] = df["away_team"].map(team_owner_map)

    df["home_group"] = df["home_team"].map(team_group_map)
    df["away_group"] = df["away_team"].map(team_group_map)

    return df


def get_matches_for_date(matches_df: pd.DataFrame, selected_date) -> pd.DataFrame:
    return matches_df[matches_df["date"] == selected_date].copy()


def get_member_vs_member_matches(matches_df: pd.DataFrame) -> pd.DataFrame:
    return matches_df[
        matches_df["home_owner"].notna()
        & matches_df["away_owner"].notna()
        & (matches_df["home_owner"] != matches_df["away_owner"])
        ].copy()


def format_score(row) -> str:
    if pd.isna(row["home_score"]) or pd.isna(row["away_score"]):
        return "vs"

    return f"{int(row['home_score'])} - {int(row['away_score'])}"