# -*- coding: utf-8 -*-
"""Generator SYNTETYCZNYCH danych w formacie API-Football — tylko do testów narzędzia (dane fikcyjne)."""
import json, os, random, sys

TEAMS = ["Widzew Łódź", "Piast Gliwice", "Legia", "Lech", "Górnik", "Korona", "Pogoń", "Zagłębie", "Cracovia",
         "Radomiak", "Jagiellonia", "Śląsk", "Motor", "Wisła Płock", "Wisła Kraków", "GKS", "Wieczysta", "Raków"]
POS = ["Goalkeeper"] * 2 + ["Defender"] * 7 + ["Midfielder"] * 7 + ["Attacker"] * 5

def mkplayers(rng, season, squads):
    out = []
    for tid, squad in squads.items():
        for pid, name, pos, skill in squad:
            mins = rng.randint(300, 2900)
            m = mins / 90
            g = lambda k: max(0, int(rng.gauss(k * m * skill, 1 + k * m * 0.2)))
            att = pos == "Attacker"; mid = pos == "Midfielder"; de = pos == "Defender"
            shots = g(2.4 if att else 1.0 if mid else 0.4)
            out.append({"player": {"id": pid, "name": name, "age": 18 + pid % 17},
                        "statistics": [{"team": {"id": tid, "name": TEAMS[tid - 1]}, "league": {"id": 106, "season": season},
                         "games": {"appearences": int(m) + 1, "minutes": mins, "position": pos, "rating": f"{6.2 + skill * 0.6:.2f}"},
                         "shots": {"total": shots, "on": int(shots * min(0.7, 0.25 + 0.15 * skill))},
                         "goals": {"total": g(0.5 if att else 0.1 if mid else 0.04), "assists": g(0.2 if att else 0.15 if mid else 0.05),
                                   "conceded": g(1.2) if pos == "Goalkeeper" else 0, "saves": g(3) if pos == "Goalkeeper" else 0},
                         "passes": {"total": g(25 if mid else 20 if de else 14), "key": g(1.2 if att else 1.0 if mid else 0.2), "accuracy": 70 + rng.randint(0, 20)},
                         "tackles": {"total": g(1.0 if att else 2.2 if mid else 2.0), "blocks": g(0.3 if de else 0.1), "interceptions": g(0.5 if att else 1.2)},
                         "duels": {"total": g(12), "won": g(6)},
                         "dribbles": {"attempts": g(3 if att else 1.5), "success": g(1.8 if att else 0.8), "past": g(0.8 if de else 0.3)},
                         "fouls": {"drawn": g(1.4 if att else 1.1), "committed": g(1.2)},
                         "cards": {"yellow": g(0.18), "red": 0}}]})
    return out

def build(root, seed=7):
    rng = random.Random(seed)
    squads, pid = {}, 1
    for tid in range(1, 19):
        sq = []
        for pos in POS:
            sq.append((pid, f"Zawodnik {pid:03d}", pos, rng.uniform(0.6, 1.4))); pid += 1
        squads[tid] = sq
    for season in (2023, 2024, 2025, 2026):
        d = os.path.join(root, str(season)); os.makedirs(os.path.join(d, "fixtures"), exist_ok=True)
        json.dump([{"team": {"id": i + 1, "name": n}} for i, n in enumerate(TEAMS)], open(os.path.join(d, "teams.json"), "w", encoding="utf-8"), ensure_ascii=False)
        # terminarz: rundy round-robin
        ids = list(range(1, 19)); fx = []; fid = season * 1000; ts = 1_700_000_000 + (season - 2023) * 31_000_000
        rounds = 9 if season == 2026 else 34
        for r in range(1, 35):
            arr = ids[:1] + ids[-(r % 17):] + ids[1:-(r % 17)] if r % 17 else ids[:]
            for k in range(9):
                h, a = (arr[k], arr[17 - k]) if (r + k) % 2 else (arr[17 - k], arr[k])
                fid += 1
                done = r <= rounds
                gh, ga = rng.choice([0, 1, 1, 2, 2, 3]), rng.choice([0, 0, 1, 1, 2, 3])
                if season == 2026 and 1 in (h, a):   # Widzew: dużo remisów jak w prawdziwym sezonie
                    gh = ga = rng.choice([0, 1, 2]) if rng.random() < 0.65 else gh
                fx.append({"fixture": {"id": fid, "timestamp": ts + r * 600_000 + k, "status": {"short": "FT" if done else "NS"}},
                           "league": {"id": 106, "season": season, "round": f"Regular Season - {r}"},
                           "teams": {"home": {"id": h, "name": TEAMS[h - 1]}, "away": {"id": a, "name": TEAMS[a - 1]}},
                           "goals": {"home": gh if done else None, "away": ga if done else None}})
        json.dump(fx, open(os.path.join(d, "fixtures.json"), "w", encoding="utf-8"))
        # zawodnicy: część przechodzi między klubami (stałe id, zmienny skill)
        json.dump(mkplayers(rng, season, squads), open(os.path.join(d, "players.json"), "w", encoding="utf-8"), ensure_ascii=False)
        # szczegóły ostatniego meczu Widzewa (sezon bieżący)
        if season == 2026:
            last = [f for f in fx if f["fixture"]["status"]["short"] == "FT" and 1 in (f["teams"]["home"]["id"], f["teams"]["away"]["id"])][-1]
            def st(t):
                return {"team": {"id": t, "name": TEAMS[t - 1]}, "statistics": [
                    {"type": "Total Shots", "value": rng.randint(5, 18)}, {"type": "Shots on Goal", "value": rng.randint(1, 8)},
                    {"type": "Ball Possession", "value": f"{rng.randint(35, 65)}%"}, {"type": "Corner Kicks", "value": rng.randint(1, 9)},
                    {"type": "Fouls", "value": rng.randint(6, 18)}, {"type": "expected_goals", "value": f"{rng.uniform(0.3, 2.5):.2f}"}]}
            json.dump({"fixture": last, "statistics": [st(last["teams"]["home"]["id"]), st(last["teams"]["away"]["id"])], "events": []},
                      open(os.path.join(d, "fixtures", f"{last['fixture']['id']}.json"), "w", encoding="utf-8"), ensure_ascii=False)
    return root

if __name__ == "__main__":
    print(build(sys.argv[1]))
