"""Is legal lower than EACH other field, not just coding? Paired bootstrap over models (same resample for both fields)."""
import sys,itertools,json,numpy as np
src=open('scripts/audit.py').read().split("rng=np.random.default_rng(7)")[0]
exec(src)
five=['Harvey LAB (Vals run)','Legal Research Bench (Vals)','Mercor APEX, corporate law','Legora BAR','Certera']
sets={f:[r[1] for r in rows if r[0]==f and r[6]] for f in ['science','coding','office work','finance']}
sets['legal (rule, 9)']=[r[1] for r in rows if r[0]=='legal' and r[6]]
def field(names,s):
    r=[]
    for a,b in itertools.combinations(names,2):
        ms=[m for m in s if m in T[a] and m in T[b]]
        if len(set(ms))<8: continue
        same=tot=0
        for i,j in itertools.combinations(range(len(ms)),2):
            da=T[a][ms[i]]-T[a][ms[j]]; db=T[b][ms[i]]-T[b][ms[j]]
            if da==0 or db==0: continue
            tot+=1; same+=(da>0)==(db>0)
        if tot: r.append(same/tot)
    return np.mean(r)*100 if r else np.nan
rng=np.random.default_rng(11); N=2000
res={k:[] for k in sets}; leg=[]
for _ in range(N):
    s=list(rng.choice(cohort,len(cohort)))
    leg.append(field(five,s))
    for k,n in sets.items(): res[k].append(field(n,s))
leg=np.array(leg); out={}
print(f"legal five: {field(five,cohort):.1f}  [{np.percentile(leg,2.5):.0f},{np.percentile(leg,97.5):.0f}]")
for k,v in res.items():
    v=np.array(v); d=v-leg; ok=~np.isnan(d); d=d[ok]
    pt=field(sets[k],cohort)-field(five,cohort)
    out[k]=dict(field=float(field(sets[k],cohort)),gap=float(pt),lo=float(np.percentile(d,2.5)),hi=float(np.percentile(d,97.5)),share_not_above=float((d<=0).mean()))
    print(f"{k:18} {field(sets[k],cohort):5.1f}  gap over legal five {pt:5.1f}  [{np.percentile(d,2.5):5.1f},{np.percentile(d,97.5):5.1f}]  field<=legal in {100*(d<=0).mean():.1f}% of resamples")
json.dump(out,open('data/field_gaps.json','w'),indent=1)
# top model per benchmark, per field
print()
for k,n in list(sets.items())+[('legal five',five)]:
    tops=[]
    for b in n:
        d={m:T[b][m] for m in cohort if m in T[b]}; tops.append(max(d,key=d.get))
    print(f"{k:18} {len(n)} benchmarks, {len(set(tops))} different top models: {tops}")
