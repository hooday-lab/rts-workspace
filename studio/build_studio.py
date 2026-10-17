import json,base64,os,re
R=os.path.dirname(os.path.abspath(__file__)); F=os.path.join(R,'..','cards','fonts')
fonts=[]
for fn in sorted(os.listdir(F)):
    m=re.match(r'barlow(-condensed)?-(latin-ext|latin)-(\d+)-normal\.woff2',fn)
    if not m: continue
    fonts.append({'fam':'BC' if m.group(1) else 'BA','r':'ext' if m.group(2)=='latin-ext' else 'latin','w':int(m.group(3)),'b':base64.b64encode(open(os.path.join(F,fn),'rb').read()).decode()})
tpl=open(os.path.join(R,'studio_tpl.html'),encoding='utf-8').read()
data=open(os.path.join(R,'data.json'),encoding='utf-8').read()
bg=base64.b64encode(open(os.path.join(R,'bg.jpg'),'rb').read()).decode()
out=tpl.replace('__FONTS__',json.dumps(fonts)).replace('__DATA__',data).replace('__BG__',bg)
open(os.path.join(R,'studio.html'),'w',encoding='utf-8').write(out)
print(len(out)/1e6,'MB',len(fonts),'fonts')
