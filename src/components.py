from pathlib import Path
import base64
import streamlit as st

from src.data_loader import get_photo_path
from src.team_flags import flag_url


def refresh_live_data_button() -> None:
    if st.button("🔄 Refresh Live Data"):
        st.cache_data.clear()
        st.rerun()


def image_to_base64(image_path: Path) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def render_avatar(member_name: str, photo_filename: str | None = None, size: int = 72) -> None:
    photo_path = get_photo_path(photo_filename) if photo_filename else None

    if photo_path and Path(photo_path).exists():
        encoded = image_to_base64(Path(photo_path))

        st.markdown(
            f"""
            <img src="data:image/png;base64,{encoded}"
                 style="
                     width:{size}px;
                     height:{size}px;
                     border-radius:50%;
                     object-fit:cover;
                     border:3px solid rgba(255,255,255,0.25);
                 ">
            """,
            unsafe_allow_html=True,
        )
    else:
        initials = "".join([part[0] for part in member_name.split()[:2]]).upper()

        st.markdown(
            f"""
            <div style="
                width:{size}px;
                height:{size}px;
                border-radius:50%;
                background:#e5e7eb;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:{int(size * 0.38)}px;
                font-weight:700;
                color:#374151;
                border:2px solid #d1d5db;
            ">
                {initials}
            </div>
            """,
            unsafe_allow_html=True,
        )


def team_label_html(team_name: str | None, flag_width: int = 24) -> str:
    if not team_name:
        return "Unknown"

    url = flag_url(team_name)

    if not url:
        return team_name

    return (
        f'<span style="display:inline-flex; align-items:center; gap:8px;">'
        f'<img src="{url}" width="{flag_width}" style="border-radius:3px;">'
        f'<span>{team_name}</span>'
        f'</span>'
    )


def render_team_card(team_name: str, group: str | None = None) -> None:
    group_text = f"Group {group}" if group else ""

    st.markdown(
        f"""
        <div style="
            padding:12px;
            border-radius:12px;
            border:1px solid rgba(128,128,128,0.28);
            text-align:center;
            min-height:82px;
        ">
            <div style="font-weight:700; font-size:16px;">
                {team_label_html(team_name, flag_width=26)}
            </div>
            <div style="color:gray; font-size:13px; margin-top:6px;">
                {group_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(title: str, value: str, caption: str | None = None) -> None:
    st.markdown(
        f"""
        <div style="
            padding:18px;
            border-radius:16px;
            border:1px solid rgba(128,128,128,0.25);
            background:rgba(128,128,128,0.06);
            height:100%;
        ">
            <div style="font-size:14px; opacity:0.75;">{title}</div>
            <div style="font-size:26px; font-weight:800; margin-top:4px;">{value}</div>
            <div style="font-size:13px; opacity:0.7; margin-top:6px;">{caption or ""}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_matchup_card(
        home_team: str,
        away_team: str,
        home_owner: str,
        away_owner: str,
        home_photo: str | None,
        away_photo: str | None,
        kickoff_time: str,
        status: str,
        score: str,
) -> None:
    with st.container(border=True):
        col_home, col_mid, col_away = st.columns([3, 1.2, 3])

        with col_home:
            render_avatar(home_owner, home_photo, size=80)
            st.markdown(f"### {home_owner}")
            st.markdown(team_label_html(home_team, flag_width=30), unsafe_allow_html=True)

        with col_mid:
            st.markdown(
                f"""
                <div style="text-align:center; margin-top:18px;">
                    <div style="font-size:13px; opacity:0.75;">{kickoff_time}</div>
                    <div style="font-size:28px; font-weight:800; margin-top:8px;">{score}</div>
                    <div style="font-size:13px; opacity:0.75; margin-top:4px;">{status}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_away:
            render_avatar(away_owner, away_photo, size=80)
            st.markdown(f"### {away_owner}")
            st.markdown(team_label_html(away_team, flag_width=30), unsafe_allow_html=True)