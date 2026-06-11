TEAM_FLAG_CODES = {
    "Mexico": "mx", "South Africa": "za", "South Korea": "kr", "Czechia": "cz",
    "Canada": "ca", "Bosnia-Herzegovina": "ba", "Qatar": "qa", "Switzerland": "ch",
    "Brazil": "br", "Morocco": "ma", "Haiti": "ht", "Scotland": "gb-sct",
    "United States": "us", "Paraguay": "py", "Australia": "au", "Turkey": "tr",
    "Germany": "de", "Curaçao": "cw", "Ivory Coast": "ci", "Ecuador": "ec",
    "Netherlands": "nl", "Japan": "jp", "Tunisia": "tn", "Sweden": "se",
    "Belgium": "be", "Egypt": "eg", "Iran": "ir", "New Zealand": "nz",
    "Spain": "es", "Cape Verde Islands": "cv", "Saudi Arabia": "sa", "Uruguay": "uy",
    "France": "fr", "Iraq": "iq", "Senegal": "sn", "Norway": "no",
    "Argentina": "ar", "Algeria": "dz", "Austria": "at", "Jordan": "jo",
    "Congo DR": "cd", "Portugal": "pt", "Uzbekistan": "uz", "Colombia": "co",
    "England": "gb-eng", "Croatia": "hr", "Ghana": "gh", "Panama": "pa",
}


def flag_url(team_name: str | None) -> str | None:
    if not team_name:
        return None

    code = TEAM_FLAG_CODES.get(team_name)

    if not code:
        return None

    return f"https://flagcdn.com/w40/{code}.png"


def team_label(team_name: str | None) -> str:
    return team_name if team_name else "Unknown"