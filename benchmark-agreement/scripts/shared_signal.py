"""Do legal benchmarks share anything beyond general model strength?
General strength of a model = its average standardised score on the benchmarks of the OTHER fields.
For each pair of benchmarks inside a field: rank correlation, and the same after removing general strength (partial rank correlation)."""
import sys,itertools,json,numpy as np
from scipy.stats import rankdata
src=open('scripts/audit.py').read().split("rng=np.random.default_rng(7)")[0]
exec(src)
five=['Harvey LAB (Vals run)','Legal Research Bench (Vals)','Mercor APEX, corporate law','Legora BAR','Certera']
F={f:[r[1] for r in rows if r[0]==f and r[6]] for f in ['science','coding','office work','finance']}
F['legal']=five
def z(b,ms):
    v=np.array([T[b][m] for m in ms],float); s=v.std()
    return dict(zip(ms,(v-v.mean())/s if s>0 else v*0))
def general(field,ms_all):
    others=[b for f,bs in F.items() if f!=field for b in bs]
    acc={m:[] for m in ms_all}
    for b in others:
        ms=[m for m in ms_all if m in T[b]]
        if len(ms)<8: continue
        zz=z(b,ms)
        for m in ms: acc[m].append(zz[m])
    return {m:float(np.mean(v)) for m,v in acc.items() if len(v)>=6}
def sp(a,b): 
    ra,rb=rankdata(a),rankdata(b); return float(np.corrcoef(ra,rb)[0,1])
def partial(a,b,g):
    rab,rag,rbg=sp(a,b),sp(a,g),sp(b,g); d=np.sqrt((1-rag**2)*(1-rbg**2))
    return (rab-rag*rbg)/d if d>0 else np.nan
def field_stats(field,sample):
    ms_all=list(dict.fromkeys(sample)); G=general(field,ms_all); raw=[];par=[];wg=[]
    for a,b in itertools.combinations(F[field],2):
        ms=[m for m in sample if m in T[a] and m in T[b] and m in G]
        if len(set(ms))<8: continue
        x=[T[a][m] for m in ms]; y=[T[b][m] for m in ms]; g=[G[m] for m in ms]
        raw.append(sp(x,y)); par.append(partial(x,y,g))
    for a in F[field]:
        ms=[m for m in sample if m in T[a] and m in G]
        if len(set(ms))>=8: wg.append(sp([T[a][m] for m in ms],[G[m] for m in ms]))
    return np.nanmean(raw),np.nanmean(par),np.nanmean(wg)
rng=np.random.default_rng(3); out={}
for f in ['legal','coding','science','office work','finance']:
    pt=field_stats(f,cohort); bs=np.array([field_stats(f,list(rng.choice(cohort,len(cohort)))) for _ in range(1000)])
    lo,hi=np.nanpercentile(bs,[2.5,97.5],axis=0)
    out[f]=dict(raw=float(pt[0]),partial=float(pt[1]),with_general=float(pt[2]),raw_ci=[float(lo[0]),float(hi[0])],partial_ci=[float(lo[1]),float(hi[1])],with_general_ci=[float(lo[2]),float(hi[2])],share_partial_le0=float((bs[:,1]<=0).mean()))
    print(f"{f:12} within-field rank corr {pt[0]:.2f} [{lo[0]:.2f},{hi[0]:.2f}]   after removing general strength {pt[1]:.2f} [{lo[1]:.2f},{hi[1]:.2f}]   corr with general strength {pt[2]:.2f} [{lo[2]:.2f},{hi[2]:.2f}]   partial<=0 in {100*(bs[:,1]<=0).mean():.0f}%")
# detail for legal pairs
G=general('legal',cohort)
print('\nlegal pairs: raw / after removing general strength / n')
for a,b in itertools.combinations(five,2):
    ms=[m for m in cohort if m in T[a] and m in T[b] and m in G]
    x=[T[a][m] for m in ms]; y=[T[b][m] for m in ms]; g=[G[m] for m in ms]
    print(f"   {a[:22]:22} | {b[:22]:22} {sp(x,y):5.2f} {partial(x,y,g):5.2f}  n={len(ms)}")
print('\neach legal benchmark vs general strength:',{a[:14]:round(sp([T[a][m] for m in cohort if m in T[a] and m in G],[G[m] for m in cohort if m in T[a] and m in G]),2) for a in five})
top=sorted(G,key=G.get,reverse=True)
print('general strength, top 10:',[(m,round(G[m],2)) for m in top[:10]])
for m in ['gemini-4-argon','muse-wonder','opus-5-5','gpt-6-1-sol','gpt-6-astra','gemini-3-8-flash','grok-4-7','fable-5-2']:
    if m in G: print(f"   {m:18} general-strength rank {1+top.index(m)} of {len(top)}")
# the exception: Harvey LAB and Vals Legal Research, whoever runs LAB
def pair(a,b):
    ms=[m for m in cohort if m in T[a] and m in T[b] and m in G]
    x=[T[a][m] for m in ms]; y=[T[b][m] for m in ms]; g=[G[m] for m in ms]
    return dict(raw=sp(x,y),partial=float(partial(x,y,g)),n=len(ms))
def cluster(names,sample):
    Gs=general('legal',list(dict.fromkeys(sample))); par=[]
    for a,b in itertools.combinations(names,2):
        ms=[m for m in sample if m in T[a] and m in T[b] and m in Gs]
        if len(set(ms))<8: continue
        par.append(partial([T[a][m] for m in ms],[T[b][m] for m in ms],[Gs[m] for m in ms]))
    return np.nanmean(par)
three=five[:3]; bs=np.array([cluster(three,list(rng.choice(cohort,len(cohort)))) for _ in range(1000)])
out['extra']=dict(lab_vals__vals_lr=pair('Harvey LAB (Vals run)','Legal Research Bench (Vals)'),lab_mercor__vals_lr=pair('Harvey LAB (Mercor run)','Legal Research Bench (Vals)'),
    three=dict(partial=float(cluster(three,cohort)),lo=float(np.nanpercentile(bs,2.5)),hi=float(np.nanpercentile(bs,97.5))),
    general_rank={m:1+top.index(m) for m in ['gemini-4-argon','muse-wonder','fable-5-2','opus-5-5'] if m in top},general_models=len(top))
print(out['extra'])
json.dump(out,open('data/shared_signal.json','w'),indent=1)
