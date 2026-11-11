"""How much does a lead on one benchmark hold up on another, by the size of the lead?
For every ordered pair of benchmarks (A,B) in a field, model pairs are split into thirds by the size of their gap on A
(closest, middle, widest); the figure is how often B puts the same model ahead. Also: rubric benchmarks against lawyer votes."""
import sys,itertools,json,numpy as np
src=open('scripts/audit.py').read().split("rng=np.random.default_rng(7)")[0]
exec(src)
five=['Harvey LAB (Vals run)','Legal Research Bench (Vals)','Mercor APEX, corporate law','Legora BAR','Certera']
S={'legal (hand-picked five)':five}
for f in ['legal','science','coding','office work','finance']: S['legal (written rule)' if f=='legal' else f]=[r[1] for r in rows if r[0]==f and r[6]]
def by_gap(names,s,qs=(1/3,2/3),minn=8):
    res=[[] for _ in range(len(qs)+1)]
    for a,b in itertools.permutations(names,2):
        ms=[m for m in s if m in T[a] and m in T[b]]
        if len(set(ms))<minn: continue
        g=[];ok=[]
        for i,j in itertools.combinations(range(len(ms)),2):
            da=T[a][ms[i]]-T[a][ms[j]]; db=T[b][ms[i]]-T[b][ms[j]]
            if da==0 or db==0: continue
            g.append(abs(da)); ok.append((da>0)==(db>0))
        if len(g)<9: continue
        g=np.array(g); ok=np.array(ok); cut=[-1]+list(np.quantile(g,qs))+[np.inf]
        for k in range(len(cut)-1):
            mask=(g>cut[k])&(g<=cut[k+1])
            if mask.sum(): res[k].append(ok[mask].mean())
    return [float(np.mean(r)*100) if r else float('nan') for r in res]
rng=np.random.default_rng(5); N=500; out={'fields':{}}
for lab,names in S.items():
    pt=by_gap(names,cohort,minn=10); bs=np.array([by_gap(names,list(rng.choice(cohort,len(cohort)))) for _ in range(N)])
    lo,hi=np.nanpercentile(bs,[2.5,97.5],axis=0)
    out['fields'][lab]=dict(n=len(names),thirds=pt,lo=[float(x) for x in lo],hi=[float(x) for x in hi],widest_tenth=by_gap(names,cohort,qs=(.9,),minn=10)[1])
    print(f"{lab:26} closest {pt[0]:.0f}% [{lo[0]:.0f},{hi[0]:.0f}]   middle {pt[1]:.0f}% [{lo[1]:.0f},{hi[1]:.0f}]   widest {pt[2]:.0f}% [{lo[2]:.0f},{hi[2]:.0f}]   widest tenth {out['fields'][lab]['widest_tenth']:.0f}%")
loo=[by_gap([x for x in five if x!=n],cohort,minn=10)[2] for n in five]; out['legal_five_leave_one_out_widest']=[float(min(loo)),float(max(loo))]
print('legal five, widest third, leaving one benchmark out:',[round(x) for x in loo])
out['points']={}
for n in ['Harvey LAB (Vals run)','Legal Research Bench (Vals)','Mercor APEX, corporate law']:
    ms=[m for m in cohort if m in T[n]]; g=np.array([abs(T[n][i]-T[n][j]) for i,j in itertools.combinations(ms,2)])
    q1,q2=np.quantile(g,[1/3,2/3]); out['points'][n]=dict(models=len(ms),closest_under=float(q1),widest_over=float(q2))
    print(f"   {n:30} closest third = gaps under {q1:.1f} points, widest third = gaps over {q2:.1f}")
rub=five[:4]
def pairmean(pairs,s):
    r=[]
    for a,b in pairs:
        ms=[m for m in s if m in T[a] and m in T[b]]
        if len(set(ms))<8: continue
        same=tot=0
        for i,j in itertools.combinations(range(len(ms)),2):
            da=T[a][ms[i]]-T[a][ms[j]]; db=T[b][ms[i]]-T[b][ms[j]]
            if da==0 or db==0: continue
            tot+=1; same+=(da>0)==(db>0)
        if tot: r.append(same/tot)
    return np.mean(r)*100 if r else np.nan
RR=list(itertools.combinations(rub,2)); RC=[(a,'Certera') for a in rub]
d=np.array([(lambda s:pairmean(RR,s)-pairmean(RC,s))(list(rng.choice(cohort,len(cohort)))) for _ in range(2000)]); d=d[~np.isnan(d)]
rr,rc=pairmean(RR,cohort),pairmean(RC,cohort)
out['rubric_vs_votes']=dict(rubric_rubric=float(rr),rubric_votes=float(rc),diff=float(rr-rc),lo=float(np.percentile(d,2.5)),hi=float(np.percentile(d,97.5)))
print(f"rubric vs rubric {rr:.1f}, rubric vs lawyer votes {rc:.1f}, difference {rr-rc:.1f} [{np.percentile(d,2.5):.1f},{np.percentile(d,97.5):.1f}]")
json.dump(out,open('data/gap_size.json','w'),indent=1)
