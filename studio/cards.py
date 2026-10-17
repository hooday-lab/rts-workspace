# -*- coding: utf-8 -*-
"""Szablony kart 1920x1080 (HTML/SVG) i render do PNG."""
import math, os
from .analysis import MET, POS

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, "card.css"), encoding="utf-8").read().replace("@FONTS@", "file://" + os.path.join(HERE, "fonts"))
CSS += """
.main{flex:1;min-height:0;display:flex;align-items:center}
.who{font:600 28px BA;color:var(--ink2);margin-bottom:16px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.tile{border:2px solid var(--hair);border-radius:10px;padding:14px 18px;background:rgba(255,255,255,.02)}
.tile b{display:block;font:800 84px/.9 BC}.tile span{font:600 24px BA;color:var(--ink2)}
.tile.hot{border-color:var(--accent)}
.pcol{display:grid;grid-template-columns:420px 640px 1fr;gap:70px;width:100%;align-items:center}
.chart-t{font:800 30px BC;letter-spacing:2px;text-transform:uppercase;color:var(--ink2);margin-bottom:6px}
.fx{margin-top:26px;border-left:6px solid var(--accent);padding:6px 0 6px 22px;font:800 46px/1.05 BC;text-transform:uppercase}
.fx small{display:block;font:400 22px BA;color:var(--muted);text-transform:none;margin-top:8px}
.cmp{width:100%;display:flex;flex-direction:column;gap:8px}
.cmp .hd,.crow{display:grid;grid-template-columns:1fr 380px 1fr;align-items:center}
.cmp .hd{align-items:end;margin-bottom:8px}.cmp .hd .n{font:800 58px/.9 BC;text-transform:uppercase}.cmp .hd .r{text-align:right}
.cmp .hd small{display:block;font:600 24px BA;color:var(--ink2);margin-top:6px}
.crow{height:54px}.crow .lab{text-align:center;font:600 27px BA;color:var(--ink2)}
.crow .s{display:flex;align-items:center;gap:14px}.crow .s.l{flex-direction:row-reverse}
.crow .bar{height:26px;border-radius:4px}.crow .v{font:800 38px BC;min-width:100px}.crow .l .v{text-align:right}
.bigfact{width:100%;display:grid;grid-template-columns:720px 1fr;gap:64px;align-items:center}
.bigfact .big{font:800 360px/.78 BC;letter-spacing:-4px}
.bigfact .big small{display:block;font:800 58px/1 BC;text-transform:uppercase;color:var(--ink2);margin-top:28px;letter-spacing:1px}
.bigfact .txt{font:800 80px/1 BC;text-transform:uppercase}
.bigfact .txt small{display:block;font:600 34px/1.3 BA;color:var(--ink2);margin-top:20px;text-transform:none}
.cols{display:flex;gap:14px;align-items:flex-end;height:340px;margin-top:36px;border-bottom:2px solid var(--hair)}
.cols div{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:8px;height:100%}
.cols b{font:800 38px BC}.cols i{display:block;width:100%;background:var(--neutral);border-radius:6px 6px 0 0}
.cols .me i{background:var(--accent)}.cols em{font:600 22px BA;font-style:normal;color:var(--ink2);margin-top:8px}
.mrow{display:grid;grid-template-columns:1fr 420px 1fr;align-items:center;height:76px}
.mrow .lab{text-align:center;font:600 30px BA;color:var(--ink2)}
.mrow .s{display:flex;align-items:center;gap:16px}.mrow .s.l{flex-direction:row-reverse}
.mrow .bar{height:32px;border-radius:4px}.mrow .v{font:800 48px BC;min-width:90px}.mrow .l .v{text-align:right}
.mteams{display:grid;grid-template-columns:1fr 420px 1fr;align-items:center;margin-bottom:6px}
.mteams b{font:800 64px BC;text-transform:uppercase}.mteams .r{text-align:right}
.mteams .sc{text-align:center;font:800 120px/.8 BC}
"""

def fmt(v, d=0):
    return f"{v:.{d}f}".replace(".", ",")

def page(title, sub, main, src):
    return f"""<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head>
<body><div class="card"><div class="stripe"><i></i><i></i><i></i></div>
<header><div class="tag"><i></i>#RTSstat</div><h1>{title}</h1><p class="sub">{sub}</p></header>
<main>{main}</main>
<footer><div class="src">{src}</div><div class="brand"><b>ROZMOWY TYLKO SPORTOWE</b><span>od kibiców dla kibiców</span></div></footer></div></body></html>"""

def season_label(s):
    return f"{s}/{str(s + 1)[2:]}"

# ---------------------------------------------------------------- pizza + trend
def pizza(p):
    spec = MET[p["pos"]]; N = len(spec); cx = cy = 320; R0, R1 = 64, 250; gap = .02
    s = '<svg width="760" height="640" viewBox="-60 0 760 640" style="display:block;overflow:visible">'
    for v in (50, 100):
        s += f'<circle cx="{cx}" cy="{cy}" r="{R0 + (R1 - R0) * v / 100}" fill="none" stroke="#2A2D32" stroke-width="{2 if v == 50 else 1}"/>'
    pt = lambda a, r: (cx + r * math.cos(a), cy + r * math.sin(a))
    for i, (_, lab, _, d, u, _) in enumerate(spec):
        a0 = -math.pi / 2 + i * 2 * math.pi / N + gap; a1 = -math.pi / 2 + (i + 1) * 2 * math.pi / N - gap; am = (a0 + a1) / 2
        r = R0 + (R1 - R0) * p["pct"][i] / 100; hot = p["pct"][i] >= 70
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pt(a0, R0), pt(a0, r), pt(a1, r), pt(a1, R0)
        s += f'<path d="M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}A{r:.1f} {r:.1f} 0 0 1 {x2:.1f} {y2:.1f}L{x3:.1f} {y3:.1f}A{R0} {R0} 0 0 0 {x0:.1f} {y0:.1f}Z" fill="{"#E5242B" if hot else "#6B7078"}"/>'
        tx, ty = pt(am, R1 + 30); c = math.cos(am)
        anchor = "start" if c > .25 else "end" if c < -.25 else "middle"
        s += (f'<text x="{tx:.1f}" y="{ty - 2:.1f}" text-anchor="{anchor}" fill="#B4BAC2" font-family="BA" font-weight="600" font-size="19">{lab.replace(" / 90", "")}</text>'
              f'<text x="{tx:.1f}" y="{ty + 24:.1f}" text-anchor="{anchor}" fill="#F4F4F2" font-family="BC" font-weight="800" font-size="27">{fmt(p["vals"][i], d)}{u}'
              f'<tspan fill="#7D848D" font-size="19" font-weight="600"> · {p["pct"][i]}</tspan></text>')
    return s + "</svg>"

def line(points, w=560, h=260):
    """points: [(etykieta, wartość)]"""
    L, B, T = 44, 40, 24; mx = max(v for _, v in points) * 1.15 or 1
    x = lambda i: L + (w - L - 44) * (i / max(1, len(points) - 1)); y = lambda v: h - B - (h - B - T) * v / mx
    s = f'<svg width="100%" viewBox="0 0 {w} {h}" style="display:block">'
    for f in (0, .5, 1):
        v = mx * f
        s += f'<line x1="{L}" x2="{w - 44}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="#2A2D32"/><text x="{L - 8}" y="{y(v) + 7:.1f}" text-anchor="end" fill="#7D848D" font-family="BA" font-size="18">{fmt(v, 1)}</text>'
    s += '<polyline fill="none" stroke="#E5242B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" points="' + " ".join(f"{x(i):.1f},{y(v):.1f}" for i, (_, v) in enumerate(points)) + '"/>'
    for i, (lab, v) in enumerate(points):
        r = 10 if i == len(points) - 1 else 7
        s += f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="{r}" fill="#E5242B" stroke="#0F1012" stroke-width="3"/><text x="{x(i):.1f}" y="{h - 12}" text-anchor="middle" fill="#B4BAC2" font-family="BA" font-size="19">{lab}</text>'
    lab, v = points[-1]
    s += f'<text x="{x(len(points) - 1):.1f}" y="{y(v) - 20:.1f}" text-anchor="end" fill="#F4F4F2" font-family="BC" font-weight="800" font-size="34">{fmt(v, 2)}</text>'
    return s + "</svg>"

# ---------------------------------------------------------------- karty
def card_player(p, history, src):
    spec = MET[p["pos"]]; st = p["st"]; g = st["goals"]
    best = max(range(len(p["pct"])), key=lambda i: p["pct"][i])
    trend = [(season_label(h["season"]), h["vals"][0]) for h in history]  # pierwszy wskaźnik pozycji (gole/90, odbiory/90…)
    t_label = spec[0][1]
    tiles = (f'<div class="tile hot"><b>{g["total"] or 0}</b><span>gole</span></div><div class="tile"><b>{g["assists"] or 0}</b><span>asysty</span></div>'
             f'<div class="tile"><b>{p["apps"]}</b><span>mecze</span></div><div class="tile"><b>{p["min"]}</b><span>minuty</span></div>')
    main = (f'<div class="pcol"><div><div class="who">{POS.get(p["pos"], p["pos"])} · {p["team"]} · {p["age"]} lat</div><div class="tiles">{tiles}</div></div>'
            f'<div>{pizza(p)}</div><div style="padding-left:70px"><div class="chart-t">{t_label}, sezon po sezonie</div>{line(trend) if len(trend) > 1 else ""}'
            f'<div class="fx">Najmocniejsza strona: {spec[best][1].lower()}<small>percentyl {p["pct"][best]} wśród zawodników na tej pozycji (min. 450 minut)</small></div></div></div>')
    return page(p["name"], "Profil na tle ligi: czerwone pola to top 30% pozycji. Obok wartości percentyl.", main, src)

def card_compare(a, b, why, src):
    spec = MET[a["pos"]]
    rows = ""
    for i, (_, lab, _, d, u, _) in enumerate(spec[:7]):
        la, lb = a["pct"][i] > b["pct"][i], b["pct"][i] > a["pct"][i]
        col = lambda w: "#E5242B" if w else "#6B7078"
        rows += (f'<div class="crow"><div class="s l"><div class="bar" style="width:{a["pct"][i] * 4.6:.0f}px;background:{col(la)}"></div><span class="v">{fmt(a["vals"][i], d)}{u}</span></div>'
                 f'<div class="lab">{lab}</div><div class="s"><div class="bar" style="width:{b["pct"][i] * 4.6:.0f}px;background:{col(lb)}"></div><span class="v">{fmt(b["vals"][i], d)}{u}</span></div></div>')
    def head(x):
        g = x["st"]["goals"]
        return f'{x["name"]}<small>{x["team"]} · {season_label(x["season"])} · {g["total"] or 0} goli · {g["assists"] or 0} asyst · {x["min"]} min</small>'
    main = f'<div class="cmp"><div class="hd"><div class="n">{head(a)}</div><div></div><div class="n r">{head(b)}</div></div>{rows}</div>'
    return page(f'{a["name"]} kontra {b["name"]}', why or "Porównanie na tych samych wskaźnikach.", main, src + " · słupek = percentyl na pozycji, czerwony = lepszy")

def card_fact(f, src):
    series = f["series"] if f["kind"] == "sezon" else []
    if f["kind"] == "sezon":
        mx = max(v for _, v in series) or 1
        cols = "".join(f'<div class="{"me" if i == len(series) - 1 else ""}"><b>{v:g}</b><i style="height:{max(6, v / mx * 220):.0f}px"></i><em>{season_label(s)}</em></div>' for i, (s, v) in enumerate(series))
        big = "∞" if f["record"] else str(f["run"] + 1)
        unit = "rekord w danych" if f["record"] else "sezonów"
        ctx = (f'W {len(series) - 1} wcześniejszych sezonach w naszych danych nie było takiej wartości.' if f["record"]
               else f'Poprzednio tak było w sezonie {season_label(f["last"])}.')
        main = (f'<div style="width:100%"><div class="bigfact"><div class="big">{big}<small>{unit}</small></div>'
                f'<div class="txt">{f["title"]}<small>Dziś: {f["value"]:g}. {ctx}</small></div></div><div class="cols">{cols}</div></div>')
        return page("Fun fakt z historii", "Znaleziony automatycznie: sezon po sezonie, ten sam moment rozgrywek.", main, src)
    ctx = ("W naszych danych nigdy wcześniej tak długiej serii." if f["record"] else f'Ostatnio tak długa seria: sezon {season_label(f["last"])}.')
    main = f'<div class="bigfact" style="grid-template-columns:600px 1fr"><div class="big">{f["value"]}<small>mecze z rzędu</small></div><div class="txt">{f["key"]}<small>{ctx}</small></div></div>'
    return page("Seria", "Aktualna seria Widzewa na tle całej dostępnej historii.", main, src)

def card_match(det, wid, src):
    stats = {s["team"]["id"]: {x["type"]: x["value"] for x in s["statistics"]} for s in det["statistics"]}
    fx = det["fixture"]; h, a = fx["teams"]["home"], fx["teams"]["away"]
    def num(v):
        return float(str(v).replace("%", "")) if v not in (None, "") else 0.0
    defs = [("Total Shots", "Strzały", 0, ""), ("Shots on Goal", "Strzały celne", 0, ""), ("Ball Possession", "Posiadanie piłki", 0, "%"),
            ("Corner Kicks", "Rzuty rożne", 0, ""), ("Fouls", "Faule", 0, ""), ("expected_goals", "xG", 2, "")]
    rows = ""
    for key, lab, d, u in defs:
        va, vb = num(stats[h["id"]].get(key)), num(stats[a["id"]].get(key))
        m = max(va, vb, 1)
        rows += (f'<div class="mrow"><div class="s l"><div class="bar" style="width:{va / m * 480:.0f}px;background:{"#E5242B" if h["id"] == wid else "#6B7078"}"></div><span class="v">{fmt(va, d)}{u}</span></div>'
                 f'<div class="lab">{lab}</div><div class="s"><div class="bar" style="width:{vb / m * 480:.0f}px;background:{"#E5242B" if a["id"] == wid else "#6B7078"}"></div><span class="v">{fmt(vb, d)}{u}</span></div></div>')
    g = fx and det["fixture"]["goals"]
    main = (f'<div style="width:100%"><div class="mteams"><b>{h["name"]}</b><div class="sc">{g["home"]}:{g["away"]}</div><b class="r">{a["name"]}</b></div>{rows}</div>')
    return page("Mecz w liczbach", "Kto naprawdę dominował? Statystyki drużyn z ostatniego meczu.", main, src)

def render(html, png_path):
    from playwright.sync_api import sync_playwright
    png_path = os.path.abspath(png_path); html_path = os.path.splitext(png_path)[0] + ".html"
    open(html_path, "w", encoding="utf-8").write(html)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto("file://" + html_path); pg.wait_for_timeout(600); pg.screenshot(path=png_path); b.close()
    return png_path
