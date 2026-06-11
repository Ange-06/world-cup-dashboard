import streamlit as st

from src.api import load_standings
from src.data_loader import load_teams
from src.standings import attach_team_metadata, get_group_table
from src.team_flags import flag_url


st.set_page_config(
    page_title="Group Tables",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Group Stage Tables")
st.caption("Live group-stage standings with each team’s family owner.")

standings_df = load_standings()
teams_df = load_teams()

if standings_df.empty:
    st.error("No standings data available from the API.")
    st.stop()

standings_with_owners = attach_team_metadata(standings_df, teams_df)

missing_owners = standings_with_owners[standings_with_owners["member_name"].isna()]

if not missing_owners.empty:
    st.warning(
        "Some API team names do not match teams.csv. "
        "Check the mismatched team names below."
    )
    st.dataframe(
        missing_owners[["team"]].drop_duplicates(),
        use_container_width=True,
        hide_index=True,
    )

groups = list("ABCDEFGHIJKL")

for row_start in range(0, len(groups), 3):
    cols = st.columns(3)

    for col, group_letter in zip(cols, groups[row_start:row_start + 3]):
        with col:
            st.subheader(f"Group {group_letter}")

            group_table = get_group_table(standings_with_owners, group_letter)

            if group_table.empty:
                st.info("No teams found for this group.")
                continue

            group_table = group_table.copy()

            # Add real image flag URL column for Streamlit ImageColumn rendering.
            group_table.insert(
                loc=1,
                column="flag",
                value=group_table["team"].apply(flag_url),
            )

            display_table = group_table.rename(
                columns={
                    "rank": "#",
                    "flag": "Flag",
                    "team": "Team",
                    "member_name": "Owner",
                    "played": "P",
                    "won": "W",
                    "draw": "D",
                    "lost": "L",
                    "goals_for": "GF",
                    "goals_against": "GA",
                    "goal_difference": "GD",
                    "points": "Pts",
                }
            )

            st.dataframe(
                display_table,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Flag": st.column_config.ImageColumn(
                        "Flag",
                        width="small",
                    ),
                    "#": st.column_config.NumberColumn(
                        "#",
                        width="small",
                    ),
                    "Team": st.column_config.TextColumn(
                        "Team",
                        width="medium",
                    ),
                    "Owner": st.column_config.TextColumn(
                        "Owner",
                        width="medium",
                    ),
                    "P": st.column_config.NumberColumn("P", width="small"),
                    "W": st.column_config.NumberColumn("W", width="small"),
                    "D": st.column_config.NumberColumn("D", width="small"),
                    "L": st.column_config.NumberColumn("L", width="small"),
                    "GF": st.column_config.NumberColumn("GF", width="small"),
                    "GA": st.column_config.NumberColumn("GA", width="small"),
                    "GD": st.column_config.NumberColumn("GD", width="small"),
                    "Pts": st.column_config.NumberColumn("Pts", width="small"),
                },
            )