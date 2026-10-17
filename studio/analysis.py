# -*- coding: utf-8 -*-
"""Wskaźniki zawodników, percentyle, dobór porównań i silnik fun faktów."""
import math
from .data import finished, result_for

POS = {"Attacker": "Napastnik", "Midfielder": "Pomocnik", "Defender": "Obrońca", "Goalkeeper": "Bramkarz"}
MIN_POOL = 450  # minimum minut do puli porównawczej (jak FBref dla raportów)

def _n(x):
    return x if isinstance(x, (int, float)) else 0

def _per90(v, m):
    return v / m * 90 if m else 0

def _pct(a, b):
    return 100 * a / b if b else 0

# (klucz, etykieta, funkcja(st, minuty) -> wartość, miejsca po przecinku, jednostka, odwrócony)
def _att():
    return [
     ("g90", "Gole / 90", lambda s, m: _per90(_n(s["goals"]["total"]), m), 2, "", False),
     ("sh90", "Strzały / 90", lambda s, m: _per90(_n(s["shots"]["total"]), m), 1, "", False),
     ("sot", "Celne %", lambda s, m: _pct(_n(s["shots"]["on"]), _n(s["shots"]["total"])), 0, "%", False),
     ("a90", "Asysty / 90", lambda s, m: _per90(_n(s["goals"]["assists"]), m), 2, "", False),
     ("kp90", "Kluczowe podania / 90", lambda s, m: _per90(_n(s["passes"]["key"]), m), 1, "", False),
     ("dr90", "Dryblingi / 90", lambda s, m: _per90(_n(s["dribbles"]["success"]), m), 1, "", False),
     ("duel", "Wygrane pojedynki %", lambda s, m: _pct(_n(s["duels"]["won"]), _n(s["duels"]["total"])), 0, "%", False),
     ("tk90", "Odbiory / 90", lambda s, m: _per90(_n(s["tackles"]["total"]), m), 1, "", False),
     ("fd90", "Wymuszone faule / 90", lambda s, m: _per90(_n(s["fouls"]["drawn"]), m), 1, "", False),
     ("fc90", "Faule / 90", lambda s, m: _per90(_n(s["fouls"]["committed"]), m), 1, "", True)]

def _passacc(s):
    t, a = _n(s["passes"]["total"]), _n(s["passes"]["accuracy"])
    # API bywa zwraca liczbę celnych podań, a bywa procent; jeśli a <= t traktujemy jako liczbę
    return _pct(a, t) if a <= t else a

MET = {
 "Attacker": _att(),
 "Midfielder": [
     ("g90", "Gole / 90", lambda s, m: _per90(_n(s["goals"]["total"]), m), 2, "", False),
     ("a90", "Asysty / 90", lambda s, m: _per90(_n(s["goals"]["assists"]), m), 2, "", False),
     ("kp90", "Kluczowe podania / 90", lambda s, m: _per90(_n(s["passes"]["key"]), m), 1, "", False),
     ("p90", "Podania / 90", lambda s, m: _per90(_n(s["passes"]["total"]), m), 0, "", False),
     ("pacc", "Celność podań %", lambda s, m: _passacc(s), 0, "%", False),
     ("dr90", "Dryblingi / 90", lambda s, m: _per90(_n(s["dribbles"]["success"]), m), 1, "", False),
     ("duel", "Wygrane pojedynki %", lambda s, m: _pct(_n(s["duels"]["won"]), _n(s["duels"]["total"])), 0, "%", False),
     ("tki", "Odbiory + przechwyty / 90", lambda s, m: _per90(_n(s["tackles"]["total"]) + _n(s["tackles"]["interceptions"]), m), 1, "", False),
     ("fd90", "Wymuszone faule / 90", lambda s, m: _per90(_n(s["fouls"]["drawn"]), m), 1, "", False),
     ("fc90", "Faule / 90", lambda s, m: _per90(_n(s["fouls"]["committed"]), m), 1, "", True)],
 "Defender": [
     ("tk90", "Odbiory / 90", lambda s, m: _per90(_n(s["tackles"]["total"]), m), 1, "", False),
     ("int90", "Przechwyty / 90", lambda s, m: _per90(_n(s["tackles"]["interceptions"]), m), 1, "", False),
     ("blk90", "Bloki / 90", lambda s, m: _per90(_n(s["tackles"]["blocks"]), m), 1, "", False),
     ("duel", "Wygrane pojedynki %", lambda s, m: _pct(_n(s["duels"]["won"]), _n(s["duels"]["total"])), 0, "%", False),
     ("pacc", "Celność podań %", lambda s, m: _passacc(s), 0, "%", False),
     ("p90", "Podania / 90", lambda s, m: _per90(_n(s["passes"]["total"]), m), 0, "", False),
     ("ga90", "Gole + asysty / 90", lambda s, m: _per90(_n(s["goals"]["total"]) + _n(s["goals"]["assists"]), m), 2, "", False),
     ("past90", "Minięty w dryblingu / 90", lambda s, m: _per90(_n(s["dribbles"]["past"]), m), 1, "", True),
     ("fc90", "Faule / 90", lambda s, m: _per90(_n(s["fouls"]["committed"]), m), 1, "", True),
     ("cards90", "Kartki / 90", lambda s, m: _per90(_n(s["cards"]["yellow"]) + 2 * _n(s["cards"]["red"]), m), 2, "", True)],
 "Goalkeeper": [
     ("sv90", "Obrony / 90", lambda s, m: _per90(_n(s["goals"]["saves"]), m), 1, "", False),
     ("ga90", "Stracone / 90", lambda s, m: _per90(_n(s["goals"]["conceded"]), m), 2, "", True),
     ("svp", "Skuteczność obron %", lambda s, m: _pct(_n(s["goals"]["saves"]), _n(s["goals"]["saves"]) + _n(s["goals"]["conceded"])), 0, "%", False),
     ("pacc", "Celność podań %", lambda s, m: _passacc(s), 0, "%", False),
     ("p90", "Podania / 90", lambda s, m: _per90(_n(s["passes"]["total"]), m), 0, "", False)],
}

def attach_metrics(rows):
    for r in rows:
        spec = MET.get(r["pos"])
        r["vals"] = [fn(r["st"], r["min"]) for (_, _, fn, _, _, _) in spec] if spec else []

def percentiles(rows, min_pool=MIN_POOL):
    """Dopisuje r['pct'] (0-100, 100 = najlepszy) względem puli tej samej pozycji."""
    attach_metrics(rows)
    for pos, spec in MET.items():
        pool = [r for r in rows if r["pos"] == pos and r["min"] >= min_pool]
        for r in rows:
            if r["pos"] != pos:
                continue
            r["pct"] = []
            for i, (_, _, _, _, _, inv) in enumerate(spec):
                col = [p["vals"][i] for p in pool]
                v = r["vals"][i]
                if not col:
                    r["pct"].append(50); continue
                lo = sum(1 for x in col if x < v)
                eq = sum(1 for x in col if x == v)
                q = 100 * (lo + 0.5 * eq) / len(col)
                r["pct"].append(round(100 - q if inv else q))
    return rows

def find_player(rows, query, team_hint=None):
    q = query.lower()
    hits = [r for r in rows if q in r["name"].lower() and (not team_hint or team_hint.lower() in r["team"].lower())]
    return sorted(hits, key=lambda r: -r["min"])

def _dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a["pct"], b["pct"])))

def suggest(store, rows_by_season, p, next_opp_id=None, widzew_id=None, n_back=2):
    """Zwraca listę propozycji porównań: [{type, why, row}] dla zawodnika p (wiersz z percentyli)."""
    cur = rows_by_season[p["season"]]
    pool = [r for r in cur if r["pos"] == p["pos"] and r["pid"] != p["pid"] and r["min"] >= max(MIN_POOL, 0.5 * p["min"])]
    out, used = [], set()
    def add(r, typ, why):
        if r is None:
            return
        key = (r["pid"], r["season"])
        if key not in used:
            used.add(key); out.append({"type": typ, "why": why, "row": r})
    spec = MET[p["pos"]]
    if pool:
        byd = sorted(pool, key=lambda r: _dist(p, r))
        sim = lambda r: max(0, round(100 - _dist(p, r) / (math.sqrt(len(p["pct"])) * 100) * 160))
        add(byd[0], "Bliźniak stylu", f"Najbardziej podobny profil w lidze, zgodność {sim(byd[0])}%")
        bi = max(range(len(p["pct"])), key=lambda i: p["pct"][i])
        top = max(pool, key=lambda r: r["pct"][bi])
        add(top, "Wzorzec w jego mocnej stronie", f"Najlepszy w lidze w kategorii: {spec[bi][1].lower()} (percentyl {top['pct'][bi]})")
        if next_opp_id:
            opp = [r for r in pool if r["team_id"] == next_opp_id]
            if opp:
                add(max(opp, key=lambda r: r["min"]), "Następny rywal", "Najwięcej minut na tej pozycji u rywala")
        add(byd[-1], "Odwrotny profil", "Zupełnie inny styl gry, dobry punkt do dyskusji w podcaście")
    # poprzednicy w Widzewie (inne sezony) i sam zawodnik sprzed lat
    if widzew_id:
        for season in sorted(rows_by_season, reverse=True):
            if season == p["season"]:
                continue
            rows = rows_by_season[season]
            former = [r for r in rows if r["team_id"] == widzew_id and r["pos"] == p["pos"] and r["pid"] != p["pid"] and r["min"] >= 900]
            if former:
                add(max(former, key=lambda r: r["min"]), "Poprzednik w Widzewie", f"Grał na tej pozycji w Widzewie w sezonie {season}/{str(season + 1)[2:]}")
                break
    for season in sorted(rows_by_season, reverse=True):
        if season <= p["season"] - n_back:
            me = [r for r in rows_by_season[season] if r["pid"] == p["pid"] and r["pos"] == p["pos"] and r["min"] >= MIN_POOL]
            if me:
                add(me[0], "On sam sprzed lat", f"Ten sam zawodnik w sezonie {season}/{str(season + 1)[2:]}")
                break
    return out

# ------------------------------------------------------------------ fun fakty
def team_rounds(store, season, tid):
    fx = sorted(finished(store.fixtures(season)), key=lambda f: f["fixture"]["timestamp"])
    out = []
    for f in fx:
        if tid in (f["teams"]["home"]["id"], f["teams"]["away"]["id"]):
            gf, gc, home, o, rnd = result_for(f, tid)
            out.append({"gf": gf, "ga": gc, "home": home, "o": o, "ts": f["fixture"]["timestamp"]})
    return out

def after_n(rounds, n):
    r = rounds[:n]
    return {"pts": sum(3 if x["o"] == "W" else 1 if x["o"] == "R" else 0 for x in r),
            "gf": sum(x["gf"] for x in r), "ga": sum(x["ga"] for x in r),
            "draws": sum(1 for x in r if x["o"] == "R"), "wins": sum(1 for x in r if x["o"] == "W"),
            "losses": sum(1 for x in r if x["o"] == "P"), "cs": sum(1 for x in r if x["ga"] == 0),
            "homewins": sum(1 for x in r if x["home"] and x["o"] == "W")}

TEAM_FACTS = [  # klucz, (fraza dla najniższej, fraza dla najwyższej)
 ("pts", "Najmniej punktów po {n} kolejkach", "Najwięcej punktów po {n} kolejkach"),
 ("gf", "Najmniej bramek strzelonych po {n} kolejkach", "Najwięcej bramek strzelonych po {n} kolejkach"),
 ("ga", "Najmniej bramek straconych po {n} kolejkach", "Najwięcej bramek straconych po {n} kolejkach"),
 ("draws", "Najmniej remisów po {n} kolejkach", "Najwięcej remisów po {n} kolejkach"),
 ("wins", "Najmniej wygranych po {n} kolejkach", "Najwięcej wygranych po {n} kolejkach"),
 ("losses", "Najmniej porażek po {n} kolejkach", "Najwięcej porażek po {n} kolejkach"),
 ("cs", "Najmniej czystych kont po {n} kolejkach", "Najwięcej czystych kont po {n} kolejkach"),
 ("homewins", "Najmniej wygranych u siebie po {n} kolejkach", "Najwięcej wygranych u siebie po {n} kolejkach")]

def mine_team_facts(store, tid, min_run=3):
    cur = store.current
    cr = team_rounds(store, cur, tid)
    n = len(cr)
    if n == 0:
        return []
    hist = {s: after_n(team_rounds(store, s, tid), n) for s in store.seasons if s != cur
            and len(team_rounds(store, s, tid)) >= n}
    now = after_n(cr, n)
    seasons = sorted(hist)
    facts = []
    for key, lo_t, hi_t in TEAM_FACTS:
        for direction, tmpl in (("lo", lo_t), ("hi", hi_t)):
            run, last = 0, None
            for s in reversed(seasons):
                worse = hist[s][key] > now[key] if direction == "lo" else hist[s][key] < now[key]
                if not worse:
                    last = s; break
                run += 1
            if run >= min_run:
                facts.append({"kind": "sezon", "key": key, "dir": direction, "title": tmpl.format(n=n), "value": now[key],
                              "run": run, "last": last, "series": [(s, hist[s][key]) for s in seasons] + [(cur, now[key])],
                              "record": last is None, "score": run + (1 if last is None else 0)})
    facts += mine_streaks(store, tid)
    return sorted(facts, key=lambda f: -f["score"])

def mine_streaks(store, tid):
    """Seria bieżąca vs wcześniejsze serie w dostępnych sezonach (styl OptaJoe: 'najdłuższa od ...')."""
    games = []
    for s in store.seasons:
        for x in team_rounds(store, s, tid):
            x["season"] = s; games.append(x)
    if len(games) < 10:
        return []
    kinds = [("bez wygranej", lambda x: x["o"] != "W", False), ("bez porażki", lambda x: x["o"] != "P", False),
             ("bez wygranej u siebie", lambda x: x["o"] != "W", True), ("remisów z rzędu", lambda x: x["o"] == "R", False),
             ("bez czystego konta", lambda x: x["ga"] > 0, False)]
    facts = []
    for name, cond, home_only in kinds:
        seq = [x for x in games if x["home"]] if home_only else games
        flags = [cond(x) for x in seq]
        cur = 0
        for f in reversed(flags):
            if f: cur += 1
            else: break
        if cur < 3:
            continue
        runs, run = [], 0           # wcześniejsze serie: (długość, sezon końca)
        for i, f in enumerate(flags[:len(flags) - cur]):
            if f: run += 1
            else:
                if run: runs.append((run, seq[i - 1]["season"]))
                run = 0
        if run: runs.append((run, seq[len(flags) - cur - 1]["season"]))
        longer = [r for r in runs if r[0] >= cur]
        last = longer[-1][1] if longer else None
        facts.append({"kind": "seria", "key": name, "title": f"{cur} meczów {name}", "value": cur, "last": last,
                      "record": not longer, "run": cur, "score": cur + (3 if not longer else 0)})
    return facts
