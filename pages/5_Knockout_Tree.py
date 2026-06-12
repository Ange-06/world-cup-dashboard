import pandas as pd
import streamlit as st

from src.api import load_matches
from src.data_loader import load_teams, load_members
from src.matchups import attach_owners, format_score
from src.knockout import (
    KNOCKOUT_STAGE_ORDER,
    KNOCKOUT_STAGE_LABELS,
    get_knockout_matches,
    get_stage_matches,
    get_match_winner,
)
from src.components import (
    refresh_live_data_button,
    render_avatar,
    team_label_html,
)
from src.time_utils import add_time_columns


st.set_page_config(
    page_title="Knockout Tree",
    page_icon="🌳",
    layout="wide",
)

st.title("🌳 Knockout Stage Tree")
st.caption("Live knockout-stage bracket with family ownership, flags, match times, and scores.")

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

knockout_df = get_knockout_matches(matches_with_owners)

if knockout_df.empty:
    st.info(
        "No knockout-stage matches are available yet. "
        "This page will automatically populate once the API provides knockout fixtures."
    )
    st.stop()


def clean_value(value, fallback: str = "TBC") -> str:
    if value is None or pd.isna(value):
        return fallback

    value = str(value).strip()

    if value.lower() in ["nan", "none", ""]:
        return fallback

    return value


def render_knockout_match(match, match_number: int) -> None:
    home_team = clean_value(match.get("home_team"))
    away_team = clean_value(match.get("away_team"))

    home_owner = clean_value(match.get("home_owner"))
    away_owner = clean_value(match.get("away_owner"))

    home_photo = match.get("home_photo")
    away_photo = match.get("away_photo")

    kickoff_time = clean_value(match.get("kickoff_time"), "Time TBC")
    status = clean_value(match.get("status"))
    winner_team = get_match_winner(match)

    with st.container(border=True):
        st.markdown(f"### Match {match_number}")
        st.caption(kickoff_time)

        col_home, col_score, col_away = st.columns([3, 1, 3])

        with col_home:
            render_avatar(home_owner, home_photo, size=64)
            st.markdown(f"**{home_owner}**")
            st.markdown(
                team_label_html(home_team, flag_width=26),
                unsafe_allow_html=True,
            )

        with col_score:
            st.markdown(
                f"""
                <div style="text-align:center; font-size:24px; font-weight:800; margin-top:28px;">
                    {format_score(match)}
                </div>
                <div style="text-align:center; font-size:12px; opacity:0.7;">
                    {status}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_away:
            render_avatar(away_owner, away_photo, size=64)
            st.markdown(f"**{away_owner}**")
            st.markdown(
                team_label_html(away_team, flag_width=26),
                unsafe_allow_html=True,
            )

        if winner_team:
            st.success(f"Winner: {winner_team}")


MATCHES_PER_ROW = 4

for stage in KNOCKOUT_STAGE_ORDER:
    stage_matches = get_stage_matches(knockout_df, stage)

    st.divider()
    st.header(KNOCKOUT_STAGE_LABELS[stage])

    if stage_matches.empty:
        st.info("Fixtures not available yet.")
        continue

    stage_matches = stage_matches.reset_index(drop=True)

    for row_start in range(0, len(stage_matches), MATCHES_PER_ROW):
        cols = st.columns(MATCHES_PER_ROW)
        row_matches = stage_matches.iloc[row_start:row_start + MATCHES_PER_ROW]

        for col, (idx, match) in zip(cols, row_matches.iterrows()):
            with col:
                render_knockout_match(match, idx + 1)

st.divider()

st.subheader("Knockout Scoring Reminder")

st.markdown(
    """
    - Reach Round of 32 = **+2 points**
    - Reach Round of 16 = **+4 points**
    - Reach Quarter-Final = **+6 points**
    - Reach Semi-Final = **+10 points**
    - Reach Final = **+15 points**
    - Win World Cup = **+25 points**
    """
)