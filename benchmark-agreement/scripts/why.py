"""Why do legal benchmarks agree less? Hold the evaluator fixed (Vals), and separate noise from real disagreement using Vals' published standard errors."""
import json,itertools,numpy as np,sys
rng=np.random.default_rng(5)
V=lambda s:json.load(open(f'raw/vals_views/{s}.json'))['tasks']['overall']
cohort=sorted(V('hlab'))
F={'legal':['hlab','legal_research','immigration'],'finance':['fabv2-1','emb-v1-1','tax_agent_bench'],'coding':['terminal-bench-4','vibe-code','code-migration-v1-1','ioi','programbench','swebench-multimodal'],'science':['biomysterybench','mysterymechanism','terminal-bench-science']}
def conc(x,y):
    s=t=0
    for i,j in itertools.combinations(range(len(x)),2):
        a=x[i]-x[j]; b=y[i]-y[j]
        if a==0 or b==0: continue
        t+=1; s+=(a>0)==(b>0)
    return s/t
out=[]
for f,bl in F.items():
    obs=[];ceil=[];rel=[]
    for a,b in itertools.combinations(bl,2):
        A,B=V(a),V(b); ms=[m for m in cohort if m in A and m in B and A[m].get('accuracy') is not None and B[m].get('accuracy') is not None]
        if len(ms)<10: continue
        xa=np.array([A[m]['accuracy'] for m in ms]); xb=np.array([B[m]['accuracy'] for m in ms]); sa=np.array([A[m].get('stderr') or 0 for m in ms]); sb=np.array([B[m].get('stderr') or 0 for m in ms])
        o=conc(xa,xb)
        # ceiling: if both benchmarks ranked models identically underneath, how often would they agree given each one's own noise?
        # underlying order taken from benchmark A; benchmark B keeps its own score distribution, reordered to match A's order.
        ordA=np.argsort(np.argsort(xa)); tb=np.sort(xb)[ordA]
        c=np.mean([conc(xa+rng.normal(0,sa),tb+rng.normal(0,sb)) for _ in range(300)])
        ordB=np.argsort(np.argsort(xb)); ta=np.sort(xa)[ordB]
        c2=np.mean([conc(ta+rng.normal(0,sa),xb+rng.normal(0,sb)) for _ in range(300)])
        c=(c+c2)/2
        obs.append(o);ceil.append(c)
        out.append(f"   {f:8} {a:20} {b:22} n={len(ms):2} observed {o*100:5.1f}%   if they measured the same thing, noise alone allows {c*100:5.1f}%")
    out.append(f"{f.upper():8} same evaluator (Vals): observed {np.mean(obs)*100:.1f}%  noise ceiling {np.mean(ceil)*100:.1f}%  shortfall below ceiling {(np.mean(ceil)-np.mean(obs))*100:.1f} points\n")
# self-reliability of each legal benchmark's ranking
for s in F['legal']+F['finance']+['terminal-bench-4','vibe-code']:
    A=V(s); ms=[m for m in cohort if m in A]; x=np.array([A[m]['accuracy'] for m in ms]); se=np.array([A[m].get('stderr') or 0 for m in ms])
    r=np.mean([conc(x+rng.normal(0,se),x+rng.normal(0,se)) for _ in range(300)]); out.append(f"   rerun-with-same-noise agreement {s:20} {r*100:.1f}%  (score range {x.min():.0f} to {x.max():.0f}, typical margin ±{np.median(se):.1f})")
sys.stderr.write('\n'.join(out)+'\n')
