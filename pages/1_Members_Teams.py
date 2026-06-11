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

for row_start in range(0, len(members_df), 3):
    cols = st.columns(3)

    for col, (_, member) in zip(cols, members_df.iloc[row_start:row_start + 3].iterrows()):
        with col:
            member_id = member["member_id"]
            member_name = member["member_name"]
            photo_filename = member["photo"]

            member_teams = teams_df[teams_df["member_id"] == member_id]

            with st.container(border=True):
                avatar_col, name_col = st.columns([1, 2])

                with avatar_col:
                    render_avatar(member_name, photo_filename, size=105)

                with name_col:
                    st.subheader(member_name)
                    st.caption(f"{len(member_teams)} teams")

                st.divider()

                team_cols = st.columns(2)

                for idx, (_, team_row) in enumerate(member_teams.iterrows()):
                    with team_cols[idx % 2]:
                        render_team_card(
                            team_name=team_row["team"],
                            group=team_row["group"],
                        )