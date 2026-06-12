import pandas as pd


SA_TIMEZONE = "Africa/Johannesburg"


def format_match_time(row) -> str:
    """
    Returns kickoff time as UTC and South African time.
    Example: 19:00 UTC / 21:00 SAST
    """
    utc_dt = row.get("utc_date")

    if pd.isna(utc_dt):
        return "Time TBC"

    utc_dt = pd.to_datetime(utc_dt, utc=True)
    sa_dt = utc_dt.tz_convert(SA_TIMEZONE)

    return f"{utc_dt.strftime('%H:%M')} UTC / {sa_dt.strftime('%H:%M')} SAST"


def add_time_columns(matches_df: pd.DataFrame) -> pd.DataFrame:
    df = matches_df.copy()

    if "utc_date" in df.columns:
        df["kickoff_time"] = df.apply(format_match_time, axis=1)

    return df