import requests

URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/all/teams/{team_id}/schedule?season={season}"


def fetch_schedule(season: int, team_id: str = "874") -> dict:
    resposta = requests.get(URL.format(team_id=team_id, season=season), timeout=30)
    resposta.raise_for_status()
    return resposta.json()
