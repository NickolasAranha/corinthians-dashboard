from datetime import datetime
from zoneinfo import ZoneInfo

from etl.modelos import Match

FUSO = ZoneInfo("America/Sao_Paulo")
STATUS_ENCERRADOS = {"STATUS_FULL_TIME", "STATUS_FINAL_AET", "STATUS_FINAL_PEN"}
COMPETICOES = {
    "bra.1": "Brasileirão",
    "bra.camp.paulista": "Paulistão",
    "bra.copa_do_brazil": "Copa do Brasil",
    "conmebol.libertadores": "Libertadores",
    "bra.supercopa_do_brazil": "Supercopa do Brasil",
}


def _resultado(gols_pro: int, gols_contra: int) -> tuple[str, int]:
    if gols_pro > gols_contra:
        return "Vitória", 3
    if gols_pro < gols_contra:
        return "Derrota", 0
    return "Empate", 1


def parse_events(raw: dict, team_id: str = "874") -> list[Match]:
    jogos = []
    for event in raw.get("events", []):
        comp = event["competitions"][0]
        status = comp["status"]["type"]["name"]
        if status not in STATUS_ENCERRADOS:
            continue
        nosso = next(c for c in comp["competitors"] if c["team"]["id"] == team_id)
        outro = next(c for c in comp["competitors"] if c["team"]["id"] != team_id)
        gols_pro = int(nosso["score"]["value"])
        gols_contra = int(outro["score"]["value"])
        resultado, pontos = _resultado(gols_pro, gols_contra)
        data = (datetime.fromisoformat(event["date"].replace("Z", "+00:00"))
                .astimezone(FUSO).date())
        mando = "Neutro" if comp.get("neutralSite") else (
            "Casa" if nosso["homeAway"] == "home" else "Fora")
        liga = event["league"]
        jogos.append(Match(
            id_jogo=str(event["id"]),
            data=data,
            temporada=data.year,
            competicao=COMPETICOES.get(liga["slug"], liga["name"]),
            adversario=outro["team"]["displayName"],
            mando=mando,
            gols_pro=gols_pro,
            gols_contra=gols_contra,
            resultado=resultado,
            pontos=pontos,
            decidido_penaltis="Sim" if status == "STATUS_FINAL_PEN" else "Não",
        ))
    return sorted(jogos, key=lambda m: m.data)
