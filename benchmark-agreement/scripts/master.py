import json, itertools, numpy as np, sys
sys.path.insert(0,'scripts')
from canon import canon
from scipy.stats import spearmanr
rng=np.random.default_rng(11)
ORDER={'max':5,'xhigh':4,'high':3,'medium':2,'low':1,'auto':0,None:3,'None':3}
KEEP_DISTINCT={'tencent/hy4-preview':'hy4-preview'}
UNCERTAIN={'mistral-large-4','deepseek-v4-1-flash','qwen-3-8','hy4'}   # label matches that may not be the identical checkpoint across sources
def pick(cands):
    """cands: list of (canon_key, effort, value, raw_label). Keep one row per model: highest effort, then dated/explicit label."""
    out={}
    for k,e,v,raw in cands:
        if v is None: continue
        score=(ORDER.get(e,3), 1 if any(ch.isdigit() for ch in raw[-4:]) else 0)
        if k not in out or score>out[k][0]: out[k]=(score,v,raw)
    return {k:v[1] for k,v in out.items()}, {k:v[2] for k,v in out.items()}
def vals(slug,task='overall'):
    t=json.load(open(f'raw/vals_views/{slug}.json'))['tasks'][task]; c=[]
    for m,v in t.items():
        if m.startswith('decision/') or any(x in m for x in ['-range','-parallel','-exa']): continue
        k=KEEP_DISTINCT.get(m,canon(m)); e=v.get('compute_effort') or v.get('reasoning_effort')
        # prefer the variant Vals itself ran on LAB (internal/dated ids)
        c.append((k,e if e in ORDER else None,v.get('accuracy'),m))
    return pick(c)
def aa(f,metric,sub=None):
    c=[]
    for r in json.load(open(f'raw/aa/{f}.json'))['rows']:
        if sub:
            v=(r.get('breakdowns') or {})
            for s in sub: v=v.get(s) if isinstance(v,dict) else None
        else: v=r['metrics'].get(metric)
        c.append((canon(r['aa_model_slug']),r.get('reasoning_setting'),v,r['aa_model_slug']))
    return pick(c)
def other(f,metric):
    c=[]
    for r in json.load(open(f'raw/other/{f}.json'))['rows']:
        c.append((canon(r.get('model_id') or r['model_display_name']),r.get('reasoning_setting'),r['metrics'].get(metric),r.get('model_id') or r['model_display_name']))
    return pick(c)
COLS={
 'LAB (Vals run)':vals('hlab'), 'LAB (AA run, ungated)':aa('harvey_lab_aa_v1_1','all_pass_rate_ungated'), 'LAB (AA run, hallucination-gated)':aa('harvey_lab_aa_v1_1','hallucination_gated_all_pass_rate'),
 'Vals Legal Research':vals('legal_research'), 'Vals Immigration':vals('immigration'),
 'APEX-Agents corporate law (Mercor)':other('mercor_apex_agents','law_mean_score_pct'), 'Legora BAR':other('legora_bar_2026-10','quality_rel_index'),
 'GDP.pdf legal slice (AA)':aa('gdp_pdf',None,('mean_pass_by_domain','Legal')), 'Omniscience law slice (AA)':aa('aa_omniscience',None,('net_score_by_domain','Law')),
 'LegalBench (Vals)':vals('legal_bench'),
 # coding reference
 'Terminal-Bench 4 (Vals run)':vals('terminal-bench-4'), 'Terminal-Bench 4 (AA run)':aa('terminal_bench_4_0','score'), 'Vibe Code (Vals)':vals('vibe-code'), 'FrontierCode 2 (AA)':aa('frontiercode_2_0','score'), 'SciCode (AA)':aa('scicode','score'),
}
T={k:v[0] for k,v in COLS.items()}; RAW={k:v[1] for k,v in COLS.items()}
def pair(a,b,drop_uncertain=False,nboot=3000):
    ms=sorted(set(T[a])&set(T[b]))
    if drop_uncertain: ms=[m for m in ms if m not in UNCERTAIN]
    n=len(ms)
    if n<10: return None
    x=np.array([T[a][m] for m in ms],float); y=np.array([T[b][m] for m in ms],float)
    bs=[spearmanr(x[i],y[i])[0] for i in (rng.integers(0,n,n) for _ in range(nboot))]
    return dict(n=n,rho=float(spearmanr(x,y)[0]),lo=float(np.nanpercentile(bs,2.5)),hi=float(np.nanpercentile(bs,97.5)),models=ms)
if __name__=='__main__':
    for k in T: print(f"{k:38} models: {len(T[k])}")
    legal=list(COLS)[:10]; code=list(COLS)[10:]
    print('\n--- legal vs legal ---')
    res={}
    for a,b in itertools.combinations(legal,2):
        p=pair(a,b); q=pair(a,b,True)
        if p:
            res[f'{a}|{b}']=p
            print(f"{a:36} | {b:36} n={p['n']:2} rho={p['rho']:+.2f} [{p['lo']:+.2f},{p['hi']:+.2f}]   (excluding uncertain name matches: {('%+.2f n=%d'%(q['rho'],q['n'])) if q else 'n<10'})")
    print('\n--- coding vs coding ---')
    for a,b in itertools.combinations(code,2):
        p=pair(a,b)
        if p: res[f'{a}|{b}']=p; print(f"{a:36} | {b:36} n={p['n']:2} rho={p['rho']:+.2f} [{p['lo']:+.2f},{p['hi']:+.2f}]")
    json.dump({'T':T,'RAW':RAW,'pairs':res},open('data/master.json','w'),indent=1)
