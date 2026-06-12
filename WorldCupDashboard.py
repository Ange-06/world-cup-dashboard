import pandas as pd
import streamlit as st

from src.api import load_matches, load_standings
from src.data_loader import load_teams, load_members
from src.standings import attach_team_metadata, get_group_table
from src.matchups import attach_owners, format_score
from src.scoring import (
    calculate_team_scores,
    calculate_member_leaderboard,
    get_competition_leaders,
    get_team_of_tournament,
)
from src.components import (
    render_metric_card,
    refresh_live_data_button,
    render_matchup_card,
    team_label_html,
)
from src.time_utils import add_time_columns


st.set_page_config(
    page_title="World Cup Family Dashboard",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ FIFA World Cup 2026 Family Dashboard")
st.caption("Family competition tracker with live fixtures, standings, and ownership scoring.")

refresh_live_data_button()

matches_df = add_time_columns(load_matches())
standings_df = load_standings()
teams_df = load_teams()
members_df = load_members()
rules_df = pd.read_csv("data/rules.csv")

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

today = pd.Timestamp.now(tz="UTC").date()

matches_with_owners = attach_owners(matches_df, teams_df)

member_photo_map = members_df.set_index("member_name")["photo"].to_dict()
matches_with_owners["home_photo"] = matches_with_owners["home_owner"].map(member_photo_map)
matches_with_owners["away_photo"] = matches_with_owners["away_owner"].map(member_photo_map)

today_matches = matches_with_owners[matches_with_owners["date"] == today].copy()

col1, col2, col3, col4 = st.columns(4)

with col1:
    if leaders.empty:
        render_metric_card("🏆 Competition Leader", "No leader yet", "")
    else:
        leader_names = ", ".join(leaders["member_name"].tolist())
        leader_points = int(leaders["total_points"].iloc[0])
        render_metric_card("🏆 Competition Leader", leader_names, f"{leader_points} pts")

with col2:
    if team_of_tournament.empty:
        render_metric_card("🔥 Team of Tournament", "No team yet", "")
    else:
        top_team = team_of_tournament.iloc[0]
        render_metric_card(
            "🔥 Team of Tournament",
            top_team["team"],
            f"{top_team['member_name']} — {int(top_team['team_score'])} pts",
        )
        st.markdown(
            team_label_html(top_team["team"], flag_width=32),
            unsafe_allow_html=True,
        )

with col3:
    render_metric_card("⚽ Matches Today", str(len(today_matches)), "UTC date filter")

with col4:
    active_teams = int((team_scores["played"] > 0).sum())
    render_metric_card("👥 Family Members", "12", f"{active_teams}/48 teams have played")

st.divider()

st.subheader("⚽ Playing Today")

if today_matches.empty:
    st.info("No World Cup matches scheduled today.")
else:
    for _, match in today_matches.iterrows():
        render_matchup_card(
            home_team=match["home_team"],
            away_team=match["away_team"],
            home_owner=match["home_owner"],
            away_owner=match["away_owner"],
            home_photo=match["home_photo"],
            away_photo=match["away_photo"],
            kickoff_time=match["kickoff_time"],
            status=match["status"],
            score=format_score(match),
        )

st.divider()

st.subheader("🏆 Leaderboard Preview")

display_leaderboard = leaderboard.head(5).rename(
    columns={
        "rank": "#",
        "member_name": "Member",
        "total_points": "Points",
        "wins": "W",
        "draws": "D",
        "losses": "L",
        "goal_difference": "GD",
    }
)

st.dataframe(
    display_leaderboard[
        ["#", "Member", "Points", "W", "D", "L", "GD"]
    ],
    use_container_width=True,
    hide_index=True,
)

st.caption("Use the sidebar to view members, group tables, matchups, leaderboard, and later the knockout tree.")