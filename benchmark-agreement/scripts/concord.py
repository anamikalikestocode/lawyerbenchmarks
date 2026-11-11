import json,itertools,numpy as np,sys
sys.path.insert(0,'scripts')
from final import T,LEGAL,CODE,cohort
rng=np.random.default_rng(71)
def conc(a,b,ms,minn=10):
    """Share of model pairs that the two benchmarks put in the same order (ties in either benchmark dropped)."""
    ms=[m for m in ms if m in T[a] and m in T[b]]
    if len(set(ms))<minn: return None,len(set(ms))
    same=tot=0
    for i,j in itertools.combinations(range(len(ms)),2):
        da=T[a][ms[i]]-T[a][ms[j]]; db=T[b][ms[i]]-T[b][ms[j]]
        if da==0 or db==0: continue
        tot+=1; same+= (da>0)==(db>0)
    return same/tot,len(ms)
def allpairs(G,ms,minn=10): return {(x,y):conc(G[x],G[y],ms,minn) for x,y in itertools.combinations(G,2)}
def pooled(P): v=[x[0] for x in P.values() if x[0] is not None]; return float(np.median(v)),float(np.mean(v))
if __name__=='__main__':
    PL=allpairs(LEGAL,cohort); PC=allpairs(CODE,cohort)
    print('legal median/mean concordance',np.round(pooled(PL),3),' coding',np.round(pooled(PC),3))
    SAME={'LAB: Vals vs Artificial Analysis':('LAB (Vals run)','LAB (AA run, ungated)'),'LAB: Vals vs Mercor':('LAB (Vals run)','LAB (Mercor run)'),'LAB: Artificial Analysis vs Mercor':('LAB (AA run, ungated)','LAB (Mercor run)'),'Terminal-Bench 4: Vals vs Artificial Analysis':('Terminal-Bench 4 (Vals run)','Terminal-Bench 4 (AA run)')}
    S={k:conc(a,b,cohort) for k,(a,b) in SAME.items()}; print({k:(round(v[0],3),v[1]) for k,v in S.items()})
    per={}
    for k in LEGAL: per[k]=float(np.mean([x[0] for (i,j),x in PL.items() if k in (i,j) and x[0] is not None]))
    perc={k:float(np.mean([x[0] for (i,j),x in PC.items() if k in (i,j) and x[0] is not None])) for k in CODE}
    print('per legal',{k:round(v,3) for k,v in per.items()}); print('per coding',{k:round(v,3) for k,v in perc.items()})
    # bootstrap
    bl=[];bc=[];bd=[];bper={k:[] for k in LEGAL}
    for _ in range(2000):
        s=list(rng.choice(cohort,len(cohort))); p=allpairs(LEGAL,s,8); c=allpairs(CODE,s,8); a=pooled(p)[1]; b=pooled(c)[1]; bl.append(a);bc.append(b);bd.append(b-a)
        for k in LEGAL:
            v=[x[0] for (i,j),x in p.items() if k in (i,j) and x[0] is not None]; bper[k].append(np.mean(v) if v else np.nan)
    ci=lambda v:[float(x) for x in np.nanpercentile(v,[2.5,97.5])]
    print('legal mean CI',np.round(ci(bl),3),'coding',np.round(ci(bc),3),'diff',round(pooled(PC)[1]-pooled(PL)[1],3),np.round(ci(bd),3),'P',(np.array(bd)<=0).mean())
    # cross-publisher only
    VALSRUN={'Harvey LAB','Vals Legal Research'}; AARUN={'FrontierCode 2','SciCode'}
    xl=[x[0] for (i,j),x in PL.items() if not ({i,j}<=VALSRUN) and x[0] is not None]
    xc=[x[0] for (i,j),x in PC.items() if (i in AARUN)!=(j in AARUN) and x[0] is not None]
    print('cross-evaluator only: legal mean %.3f median %.3f (%d pairs) | coding mean %.3f median %.3f (%d pairs)'%(np.mean(xl),np.median(xl),len(xl),np.mean(xc),np.median(xc),len(xc)))
    # score spread: how compressed is each benchmark among cohort models (coefficient: IQR / range share)
    for G in (LEGAL,CODE):
        for k,v in G.items():
            x=np.array([T[v][m] for m in cohort if m in T[v]],float); print(f"   {k:22} n={len(x):2} min {x.min():7.2f} median {np.median(x):7.2f} max {x.max():7.2f}  distinct values {len(set(np.round(x,2)))}")
    json.dump({'legal_pairs':{f'{a}|{b}':v for (a,b),v in PL.items()},'coding_pairs':{f'{a}|{b}':v for (a,b),v in PC.items()},'same':S,'per_legal':per,'per_legal_ci':{k:ci(v) for k,v in bper.items()},'per_coding':perc,'legal':pooled(PL),'coding':pooled(PC),'legal_ci':ci(bl),'coding_ci':ci(bc),'diff_ci':ci(bd),'cross':{'legal':float(np.mean(xl)),'coding':float(np.mean(xc))}},open('data/concord.json','w'),indent=1)
