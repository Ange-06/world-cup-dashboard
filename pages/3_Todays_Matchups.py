import streamlit as st

from src.api import load_matches
from src.data_loader import load_teams, load_members
from src.matchups import (
    attach_owners,
    get_matches_for_date,
    get_member_vs_member_matches,
    format_score,
)
from src.components import refresh_live_data_button, render_matchup_card
from src.time_utils import add_time_columns


st.set_page_config(
    page_title="Today's Matchups",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ Today's Matchups")
st.caption("Daily World Cup fixtures with family ownership matchups.")

refresh_live_data_button()

matches_df = add_time_columns(load_matches())
teams_df = load_teams()
members_df = load_members()

if matches_df.empty:
    st.error("No match data available from the API.")
    st.stop()

matches_with_owners = attach_owners(matches_df, teams_df)

member_photo_map = members_df.set_index("member_name")["photo"].to_dict()

matches_with_owners["home_photo"] = matches_with_owners["home_owner"].map(member_photo_map)
matches_with_owners["away_photo"] = matches_with_owners["away_owner"].map(member_photo_map)

available_dates = sorted(matches_with_owners["date"].dropna().unique())

selected_date = st.selectbox(
    "Select match day",
    options=available_dates,
    index=0,
)

daily_matches = get_matches_for_date(matches_with_owners, selected_date)

st.subheader(f"Matches on {selected_date}")

if daily_matches.empty:
    st.info("No matches scheduled for this date.")
else:
    for _, match in daily_matches.iterrows():
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

st.subheader("Family Member-vs-Member Matches")

member_vs_member = get_member_vs_member_matches(daily_matches)

if member_vs_member.empty:
    st.info("No member-vs-member matchups on this date.")
else:
    for _, match in member_vs_member.iterrows():
        st.success(
            f"{match['kickoff_time']} — "
            f"{match['home_owner']} ({match['home_team']}) "
            f"vs {match['away_owner']} ({match['away_team']})"
        )