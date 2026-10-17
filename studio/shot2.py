import os,json,re,sys
from playwright.sync_api import sync_playwright
mock=re.search(r'MOCK="""(.*?)"""',open('test_site.py').read(),re.S).group(1)
D=open('rtsstat-data.json',encoding='utf-8').read()
html=open('/home/claude/rtsstat/index.html',encoding='utf-8').read()
html=html.replace('<script src="https://www.gstatic.com','<!--').replace('<script src="config.js"></script>','--><script>'+mock+'</script>',1)
html=html.replace('src="brand/','src="file:///home/claude/rtsstat/brand/').replace('href="brand/','href="file:///home/claude/rtsstat/brand/')
open('site/t4.html','w',encoding='utf-8').write(html)
pre="window.__store={'data/stats':{json:"+json.dumps(D)+"}};window.__members={};window.__user={email:'hooday@gmail.com'};"
errs=[]
with sync_playwright() as pw:
    b=pw.chromium.launch()
    def page(vp,mob,scale=1):
        ctx=b.new_context(viewport=vp,is_mobile=mob,has_touch=mob,device_scale_factor=scale);pg=ctx.new_page();pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
        pg.add_init_script(pre);pg.goto('file://'+os.path.abspath('site/t4.html'));pg.wait_for_timeout(1200);return pg
    pg=page({'width':1440,'height':900},False);pg.screenshot(path='site/n_home_d.png')
    pg.click('.ni:has-text("Mecz")');pg.wait_for_timeout(900);pg.screenshot(path='site/n_match_d.png')
    pg.click('.ni:has-text("Ustawienia")');pg.wait_for_timeout(500);pg.screenshot(path='site/n_admin_d.png')
    m=page({'width':390,'height':844},True,2);m.screenshot(path='site/n_home_m.png')
    m.click('#burger');m.wait_for_timeout(500);m.screenshot(path='site/n_drawer_m.png')
    m.click('.ni:has-text("Zawodnik")');m.wait_for_timeout(900);m.screenshot(path='site/n_player_m.png')
    print('mobile scrollW',m.evaluate('document.documentElement.scrollWidth'))
    t=page({'width':820,'height':1000},True);t.screenshot(path='site/n_home_t.png')
    print(errs);b.close()
