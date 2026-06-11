import pandas as pd
import streamlit as st

from src.api import load_standings
from src.data_loader import load_teams
from src.standings import attach_team_metadata, get_group_table
from src.scoring import (
    calculate_team_scores,
    calculate_member_leaderboard,
    get_competition_leaders,
    get_team_of_tournament,
)
from src.team_flags import flag_url


st.set_page_config(
    page_title="Leaderboard",
    page_icon="🏆",
    layout="wide",
)

st.title("🏆 Family Competition Leaderboard")
st.caption("Leaderboard based on live World Cup group-stage performance.")

standings_df = load_standings()
teams_df = load_teams()
rules_df = pd.read_csv("data/rules.csv")

if standings_df.empty:
    st.error("No standings data available from the API.")
    st.stop()

standings_with_owners = attach_team_metadata(standings_df, teams_df)

ranked_groups = []

for group_letter in list("ABCDEFGHIJKL"):
    group_table = get_group_table(standings_with_owners, group_letter)
    ranked_groups.append(group_table)

ranked_standings = pd.concat(ranked_groups, ignore_index=True)

ranked_standings = ranked_standings.merge(
    teams_df[["team", "member_id", "group"]],
    on="team",
    how="left",
)

team_scores = calculate_team_scores(ranked_standings, rules_df)
leaderboard = calculate_member_leaderboard(team_scores)

leaders = get_competition_leaders(leaderboard)
team_of_tournament = get_team_of_tournament(team_scores)

# -----------------------------
# Summary cards
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Competition Leader")

    if leaders.empty:
        st.info("No leader yet.")
    else:
        leader_names = ", ".join(leaders["member_name"].tolist())
        leader_points = int(leaders["total_points"].iloc[0])

        st.metric(
            label=leader_names,
            value=f"{leader_points} pts",
        )

with col2:
    st.subheader("🔥 Team of the Tournament So Far")

    if team_of_tournament.empty:
        st.info("No team leader yet.")
    else:
        top_team = team_of_tournament.iloc[0]

        st.metric(
            label=f"{top_team['team']} — {top_team['member_name']}",
            value=f"{int(top_team['team_score'])} pts",
        )

st.divider()

# -----------------------------
# Main leaderboard
# -----------------------------
st.subheader("Overall Leaderboard")

display_leaderboard = leaderboard.rename(
    columns={
        "rank": "#",
        "member_name": "Member",
        "total_points": "Total Points",
        "wins": "W",
        "draws": "D",
        "losses": "L",
        "goals_for": "GF",
        "goals_against": "GA",
        "goal_difference": "GD",
        "teams": "Teams",
    }
)

st.dataframe(
    display_leaderboard,
    use_container_width=True,
    hide_index=True,
)

st.divider()

# -----------------------------
# Team scores
# -----------------------------
st.subheader("Team-by-Team Scores")

team_scores = team_scores.copy()
team_scores.insert(0, "flag", team_scores["team"].apply(flag_url))

team_scores_display = team_scores[
    [
        "flag",
        "team",
        "member_name",
        "group",
        "rank",
        "played",
        "won",
        "draw",
        "lost",
        "goals_for",
        "goals_against",
        "goal_difference",
        "points",
        "base_points",
        "group_bonus",
        "team_score",
    ]
].rename(
    columns={
        "flag": "Flag",
        "team": "Team",
        "member_name": "Owner",
        "group": "Group",
        "rank": "Group Rank",
        "played": "P",
        "won": "W",
        "draw": "D",
        "lost": "L",
        "goals_for": "GF",
        "goals_against": "GA",
        "goal_difference": "GD",
        "points": "FIFA Points",
        "base_points": "Base Points",
        "group_bonus": "Group Bonus",
        "team_score": "Team Score",
    }
)

st.dataframe(
    team_scores_display,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Flag": st.column_config.ImageColumn("Flag", width="small"),
    },
)