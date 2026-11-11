import json,itertools,numpy as np,sys
sys.path.insert(0,'scripts')
from full import T
from master import vals, UNCERTAIN
from scipy.stats import spearmanr,kendalltau
rng=np.random.default_rng(61)
T=dict(T)
for slug,name in [('code-migration-v1-1','Code Migration (Vals)'),('ioi','IOI (Vals run)'),('programbench','ProgramBench (Vals run)'),('swebench-multimodal','SWE-bench Multimodal (Vals run)')]:
    T[name]=vals(slug)[0]
cohort=sorted(T['LAB (Vals run)'])
LEGAL={'Harvey LAB':'LAB (Vals run)','Vals Legal Research':'Vals Legal Research','Mercor APEX law':'APEX-Agents corporate law (Mercor)','Legora BAR':'Legora BAR','Certera':'Certera (votes by legal professionals)'}
CODE={'Terminal-Bench 4':'Terminal-Bench 4 (Vals run)','Vibe Code':'Vibe Code (Vals)','FrontierCode 2':'FrontierCode 2 (AA)','SciCode':'SciCode (AA)','Code Migration':'Code Migration (Vals)','IOI':'IOI (Vals run)','ProgramBench':'ProgramBench (Vals run)','SWE-bench Multimodal':'SWE-bench Multimodal (Vals run)'}
def rho(a,b,ms,minn=10,f=spearmanr):
    ms=[m for m in ms if m in T[a] and m in T[b]]
    if len(set(ms))<minn: return None,len(set(ms))
    return f([T[a][m] for m in ms],[T[b][m] for m in ms])[0],len(ms)
def pairs(G,ms,minn=10,f=spearmanr): return {(a,b):rho(G[a],G[b],ms,minn,f) for a,b in itertools.combinations(G,2)}
med=lambda PP:float(np.nanmedian([v[0] for v in PP.values() if v[0] is not None]))
def boot(L,C,ms,n=3000):
    ml=[];mc=[];d=[];per={k:[] for k in L}
    for _ in range(n):
        s=list(rng.choice(ms,len(ms))); p=pairs(L,s,8); c=pairs(C,s,8); a,b=med(p),med(c); ml.append(a);mc.append(b);d.append(b-a)
        for k in L:
            v=[x[0] for (i,j),x in p.items() if k in (i,j) and x[0] is not None]; per[k].append(np.mean(v) if v else np.nan)
    return ml,mc,d,per
def report(label,L,C,ms,minn=10,f=spearmanr,doboot=True):
    P=pairs(L,ms,minn,f); Cp=pairs(C,ms,minn,f)
    nl=sum(v[0] is not None for v in P.values()); nc=sum(v[0] is not None for v in Cp.values())
    s=f"{label:58} legal {med(P):.2f} ({nl} pairs)  coding {med(Cp):.2f} ({nc} pairs)  gap {med(Cp)-med(P):.2f}"
    out=dict(legal=med(P),coding=med(Cp),nl=nl,nc=nc)
    if doboot:
        ml,mc,d,per=boot(L,C,ms); out.update(legal_ci=list(np.nanpercentile(ml,[2.5,97.5])),coding_ci=list(np.nanpercentile(mc,[2.5,97.5])),gap_ci=list(np.nanpercentile(d,[2.5,97.5])),p=float((np.array(d)<=0).mean()),per=per)
        s+=f"  [{out['gap_ci'][0]:.2f},{out['gap_ci'][1]:.2f}]  P(coding<=legal)={out['p']:.4f}"
    print(s); return out,P,Cp
print('cohort',len(cohort))
main,P,Cp=report('MAIN: 6 legal, 8 coding, 37 current models',LEGAL,CODE,cohort)
print('  legal CI',np.round(main['legal_ci'],2),'coding CI',np.round(main['coding_ci'],2))
print('\nlegal pairs:')
for (a,b),(r,n) in sorted(P.items(),key=lambda kv:-(kv[1][0] if kv[1][0] is not None else -9)): print(f"   {a:22} {b:22} n={n:2} {('%+.2f'%r) if r is not None else 'too few'}")
print('\nper legal benchmark (bars):')
bars={}
for k in LEGAL:
    v=[x[0] for (i,j),x in P.items() if k in (i,j) and x[0] is not None]; lo,hi=np.nanpercentile(main['per'][k],[2.5,97.5]); bars[k]=(float(np.mean(v)),float(lo),float(hi),len([m for m in cohort if m in T[LEGAL[k]]]))
    print(f"   {k:22} {np.mean(v):.2f} [{lo:.2f},{hi:.2f}]  models {bars[k][3]}  pairs {len(v)}")
print('\ncoding pairs:')
for (a,b),(r,n) in sorted(Cp.items(),key=lambda kv:-(kv[1][0] if kv[1][0] is not None else -9)): print(f"   {a:22} {b:22} n={n:2} {('%+.2f'%r) if r is not None else 'too few'}")
print('\n--- robustness ---')
rob={}
rob['original 4 coding benchmarks'],_,_=report('coding = the original four',LEGAL,{k:CODE[k] for k in ['Terminal-Bench 4','Vibe Code','FrontierCode 2','SciCode']},cohort)
rob['no uncertain matches'],_,_=report('excluding 4 models with uncertain name matches',LEGAL,CODE,[m for m in cohort if m not in UNCERTAIN])
rob['kendall'],_,_=report("Kendall's tau instead of Spearman",LEGAL,CODE,cohort,f=kendalltau,doboot=False)
allm=sorted(set().union(*[set(T[v]) for v in list(LEGAL.values())+list(CODE.values())]))
rob['all models'],_,_=report('all models any source tested (not just the 37)',LEGAL,CODE,allm,doboot=False)
for drop in LEGAL:
    rob['drop '+drop],_,_=report('leave out '+drop,{k:v for k,v in LEGAL.items() if k!=drop},CODE,cohort,doboot=False)
rob['min 15 shared'],_,_=report('only pairs sharing 15+ models',LEGAL,CODE,cohort,minn=15,doboot=False)
main.pop('per'); 
for v in rob.values(): v.pop('per',None)
json.dump({'main':main,'bars':bars,'legal_pairs':{f'{a}|{b}':v for (a,b),v in P.items()},'coding_pairs':{f'{a}|{b}':v for (a,b),v in Cp.items()},'robustness':rob},open('data/final.json','w'),indent=1)
