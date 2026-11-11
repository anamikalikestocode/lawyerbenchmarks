"""Inclusion audit: one written rule, applied the same way to every field, compared with the hand-picked sets."""
import sys,io,contextlib,json,glob,os,itertools,numpy as np
sys.path.insert(0,'scripts')
with contextlib.redirect_stdout(io.StringIO()):
    from full import cohort
    from master import vals,aa,other,pick
    from full import inv
    from canon import canon
MIN=15
rows=[]   # (field, name, publisher, runner, cohort_n, table, include, reason)
def cov(d): return len([m for m in cohort if m in d])
# ---- Vals: every benchmark page ----
VM={os.path.basename(p)[:-5]:json.load(open(p))['metadata'] for p in glob.glob('raw/vals_views/*.json')}
fam={}
for s,m in VM.items(): fam.setdefault(m['family'],[]).append((str(m.get('updated')),s))
latest={f:max(v)[1] for f,v in fam.items()}
FIELD={'legal':'legal','coding':'coding','finance':'finance','healthcare':'medicine','science':'science','math':'maths','academic':'general knowledge','cyber':'cyber'}
for s,m in sorted(VM.items()):
    d=vals(s)[0]; n=cov(d); ind=m.get('industry'); f=FIELD.get(ind)
    name={'hlab':'Harvey LAB (Vals run)'}.get(s,m['benchmark']+' (Vals)')
    if f is None: inc,why=False,f"Vals files it under '{ind}', not one of the fields"
    elif latest[m['family']]!=s: inc,why=False,'older version of a benchmark already listed'
    elif n<MIN: inc,why=False,f'only {n} of the 37 models'
    else: inc,why=True,''
    rows.append([f or ind,name,'Harvey' if s=='hlab' else 'Vals','Vals',n,d,inc,why])
def add(field,name,pub,runner,d,inc=None,why=''):
    n=cov(d)
    if inc is None: inc,why=(n>=MIN),('' if n>=MIN else f'only {n} of the 37 models')
    rows.append([field,name,pub,runner,n,d,inc,why])
# ---- Artificial Analysis ----
add('legal','Harvey LAB (AA run)','Harvey','Artificial Analysis',aa('harvey_lab_aa_v1_1','hallucination_gated_all_pass_rate')[0],False,'second run of a benchmark already listed')
add('legal','GDP.pdf legal slice (AA)','Artificial Analysis','Artificial Analysis',aa('gdp_pdf',None,('mean_pass_by_domain','Legal'))[0],False,'a breakdown inside a general benchmark, not its own leaderboard')
add('legal','Omniscience law slice (AA)','Artificial Analysis','Artificial Analysis',aa('aa_omniscience',None,('net_score_by_domain','Law'))[0],False,'a breakdown inside a general benchmark, not its own leaderboard')
add('coding','FrontierCode 2 (AA)','Artificial Analysis','Artificial Analysis',aa('frontiercode_2_0','score')[0])
add('coding','SciCode (AA)','academic','Artificial Analysis',aa('scicode','score')[0])
add('coding','Terminal-Bench 4 (AA run)','Terminal-Bench','Artificial Analysis',aa('terminal_bench_4_0','score')[0],False,'second run of a benchmark already listed')
add('coding','FrontierCode 1.1 (AA)','Artificial Analysis','Artificial Analysis',aa('frontiercode_1_1','score')[0],False,'older version of a benchmark already listed')
add('coding','Terminal-Bench 2.1 (AA run)','Terminal-Bench','Artificial Analysis',aa('terminal_bench_2_1','score')[0],False,'older version of a benchmark already listed')
add('coding','Terminal-Bench Hard (AA)','Artificial Analysis','Artificial Analysis',aa('terminal_bench_hard','score')[0])
add('science','Terminal-Bench Science (AA run)','Terminal-Bench','Artificial Analysis',aa('terminal_bench_science_0_1','score')[0],False,'second run of a benchmark already listed')
add('office work','GDPval-AA','Artificial Analysis','Artificial Analysis',aa('gdpval_aa','elo')[0])
add('office work','AA-Briefcase','Artificial Analysis','Artificial Analysis',aa('aa_briefcase','elo')[0])
add('office work','AutomationBench-AA','Artificial Analysis','Artificial Analysis',aa('automationbench_aa','score')[0])
add('office work','GDP.pdf (AA)','Artificial Analysis','Artificial Analysis',aa('gdp_pdf','all_pass')[0])
add('general knowledge','AA-Omniscience','Artificial Analysis','Artificial Analysis',aa('aa_omniscience','net_score')[0])
# ---- others ----
add('legal','Mercor APEX, corporate law','Mercor','Mercor',other('mercor_apex_agents','law_mean_score_pct')[0])
add('office work','Mercor APEX-Agents, overall','Mercor','Mercor',other('mercor_apex_agents','overall_mean_score_pct')[0])
add('legal','Legora BAR','Legora','Legora',other('legora_bar_2026-10','quality_rel_index')[0])
add('legal','Certera','Certera','Certera',inv('certera-legal-ai-leaderboard','elo_score'))
add('legal','GDPx legal (SemiAnalysis)','SemiAnalysis','SemiAnalysis',inv('gdpx-legal','partial_score_pct'))
add('legal','Contract Workflows (legalbenchmarks.ai)','legalbenchmarks.ai','legalbenchmarks.ai',inv('legalbenchmarks-contract-workflows','task_pass_rate_pct'))
add('legal','Data Extraction (legalbenchmarks.ai)','legalbenchmarks.ai','legalbenchmarks.ai',inv('legalbenchmarks-data-extraction','task_pass_rate_pct'))
add('legal','DAYJOB law (Surge)','Surge','Fireworks copy',inv('surge-dayjob-law','score_pct'))
add('legal','SnorkelLegal','Snorkel','Snorkel',inv('snorkel-legal','pass_at_1_pct'))
add('legal','PRBench legal (Scale)','Scale','Scale',inv('scale-prbench-legal','score'))
add('legal','Harvey LAB (Mercor run)','Harvey','Mercor',inv('mercor-harvey-lab-leaderboard','pass_at_1_pct'),False,'second run of a benchmark already listed')
add('legal','Dutch legal research DELTA','legalbenchmarks.ai','legalbenchmarks.ai',inv('legalbenchmarks-delta','task_pass_rate_pct'))
add('legal','CorporateBench (Epiq)','Epiq','Fireworks',inv('epiq-corporatebench','score_pct'))
T={r[1]:r[5] for r in rows}
def pairs(names,minn=10):
    out=[]
    for a,b in itertools.combinations(names,2):
        ms=[m for m in cohort if m in T[a] and m in T[b]]
        if len(ms)<minn: continue
        same=tot=0
        for i,j in itertools.combinations(ms,2):
            da=T[a][i]-T[a][j]; db=T[b][i]-T[b][j]
            if da==0 or db==0: continue
            tot+=1; same+=(da>0)==(db>0)
        out.append((a,b,same/tot,len(ms)))
    return out
rng=np.random.default_rng(7)
def boot(names,n=400):
    v=[]
    for _ in range(n):
        s=list(rng.choice(cohort,len(cohort))); r=[]
        for a,b in itertools.combinations(names,2):
            ms=[m for m in s if m in T[a] and m in T[b]]
            if len(set(ms))<8: continue
            same=tot=0
            for i,j in itertools.combinations(range(len(ms)),2):
                da=T[a][ms[i]]-T[a][ms[j]]; db=T[b][ms[i]]-T[b][ms[j]]
                if da==0 or db==0: continue
                tot+=1; same+=(da>0)==(db>0)
            if tot: r.append(same/tot)
        if r: v.append(np.mean(r))
    return np.percentile(v,[2.5,97.5])*100
out=[]
out.append('=== LEGAL candidates ===')
for r in sorted([r for r in rows if r[0]=='legal'],key=lambda r:(-r[6],-r[4])): out.append(f"  {'IN ' if r[6] else 'out'} {r[1]:42} run by {r[3]:20} {r[4]:2}/37  {r[7]}")
res={}
out.append('\n=== By the written rule, every field ===')
for f in ['science','coding','medicine','office work','finance','maths','cyber','general knowledge','legal']:
    inc=[r for r in rows if r[0]==f and r[6]]; names=[r[1] for r in inc]; P=pairs(names)
    if not P: out.append(f"{f:18} {len(names)} benchmarks: no pairing with 10+ shared models"); continue
    m=np.mean([p[2] for p in P])*100; lo,hi=boot(names) if len(P)>1 or True else (0,0)
    runners=sorted(set(r[3] for r in inc)); res[f]=(m,lo,hi,len(names),len(P),names)
    out.append(f"{f:18} {len(names)} benchmarks, {len(P):2} pairings: {m:5.1f}% [{lo:.0f},{hi:.0f}]  run by: {', '.join(runners)}")
    out.append('      '+'; '.join(f"{r[1]} ({r[4]})" for r in inc))
    ex=[r for r in rows if r[0]==f and not r[6]]
    if f!='legal': out.append('      left out: '+'; '.join(f"{r[1]} [{r[7]}]" for r in ex))
out.append('\n=== Legal under different inclusion choices ===')
VAR=[]
def L(label,names): 
    P=pairs(names); lo,hi=boot(names); VAR.append([label,len(names),len(P),float(np.mean([p[2] for p in P])*100),float(lo),float(hi)]); out.append(f"  {label:58} {len(names)} benchmarks, {len(P):2} pairings: {np.mean([p[2] for p in P])*100:5.1f}% [{lo:.0f},{hi:.0f}]")
rule=[r[1] for r in rows if r[0]=='legal' and r[6]]
five=['Harvey LAB (Vals run)','Legal Research Bench (Vals)','Mercor APEX, corporate law','Legora BAR','Certera']
L('written rule (15+ models, own leaderboard, one run each)',rule)
L('your hand-picked five',five)
L('rule, minimum 10 models instead of 15',[r[1] for r in rows if r[0]=='legal' and (r[6] or (r[7].startswith('only') and r[4]>=10))])
L('rule, minimum 20 models',[n for n in rule if cov(T[n])>=20])
L('rule, one benchmark per publisher',[n for n in rule if n not in ('Immigration (Vals)','Data Extraction (legalbenchmarks.ai)')])
L('rule, plus the two slices from Artificial Analysis',rule+['GDP.pdf legal slice (AA)','Omniscience law slice (AA)'])
L('rule, task benchmarks only (no Certera votes)',[n for n in rule if n!='Certera'])
L('only benchmarks run by an independent evaluator or vote',[n for n in rule if n in ('Harvey LAB (Vals run)','Legal Research Bench (Vals)','Immigration (Vals)','Certera','GDPx legal (SemiAnalysis)','Contract Workflows (legalbenchmarks.ai)','Data Extraction (legalbenchmarks.ai)')])
sys.stderr.write('\n'.join(out)+'\n'); json.dump({k:[float(x) for x in v[:3]]+[v[3],v[4],v[5]] for k,v in res.items()},open('data/audit_fields.json','w'),indent=1)
json.dump([[r[0],r[1],r[2],r[3],r[4],r[6],r[7]] for r in rows],open('data/audit_candidates.json','w'),indent=1)
json.dump(VAR,open('data/audit_legal_variants.json','w'),indent=1)
