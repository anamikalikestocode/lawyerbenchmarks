"""Top model on each legal and coding leaderboard (full leaderboard, ties kept)."""
import sys,itertools,json,numpy as np
src=open('scripts/audit.py').read().split("rng=np.random.default_rng(7)")[0]
exec(src)
five=['Harvey LAB (Vals run)','Legal Research Bench (Vals)','Mercor APEX, corporate law','Legora BAR','Certera']
coding=[r[1] for r in rows if r[0]=='coding' and r[6]]
def top(n):
    d=T[n]; mx=max(d.values()); t=sorted(m for m,v in d.items() if v==mx); s=sorted(d.values(),reverse=True)
    return dict(top=t,score=float(mx),second=float(s[len(t)]) if len(s)>len(t) else None,top_in_cohort=all(m in cohort for m in t),models=len(d))
out={'legal':{n:top(n) for n in five},'coding':{n:top(n) for n in coding}}
for k,v in list(out.items()):
    allt=[m for x in v.values() for m in x['top']]; cnt={m:sum(m in x['top'] for x in v.values()) for m in set(allt)}
    out[k+'_summary']=dict(benchmarks=len(v),distinct_top_models=len(set(allt)),most=max(cnt.values()),most_model=max(cnt,key=cnt.get),ties=sum(len(x['top'])>1 for x in v.values()))
    print(k,out[k+'_summary']); [print('   ',n,x['top'],x['score'],x['second']) for n,x in v.items()]
json.dump(out,open('data/tops.json','w'),indent=1)
