import streamlit as st

from src.api import load_matches
from src.data_loader import load_teams
from src.matchups import (
    attach_owners,
    get_matches_for_date,
    get_member_vs_member_matches,
    format_score,
)
from src.components import team_label_html


st.set_page_config(
    page_title="Today's Matchups",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ Today's Matchups")
st.caption("Daily World Cup fixtures with family ownership matchups.")

matches_df = load_matches()
teams_df = load_teams()

if matches_df.empty:
    st.error("No match data available from the API.")
    st.stop()

matches_with_owners = attach_owners(matches_df, teams_df)

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
        with st.container(border=True):
            col_home, col_score, col_away = st.columns([3, 1, 3])

            with col_home:
                st.markdown(
                    f"### {team_label_html(match['home_team'], flag_width=34)}",
                    unsafe_allow_html=True,
                )
                st.markdown(f"Owner: **{match['home_owner']}**")
                st.caption(f"Group {match['home_group']}")

            with col_score:
                st.markdown(
                    f"""
                    <div style="text-align:center; font-size:28px; font-weight:700; margin-top:25px;">
                        {format_score(match)}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.caption(match["status"])

            with col_away:
                st.markdown(
                    f"### {team_label_html(match['away_team'], flag_width=34)}",
                    unsafe_allow_html=True,
                )
                st.markdown(f"Owner: **{match['away_owner']}**")
                st.caption(f"Group {match['away_group']}")

st.divider()

st.subheader("Family Member-vs-Member Matches")

member_vs_member = get_member_vs_member_matches(daily_matches)

if member_vs_member.empty:
    st.info("No member-vs-member matchups on this date.")
else:
    for _, match in member_vs_member.iterrows():
        st.success(
            f"{match['home_owner']} ({match['home_team']}) "
            f"vs {match['away_owner']} ({match['away_team']})"
        )

        st.markdown(
            f"""
            <div style="
                padding:10px 14px;
                border-radius:10px;
                border:1px solid rgba(128,128,128,0.25);
                margin-bottom:8px;
            ">
                <strong>{match['home_owner']}</strong>
                &nbsp; {team_label_html(match['home_team'], flag_width=24)}
                &nbsp;&nbsp; vs &nbsp;&nbsp;
                <strong>{match['away_owner']}</strong>
                &nbsp; {team_label_html(match['away_team'], flag_width=24)}
            </div>
            """,
            unsafe_allow_html=True,
        )