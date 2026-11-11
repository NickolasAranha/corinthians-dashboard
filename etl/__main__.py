import argparse
import json
import sys
from pathlib import Path

from etl.espn import fetch_schedule
from etl.exportar import write_matches_csv
from etl.parse import parse_events
from etl.tecnicos import assign_coaches, load_coaches


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="etl", description="Gera data/jogos.csv a partir da ESPN")
    p.add_argument("--temporada", type=int, required=True)
    p.add_argument("--tecnicos", type=Path, default=Path("data/tecnicos.csv"))
    p.add_argument("--saida", type=Path, default=Path("data/jogos.csv"))
    p.add_argument("--entrada-json", type=Path, default=None,
                   help="lê este JSON em vez de chamar a API")
    args = p.parse_args(argv)

    if args.entrada_json:
        raw = json.loads(args.entrada_json.read_text(encoding="utf-8"))
    else:
        raw = fetch_schedule(args.temporada)
    jogos = [m for m in parse_events(raw) if m.temporada == args.temporada]
    jogos = assign_coaches(jogos, load_coaches(args.tecnicos))
    write_matches_csv(jogos, args.saida)
    print(f"{len(jogos)} jogos gravados em {args.saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
