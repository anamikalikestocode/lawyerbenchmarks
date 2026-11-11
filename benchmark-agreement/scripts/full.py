import json,itertools,numpy as np,sys,re
sys.path.insert(0,'scripts')
from canon import canon
from master import T, pick
from scipy.stats import spearmanr
rng=np.random.default_rng(41)
FIX={'deepseek-4-1-flash':'deepseek-v4-1-flash','deepseek-v4p1-flash':'deepseek-v4-1-flash','gemini-flash-3-8':'gemini-3-8-flash','gemini-4-argon*':'gemini-4-argon','fable-5-1-adaptive':'fable-5-1','fable-5-adaptive':'fable-5','gpt-6-1-sol':'gpt-6-1-sol'}
def inv(f,metric):
    c=[]
    for r in json.load(open(f'raw/inventory/{f}.json'))['rows']:
        lab=r.get('model_id') or r['model_display_name']; k=canon(lab); k=FIX.get(k,k)
        e=(r.get('reasoning_setting') or '').lower(); e=next((x for x in ['max','xhigh','high','medium','low'] if x in e),None)
        c.append((k,e,r['metrics'].get(metric),lab))
    return pick(c)[0]
T=dict(T)
T['GDPx legal (SemiAnalysis)']=inv('gdpx-legal','partial_score_pct')
T['DAYJOB law (Surge)']=inv('surge-dayjob-law','score_pct')
T['Contract Workflows (legalbenchmarks.ai)']=inv('legalbenchmarks-contract-workflows','task_pass_rate_pct')
T['Data Extraction (legalbenchmarks.ai)']=inv('legalbenchmarks-data-extraction','task_pass_rate_pct')
T['PRBench legal (Scale)']=inv('scale-prbench-legal','score')
T['SnorkelLegal']=inv('snorkel-legal','pass_at_1_pct')
T['Certera (votes by legal professionals)']=inv('certera-legal-ai-leaderboard','elo_score')
T['LAB (Mercor run)']=inv('mercor-harvey-lab-leaderboard','pass_at_1_pct')
cohort=sorted(T['LAB (Vals run)'])
LEGAL=['LAB (Vals run)','Vals Legal Research','Vals Immigration','APEX-Agents corporate law (Mercor)','Legora BAR','GDPx legal (SemiAnalysis)','DAYJOB law (Surge)','Contract Workflows (legalbenchmarks.ai)','Data Extraction (legalbenchmarks.ai)','PRBench legal (Scale)','SnorkelLegal','Certera (votes by legal professionals)']
CODE=['Terminal-Bench 4 (Vals run)','Vibe Code (Vals)','FrontierCode 2 (AA)','SciCode (AA)']
def rho(a,b,ms,minn=10):
    ms=[m for m in ms if m in T[a] and m in T[b]]
    if len(set(ms))<minn: return None,len(set(ms))
    return spearmanr([T[a][m] for m in ms],[T[b][m] for m in ms])[0],len(ms)
def pairs(names,ms,minn=10): 
    return {(a,b):rho(a,b,ms,minn) for a,b in itertools.combinations(names,2)}
if __name__=='__main__':
    for k in LEGAL+['LAB (Mercor run)']: print(f"{k:42} cohort models {len([m for m in cohort if m in T[k]]):2}  top: {sorted([m for m in cohort if m in T[k]],key=lambda m:-T[k][m])[:2]}")
    P=pairs(LEGAL,cohort); C=pairs(CODE,cohort)
    ok={k:v for k,v in P.items() if v[0] is not None}
    rs=[v[0] for v in ok.values()]
    print(f"\nlegal: {len(LEGAL)} benchmarks, {len(ok)} of {len(P)} pairs with >=10 shared models; median {np.median(rs):.2f} mean {np.mean(rs):.2f} range {min(rs):.2f}..{max(rs):.2f}; IQR {np.percentile(rs,25):.2f}-{np.percentile(rs,75):.2f}")
    cr=[v[0] for v in C.values()]; print(f"coding: {len(cr)} pairs median {np.median(cr):.2f}")
    print('\nper legal benchmark: mean agreement with the other legal benchmarks')
    for k in LEGAL:
        v=[x[0] for (a,b),x in ok.items() if k in (a,b)]; print(f"  {k:42} {np.mean(v):.2f}  over {len(v)} pairs")
    print('\nsame benchmark, different evaluator:')
    for a,b in [('LAB (Vals run)','LAB (AA run, ungated)'),('LAB (Vals run)','LAB (Mercor run)'),('LAB (AA run, ungated)','LAB (Mercor run)'),('Terminal-Bench 4 (Vals run)','Terminal-Bench 4 (AA run)')]:
        r,n=rho(a,b,cohort); print(f"  {a:30} {b:30} n={n} rho={r:.2f}")
    # bootstrap over models
    med=lambda PP:np.nanmedian([v[0] for v in PP.values() if v[0] is not None])
    ml=[];mc=[];d=[]
    for _ in range(1500):
        s=list(rng.choice(cohort,len(cohort))); a=med(pairs(LEGAL,s,8)); b=med(pairs(CODE,s,8)); ml.append(a); mc.append(b); d.append(b-a)
    print('\nlegal median %.2f [%.2f,%.2f]  coding median %.2f [%.2f,%.2f]  diff %.2f [%.2f,%.2f]  P(coding<=legal)=%.4f'%(med(P),*np.nanpercentile(ml,[2.5,97.5]),med(C),*np.nanpercentile(mc,[2.5,97.5]),med(C)-med(P),*np.nanpercentile(d,[2.5,97.5]),(np.array(d)<=0).mean()))
    print('\nall legal pairs:')
    for (a,b),(r,n) in sorted(ok.items(),key=lambda kv:-kv[1][0]): print(f"  {a[:34]:35} {b[:34]:35} n={n:2} {r:+.2f}")
    json.dump({'T':T,'LEGAL':LEGAL,'CODE':CODE,'cohort':cohort},open('data/full.json','w'),indent=1)
