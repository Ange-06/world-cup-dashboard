import pandas as pd


def load_rules_dict(rules_df: pd.DataFrame) -> dict:
    return dict(zip(rules_df["event"], rules_df["points"]))


def add_group_completion_status(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a boolean column showing whether each team's group is complete.

    For the 2026 World Cup group stage:
    - Each group has 4 teams
    - Each team plays 3 group matches
    - Group winner/runner-up bonuses should only apply once every team
      in that group has played all 3 matches.
    """
    df = df.copy()

    group_completion = (
        df.groupby("group")["played"]
        .min()
        .reset_index()
        .rename(columns={"played": "min_group_played"})
    )

    group_completion["group_complete"] = group_completion["min_group_played"] >= 3

    df = df.merge(
        group_completion[["group", "group_complete"]],
        on="group",
        how="left",
    )

    df["group_complete"] = df["group_complete"].fillna(False)

    return df


def calculate_team_scores(standings_df: pd.DataFrame, rules_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates competition points for each team.

    Immediate points:
    - Win
    - Draw
    - Loss

    Delayed points:
    - GroupWinner
    - GroupRunnerUp

    Group bonuses only apply after the group is complete.
    """
    rules = load_rules_dict(rules_df)

    df = standings_df.copy()

    df = add_group_completion_status(df)

    df["base_points"] = (
            df["won"] * rules.get("Win", 3)
            + df["draw"] * rules.get("Draw", 1)
            + df["lost"] * rules.get("Loss", 0)
    )

    df["group_bonus"] = 0

    group_bonus_mask = df["group_complete"] == True

    df.loc[
        group_bonus_mask & (df["rank"] == 1),
        "group_bonus",
    ] = rules.get("GroupWinner", 5)

    df.loc[
        group_bonus_mask & (df["rank"] == 2),
        "group_bonus",
    ] = rules.get("GroupRunnerUp", 3)

    df["team_score"] = df["base_points"] + df["group_bonus"]

    return df


def calculate_member_leaderboard(team_scores_df: pd.DataFrame) -> pd.DataFrame:
    leaderboard = (
        team_scores_df.groupby(["member_id", "member_name"], as_index=False)
        .agg(
            total_points=("team_score", "sum"),
            wins=("won", "sum"),
            draws=("draw", "sum"),
            losses=("lost", "sum"),
            goals_for=("goals_for", "sum"),
            goals_against=("goals_against", "sum"),
            goal_difference=("goal_difference", "sum"),
            teams=("team", lambda x: ", ".join(x)),
        )
    )

    leaderboard = leaderboard.sort_values(
        by=["total_points", "wins", "goal_difference", "goals_for"],
        ascending=[False, False, False, False],
    )

    leaderboard["rank"] = range(1, len(leaderboard) + 1)

    return leaderboard[
        [
            "rank",
            "member_name",
            "total_points",
            "wins",
            "draws",
            "losses",
            "goals_for",
            "goals_against",
            "goal_difference",
            "teams",
        ]
    ]


def get_competition_leaders(leaderboard_df: pd.DataFrame) -> pd.DataFrame:
    if leaderboard_df.empty:
        return leaderboard_df

    top_score = leaderboard_df["total_points"].max()

    return leaderboard_df[
        leaderboard_df["total_points"] == top_score
        ].copy()


def get_team_of_tournament(team_scores_df: pd.DataFrame) -> pd.DataFrame:
    if team_scores_df.empty:
        return team_scores_df

    max_score = team_scores_df["team_score"].max()

    return team_scores_df[
        team_scores_df["team_score"] == max_score
        ].sort_values(
        by=["points", "goal_difference", "goals_for"],
        ascending=[False, False, False],
    )