# -*- coding: utf-8 -*-
"""#RTSstats — karta 'Liczba przed Piastem' dopasowana do tła RTS (logo w prawym górnym rogu, lewy panel wolny)."""
import os, sys, re
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "cards")
sys.path.insert(0, os.path.join(ROOT,"build"))
import piast_card as pc
src = open(os.path.join(ROOT,"build","make_cards2.py"),encoding="utf-8").read()
CSS = re.search(r'CSS = """(.*?)"""', src, re.S).group(1)

def row(rows, name, big, cap, me):
    tiles=""
    for k,o,g,a,b,r in rows:
        cls={"R":"draw","W":"win","P":"loss"}[r]
        tiles+=f'<div class="t {cls}"><div class="k">{k}</div><div class="o">{o}</div><div class="s">{a}:{b}</div></div>'
    return f'<div class="rw {"me" if me else ""}"><div class="hd"><b>{big}</b><div><i>{name}</i><span>{cap}</span></div></div><div class="tiles">{tiles}</div></div>'

CSS2 = CSS + """
html,body{background:#7a0008}
.card{padding:0!important;background:none!important}
.bg{position:absolute;inset:0;background:url('%BG%') center/cover no-repeat;z-index:0}
.scrim{position:absolute;left:44px;top:44px;width:1400px;height:380px;z-index:1;clip-path:polygon(0 0,1405px 0,1370px 100%,0 100%);-webkit-mask-image:linear-gradient(180deg,#000 70%,transparent);
 background:linear-gradient(180deg,rgba(12,6,8,.58),rgba(12,6,8,.66))}
.scrim2{position:absolute;left:44px;top:330px;width:1832px;height:706px;z-index:1;
 background:linear-gradient(180deg,rgba(12,6,8,.0),rgba(12,6,8,.66) 7%,rgba(12,6,8,.78))}
.wrap{position:absolute;left:104px;top:76px;width:1712px;height:920px;z-index:2;display:flex;flex-direction:column}
.tag{font-size:26px!important}
h1{font-size:96px!important;margin-top:4px!important}
.sub{font-size:32px!important;max-width:1450px!important;margin-top:10px!important}
.when{margin-top:16px;display:inline-flex;gap:14px;align-items:center;font:800 28px BC;letter-spacing:3px;text-transform:uppercase;border:3px solid #fff;padding:6px 18px;border-radius:6px;align-self:flex-start;background:rgba(0,0,0,.3)}
.when span{font:600 24px BA;letter-spacing:1px;text-transform:none;color:#ffd9da}
main{display:flex;flex-direction:column;justify-content:flex-end;gap:16px;flex:1;padding-bottom:6px}
.rw{display:flex;flex-direction:column;gap:8px}
.hd{display:flex;align-items:center;gap:22px}
.hd b{font:800 112px/.82 BC;min-width:80px}
.rw.me .hd b{color:#fff}
.hd i{display:block;font:800 52px/1 BC;font-style:normal;text-transform:uppercase;letter-spacing:1px}
.hd span{display:block;font:800 26px BC;letter-spacing:3px;text-transform:uppercase;color:#ffd9da;margin-top:4px}
.tiles{display:flex;gap:12px}
.t{flex:1;height:162px;border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:9px 2px 9px}
.t .k{font:600 24px BA;letter-spacing:1px;opacity:.9}
.t .o{font:800 28px/1 BC;text-transform:uppercase;text-align:center;min-height:22px}
.t .s{font:800 66px/1 BC}
.t.draw{background:#E5242B;color:#fff;box-shadow:0 0 0 3px #fff inset}
.t.win{background:#F2F2F2;color:#0F1012}
.t.loss{background:rgba(10,6,8,.72);border:3px solid #cfcfd2;color:#e8e8ea}
.lg{display:flex;gap:30px;font:600 22px BA;color:#f1dede;align-items:center}
.lg span{display:flex;align-items:center;gap:9px}
.wrap{text-shadow:0 1px 6px rgba(60,0,0,.55)}.t{text-shadow:none}.tag{color:#fff!important}.tag i{background:#fff!important}.sub{color:#fff1f1!important}.foot{font:400 20px BA;color:#e9cfd0;margin-top:6px}
"""

def build(bg):
    main = (row(pc.W,"Widzew","6","remisów w 9 meczach",True)+row(pc.P,"Piast","1","remis w 9 meczach",False))
    lg='<div class="lg"><span><i class="sw" style="background:#E5242B;box-shadow:0 0 0 2px #fff inset"></i>remis</span><span><i class="sw" style="background:#F2F2F2"></i>wygrana</span><span><i class="sw" style="border:3px solid #cfcfd2"></i>porażka</span><span>w kafelku: kolejka · wynik z perspektywy drużyny</span></div>'
    return f"""<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>Liczba przed Piastem</title><style>{CSS2.replace('%BG%',bg)}</style></head>
<body><div class="card"><div class="bg"></div>
<div class="wrap"><div class="tag"><i></i>#RTSstats · Liczba przed rywalem</div><h1>6 remisów kontra 1</h1>
<p class="sub">Widzew – najwięcej remisów w lidze. Piast – tylko jeden. Któraś seria pęknie w niedzielę.</p>
<div class="when">Piast – Widzew<span>niedziela 11.10 · 14:45 · Gliwice</span></div>
<main>{main}{lg}</main>
<div class="foot">#RTSstats · stan po 9. kolejce Ekstraklasy 2026/27 · dane: API-Football (kolejki 1–9)</div></div></div></body></html>"""

if __name__=="__main__":
    from playwright.sync_api import sync_playwright
    bg=os.path.abspath(sys.argv[1]); name=sys.argv[2]
    p=os.path.join(OUT,name+".html"); open(p,"w",encoding="utf-8").write(build(bg))
    with sync_playwright() as pw:
        b=pw.chromium.launch(); pg=b.new_page(viewport={"width":1920,"height":1080})
        pg.goto("file://"+p); pg.wait_for_timeout(800); pg.evaluate("document.fonts.ready")
        pg.screenshot(path=os.path.join(OUT,name+".png")); b.close()
    print("ok",name)
