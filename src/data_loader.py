from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PHOTOS_DIR = PROJECT_ROOT / "assets" / "photos"


def load_members() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "members.csv")


def load_teams() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "teams.csv")


def get_photo_path(photo_filename: str) -> Path | None:
    photo_path = PHOTOS_DIR / photo_filename

    if photo_path.exists():
        return photo_path

    return None