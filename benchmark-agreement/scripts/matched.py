"""Like-for-like check: compare fields on the SAME models, not just the same pool of 37.
Legal pairings often share only 15-29 models (mostly big-lab frontier models); coding pairings share up to 37, including weak models that are easy to rank."""
import sys,io,contextlib,itertools,numpy as np,json
sys.path.insert(0,'scripts')
with contextlib.redirect_stdout(io.StringIO()):
    from full import T as TF, cohort
    from master import vals, aa, other
T=dict(TF)
def add(name,d): T[name]=d[0]; return name
LEGAL=['LAB (Vals run)','Vals Legal Research','APEX-Agents corporate law (Mercor)','Legora BAR','Certera (votes by legal professionals)']
F={'legal':LEGAL,
 'coding':['Terminal-Bench 4 (Vals run)','Vibe Code (Vals)','FrontierCode 2 (AA)','SciCode (AA)',add('cm',vals('code-migration-v1-1')),add('ioi',vals('ioi')),add('pb',vals('programbench')),add('swemm',vals('swebench-multimodal'))],
 'finance':[add('fa',vals('fabv2-1')),add('emb',vals('emb-v1-1')),add('tax',vals('tax_agent_bench'))],
 'science':[add('bio',vals('biomysterybench')),add('mm',vals('mysterymechanism')),add('tbs',vals('terminal-bench-science'))],
 'office work':[add('gv',aa('gdpval_aa','elo')),add('br',aa('aa_briefcase','elo')),add('ab',aa('automationbench_aa','score')),add('gp',aa('gdp_pdf','all_pass')),add('apx',other('mercor_apex_agents','overall_mean_score_pct'))]}
def conc(a,b,ms,minn=8):
    ms=[m for m in ms if m in T[a] and m in T[b]]
    if len(set(ms))<minn: return None
    same=tot=0
    for i,j in itertools.combinations(range(len(ms)),2):
        da=T[a][ms[i]]-T[a][ms[j]]; db=T[b][ms[i]]-T[b][ms[j]]
        if da==0 or db==0: continue
        tot+=1; same+=(da>0)==(db>0)
    return same/tot if tot else None
def field(G,ms,minn=8):
    v=[conc(a,b,ms,minn) for a,b in itertools.combinations(G,2)]; v=[x for x in v if x is not None]
    return (float(np.mean(v)),len(v)) if v else (None,0)
out=[]
out.append('(0) each field on its own shared models within the 37 (what the slides show)')
for k,G in F.items(): m,n=field(G,cohort,10); out.append(f"    {k:12} {m*100:5.1f}%  ({n} pairings)")
S=[m for m in cohort if all(m in T[b] for b in LEGAL)]
out.append(f"\n(1) every field on the SAME {len(S)} models (the ones all five legal benchmarks tested): {S}")
for k,G in F.items():
    m,n=field(G,S,8); cov=[sum(x in T[b] for x in S) for b in G]
    out.append(f"    {k:12} {('%5.1f%%'%(m*100)) if m else '  n/a'}  ({n} pairings; models covered per benchmark {min(cov)}-{max(cov)})")
rng=np.random.default_rng(3); res={k:[] for k in F}; diffs={k:[] for k in F if k!='legal'}
for _ in range(3000):
    s=list(rng.choice(S,len(S))); L=field(LEGAL,s,6)[0]
    if L is None: continue
    for k,G in F.items():
        v=field(G,s,6)[0]
        if v is None: continue
        res[k].append(v)
        if k!='legal': diffs[k].append(v-L)
for k in F: out.append(f"    {k:12} 95% interval {np.percentile(res[k],2.5)*100:.0f}% to {np.percentile(res[k],97.5)*100:.0f}%"+('' if k=='legal' else f"   minus legal: {np.mean(diffs[k])*100:+.1f} [{np.percentile(diffs[k],2.5)*100:+.1f},{np.percentile(diffs[k],97.5)*100:+.1f}]  share of resamples at or below legal {(np.array(diffs[k])<=0).mean():.3f}"))
out.append('\n(2) matched: for each legal pairing, the other fields are scored on exactly that pairing\'s shared models')
acc={k:[] for k in F}
for a,b in itertools.combinations(LEGAL,2):
    Sab=[m for m in cohort if m in T[a] and m in T[b]]; l=conc(a,b,Sab,10)
    row=f"    {a[:24]:25} {b[:24]:25} n={len(Sab):2} legal {l*100:5.1f}%"
    acc['legal'].append(l)
    for k in ['coding','finance','science','office work']:
        m,n=field(F[k],Sab,8)
        if m is not None: acc[k].append(m); row+=f" | {k} {m*100:5.1f}%"
    out.append(row)
for k in F: out.append(f"    MEAN {k:12} {np.mean(acc[k])*100:5.1f}%  (over {len(acc[k])} legal pairings)")
json.dump({'common_models':S,'common':{k:field(G,S,8) for k,G in F.items()},'matched_mean':{k:float(np.mean(v)) for k,v in acc.items()}},open('data/matched.json','w'),indent=1)
sys.stderr.write('\n'.join(out)+'\n')
