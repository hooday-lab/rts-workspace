import re,os,json,base64
R=os.path.dirname(os.path.abspath(__file__))
SC='/tmp/claude-0/-home-claude/99ecf882-ab64-5549-bd5c-f97dd0906d48/scratchpad/web/'
tpl=open(SC+'studio_tpl.html',encoding='utf-8').read().split('\n')
L=lambda a,b:'\n'.join(tpl[a-1:b])   # 1-indexed inclusive
css=L(3,72)  # between <style> and </style>
assert tpl[1].startswith('<style>') and tpl[72-0].startswith('</style>') or True
# znajdz linie
def idx(prefix,start=0):
    for i,l in enumerate(tpl[start:],start):
        if l.startswith(prefix): return i
    raise Exception(prefix)
i_style_end=idx('</style>')
css='\n'.join(tpl[2:i_style_end])
i_script=idx('<script>')
i_help=idx('/* ---------- pomocnicze')
i_dane=idx('/* ---------- dane')
i_stan=idx('/* ---------- stan i capability')
i_ui=idx('/* ---------- UI główne')
i_adm=idx('/* ---------- admin')
head_js='\n'.join(l for l in tpl[i_script+1:i_dane] if not l.startswith('const D=') )
head_js=head_js.replace('const FONTS=__FONTS__;','const FONTS=__FONTS__;')
engine='\n'.join(tpl[i_dane:i_stan])
state='''/* ---------- stan ---------- */
let isAdmin=!!ctx.isAdmin,downloads=true;
let SET={bg:null,cards:ctx.cards||{}};
let bgData=ctx.bg||BG_DEFAULT;
const S={type:'rival',p:{},url:null,postEd:false,busy:false};
function saveBlob(name,blob){const u=URL.createObjectURL(blob);const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),4000)}
'''
ui='\n'.join(tpl[i_ui:i_adm])
ui=re.sub(r"await downloads\.save\(\{filename:(`[^`]*`),data:blob\}\);",r"saveBlob(\1,blob);",ui)
ui=ui.replace("if(!downloads){m.textContent='Pobieranie niedostępne w tym widoku – zrób zrzut podglądu.';m.className='msg err';return}","")
assert 'downloads.save' not in ui
admin=open(R+'/p_admin.js',encoding='utf-8').read()
auth=open(R+'/p_auth.js',encoding='utf-8').read()
js=head_js+'\nasync function runApp(D,ctx){\n'+engine+'\n'+state+'\n'+ui+'\n'+admin+'\n'+auth
body='''<div class="wrap">
<header class="top"><div class="brand">RTS<b>stat</b> Studio</div><div class="who" id="who"></div></header>
<div id="boot" class="msg">Ładuję…</div>
<section id="gate" class="gate" hidden>
  <h2>Wejście dla ekipy</h2>
  <p class="msg">Zaloguj się kontem Google. Wejdą tylko adresy, które admin dodał do listy ekipy.</p>
  <div class="actions"><button class="btn pri" id="g-go">Zaloguj przez Google</button></div>
  <div class="msg" id="g-msg"></div>
</section>
<section id="deny" class="gate" hidden>
  <h2>Brak dostępu</h2>
  <p class="msg">Zalogowano jako <b id="d-email"></b>, ale tego adresu nie ma na liście ekipy. Podaj go adminowi (Bartkowi), żeby Cię dodał, i odśwież stronę. Możesz też zalogować się innym kontem Google.</p>
  <div class="actions"><button class="btn" id="d-out">Wyloguj i zmień konto</button></div>
</section>
<section id="setup" class="gate" hidden>
  <h2>Konfiguracja</h2>
  <p class="msg">Strona nie ma jeszcze danych połączenia z Firebase (plik config.js). Admin musi go uzupełnić.</p>
</section>
<section id="first" class="gate" hidden>
  <h2>Pierwsze uruchomienie</h2>
  <p class="msg">Baza jest pusta. Wgraj plik <code>rtsstat-data.json</code> z danymi do kart (dostajesz go od Claude'a).</p>
  <input type="file" id="first-f" accept="application/json,.json"><div class="msg" id="first-msg"></div>
</section>
<section id="studio" hidden>
  <nav class="tabs" id="tabs" role="tablist"></nav>
  <div id="view"></div>
</section>
</div>'''
fonts=[]
F=SC+'../cards/fonts'
for fn in sorted(os.listdir(F)):
    m=re.match(r'barlow(-condensed)?-(latin-ext|latin)-(\d+)-normal\.woff2',fn)
    if m: fonts.append({'fam':'BC' if m.group(1) else 'BA','r':'ext' if m.group(2)=='latin-ext' else 'latin','w':int(m.group(3)),'b':base64.b64encode(open(os.path.join(F,fn),'rb').read()).decode()})
bg=base64.b64encode(open(SC+'bg.jpg','rb').read()).decode()
js=js.replace('__FONTS__',json.dumps(fonts)).replace('__BG__',bg)
FB='10.14.1'
html=f'''<!doctype html>
<html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>RTSstat Studio</title>
<style>
{css}
</style></head><body>
{body}
<script src="https://www.gstatic.com/firebasejs/{FB}/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/{FB}/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/{FB}/firebase-firestore-compat.js"></script>
<script src="config.js"></script>
<script>
{js}
</script></body></html>'''
os.makedirs(R+'/site',exist_ok=True)
open(R+'/site/index.html','w',encoding='utf-8').write(html)
print(len(html)/1e6,'MB')
