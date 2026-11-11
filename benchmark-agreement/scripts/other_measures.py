"""Is 'which of two models is better' a defensible way to count agreement? The same comparison under other measures:
pairs (the headline), triples (same order of three models), same top model, top-3 overlap, Kendall tau, Spearman;
and pairs restricted to the strongest models."""
import sys,itertools,json,numpy as np
from scipy.stats import rankdata,kendalltau
src=open('scripts/audit.py').read().split("rng=np.random.default_rng(7)")[0]
exec(src)
five=['Harvey LAB (Vals run)','Legal Research Bench (Vals)','Mercor APEX, corporate law','Legora BAR','Certera']
F={f:[r[1] for r in rows if r[0]==f and r[6]] for f in ['science','coding','office work','finance']}; F['legal']=five
def shared(a,b,s,minn): 
    ms=[m for m in s if m in T[a] and m in T[b]]; return ms if len(set(ms))>=minn else None
def pairs_(a,b,ms):
    same=tot=0
    for i,j in itertools.combinations(range(len(ms)),2):
        da=T[a][ms[i]]-T[a][ms[j]]; db=T[b][ms[i]]-T[b][ms[j]]
        if da==0 or db==0: continue
        tot+=1; same+=(da>0)==(db>0)
    return same/tot if tot else np.nan
def triples_(a,b,ms,rng=None,cap=4000):
    idx=list(itertools.combinations(range(len(ms)),3))
    if rng is not None and len(idx)>cap: idx=[idx[k] for k in rng.choice(len(idx),cap,replace=False)]
    same=tot=0
    for t in idx:
        xa=[T[a][ms[k]] for k in t]; xb=[T[b][ms[k]] for k in t]
        if len(set(xa))<3 or len(set(xb))<3: continue
        tot+=1; same+= (np.argsort(xa)==np.argsort(xb)).all()
    return same/tot if tot else np.nan
def top1_(a,b,ms):
    u=list(dict.fromkeys(ms)); return float(max(u,key=lambda m:T[a][m])==max(u,key=lambda m:T[b][m]))
def top3_(a,b,ms):
    u=list(dict.fromkeys(ms)); ta=set(sorted(u,key=lambda m:-T[a][m])[:3]); tb=set(sorted(u,key=lambda m:-T[b][m])[:3]); return len(ta&tb)/3
def tau_(a,b,ms): return kendalltau([T[a][m] for m in ms],[T[b][m] for m in ms]).statistic
def rho_(a,b,ms): return float(np.corrcoef(rankdata([T[a][m] for m in ms]),rankdata([T[b][m] for m in ms]))[0,1])
M={'pairs':pairs_,'triples':triples_,'same_top':top1_,'top3_overlap':top3_,'kendall_tau':tau_,'spearman':rho_}
def field(names,s,minn,which):
    r={k:[] for k in which}
    for a,b in itertools.combinations(names,2):
        ms=shared(a,b,s,minn)
        if ms is None: continue
        for k in which: r[k].append(M[k](a,b,ms))
    return {k:float(np.nanmean(v)) if v else float('nan') for k,v in r.items()}
rng=np.random.default_rng(21); out={}
which=list(M)
for f in ['legal','coding','science','office work','finance']:
    pt=field(F[f],cohort,10,which)
    bs=[field(F[f],list(rng.choice(cohort,len(cohort))),8,['pairs','triples','same_top','top3_overlap']) for _ in range(300)]
    ci={k:[float(np.nanpercentile([b[k] for b in bs],2.5)),float(np.nanpercentile([b[k] for b in bs],97.5))] for k in bs[0]}
    out[f]=dict(point=pt,ci=ci)
    print(f"{f:12} pairs {pt['pairs']*100:4.0f}% [{ci['pairs'][0]*100:.0f},{ci['pairs'][1]*100:.0f}]  triples {pt['triples']*100:4.0f}% [{ci['triples'][0]*100:.0f},{ci['triples'][1]*100:.0f}]  same #1 {pt['same_top']*100:4.0f}% [{ci['same_top'][0]*100:.0f},{ci['same_top'][1]*100:.0f}]  top-3 overlap {pt['top3_overlap']*100:4.0f}% [{ci['top3_overlap'][0]*100:.0f},{ci['top3_overlap'][1]*100:.0f}]  tau {pt['kendall_tau']:.2f}  spearman {pt['spearman']:.2f}")
# strongest models only: rank models by average percentile across every included benchmark in all five fields
allb=[b for bs in F.values() for b in bs]
def pct(b):
    ms=[m for m in cohort if m in T[b]]; r=rankdata([T[b][m] for m in ms]); return {m:(r[i]-1)/(len(ms)-1) for i,m in enumerate(ms)}
P={b:pct(b) for b in allb}
strength={m:np.mean([P[b][m] for b in allb if m in P[b]]) for m in cohort}
order=sorted(cohort,key=strength.get,reverse=True)
print('\nstrongest models by average percentile across all benchmarks:',order[:15])
out['strongest']={}
for N in [10,12,15,20]:
    top=order[:N]; res={}
    for f in ['legal','coding']:
        pt=field(F[f],top,5,['pairs'])['pairs']
        bs=[field(F[f],list(rng.choice(top,len(top))),4,['pairs'])['pairs'] for _ in range(600)]
        res[f]=dict(pairs=pt,lo=float(np.nanpercentile(bs,2.5)),hi=float(np.nanpercentile(bs,97.5)))
    npair={f:sum(shared(a,b,top,5) is not None for a,b in itertools.combinations(F[f],2)) for f in ['legal','coding']}
    out['strongest'][N]=res
    print(f"  top {N:2}: legal {res['legal']['pairs']*100:.0f}% [{res['legal']['lo']*100:.0f},{res['legal']['hi']*100:.0f}] ({npair['legal']} pairings)   coding {res['coding']['pairs']*100:.0f}% [{res['coding']['lo']*100:.0f},{res['coding']['hi']*100:.0f}] ({npair['coding']} pairings)")
UNC={'mistral-large-4','qwen-3-8','hy4','deepseek-v4-1-flash'}; pool=[m for m in cohort if m not in UNC]
out['without_uncertain']=dict(models=len(pool),legal=field(F['legal'],pool,10,['pairs'])['pairs'],coding=field(F['coding'],pool,10,['pairs'])['pairs'])
lb='LegalBench (Vals)'; r=[pairs_(a,b,shared(a,b,cohort,10)) for a,b in itertools.combinations(five+[lb],2) if shared(a,b,cohort,10)]
out['legalbench']=dict(models_on_leaderboard=len(T[lb]),of_cohort=len([m for m in cohort if m in T[lb]]),lowest=float(min(T[lb][m] for m in cohort if m in T[lb])),highest=float(max(T[lb][m] for m in cohort if m in T[lb])),five_plus_legalbench=float(np.mean(r)),pairings=len(r))
print(out['without_uncertain'],out['legalbench'])
json.dump(out,open('data/other_measures.json','w'),indent=1)
