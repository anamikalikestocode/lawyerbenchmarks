"""All-or-nothing versus partial-credit scoring on the same runs.
For each legal benchmark that publishes both: score range, how many model pairs are separated beyond the margin of error,
how often the two scorings order models the same way, and how well each agrees with the other legal benchmarks."""
import sys,io,contextlib,json,itertools,numpy as np
sys.path.insert(0,'scripts')
src=open('scripts/audit.py').read().split("rng=np.random.default_rng(7)")[0]
with contextlib.redirect_stdout(io.StringIO()): exec(src)
from canon import canon
def vals_metric(slug,task):
    """same model selection as the main analysis (master.vals), plus the published standard error"""
    with contextlib.redirect_stdout(io.StringIO()):
        from master import vals
    acc,raw=vals(slug,task); t=json.load(open(f'raw/vals_views/{slug}.json'))['tasks'][task]
    return acc,{k:t[raw[k]].get('stderr') for k in acc}
def conc(A,B,pool,minn=10):
    ms=[m for m in pool if m in A and m in B]
    if len(ms)<minn: return None,len(ms)
    same=tot=0
    for i,j in itertools.combinations(ms,2):
        da=A[i]-A[j]; db=B[i]-B[j]
        if da==0 or db==0: continue
        tot+=1; same+=(da>0)==(db>0)
    return same/tot*100,len(ms)
def separated(acc,se,pool):
    ms=[m for m in pool if m in acc and se.get(m)]
    pr=list(itertools.combinations(ms,2)); sep=sum(abs(acc[a]-acc[b])>1.96*np.hypot(se[a],se[b]) for a,b in pr)
    return sep/len(pr)*100,len(ms)
others={'Vals Legal Research':'Legal Research Bench (Vals)','Mercor APEX law':'Mercor APEX, corporate law','Legora BAR':'Legora BAR','Certera':'Certera','Harvey LAB':'Harvey LAB (Vals run)'}
def vs_others(D,skip):
    r=[conc(D,T[t],cohort)[0] for k,t in others.items() if k!=skip]; r=[x for x in r if x is not None]; return np.mean(r) if r else None
out={}
pairs=[('Harvey LAB (Vals run)','hlab','overall','criteria_pass_rate','Harvey LAB'),('Vals Legal Research','legal_research','overall','weighted_pass','Vals Legal Research')]
for name,slug,tb,tp,skip in pairs:
    b,bse=vals_metric(slug,tb); p,pse=vals_metric(slug,tp)
    co=[m for m in cohort if m in b and m in p]
    rb=[b[m] for m in co]; rp=[p[m] for m in co]
    sb,_=separated(b,bse,co); spp,_=separated(p,pse,co)
    out[name]=dict(models=len(co),binary_range=[min(rb),max(rb)],partial_range=[min(rp),max(rp)],binary_separated=sb,partial_separated=spp,
        binary_vs_partial=conc(b,p,co)[0],binary_vs_other_legal=vs_others(b,skip),partial_vs_other_legal=vs_others(p,skip))
# Mercor APEX law: mean score (partial) and pass@1 (binary); same row selection as the main analysis (by model id, highest effort)
with contextlib.redirect_stdout(io.StringIO()):
    from master import other
mb=other('mercor_apex_agents','law_pass_at_1_pct')[0]; mp=other('mercor_apex_agents','law_mean_score_pct')[0]; mbe={}; mpe={}
co=[m for m in cohort if m in mb and m in mp]
out['Mercor APEX law']=dict(models=len(co),binary_range=[min(mb[m] for m in co),max(mb[m] for m in co)],partial_range=[min(mp[m] for m in co),max(mp[m] for m in co)],
    binary_separated=separated(mb,mbe,co)[0] if any(mbe.get(m) for m in co) else None,partial_separated=separated(mp,mpe,co)[0] if any(mpe.get(m) for m in co) else None,
    binary_vs_partial=conc(mb,mp,co)[0],binary_vs_other_legal=vs_others(mb,'Mercor APEX law'),partial_vs_other_legal=vs_others(mp,'Mercor APEX law'))
# Artificial Analysis run of LAB: criterion pass (partial), all-pass (binary), all-pass gated on made-up facts
with contextlib.redirect_stdout(io.StringIO()):
    from master import aa
cp=aa('harvey_lab_aa_v1_1','criterion_pass_rate')[0]; ap=aa('harvey_lab_aa_v1_1','all_pass_rate_ungated')[0]; gp=aa('harvey_lab_aa_v1_1','hallucination_gated_all_pass_rate')[0]
co=[m for m in cohort if m in cp and m in ap and m in gp]
out['Harvey LAB (Artificial Analysis run)']=dict(models=len(co),binary_range=[min(ap[m] for m in co)*100,max(ap[m] for m in co)*100],partial_range=[min(cp[m] for m in co)*100,max(cp[m] for m in co)*100],
    gated_range=[min(gp[m] for m in co)*100,max(gp[m] for m in co)*100],binary_vs_partial=conc(ap,cp,co)[0],binary_vs_gated=conc(ap,gp,co)[0],partial_vs_gated=conc(cp,gp,co)[0],
    binary_vs_other_legal=vs_others(ap,'Harvey LAB'),partial_vs_other_legal=vs_others(cp,'Harvey LAB'),gated_vs_other_legal=vs_others(gp,'Harvey LAB'))
# GDPx legal: binary and partial
g=json.load(open('raw/inventory/gdpx-legal.json'))
bins=[r['metrics'].get('binary_score_pct') for r in g['rows'] if r.get('metrics')]; parts=[r['metrics'].get('partial_score_pct') for r in g['rows'] if r.get('metrics')]
out['GDPx legal']=dict(models=len([x for x in bins if x is not None]),binary_range=[min(x for x in bins if x is not None),max(x for x in bins if x is not None)],partial_range=[min(x for x in parts if x is not None),max(x for x in parts if x is not None)])
for k,v in out.items():
    print('\n'+k); [print(f"   {a}: {np.round(b,1).tolist() if isinstance(b,list) else (round(b,1) if isinstance(b,float) else b)}") for a,b in v.items()]
# how often a task that met every rubric criterion still had a material made-up fact (Artificial Analysis' checker)
allc=[m for m in aa('harvey_lab_aa_v1_1','all_pass_rate_ungated')[0]]
ug=aa('harvey_lab_aa_v1_1','all_pass_rate_ungated')[0]; gg=aa('harvey_lab_aa_v1_1','hallucination_gated_all_pass_rate')[0]
both=[m for m in ug if m in gg and ug[m]>0]
out['made_up_fact_gate']=dict(models=len(both),share_of_rubric_perfect_removed=1-sum(gg[m] for m in both)/sum(ug[m] for m in both),
    models_lower_when_gated=sum(gg[m]<ug[m] for m in both))
print('\nmade-up-fact gate:',out['made_up_fact_gate'])
json.dump(out,open('data/binary_vs_partial.json','w'),indent=1,default=float)
