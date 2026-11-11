import csv
from dataclasses import replace
from datetime import date
from pathlib import Path

from etl.modelos import CoachPeriod, Match


def load_coaches(path: Path) -> list[CoachPeriod]:
    with open(path, encoding="utf-8", newline="") as f:
        periodos = [
            CoachPeriod(
                tecnico=r["tecnico"],
                inicio=date.fromisoformat(r["inicio"]),
                fim=date.fromisoformat(r["fim"]) if r["fim"] else None,
                interino=r["interino"],
            )
            for r in csv.DictReader(f)
        ]
    ordenados = sorted(periodos, key=lambda p: p.inicio)
    for anterior, atual in zip(ordenados, ordenados[1:]):
        if (anterior.fim or date.max) >= atual.inicio:
            raise ValueError(
                f"Períodos sobrepostos em {path}: {anterior.tecnico} e {atual.tecnico}")
    return periodos


def assign_coaches(matches: list[Match], periods: list[CoachPeriod]) -> list[Match]:
    saida = []
    for m in matches:
        dono = next((p for p in periods if p.inicio <= m.data <= (p.fim or date.max)), None)
        if dono is None:
            raise ValueError(
                f"Nenhum técnico cobre o jogo de {m.data.isoformat()} contra {m.adversario}; "
                "ajuste data/tecnicos.csv")
        saida.append(replace(m, tecnico=dono.tecnico))
    return saida
