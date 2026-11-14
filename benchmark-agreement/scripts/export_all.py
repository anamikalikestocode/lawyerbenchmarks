"""One markdown file with everything: the write-up, the final captions and slides, every score used and every pairing."""
import sys,itertools,json,numpy as np,shutil,os
src=open('scripts/audit.py').read().split("rng=np.random.default_rng(7)")[0]
exec(src)
R='/home/user/lawyerbenchmarks/benchmark-agreement'
five=['Harvey LAB (Vals run)','Legal Research Bench (Vals)','Mercor APEX, corporate law','Legora BAR','Certera']
F={'Legal (the five on the chart)':five}
for f in ['legal','science','coding','office work','finance','medicine','cyber']:
    F[{'legal':'Legal (all nine by the written rule)'}.get(f,f.capitalize())]=[r[1] for r in rows if r[0]==f and r[6]]
def conc(a,b):
    ms=[m for m in cohort if m in T[a] and m in T[b]]
    same=tot=0
    for i,j in itertools.combinations(ms,2):
        da=T[a][i]-T[a][j]; db=T[b][i]-T[b][j]
        if da==0 or db==0: continue
        tot+=1; same+=(da>0)==(db>0)
    return (same/tot*100 if tot else None),len(ms)
fmt=lambda v:'' if v is None else (f"{v:.3f}" if abs(v)<2 else f"{v:.1f}")
o=[]; w=o.append
w("# The Benchmark of Benchmarks: everything\n")
w("Compiled 14 November 2026 from the analysis files. Leaderboard data was collected 9 to 11 November 2026. The 37 models are the ones Vals ran on Harvey LAB between 19 October and 9 November 2026.\n")
w("## The two final charts\n")
w("![Slide 1: The Benchmark of Benchmarks](slide1-v2.png)\n")
w("![Slide 2: Legal Benchmarks](slide2-v2.png)\n")
w("## The final captions\n")
w("Post 1:\n\n```\ni benchmarked the benchmarks\n\nif you ask which AI model is better, different coding benchmarks agree 79% of the time vs 62% for legal (coin flip = 50%)\n\neach benchmark has its own standard for good answers but those vary more in law than other fields\n```\n")
w("Post 2:\n\n```\nhow much should you trust a legal benchmark? way less than a coding one\n\n- a few points up/down is largely arbitrary\n- if many benchmarks agree, the model is probably just stronger overall (not necessarily better at law)\n```\n")
w("## Headline numbers\n")
w("| Field | Agreement on which of two models is better | Benchmarks |\n|---|---|---|")
A=json.load(open('data/audit_fields.json')); C=json.load(open('data/concord.json'))
for k in ['science','coding','office work','finance']: w(f"| {k.capitalize()} | {A[k][0]:.1f}% ({A[k][1]:.0f} to {A[k][2]:.0f}) | {A[k][3]} |")
w(f"| Legal (five on the chart) | {C['legal'][1]*100:.1f}% ({C['legal_ci'][0]*100:.0f} to {C['legal_ci'][1]*100:.0f}) | 5 |")
w(f"| Legal (nine by the rule) | {A['legal'][0]:.1f}% ({A['legal'][1]:.0f} to {A['legal'][2]:.0f}) | 9 |\n")
w("A coin flip is 50%. Ranges are 95% intervals from resampling the models.\n")
w("---\n\n# Part 1. The full write-up\n")
w(open(R+'/README.md').read().replace('\n# ','\n## ',1).split('\n',1)[1])
w("\n---\n\n# Part 2. Every score used\n")
w("One score per model per benchmark, at the model's highest effort setting. Blank means the model is not on that leaderboard. Units differ by benchmark (percent, Elo, index), so compare down a column, not across.\n")
for name,bs in F.items():
    if name.startswith('Legal (the five'): continue
    w(f"### {name}\n"); w("| Model | "+" | ".join(bs)+" |"); w("|---|"+"---|"*len(bs))
    for m in sorted(cohort):
        if any(m in T[b] for b in bs): w(f"| {m} | "+" | ".join(fmt(T[b].get(m)) for b in bs)+" |")
    w("")
w("---\n\n# Part 3. Every pairing\n")
w("How often two benchmarks agree on which of two models is better, over the models they share. Pairings with fewer than 10 shared models are left out of the field averages.\n")
for name,bs in F.items():
    if name.startswith('Legal (the five'): continue
    w(f"### {name}\n"); w("| Benchmark A | Benchmark B | Shared models | Agree |\n|---|---|---|---|")
    for a,b in itertools.combinations(bs,2):
        v,n=conc(a,b); w(f"| {a} | {b} | {n} | {'' if v is None else f'{v:.1f}%'}{' (under 10 models, not counted)' if n<10 else ''} |")
    w("")
w("---\n\n# Part 4. Candidates considered and why each is in or out\n")
w("| Field | Benchmark | Publisher | Run by | Models of the 37 | Included | Reason if not |\n|---|---|---|---|---|---|---|")
for r in rows: w(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {'yes' if r[6] else 'no'} | {r[7]} |")
w("\n---\n\n# Part 5. The 37 models\n\n"+", ".join(sorted(cohort))+"\n")
w("# Part 6. Files\n\nThe analysis code is in `scripts/`, the result files in `data/`, and the lawyer pilot materials in `pilot/`. Raw downloaded leaderboards (about 400 MB) are not included.\n")
open(R+'/EVERYTHING.md','w').write('\n'.join(o)); print(len('\n'.join(o)),'chars')
