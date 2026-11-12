"""Build the grading page from tasks.json and answers.json. Model names never go into the page; key.json keeps the mapping.
usage: build.py [answers.json] [out.html]"""
import json,random,itertools,sys,html
ans_path=sys.argv[1] if len(sys.argv)>1 else 'answers.json'; out=sys.argv[2] if len(sys.argv)>2 else 'grade.html'
tasks=json.load(open('tasks.json')); answers=json.load(open(ans_path)); rnd=random.Random(20261112)
MODELS=['gemini-4-argon','gpt-6.1-sol','claude-opus-5-5','gpt-6-astra','gpt-6-luna']   # the last one is a deliberately weaker model, as a sanity check
key={}; page=[]
for t in tasks:
    missing=[m for m in MODELS if not answers.get(t['id'],{}).get(m)]
    if missing: sys.exit(f"no answer yet for {t['id']}: {missing}. Run generate.py first.")
    order=MODELS[:]; rnd.shuffle(order); prs=[]
    for a,b in itertools.combinations(range(len(MODELS)),2):
        l,r=(a,b) if rnd.random()<0.5 else (b,a); pid=f"{t['id']}-{l}{r}"; prs.append({'id':pid,'l':l,'r':r}); key[pid]=[order[l],order[r]]
    rnd.shuffle(prs)
    rep=prs[0]; rid=rep['id']+'-again'; prs.append({'id':rid,'l':rep['r'],'r':rep['l']}); key[rid]=[order[rep['r']],order[rep['l']]]   # one pair shown twice, sides swapped
    page.append({'id':t['id'],'title':t['title'],'prompt':t['prompt'],'answers':[answers[t['id']][m] for m in order],'pairs':prs})
json.dump(key,open('key.json','w'),indent=1)
doc=open('template.html').read().replace('/*DATA*/',json.dumps(page).replace('</','<\\/'))
open(out,'w').write(doc); print('wrote',out,sum(len(t['pairs']) for t in page),'comparisons')
