import json,sys
S=sys.argv[1]; LAST=int(sys.argv[2])
d=json.load(open(S+'/stats_k10.json')); r=json.load(open(S+'/k11_raw.json'))
new_ids={f[0] for f in r['fx']}
assert not {t[0] for t in d['tstats']}&new_ids and not {g[0] for g in d['goals']}&new_ids
# fx: aktualizacja lub dopisanie
fx={f[0]:f for f in d['fx']}; before=len(fx)
for f in r['fx']: fx[f[0]]=f
d['fx']=sorted(fx.values(),key=lambda f:(f[2],f[0]))
# tstats
def n(v): return None if v is None else v
for fid,tid,v in r['st']:
    pct=round(v['Passes accurate']/v['Total passes']*100) if v.get('Total passes') else None
    d['tstats'].append([fid,tid,int(v['Ball Possession'].rstrip('%')),v['Total Shots'],v['Shots on Goal'],v['Corner Kicks'],v['Fouls'],v['Yellow Cards'],v['Red Cards'],v['Goalkeeper Saves'],v['Total passes'],pct,float(v['expected_goals'])])
# goals
T={'Normal Goal':'N','Penalty':'P','Own Goal':'O'}
for fid,el,ex,tid,pl,ast,det in r['ev']:
    if det in T: d['goals'].append([fid,el,tid,pl,ast,T[det]])
# players
PI={p[0]:p for p in d['players']}; added=[];fxd={f[0]:f for f in r['fx']}
for row in r['pl']:
    fid,tid,pid,name,pos,start,mins,rat=row[:8]; s=row[8:]
    f=fxd[fid]; opp_goals=f[6] if f[3]==tid else f[5]
    conc=s[-1] if s[-1] is not None else (opp_goals if pos=='G' else 0)
    s=[x or 0 for x in s[:-1]]+[conc]
    rat=float(rat) if rat not in (None,'0','') else None
    if pid==102542: name='Steve Kingue'
    if pid not in PI:
        p=[pid,name,tid,pos,0,0,0,None]+[0]*20; PI[pid]=p; d['players'].append(p); added.append((pid,name,tid))
    p=PI[pid]
    if rat is not None:
        p[7]=round(((p[7] or rat)*p[4]+rat)/(p[4]+1),2) if p[7] is not None else rat
    p[4]+=1; p[5]+=1 if start else 0; p[6]+=mins
    for i,v in enumerate(s): p[8+i]+=v
    p[2]=tid
# upcoming: usuń rozegrane
played={(fxd[i][3],fxd[i][4]) for i in fxd}
TN={t[0]:t[1] for t in d['teams']}
d['upcoming']=[u for u in d['upcoming'] if (u[2],u[3]) not in {(TN[a],TN[b]) for a,b in played}]
d['meta']={'generatedAt':'2026-10-17','lastRound':LAST,'season':d['meta']['season']}
json.dump(d,open(S+'/stats_k11.json','w'),ensure_ascii=False,separators=(',',':'))
print('fx',before,'->',len(d['fx']),'| tstats',len(d['tstats']),'| goals',len(d['goals']),'| players',len(d['players']),'| upcoming',len(d['upcoming']))
print('nowi zawodnicy:',added)
print('id sum',sum(p[0] for p in d['players']))
