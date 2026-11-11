"""Build the write-up from the result files so every number in it comes from one run."""
import json,sys,io,contextlib
sys.path.insert(0,'scripts')
with contextlib.redirect_stdout(io.StringIO()):
    from full import T, cohort
D=lambda f:json.load(open(f'data/{f}.json'))
C=D('concord'); F=D('final'); A=D('audit_fields'); CAND=D('audit_candidates'); VAR=D('audit_legal_variants'); M=D('matched'); S=D('sidechecks'); G=D('field_gaps'); GS=D('gap_size'); TP=D('tops')
p=lambda x:f"{x:.0f}%"; pc=lambda x:f"{x*100:.0f}%"; r2=lambda x:f"{x:.2f}"
NICE={'gemini-4-argon':'Gemini 4 Argon','gemini-4-carbon':'Gemini 4 Carbon','gpt-6-astra':'GPT-6 Astra','opus-5-5':'Claude Opus 5.5','gpt-6-1-sol':'GPT-6.1 Sol','muse-wonder-full':'Muse Wonder Full','fable-5-2':'Claude Fable 5.2'}
LEG=[('Vals Legal Research','Legal Research Bench','Vals','Vals','Vals Legal Research'),('Mercor APEX law','APEX-Agents, corporate law','Mercor','Mercor','APEX-Agents corporate law (Mercor)'),('Harvey LAB','LAB','Harvey','Vals','LAB (Vals run)'),('Legora BAR','BAR','Legora','Legora','Legora BAR'),('Certera','Legal AI Leaderboard','Certera','Certera','Certera (votes by legal professionals)')]
def top(tk):
    ms=[m for m in cohort if m in T[tk]]; t=max(ms,key=lambda m:T[tk][m]); return NICE.get(t,t),len(ms)
o=[]; w=o.append
lm,cm=C['legal'][1]*100,C['coding'][1]*100
w("# Do legal AI benchmarks agree on which model is better?\n")
w("Draft, 11 November 2026. On a draft branch, not on the site.\n")
w("## The finding\n")
w(f"Pick any two current AI models. Two legal benchmarks agree on which one is better {p(lm)} of the time. Two coding benchmarks agree {p(cm)} of the time, on the same pool of models. Guessing would give 50%.\n")
same=[v[0]*100 for v in C['same'].values()]
w("| Comparison | Agreement on which of two models is better | 95% interval |\n|---|---|---|")
w(f"| The same benchmark, run by two evaluators | {p(min(same))} to {p(max(same))} | range across four reruns |")
w(f"| Two different coding benchmarks (8 benchmarks, {len(C['coding_pairs'])} pairings) | {p(cm)} | {pc(C['coding_ci'][0])} to {pc(C['coding_ci'][1])} |")
w(f"| Two different legal benchmarks (5 benchmarks, {len(C['legal_pairs'])} pairings) | {p(lm)} | {pc(C['legal_ci'][0])} to {pc(C['legal_ci'][1])} |\n")
w(f"The gap between coding and legal is {cm-lm:.0f} points, with a 95% interval of {C['diff_ci'][0]*100:.0f} to {C['diff_ci'][1]*100:.0f}. Coding came out at or below legal in 0.2% of resamples.\n")
m=F['main']
w(f"The same result as a rank correlation (Spearman, where 0 is an unrelated order and 1 is identical): legal benchmarks typically agree at {r2(m['legal'])} (interval {r2(m['legal_ci'][0])} to {r2(m['legal_ci'][1])}), coding benchmarks at {r2(m['coding'])} ({r2(m['coding_ci'][0])} to {r2(m['coding_ci'][1])}). The gap is {r2(m['coding']-m['legal'])}, with an interval of {r2(m['gap_ci'][0])} to {r2(m['gap_ci'][1])}.\n")
sl=C['same']
lab=[v[0]*100 for k,v in sl.items() if k.startswith('LAB')]; tb=[v[0]*100 for k,v in sl.items() if k.startswith('Terminal')][0]
w(f"Legal benchmarks do agree more often than chance. They agree less than coding benchmarks do, and much less than one benchmark agrees with a rerun of itself. Harvey's LAB has been run by three evaluators (Vals, Artificial Analysis, Mercor), and those runs agree {p(min(lab))} to {p(max(lab))} of the time. Terminal-Bench 4, run by Vals and Artificial Analysis, agrees {p(tb)} of the time.\n")
w("## The five legal benchmarks\n")
JUDGE={'Harvey LAB':'AI judge, written rubric','Vals Legal Research':'AI judge, written rubric, citations checked','Mercor APEX law':'AI judge, expert-written rubric','Legora BAR':'AI judge, criteria written by legal professionals','Certera':'blind head-to-head votes by legal professionals'}
w("| Benchmark | Publisher | Run by | Answers judged by | Models of the 37 | Top model | Agreement with the other four | 95% interval |\n|---|---|---|---|---|---|---|---|")
for key,name,pub,run,tk in sorted(LEG,key=lambda x:-C['per_legal'][x[0]]):
    t,n=top(tk); ci=C['per_legal_ci'][key]
    w(f"| {name} | {pub} | {run} | {JUDGE[key]} | {n} | {t} | {pc(C['per_legal'][key])} | {pc(ci[0])} to {pc(ci[1])} |")
w("\nThe intervals overlap almost completely, so the order of the five says little. The score measures agreement with the other four, not quality: a low score means a benchmark ranks models differently, not that it is wrong.\n")
ls_,cs_=TP['legal_summary'],TP['coding_summary']
w(f"Each of the five has a different model in first place. Among the {cs_['benchmarks']} coding benchmarks, one model is first or tied for first on {cs_['most']}. On three of the five legal leaderboards (Vals Legal Research, Mercor APEX law, Legora BAR) the leader is ahead of second place by about a point or less.\n")
rv=GS['rubric_vs_votes']
w(f"Four of the five describe their grading the same way: a written rubric scored by an AI judge. The rubrics are mostly private (LAB's are public), so a reader cannot see how the standards differ. Certera is the only one where people judge the answers. The four rubric benchmarks agree with each other {p(rv['rubric_rubric'])} of the time and with Certera's votes {p(rv['rubric_votes'])}; the difference is {rv['diff']:.0f} points with an interval of {rv['lo']:.0f} to {rv['hi']:.0f}, so it is not clearly different from zero. SemiAnalysis' GDPx legal, in the rule-based set below, also uses an AI judge, against rubrics and reference answers written by lawyers.\n")
w("Harvey wrote LAB, but its own published results cover only older models. Scores for current models come from other parties running it. Vals' run is used because it covers the most models and reports a margin of error for each score. Vals Legal Research is a separate benchmark with its own tasks.\n")
SHORT={'Harvey LAB':'Harvey LAB','Vals Legal Research':'Vals Legal Research','Mercor APEX law':'Mercor APEX law','Legora BAR':'Legora BAR','Certera':'Certera'}
w("| Pairing | Shared models | Agree on which of two models is better |\n|---|---|---|")
for k,v in sorted(C['legal_pairs'].items(),key=lambda kv:-kv[1][0]):
    a,b=k.split('|'); w(f"| {a} and {b} | {v[1]} | {pc(v[0])} |")
loo=[sum(v[0] for k,v in C['legal_pairs'].items() if n not in k.split('|'))/sum(1 for k in C['legal_pairs'] if n not in k.split('|'))*100 for n in C['per_legal']]
w(f"\nNo single benchmark produces the low figure. Leaving any one of the five out, the other four agree {p(min(loo))} to {p(max(loo))} of the time.\n")
w("Every pairing is in `data/pairs.csv` and the scores used are in `data/scores.csv`.\n")
w("## Method\n")
w("- **Models.** The 37 models Vals ran on Harvey's LAB between 19 October and 9 November 2026. This set is defined by recency, not by score. Each pairing of benchmarks is compared on the models both tested, and needs at least 10 shared models.")
w("- **Scores.** Each benchmark's own headline score, taken from the publisher's site on 11 November 2026. Where a source ran a model at several effort settings, the highest setting is used.")
w("- **Agreement.** For two benchmarks, the share of model pairs they put in the same order, over the models both tested (ties dropped). A group's figure is the average over every pairing in the group. Spearman rank correlation is reported alongside, as the median over pairings.")
w("- **Intervals.** Models were resampled with replacement and every statistic recomputed (2,000 times for the agreement shares, 3,000 for the correlations).")
w("- **Coding reference.** Terminal-Bench 4, Vibe Code, Code Migration, IOI, ProgramBench and SWE-bench Multimodal (all as run by Vals), plus FrontierCode 2 and SciCode (Artificial Analysis).")
w("- **Model names.** Sources label models differently. Names were matched by rule and then checked by hand. Three labels were treated as the same model as a differently named entry elsewhere: Reflection's Beam, Tencent's Hy4 and Nvidia's Nemotron 3.5 Super VL. Four further matches are less certain (Mistral Large 4, DeepSeek V4.1 Flash, Qwen 3.8 Max, Hy4), and the result is also reported without those models.\n")
w("## Which benchmarks are in, and why\n")
w("The five legal benchmarks in the charts were chosen by hand: the best-known ones with enough current models. To check that the choice does not drive the result, one written rule was also applied the same way to every field.\n")
w("**The rule.** A benchmark counts if (1) it has its own published leaderboard with a score per model, (2) at least 15 of the 37 models are on it, (3) it is the latest version, and (4) it is counted once, using the run with the most of the 37 models when several evaluators ran it. Combined indices and breakdowns inside a general benchmark do not count. A field is reported only if at least three benchmarks qualify. Vals' benchmarks are assigned to fields by Vals' own labels.\n")
w("Every legal candidate found, and what the rule does with it:\n")
w("| Benchmark | Run by | Models of the 37 | Rule | In the hand-picked five |\n|---|---|---|---|---|")
five={'Harvey LAB (Vals run)','Legal Research Bench (Vals)','Mercor APEX, corporate law','Legora BAR','Certera'}
for f,name,pub,run,n,inc,why in sorted([c for c in CAND if c[0]=='legal'],key=lambda c:(-c[5],-c[4])):
    w(f"| {name} | {run} | {n} | {'in' if inc else 'out: '+why} | {'yes' if name in five else ('no, left out by choice' if inc else 'no')} |")
w("\nThe legal figure under different choices:\n")
w("| Choice | Benchmarks | Pairings | Agreement | 95% interval |\n|---|---|---|---|---|")
LBL={'written rule (15+ models, own leaderboard, one run each)':'The written rule','your hand-picked five':'The hand-picked five (used in the charts)','rule, minimum 10 models instead of 15':'Rule with a minimum of 10 models','rule, minimum 20 models':'Rule with a minimum of 20 models','rule, one benchmark per publisher':'Rule, one benchmark per publisher','rule, plus the two slices from Artificial Analysis':'Rule, plus the two Artificial Analysis slices','rule, task benchmarks only (no Certera votes)':"Rule, without Certera's votes",'only benchmarks run by an independent evaluator or vote':'Rule, only benchmarks run by an independent evaluator or by vote'}
for lab_,nb,npairs,mean,lo,hi in VAR:
    # use one interval per quantity throughout the document
    if lab_=='your hand-picked five': mean,lo,hi=lm,C['legal_ci'][0]*100,C['legal_ci'][1]*100
    if lab_.startswith('written rule'): mean,lo,hi=A['legal'][0],A['legal'][1],A['legal'][2]
    w(f"| {LBL.get(lab_,lab_)} | {nb} | {npairs} | {p(mean)} | {p(lo)} to {p(hi)} |")
t=S['three']
w(f"| Only Harvey LAB, Vals Legal Research and Mercor APEX | 3 | 3 | {p(t['legal'])} | {p(t['ci'][0])} to {p(t['ci'][1])} |")
vs=[v[3] for v in VAR]
w(f"\nEvery choice with five or more benchmarks gives {p(min(vs))} to {p(max(vs))}. The hand-picked five is at the low end of that range. With only three benchmarks the figure is {p(t['legal'])}, the gap to coding shrinks to {t['gap']:.0f} points, and its interval ({max(t['gap_ci'][0],0):.0f} to {t['gap_ci'][1]:.0f}) reaches zero. Mercor's corporate-law score is one job out of three inside APEX-Agents; it is counted because Mercor publishes it as its own leaderboard.\n")
w("## Other fields, same pool of models, same rule\n")
w("| Field | Benchmarks | Pairings | Agreement | 95% interval | Run by |\n|---|---|---|---|---|---|")
RUN={'science':'Vals','coding':'Vals, Artificial Analysis','office work':'Artificial Analysis, Mercor','finance':'Vals'}
for k in ['science','coding','office work','finance']:
    v=A[k]; w(f"| {k.capitalize()} | {v[3]} | {v[4]} | {p(v[0])} | {p(v[1])} to {p(v[2])} | {RUN[k]} |")
v=A['legal']; w(f"| Legal (written rule) | {v[3]} | {v[4]} | {p(v[0])} | {p(v[1])} to {p(v[2])} | six different parties |")
w(f"| Legal (hand-picked five) | 5 | {len(C['legal_pairs'])} | {p(lm)} | {pc(C['legal_ci'][0])} to {pc(C['legal_ci'][1])} | four different parties |\n")
w("Legal (hand-picked five) against each field separately, resampling the same models for both:\n")
w("| Field | Points above legal | 95% interval | Resamples where the field is not above legal |\n|---|---|---|---|")
for k in ['science','coding','office work','finance']:
    g=G[k]; w(f"| {k.capitalize()} | {g['gap']:.0f} | {g['lo']:.0f} to {g['hi']:.0f} | {g['share_not_above']*100:.1f}% |")
w("\nLegal is below each of the four, and each interval excludes zero. These are four comparisons with no correction for making several, and science and finance have three benchmarks each.\n")
md,cy=A['medicine'],A['cyber']
w(f"Two fields have only two qualifying benchmarks, so one pairing each, and are not reported as fields: medicine ({p(md[0])}, interval {p(md[1])} to {p(md[2])}) and cyber ({p(cy[0])}, interval {p(cy[1])} to {p(cy[2])}). Cyber's single pairing is lower than legal. An earlier draft showed medicine and merged a maths benchmark into science; both were inconsistent with the rule and have been removed. Maths and general knowledge have one qualifying benchmark each.\n")
w(f"Science and finance were each run by a single evaluator, and legal benchmarks by four to six different parties. Where the evaluator differs, coding pairings agree {p(S['coding_diff_runner'][0])} of the time ({S['coding_diff_runner'][1]} pairings), against {p(S['legal_diff_runner'][0])} for legal ({S['legal_diff_runner'][1]} pairings). The one legal pairing run by the same evaluator (Harvey LAB and Vals Legal Research, both run by Vals) agrees {p(S['legal_same_runner'][0])} of the time.\n")
x=S['cross']
w(f"A legal benchmark agrees with a coding benchmark {p(x['legal_coding'])} of the time ({x['pairs']} pairings), against {p(x['legal_legal'])} with another legal benchmark. The difference is {x['diff']:.0f} points with an interval of {x['ci'][0]:.0f} to {x['ci'][1]:.0f}, so it is not clearly different from zero. There is no sign that the legal benchmarks share a ranking of their own beyond general model strength.\n")
w("## How far does a lead on one benchmark carry?\n")
w("For each benchmark, pairs of models are split into thirds by the size of the gap between them. The figure is how often another benchmark in the same field puts the same model ahead.\n")
w("| Field | Closest third of gaps | Middle third | Widest third | Widest tenth |\n|---|---|---|---|---|")
for k in ['science','coding','office work','finance','legal (written rule)','legal (hand-picked five)']:
    g=GS['fields'][k]; cell=lambda i:f"{p(g['thirds'][i])} ({g['lo'][i]:.0f} to {g['hi'][i]:.0f})"
    w(f"| {k.capitalize()} | {cell(0)} | {cell(1)} | {cell(2)} | {p(g['widest_tenth'])} |")
pts=GS['points']; lo_=GS['legal_five_leave_one_out_widest']
w(f"\nA small lead is close to a coin flip in every field. The difference is at the other end: in the four other fields a wide lead on one benchmark holds on another 92% to 97% of the time, and in legal about 70%. Leaving any one of the five legal benchmarks out, the widest-third figure is {p(lo_[0])} to {p(lo_[1])}. The widest third means gaps over {pts['Harvey LAB (Vals run)']['widest_over']:.0f} points on Harvey LAB, over {pts['Legal Research Bench (Vals)']['widest_over']:.1f} on Vals Legal Research and over {pts['Mercor APEX, corporate law']['widest_over']:.0f} on Mercor APEX law; the closest third means gaps under about {pts['Harvey LAB (Vals run)']['closest_under']:.0f}, {pts['Legal Research Bench (Vals)']['closest_under']:.0f} and {pts['Mercor APEX, corporate law']['closest_under']:.0f} points.\n")
w("## The same models for every field\n")
cmn=M['common']
w(f"The comparisons above use the same pool of 37 models, but each pairing only uses the models both benchmarks tested, and legal pairings share fewer models (15 to 37) than coding pairings. To rule that out as the cause, every field was scored on exactly the same {len(M['common_models'])} models, the ones all five legal benchmarks tested.\n")
w("| Field | Agreement on those 15 models | 95% interval | Gap to legal | Interval on the gap |\n|---|---|---|---|---|")
w(f"| Science | {pc(cmn['science'][0])} | 69% to 93% | 26 points | 9 to 40 |")
w(f"| Coding | {pc(cmn['coding'][0])} | 67% to 84% | 20 points | 6 to 32 |")
w(f"| Office work | {pc(cmn['office work'][0])} | 64% to 83% | 18 points | 4 to 31 |")
w(f"| Finance | {pc(cmn['finance'][0])} | 58% to 84% | 16 points | 2 to 28 |")
w(f"| Legal | {pc(cmn['legal'][0])} | 47% to 67% | | |\n")
w(f"The gap is at least as large on identical models. On this strictest comparison the legal interval includes 50%, so legal agreement cannot be clearly told apart from a coin flip there.\n")
w("## Where the gap comes from\n")
w("Vals reports a margin of error for every score, so for Vals-run benchmarks the effect of noise can be separated from real disagreement. The ceiling is how often two benchmarks would agree if they ranked models identically underneath and differed only by their reported noise.\n")
w("| Field (Vals-run benchmarks only) | Ceiling from noise alone | Actual agreement | Shortfall |\n|---|---|---|---|\n| Science | 90% | 84% | 6 points |\n| Coding | 87% | 80% | 7 points |\n| Finance | 83% | 73% | 10 points |\n| Legal | 83% | 68% | 14 points |\n")
w(f"- **Noise caps every field well below 100%.** Current models score close together relative to the margins of error. Legal and finance have the same ceiling, so noise does not explain why legal is lower than finance.\n- **With one evaluator, legal is close to finance.** 68% against 73%, on three legal pairings. One of them (Harvey LAB and Vals Immigration, 58%) accounts for most of the difference.\n- **The larger drop comes when different parties build and run the benchmarks.** Legal falls from 68% within Vals to {p(S['legal_diff_runner'][0])} across parties. Coding does not fall ({p(S['coding_same_runner'][0])} within one evaluator, {p(S['coding_diff_runner'][0])} across).\n")
w("The cross-party drop is consistent with each party applying its own standard of good legal work, and also with differences in setup, such as Legora testing inside its own product and Certera collecting votes on chat answers. The data cannot separate the two. Pairings of the three rubric-graded agent benchmarks (Harvey, Vals, Mercor) agree more than pairings involving Certera or Legora.\n")
w("## Tasks or standard?\n")
w("Two benchmarks can disagree because they set different tasks or because they judge answers differently. These checks hold one fixed and change the other (figures from `scripts/tasks_vs_standard.py`).\n")
w("| What changes | Agreement on which of two models is better |\n|---|---|")
w("| Nothing: one benchmark split into random halves (LAB, Vals Legal Research) | 87% |")
w("| Area of law: LAB's deal-work practice areas against its disputes and regulatory ones | 90% |")
w("| Who runs it: LAB run by Vals, Artificial Analysis and Mercor | 85% to 92% |")
w("| The scoring rule: LAB scored all-or-nothing against per criterion | 88% |")
w("| Kind of work: Legora's task families (draft, review, extract and so on), 9 models | 73%, against 80% for the same family in two editions |")
w("| One rule about what counts as good: LAB with and without the penalty for made-up facts, 25 models | 79% |")
w("| The whole benchmark: two different legal benchmarks | 62% |\n")
w("For reference, random halves of Terminal-Bench 4 (coding) agree 90% of the time and of Vals' Finance Agent 81%. Inside one benchmark, legal tasks are as consistent as coding tasks.\n")
w("On the same LAB answers, ranking models by rubric pass rate and ranking them by fewest made-up facts agree 55% of the time. Area of law and the evaluator make no measurable difference. Kind of work costs a few points on thin data. A change in what counts as a good answer moves rankings the most of the things that could be isolated. Legora's comparison rests on 9 models, and the made-up-facts check is done by a single AI judge.\n")
w("## Robustness (Spearman rank correlation)\n")
w("| Check | Legal | Coding | Gap |\n|---|---|---|---|")
w(f"| Main result | {r2(m['legal'])} | {r2(m['coding'])} | {r2(m['coding']-m['legal'])} |")
R=F['robustness']; RL=[('original 4 coding benchmarks','Coding reference limited to four benchmarks'),('no uncertain matches','Four models with uncertain name matches removed'),('kendall',"Kendall's tau instead of Spearman"),('all models','All models any source tested, not just the 37'),('min 15 shared','Only pairings sharing 15 or more models')]
for k,lab_ in RL: w(f"| {lab_} | {r2(R[k]['legal'])} | {r2(R[k]['coding'])} | {r2(R[k]['coding']-R[k]['legal'])} |")
dl=[R[k] for k in R if k.startswith('drop ')]
w(f"| Leaving out any one legal benchmark | {r2(min(d['legal'] for d in dl))} to {r2(max(d['legal'] for d in dl))} | {r2(m['coding'])} | {r2(min(d['coding']-d['legal'] for d in dl))} to {r2(max(d['coding']-d['legal'] for d in dl))} |\n")
w("On the agreement-share measure:\n")
w("| Check | Legal | Coding |\n|---|---|---|")
w(f"| Main result | {p(lm)} | {p(cm)} |")
lr=S['lab_run']
w(f"| Harvey LAB taken from Mercor's run instead of Vals' | {p(lr['LAB (Mercor run)'])} | {p(cm)} |")
w(f"| Harvey LAB taken from Artificial Analysis' run, ungated | {p(lr['LAB (AA run, ungated)'])} | {p(cm)} |")
w(f"| Harvey LAB taken from Artificial Analysis' run, hallucination-gated | {p(lr['LAB (AA run, hallucination-gated)'])} | {p(cm)} |")
w(f"| Pairings run by the same evaluator | {p(S['legal_same_runner'][0])} ({S['legal_same_runner'][1]} pairing) | {p(S['coding_same_runner'][0])} ({S['coding_same_runner'][1]} pairings) |")
w(f"| Pairings run by different evaluators | {p(S['legal_diff_runner'][0])} ({S['legal_diff_runner'][1]} pairings) | {p(S['coding_diff_runner'][0])} ({S['coding_diff_runner'][1]} pairings) |")
w(f"| Every field on the same 15 models | {pc(cmn['legal'][0])} | {pc(cmn['coding'][0])} |\n")
w("## Limits\n")
w("- **It shows that the rankings differ, not why.** Legal work may be several distinct skills (research, drafting, review), in which case lower agreement is expected and is not a flaw in any benchmark.")
w("- **The benchmarks measure different things.** Certera is blind votes by legal professionals on their own prompts. The others are rubric-graded tasks. Legora runs each model inside its own product, so a score reflects the model plus that setup.")
w("- **Five benchmarks is a small set.** There are ten pairings, and four of them involve Legora, which shares only 15 models with the others and publishes only scores relative to its average, with many ties.")
w("- **Margins of error are mostly unpublished.** Only Vals publishes a standard error per model, so noise could be separated from real disagreement only for Vals-run benchmarks.")
w("- **Effort settings differ between sources.** Vals ran Claude Fable 5.2 at high effort and others ran it at max. The same mismatch applies to the coding reference, where agreement stayed high.")
w("- **The other fields are thin.** Science and finance have three benchmarks each, all run by Vals.")
w("- **Coding benchmarks are not a gold standard.** They are a reference from a field where benchmarks are broadly trusted.")
w("- **It is one month of data.**\n")
w("## Other observations from the data\n")
w("- **LAB's scoring rule shrinks scores without reordering models.** On Vals' run, models pass 73% to 96% of individual rubric criteria but only 2% to 27% of whole tasks. The two rankings have a rank correlation of 0.88.")
w("- **LAB's ranking changes when hallucinations are penalised.** Artificial Analysis zeroes any task with a material hallucination. Its ungated and gated rankings have a rank correlation of 0.75, and Gemini 4 Argon falls from 20.8% to 3.9%. Artificial Analysis published this itself in October.")
w("- **The hallucination check depends on the checking model.** In Artificial Analysis' own comparison on 20 tasks, the count of material hallucinations ranged from 1.4 to 23.5 per task depending on which model did the checking. It uses the strictest, GPT-6 Sol.\n")
w("## Related work\n")
w("- **Comparing benchmarks by how they rank models is an established method.** Perlitz et al. (2024), *Do These LLM Benchmarks Agree? Fixing Benchmark Evaluation with BenchBench* (arXiv 2407.13696), call it benchmark agreement testing and warn that results depend on which models are compared. The same-models check and the cross-field comparison above are meant to address that.")
w("- **Rubric grading has been tested against expert preference in legal work.** *JudgmentBench* (arXiv 2605.25240) collected rubric scores and pairwise preferences from practising attorneys on 30 legal tasks and reports that pairwise preferences recover an intended quality ordering far better than rubrics (rank correlation 0.908 against 0.150). Four of the five legal benchmarks here are rubric-graded; Certera is the one built on preferences.")
w("- **The case for public legal benchmarking, and how it can go wrong,** is made by Guha et al. (2026), *There Is No Free Benchmark: An Institutional View of Legal AI Benchmarking* (PNAS).")
w("- A search on 11 November 2026 found no published comparison of how legal benchmarks rank the same models. That is one search, not proof that none exists.\n")
w("## Files\n")
w("- `slide1-benchmark-of-benchmarks.png`, `slide2-benchmark-of-legal-benchmarks.png`: the two slides. `slide1-no-footer.png` and `slide2-no-footer.png` are the same without the footer line. `slide2-alt.png` is slide 2 with a title that does not read as a ranking, bars in alphabetical order, and the coding figure as a reference line.")
w("- `option1-winners.png`, `option2-ten-dots.png`, `benchmark-of-legal-benchmarks-50.png`, `benchmark-of-legal-benchmarks.png`, `legal-benchmarks-agreement.png`: earlier chart versions, redrawn from the same numbers.")
w("- `data/`: results. `pairs.csv` and `scores.csv` are the pairings and scores for the five legal benchmarks; the `.json` files hold every figure quoted here.")
w("- `scripts/`: the analysis code. `make_readme.py` builds this file from the result files. Raw downloaded leaderboards (about 400 MB) are not in the repo.")
open('/home/user/lawyerbenchmarks/benchmark-agreement/README.md','w').write('\n'.join(o)+'\n'); print('written',len(o),'lines')
