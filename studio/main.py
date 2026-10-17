# -*- coding: utf-8 -*-
"""RTSstat Studio — generator kart.  Użycie:
  python -m rtsstat --data <RTSstat-data> --out <folder> player "Nazwisko" [--team Widzew]
  python -m rtsstat ... suggest "Nazwisko"          # lista proponowanych porównań
  python -m rtsstat ... compare "Nazwisko" [--pick N | --with "Inny"]
  python -m rtsstat ... facts [--top 5]             # lista fun faktów + karty
  python -m rtsstat ... match                       # karta ostatniego meczu Widzewa
"""
import argparse, os, sys
from .data import Store, finished
from . import analysis as an, cards

def main():
    ap = argparse.ArgumentParser(prog="rtsstat")
    ap.add_argument("--data", required=True); ap.add_argument("--out", default="out")
    ap.add_argument("cmd", choices=["player", "suggest", "compare", "facts", "match"])
    ap.add_argument("name", nargs="?"); ap.add_argument("--team"); ap.add_argument("--with", dest="other")
    ap.add_argument("--pick", type=int); ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    st = Store(a.data); wid = st.widzew_id()
    rows_by = {s: an.percentiles(st.players(s)) for s in st.seasons}
    cur = rows_by[st.current]
    src = f"#RTSstat · dane: API-Football · sezon {cards.season_label(st.current)}"
    nxt = [f for f in st.fixtures(st.current) if f["fixture"]["status"]["short"] == "NS" and wid in (f["teams"]["home"]["id"], f["teams"]["away"]["id"])]
    nxt.sort(key=lambda f: f["fixture"]["timestamp"])
    next_opp = None
    if nxt:
        t = nxt[0]["teams"]; next_opp = t["away"]["id"] if t["home"]["id"] == wid else t["home"]["id"]

    def pick(name, team=None):
        hits = an.find_player(cur, name, team)
        if not hits:
            sys.exit(f"Nie znaleziono: {name}")
        return hits[0]
    slug = lambda s: "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")

    if a.cmd == "player":
        p = pick(a.name, a.team)
        hist = sorted([r for s in st.seasons for r in rows_by[s] if r["pid"] == p["pid"] and r["pos"] == p["pos"]], key=lambda r: r["season"])
        print(cards.render(cards.card_player(p, hist, src), os.path.join(a.out, f"zawodnik-{slug(p['name'])}.png")))
    elif a.cmd in ("suggest", "compare"):
        p = pick(a.name, a.team or "Widzew")
        sug = an.suggest(st, rows_by, p, next_opp, wid)
        if a.cmd == "suggest":
            for i, s in enumerate(sug, 1):
                r = s["row"]; print(f"{i}. [{s['type']}] {r['name']} · {r['team']} · {r['season']} — {s['why']}")
            return
        if a.other:
            q = pick(a.other); why = ""
        else:
            s = sug[(a.pick or 1) - 1]; q, why = s["row"], f"{s['type']}: {s['why']}"
        print(cards.render(cards.card_compare(p, q, why, src), os.path.join(a.out, f"porownanie-{slug(p['name'])}-{slug(q['name'])}.png")))
    elif a.cmd == "facts":
        fs = an.mine_team_facts(st, wid)
        for i, f in enumerate(fs, 1):
            print(f"{i}. [{f['kind']}] {f['title']} — wartość {f['value']}, {'rekord w danych' if f['record'] else 'ostatnio ' + cards.season_label(f['last'])}, score {f['score']}")
        for i, f in enumerate(fs[:a.top], 1):
            print(cards.render(cards.card_fact(f, src), os.path.join(a.out, f"fakt-{i}-{slug(f['key'])}.png")))
    elif a.cmd == "match":
        done = sorted([f for f in finished(st.fixtures(st.current)) if wid in (f["teams"]["home"]["id"], f["teams"]["away"]["id"])], key=lambda f: f["fixture"]["timestamp"])
        det = st.detail(st.current, done[-1]["fixture"]["id"])
        if not det:
            sys.exit("Brak szczegółów ostatniego meczu (fixtures/<id>.json).")
        det["fixture"] = done[-1]
        print(cards.render(cards.card_match(det, wid, src), os.path.join(a.out, "ostatni-mecz.png")))

main()
