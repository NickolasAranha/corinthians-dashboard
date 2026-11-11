import csv
from dataclasses import fields
from pathlib import Path

from etl.modelos import Match


def write_matches_csv(matches: list[Match], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    colunas = [f.name for f in fields(Match)]
    with open(path, "w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=colunas, lineterminator="\n")
        escritor.writeheader()
        for m in matches:
            linha = {c: getattr(m, c) for c in colunas}
            linha["data"] = m.data.isoformat()
            escritor.writerow(linha)
