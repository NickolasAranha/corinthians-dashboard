from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Match:
    id_jogo: str
    data: date
    temporada: int
    competicao: str
    adversario: str
    mando: str
    gols_pro: int
    gols_contra: int
    resultado: str
    pontos: int
    decidido_penaltis: str
    tecnico: str = ""


@dataclass(frozen=True)
class CoachPeriod:
    tecnico: str
    inicio: date
    fim: date | None
    interino: str
