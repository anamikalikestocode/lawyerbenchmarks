"""Do different kinds of legal task reorder models when the standard is held fixed?
Test inside single benchmarks (one author, one grading scheme, one setup), then compare with agreement across benchmarks."""
import json,itertools,numpy as np,sys
rng=np.random.default_rng(13)
def conc(x,y):
    s=t=0
    for i,j in itertools.combinations(range(len(x)),2):
        a=x[i]-x[j]; b=y[i]-y[j]
        if a==0 or b==0: continue
        t+=1; s+=(a>0)==(b>0)
    return s/t if t else None
out=[]
# ---------- 1. Legora BAR: seven task families, one standard, one product harness, 17 models ----------
L=json.load(open('raw/other/legora_bar_2026-10.json'))['rows']
fams=['analyse_answer','compare','draft','edit','extract','review','summarise']
X={f:[r['metrics'].get(f'quality_{f}_rel_index') for r in L] for f in fams}
ok=[i for i in range(len(L)) if all(X[f][i] is not None for f in fams)]
v=[]
for a,b in itertools.combinations(fams,2):
    c=conc([X[a][i] for i in ok],[X[b][i] for i in ok]); v.append(c)
out.append(f"1. Legora BAR, {len(ok)} models: its 7 task families (draft, review, extract, ...) agree with each other {np.mean(v)*100:.0f}% of the time on average (range {min(v)*100:.0f}-{max(v)*100:.0f}, 21 pairings)")
d={(a,b):conc([X[a][i] for i in ok],[X[b][i] for i in ok]) for a,b in itertools.combinations(fams,2)}
out.append('      draft vs review %.0f, draft vs extract %.0f, draft vs summarise %.0f, review vs extract %.0f'%(d[('draft','review')]*100,d[('draft','extract')]*100,d[('draft','summarise')]*100,d[('extract','review')]*100))
for a,b in [('short','medium'),('short','long'),('medium','long')]:
    xa=[r['metrics'].get(f'quality_{a}_rel_index') for r in L]; xb=[r['metrics'].get(f'quality_{b}_rel_index') for r in L]
    out.append(f"      difficulty tiers {a} vs {b}: {conc(xa,xb)*100:.0f}%")
# ---------- 2. within one Vals benchmark: split its sub-areas into halves ----------
def split_test(slug,keys,label,groups=None,models=None):
    T=json.load(open(f'raw/vals_views/{slug}.json'))['tasks']
    ms=[m for m in T['overall'] if all(m in T[k] and T[k][m].get('accuracy') is not None for k in keys)]
    if models: ms=[m for m in ms if m in models]
    M=np.array([[T[k][m]['accuracy'] for k in keys] for m in ms]); S=np.array([[T[k][m].get('stderr') or 0 for k in keys] for m in ms])
    n=len(keys); r=[]
    for _ in range(1500):
        p=rng.permutation(n); a,b=p[:n//2],p[n//2:2*(n//2)]
        r.append(conc(M[:,a].mean(1),M[:,b].mean(1)))
    s=f"   {label}: {len(ms)} models, {n} sub-areas. random halves agree {np.mean(r)*100:.0f}% (middle 90%: {np.percentile(r,5)*100:.0f}-{np.percentile(r,95)*100:.0f})"
    if groups:
        ia=[keys.index(k) for k in groups[0] if k in keys]; ib=[keys.index(k) for k in groups[1] if k in keys]
        g=conc(M[:,ia].mean(1),M[:,ib].mean(1)); pct=(np.array(r)<=g).mean()*100
        s+=f" | split by kind of work ({len(ia)} vs {len(ib)}): {g*100:.0f}% (higher than {pct:.0f}% of random splits)"
    out.append(s); return ms
cohort=sorted(json.load(open('raw/vals_views/hlab.json'))['tasks']['overall'])
H=json.load(open('raw/vals_views/hlab.json'))['tasks']
areas=[k for k in H if k.startswith('criteria_pass_rate__')]
deal=['banking_finance','capital_markets','corporate_governance','corporate_ma','emerging_companies_venture_capital','funds_asset_management','real_estate','structured_finance_securitization','tax','trusts_estates_private_client','energy_natural_resources','insurance']
disp=['antitrust_competition','arbitration_international_dispute_resolution','bankruptcy_restructuring','litigation_dispute_resolution','white_collar_defense_investigations','employment_labor','data_privacy_cybersecurity','environmental_esg','healthcare_life_sciences','immigration','intellectual_property','international_trade_sanctions']
out.append('\n2. Inside one benchmark (same author, same grading, same setup)')
split_test('hlab',areas,'Harvey LAB, criteria pass by practice area',(['criteria_pass_rate__'+k for k in deal],['criteria_pass_rate__'+k for k in disp]))
split_test('hlab',[k for k in H if k not in ('overall','criteria_pass_rate') and not k.startswith('criteria_')],'Harvey LAB, all-pass by practice area',(deal,disp))
R=json.load(open('raw/vals_views/legal_research.json'))['tasks']; rk=[k for k in R if k!='overall']
out.append('   Legal Research sub-areas: '+', '.join(rk))
split_test('legal_research',rk,'Vals Legal Research by area of law',models=set(cohort))
TB=json.load(open('raw/vals_views/terminal-bench-4.json'))['tasks']; tk=[k for k in TB if k!='overall']
out.append('   Terminal-Bench 4 categories: '+', '.join(tk))
split_test('terminal-bench-4',tk,'Terminal-Bench 4 by category (coding)',models=set(cohort))
FA=json.load(open('raw/vals_views/fabv2-1.json'))['tasks']; fk=[k for k in FA if k not in ('overall','all_pass')]
split_test('fabv2-1',fk,'Finance Agent by question type (finance)',models=set(cohort))
sys.stderr.write('\n'.join(out)+'\n')
