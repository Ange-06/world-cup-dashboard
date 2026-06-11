from __future__ import annotations

import requests
import pandas as pd
import streamlit as st


BASE_URL = "https://api.football-data.org/v4"


def _headers() -> dict:
    return {
        "X-Auth-Token": st.secrets["FOOTBALL_DATA_API_KEY"]
    }


def _competition_code() -> str:
    return st.secrets.get("FOOTBALL_DATA_COMPETITION_CODE", "WC")


def _season() -> int:
    return int(st.secrets.get("FOOTBALL_DATA_SEASON", 2026))


@st.cache_data(ttl=6 * 60 * 60)
def fetch_matches_raw() -> list[dict]:
    url = f"{BASE_URL}/competitions/{_competition_code()}/matches"

    response = requests.get(
        url,
        headers=_headers(),
        params={"season": _season()},
        timeout=20,
    )

    response.raise_for_status()

    payload = response.json()
    return payload.get("matches", [])


@st.cache_data(ttl=6 * 60 * 60)
def fetch_standings_raw() -> list[dict]:
    url = f"{BASE_URL}/competitions/{_competition_code()}/standings"

    response = requests.get(
        url,
        headers=_headers(),
        params={"season": _season()},
        timeout=20,
    )

    response.raise_for_status()

    payload = response.json()
    return payload.get("standings", [])


def load_matches() -> pd.DataFrame:
    raw_matches = fetch_matches_raw()
    rows = []

    for match in raw_matches:
        score = match.get("score", {})
        full_time = score.get("fullTime", {})

        home_team = match.get("homeTeam", {})
        away_team = match.get("awayTeam", {})

        rows.append(
            {
                "match_id": match.get("id"),
                "utc_date": match.get("utcDate"),
                "stage": match.get("stage"),
                "group": match.get("group"),
                "matchday": match.get("matchday"),
                "home_team": home_team.get("name"),
                "away_team": away_team.get("name"),
                "home_score": full_time.get("home"),
                "away_score": full_time.get("away"),
                "status": match.get("status"),
                "winner": score.get("winner"),
            }
        )

    df = pd.DataFrame(rows)

    if not df.empty:
        df["utc_date"] = pd.to_datetime(df["utc_date"], errors="coerce", utc=True)
        df["date"] = df["utc_date"].dt.date
        df["time_utc"] = df["utc_date"].dt.strftime("%H:%M")

    return df


def load_standings() -> pd.DataFrame:
    raw_standings = fetch_standings_raw()
    rows = []

    for standing_group in raw_standings:
        stage = standing_group.get("stage")

        if stage != "GROUP_STAGE":
            continue

        for row in standing_group.get("table", []):
            team = row.get("team", {})

            rows.append(
                {
                    "stage": stage,
                    "position": row.get("position"),
                    "team": team.get("name"),
                    "played": row.get("playedGames"),
                    "won": row.get("won"),
                    "draw": row.get("draw"),
                    "lost": row.get("lost"),
                    "goals_for": row.get("goalsFor"),
                    "goals_against": row.get("goalsAgainst"),
                    "goal_difference": row.get("goalDifference"),
                    "points": row.get("points"),
                }
            )

    df = pd.DataFrame(rows)

    if not df.empty:
        # The API currently returns standings without group labels,
        # so we attach groups from our local teams.csv in Phase 4.
        df = df.head(48)

    return df