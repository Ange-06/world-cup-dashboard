import pandas as pd


def attach_team_metadata(standings_df: pd.DataFrame, teams_df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds group, member_id, and member_name from local teams.csv to API standings.
    """
    metadata = teams_df[["team", "group", "member_id", "member_name"]].copy()

    merged = standings_df.merge(
        metadata,
        on="team",
        how="left",
    )

    return merged


def get_group_table(standings_df: pd.DataFrame, group_letter: str) -> pd.DataFrame:
    """
    Returns one group table sorted by points, goal difference, goals for, then team name.
    """
    group_df = standings_df[standings_df["group"] == group_letter].copy()

    group_df = group_df.sort_values(
        by=["points", "goal_difference", "goals_for", "team"],
        ascending=[False, False, False, True],
    )

    group_df["rank"] = range(1, len(group_df) + 1)

    return group_df[
        [
            "rank",
            "team",
            "member_name",
            "played",
            "won",
            "draw",
            "lost",
            "goals_for",
            "goals_against",
            "goal_difference",
            "points",
        ]
    ]