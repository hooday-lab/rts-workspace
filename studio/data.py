# -*- coding: utf-8 -*-
"""Wczytywanie danych RTSstat-data (format API-Football v3, układ folderów v2).

root/
  <sezon>/standings.json  fixtures.json  teams.json  players.json   (players.json = cała liga)
  <sezon>/fixtures/<id>.json   (events, statistics, players, lineups — tylko bieżący sezon)
  <sezon>/widzew-team-stats.json
"""
import json, os, glob

WIDZEW_PATTERN = "widzew"

def _load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)

class Store:
    def __init__(self, root):
        self.root = root
        self.seasons = sorted(int(os.path.basename(p)) for p in glob.glob(os.path.join(root, "[0-9][0-9][0-9][0-9]")))
        if not self.seasons:
            raise SystemExit("Brak folderów sezonów w " + root)
        self.current = self.seasons[-1]
        self._cache = {}

    def get(self, season, name, default=None):
        key = (season, name)
        if key not in self._cache:
            self._cache[key] = _load(os.path.join(self.root, str(season), name), default)
        return self._cache[key]

    def teams(self, season=None):
        t = self.get(season or self.current, "teams.json", [])
        return {x["team"]["id"]: x["team"]["name"] for x in t}

    def widzew_id(self):
        for season in reversed(self.seasons):
            for tid, name in self.teams(season).items():
                if WIDZEW_PATTERN in name.lower():
                    return tid
        raise SystemExit("Nie znaleziono Widzewa w teams.json")

    def fixtures(self, season):
        return self.get(season, "fixtures.json", [])

    def detail(self, season, fid):
        return _load(os.path.join(self.root, str(season), "fixtures", f"{fid}.json"))

    def players(self, season):
        """Spłaszcza /players: jeden wiersz na zawodnika (pierwszy wpis statystyk w lidze)."""
        rows = []
        for item in self.get(season, "players.json", []):
            p = item["player"]
            for st in item.get("statistics", []):
                mins = (st.get("games") or {}).get("minutes") or 0
                if mins <= 0:
                    continue
                rows.append({"pid": p["id"], "name": p["name"], "age": p.get("age"), "season": season,
                             "team_id": st["team"]["id"], "team": st["team"]["name"],
                             "pos": (st["games"] or {}).get("position") or "?", "min": mins,
                             "apps": (st["games"] or {}).get("appearences") or 0,
                             "rating": _f((st["games"] or {}).get("rating")),
                             "st": st})
        return rows

def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def finished(fx):
    return [f for f in fx if f["fixture"]["status"]["short"] in ("FT", "AET", "PEN")]

def result_for(f, team_id):
    """-> (gf, ga, home, outcome W/R/P, round_no)"""
    h = f["teams"]["home"]["id"] == team_id
    gh, ga = f["goals"]["home"], f["goals"]["away"]
    gf, gc = (gh, ga) if h else (ga, gh)
    o = "W" if gf > gc else ("R" if gf == gc else "P")
    rnd = "".join(ch for ch in (f["league"].get("round") or "") if ch.isdigit())
    return gf, gc, h, o, int(rnd) if rnd else None
