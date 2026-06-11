import streamlit as st

from src.data_loader import load_members, load_teams
from src.components import render_avatar, render_team_card


st.set_page_config(
    page_title="Members & Teams",
    page_icon="🏆",
    layout="wide",
)

st.title("🏆 Members & Teams")
st.caption("FIFA World Cup 2026 family competition team ownership.")

members_df = load_members()
teams_df = load_teams()

for _, member in members_df.iterrows():
    member_id = member["member_id"]
    member_name = member["member_name"]
    photo_filename = member["photo"]

    member_teams = teams_df[teams_df["member_id"] == member_id]

    with st.container(border=True):
        col_photo, col_info = st.columns([1, 4])

        with col_photo:
            render_avatar(member_name, photo_filename, size=120)

        with col_info:
            st.subheader(member_name)

            team_cols = st.columns(4)

            for idx, (_, team_row) in enumerate(member_teams.iterrows()):
                with team_cols[idx]:
                    render_team_card(
                        team_name=team_row["team"],
                        group=team_row["group"],
                    )