import streamlit as st

from src.data_loader import load_members, load_teams, get_photo_path


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
            photo_path = get_photo_path(photo_filename)

            if photo_path:
                st.image(str(photo_path), width=120)
            else:
                st.markdown(
                    f"""
                    <div style="
                        width:120px;
                        height:120px;
                        border-radius:50%;
                        background:#e5e7eb;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:42px;
                        font-weight:700;
                        color:#374151;
                    ">
                        {member_name[0]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with col_info:
            st.subheader(member_name)

            team_cols = st.columns(4)

            for idx, (_, team_row) in enumerate(member_teams.iterrows()):
                with team_cols[idx]:
                    st.markdown(
                        f"""
                        <div style="
                            padding:12px;
                            border-radius:12px;
                            border:1px solid #ddd;
                            text-align:center;
                        ">
                            <strong>{team_row["team"]}</strong><br>
                            <span style="color:gray;">Group {team_row["group"]}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )