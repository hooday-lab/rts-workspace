# -*- coding: utf-8 -*-
"""#RTSstat — karta 'Liczba przed Piastem' z podmienialnym tłem.
Użycie: python build/piast_card.py [sciezka_do_tla.png] [nazwa_wyjscia]
Tło: PNG/JPG 1920x1080 bez tekstu. Reszta (ciemna warstwa, treść, pasek, stopka) jest nakładana."""
import os, sys, re
sys.argv_backup = sys.argv
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "cards")
src = open(os.path.join(ROOT,"build","make_cards2.py"),encoding="utf-8").read()
CSS = re.search(r'CSS = """(.*?)"""', src, re.S).group(1)   # wspólny styl kart

# dane: api_fixtures_raw (Supabase ClubFantasy), status FT, kol. 1-9 sezonu 2026/27
W = [(1,"Motor","D",2,2,"R"),(2,"Wisła Płock","W",0,0,"R"),(3,"Jagiellonia","W",2,0,"W"),
     (4,"Korona","D",1,2,"P"),(5,"Śląsk","W",3,3,"R"),(6,"Lech","D",2,3,"P"),
     (7,"Radomiak","D",0,0,"R"),(8,"Legia","W",1,1,"R"),(9,"Wieczysta","D",2,2,"R")]
P = [(1,"Zagłębie","W",0,2,"P"),(2,"Wisła Kr.","D",4,3,"W"),(3,"Lech","W",0,3,"P"),
     (4,"Wieczysta","D",3,4,"P"),(5,"Legia","D",1,1,"R"),(6,"Motor","W",2,0,"W"),
     (7,"GKS Katowice","D",3,0,"W"),(8,"Radomiak","W",2,0,"W"),(9,"Pogoń","D",1,2,"P")]
def cnt(rows,k): return sum(1 for r in rows if r[5]==k)
assert cnt(W,"R")==6 and cnt(P,"R")==1 and cnt(W,"W")==1 and cnt(P,"W")==4  # kontrola z tabelą

def row(rows, name, big, cap, me):
    tiles=""
    for k,o,g,a,b,r in rows:
        cls={"R":"draw","W":"win","P":"loss"}[r]
        tiles+=f'<div class="t {cls}"><div class="k">{k}</div><div class="o">{o}</div><div class="s">{a}:{b}</div></div>'
    return f'''<div class="rw {'me' if me else ''}"><div class="who">{name}</div>
    <div class="tiles">{tiles}</div><div class="num"><b>{big}</b><span>{cap}</span></div></div>'''

CSS2 = CSS + """
.card{background:none!important}
.bg{position:absolute;inset:0;background:var(--surface) center/cover no-repeat;z-index:0}
.scrim{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(15,16,18,.86) 0%,rgba(15,16,18,.74) 45%,rgba(15,16,18,.90) 100%)}
.card>*{position:relative;z-index:2}
.card>.bg,.card>.scrim,.card>.stripe{position:absolute}
.stripe{z-index:3}
main{justify-content:center;gap:30px;padding-bottom:18px}.sub{max-width:1750px!important}
.rw{display:flex;align-items:center;gap:30px}
.who{width:190px;font:800 54px/1 BC;text-transform:uppercase;letter-spacing:1px}
.rw.me .who{color:#fff}.rw:not(.me) .who{color:var(--ink2)}
.tiles{display:flex;gap:9px;flex:1}
.t{flex:1;height:176px;border-radius:10px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:12px 4px 12px}
.t .k{font:600 20px BA;letter-spacing:1px;opacity:.85}
.t .o{font:800 22px/1 BC;text-transform:uppercase;letter-spacing:.3px;text-align:center;min-height:24px}
.t .s{font:800 52px/1 BC}
.t.draw{background:var(--accent);color:#fff}
.t.win{background:var(--win);color:#0F1012}
.t.loss{background:rgba(15,16,18,.55);border:3px solid var(--neutral);color:var(--ink2)}
.num{width:250px;text-align:left}
.num b{display:block;font:800 190px/.8 BC}
.num span{display:block;font:800 30px BC;letter-spacing:3px;text-transform:uppercase;color:var(--ink2);margin-top:8px}
.rw.me .num b{color:var(--accent)}
.lg{display:flex;gap:34px;font:600 24px BA;color:var(--ink2);align-items:center;margin-left:220px}
.lg span{display:flex;align-items:center;gap:10px}
.when{position:absolute;right:96px;top:70px;z-index:3;text-align:right;font:800 30px/1.15 BC;letter-spacing:3px;text-transform:uppercase}
.when span{display:block;font:600 24px BA;letter-spacing:1px;color:var(--ink2);text-transform:none}
"""

def build(bg=None):
    bgcss = f"background-image:url('{bg}');" if bg else ""
    main = (row(W,"Widzew","6","remisów w 9 meczach",True)
          + row(P,"Piast","1","remis w 9 meczach",False)
          + '<div class="lg"><span><i class="sw" style="background:#E5242B"></i>remis</span><span><i class="sw" style="background:#F2F2F2"></i>wygrana</span><span><i class="sw" style="border:3px solid #6B7078"></i>porażka</span><span>liczby = kolejka · wynik z perspektywy drużyny</span></div>')
    return f"""<!doctype html><html lang="pl"><head><meta charset="utf-8"><title>Liczba przed Piastem</title><style>{CSS2}</style></head>
<body><div class="card"><div class="bg" style="{bgcss}"></div><div class="scrim"></div>
<div class="stripe"><i></i><i></i><i></i></div>
<div class="when">Piast – Widzew<span>niedziela 11.10 · 14:45 · Gliwice</span></div>
<header><div class="tag"><i></i>#RTSstat · Liczba przed rywalem</div><h1>6 remisów kontra 1</h1>
<p class="sub">Widzew – najwięcej remisów w lidze. Piast – tylko jeden. Któraś seria pęknie w niedzielę.</p></header>
<main>{main}</main>
<footer><div class="src">#RTSstat · stan po 9. kolejce Ekstraklasy 2026/27 · dane: API-Football (kolejki 1–9)</div><div class="brand"><b>ROZMOWY TYLKO SPORTOWE</b><span>od kibiców dla kibiców</span></div></footer></div></body></html>"""

if __name__=="__main__":
    from playwright.sync_api import sync_playwright
    bg = os.path.abspath(sys.argv[1]) if len(sys.argv)>1 and sys.argv[1]!="-" else None
    name = sys.argv[2] if len(sys.argv)>2 else "11-liczba-przed-piastem"
    os.makedirs(OUT,exist_ok=True)
    p=os.path.join(OUT,name+".html"); open(p,"w",encoding="utf-8").write(build(bg))
    with sync_playwright() as pw:
        b=pw.chromium.launch(); pg=b.new_page(viewport={"width":1920,"height":1080})
        pg.goto("file://"+p); pg.wait_for_timeout(800); pg.evaluate("document.fonts.ready")
        pg.screenshot(path=os.path.join(OUT,name+".png")); b.close()
    print("ok",name)
