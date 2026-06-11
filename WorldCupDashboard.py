import streamlit as st

st.set_page_config(
    page_title="World Cup Family Dashboard",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ World Cup 2026 Family Dashboard")

st.write(
    """
    Welcome to the family World Cup competition dashboard.

    Use the sidebar to navigate between:
    - Members & Teams
    - Group Tables
    - Today's Matchups
    - Leaderboard
    - Knockout Tree
    """
)