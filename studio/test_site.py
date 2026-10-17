import os,json
from playwright.sync_api import sync_playwright
D=open('/tmp/claude-0/-home-claude/99ecf882-ab64-5549-bd5c-f97dd0906d48/scratchpad/web/data.json',encoding='utf-8').read()
MOCK="""
window.__store=window.__store||{};window.__user=window.__user||null;window.__members=window.__members||{};
(function(){
 const S=window.__store;
 function allowed(){const u=window.__user;if(!u)return false;const e=u.email;return e==='hooday@gmail.com'||(window.__members[e]!==undefined)}
 function mkdoc(p){return {get:async()=>{
   if(p.startsWith('data/')||p.startsWith('settings/')){ if(!allowed()){const er=new Error('denied');er.code='permission-denied';throw er}}
   return {id:p.split('/').pop(),exists:p in S,data:()=>S[p]}},
  set:async d=>{S[p]=d;if(p.startsWith('members/'))window.__members[p.split('/')[1]]=d},update:async d=>{S[p]={...S[p],...d}},delete:async()=>{delete S[p];if(p.startsWith('members/'))delete window.__members[p.split('/')[1]]}}}
 let cb=null;
 const auth={onAuthStateChanged:f=>{cb=f;setTimeout(()=>f(window.__user),50)},signInWithPopup:async()=>{window.__user={email:window.__nextEmail};cb(window.__user)},signOut:async()=>{window.__user=null}};
 const fsx={doc:mkdoc,collection:c=>({get:async()=>({docs:Object.keys(S).filter(k=>k.startsWith(c+'/')).map(k=>({id:k.split('/')[1],data:()=>S[k]}))})})};
 window.firebase={initializeApp:()=>{},auth:Object.assign(()=>auth,{GoogleAuthProvider:function(){this.setCustomParameters=()=>{}}}),firestore:()=>fsx};
})();
window.RTS_FIREBASE={apiKey:'x',authDomain:'x',projectId:'x',appId:'x'};
"""
html=open('site/index.html',encoding='utf-8').read()
html=html.replace('<script src="https://www.gstatic.com','<!--').replace('<script src="config.js"></script>','--><script>'+MOCK+'</script>',1)
# jedyny blok komentarza obejmuje trzy tagi gstatic
open('site/test.html','w',encoding='utf-8').write(html)

errs=[]
def run(name,pre,fn):
    with sync_playwright() as pw:
        b=pw.chromium.launch();pg=b.new_page(viewport={'width':1280,'height':900})
        pg.on('pageerror',lambda e:errs.append(name+': '+str(e)));pg.on('console',lambda m:errs.append(name+': '+m.text) if m.type=='error' else None)
        pg.add_init_script('window.__store={};window.__members={};'+pre)
        pg.goto('file://'+os.path.abspath('site/test.html'));pg.wait_for_timeout(900)
        fn(pg);b.close()
STATS="window.__store['data/stats']={json:"+json.dumps(D)+"};"
run('gate',"",lambda pg:print('gate:',pg.is_visible('#gate')))
run('deny',"window.__user={email:'obcy@x.pl'};"+STATS,lambda pg:print('deny:',pg.is_visible('#deny'),pg.inner_text('#d-email')))
run('first',"window.__user={email:'hooday@gmail.com'};",lambda pg:print('first-run:',pg.is_visible('#first')))
def admin(pg):
    print('studio:',pg.is_visible('#studio'),'tabs:',pg.inner_text('#tabs').replace('\n','|'))
    print('title:',pg.input_value('#f-title'))
    pg.click('#dl')
    pg.click('button.tab:has-text("Admin")');pg.wait_for_timeout(300)
    pg.fill('#m-email','Marek@Gmail.com');pg.click('#m-add');pg.wait_for_timeout(400)
    print('members:',pg.inner_text('#m-list').replace('\n',' | ')[:120])
    print('store members:',pg.evaluate("Object.keys(window.__members)"))
    pg.screenshot(path='shot-admin.png')
run('admin',"window.__user={email:'hooday@gmail.com'};"+STATS,admin)
def member(pg):
    print('member tabs:',pg.inner_text('#tabs').replace('\n','|'),'who:',pg.inner_text('#who')[:50])
run('member',"window.__user={email:'marek@gmail.com'};window.__members['marek@gmail.com']={role:'member'};"+STATS,member)
print('errs',errs)
