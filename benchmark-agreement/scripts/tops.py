"""Top model on each legal and coding leaderboard: on the full public leaderboard, and like-for-like
(only the models that appear on every leaderboard in the set), with where each leader ranks on the others."""
import sys,itertools,json,numpy as np
src=open('scripts/audit.py').read().split("rng=np.random.default_rng(7)")[0]
exec(src)
five=['Harvey LAB (Vals run)','Legal Research Bench (Vals)','Mercor APEX, corporate law','Legora BAR','Certera']
coding=[r[1] for r in rows if r[0]=='coding' and r[6]]
def full(n):
    d=T[n]; mx=max(d.values()); t=sorted(m for m,v in d.items() if v==mx)
    return dict(top=t,score=float(mx),models=len(d))
UNCERTAIN={'mistral-large-4','qwen-3-8','hy4','deepseek-v4-1-flash'}   # names matched across publishers with less certainty (same set as master.py)
def like_for_like(names):
    common=sorted(m for m in set(T[names[0]]) if all(m in T[n] for n in names) and m not in UNCERTAIN)
    rk=lambda n,m:1+sum(T[n][x]>T[n][m] for x in common)
    lead={n:sorted(m for m in common if rk(n,m)==1) for n in names}
    leaders=sorted(set(m for v in lead.values() for m in v))
    ranks={m:{n:rk(n,m) for n in names} for m in common}
    third=len(common)-len(common)//3   # ranks above this are the bottom third
    worst={m:max(ranks[m].values()) for m in leaders}
    return dict(common=common,n=len(common),leaders_by_benchmark=lead,distinct_leaders=len(leaders),ranks=ranks,leaders_worst_rank=worst,
                bottom_third_from=third+1,
                leaders_in_bottom_third_somewhere={m:[n for n in names if ranks[m][n]>third] for m in leaders})
out={'legal':{n:full(n) for n in five},'coding':{n:full(n) for n in coding}}
out['legal_missing']={m:[n for n in five if m not in T[n]] for m in sorted(set(x for v in out['legal'].values() for x in v['top']))}
out['legal_like_for_like']=like_for_like(five); out['coding_like_for_like']=like_for_like(coding)
c8=[n for n in coding if '1-100' not in n]; out['coding8_like_for_like']=like_for_like(c8)
for k in ['legal','coding']:
    v=out[k]; allt=[m for x in v.values() for m in x['top']]; cnt={m:sum(m in x['top'] for x in v.values()) for m in set(allt)}
    out[k+'_summary']=dict(benchmarks=len(v),distinct_top_models=len(set(allt)),most=max(cnt.values()),most_model=max(cnt,key=cnt.get),ties=sum(len(x['top'])>1 for x in v.values()))
mer=json.load(open('raw/other/mercor_apex_agents.json')); rd={canon(r['model_display_name']):r.get('release_date') for r in mer['rows']}
cer=json.load(open('raw/inventory/certera-legal-ai-leaderboard.json')); cs={canon(r['model_display_name']):r['metrics'] for r in cer['rows']}
keep=sorted(set(out['legal_like_for_like']['leaders_in_bottom_third_somewhere'])|{'gemini-4-carbon','fable-5-2','muse-ember'})
out['release_dates']={m:rd.get(m) for m in keep}
out['certera_rank_spread']={m:cs[m].get('rank_spread') for m in keep if m in cs}; out['certera_models']=len(cer['rows'])
json.dump(out,open('data/tops.json','w'),indent=1)
for k,names in [('legal_like_for_like',five),('coding_like_for_like',coding),('coding8_like_for_like',c8)]:
    L=out[k]; print(f"\n{k}: {L['n']} models on every leaderboard; {L['distinct_leaders']} different leaders; bottom third starts at rank {L['bottom_third_from']}")
    for n in names: print(f"   {n:32} leader: {L['leaders_by_benchmark'][n]}")
    for m,b in L['leaders_in_bottom_third_somewhere'].items(): print(f"   {m:20} ranks: {[L['ranks'][m][n] for n in names]}  worst: {L['leaders_worst_rank'][m]} of {L['n']}")
print('\nlegal leaders missing from:',out['legal_missing'])
