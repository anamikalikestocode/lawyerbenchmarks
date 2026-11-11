import sys,io,contextlib,itertools,numpy as np,json
sys.path.insert(0,'scripts')
with contextlib.redirect_stdout(io.StringIO()):
    from final import T,LEGAL,CODE,cohort
    from concord import conc,allpairs,pooled
    from master import vals,aa,other
T2=T
def add(name,d): T2[name]=d[0]; return name
F={
 'finance':{ 'Finance Agent (Vals)':add('fa',vals('fabv2-1')),'Financial modelling EMB (Vals)':add('emb',vals('emb-v1-1')),'Tax Agent (Vals)':add('tax',vals('tax_agent_bench'))},
 'science':{ 'BioMystery (Vals)':add('bio',vals('biomysterybench')),'MysteryMechanism (Vals)':add('mm',vals('mysterymechanism')),'Terminal-Bench Science (Vals)':add('tbs',vals('terminal-bench-science')),'Proof Bench (Vals)':add('pb',vals('proof_bench'))},
 'medicine':{ 'MedCode (Vals)':add('mc',vals('medcode')),'MedScribe (Vals)':add('ms',vals('medscribe'))},
 'office work':{ 'GDPval-AA':add('gv',aa('gdpval_aa','elo')),'AA-Briefcase':add('br',aa('aa_briefcase','elo')),'AutomationBench (AA)':add('ab',aa('automationbench_aa','score')),'GDP.pdf (AA)':add('gp',aa('gdp_pdf','all_pass')),'APEX-Agents overall (Mercor)':add('apx',other('mercor_apex_agents','overall_mean_score_pct'))},
}
rng=np.random.default_rng(91)
out=[]
def rep(name,G):
    P=allpairs(G,cohort); ok=[v[0] for v in P.values() if v[0] is not None]
    bs=[]
    for _ in range(600):
        s=list(rng.choice(cohort,len(cohort))); v=[x[0] for x in allpairs(G,s,8).values() if x[0] is not None]
        if v: bs.append(np.mean(v))
    out.append(f"{name:12} {len(G)} benchmarks, {len(ok)} pairs: {np.mean(ok)*100:5.1f}%  [{np.percentile(bs,2.5)*100:.0f}, {np.percentile(bs,97.5)*100:.0f}]   pairs: "+', '.join(f"{v[0]*100:.0f}(n={v[1]})" for v in P.values() if v[0] is not None))
rep('legal',LEGAL); rep('coding',CODE)
for k,G in F.items(): rep(k,G)
x=[conc(LEGAL[a],CODE[b],cohort)[0] for a in LEGAL for b in CODE]; x=[v for v in x if v is not None]
out.append('legal benchmark vs coding benchmark: %.1f%% (%d pairs)'%(np.mean(x)*100,len(x)))
for a in LEGAL:
    v=[conc(LEGAL[a],CODE[b],cohort)[0] for b in CODE]; v=[q for q in v if q is not None]; out.append(f"   {a:20} vs coding benchmarks: {np.mean(v)*100:.0f}%")
sys.stderr.write('\n'.join(out)+'\n')
