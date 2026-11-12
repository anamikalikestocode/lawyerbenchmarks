"""Ask each model every task once, with the same instruction, and save the answers."""
import json,subprocess,sys,concurrent.futures as cf,os
MODELS=['gemini-4-argon','gpt-6.1-sol','claude-opus-5-5','gpt-6-astra']
SYSTEM="You are helping a lawyer at a small firm that advises early-stage startups. Write the answer the lawyer would send. Use at most 150 words. Plain text only: no markdown, no bullet symbols, no headings."
tasks=json.load(open('tasks.json'))
def ask(model,task):
    body=json.dumps({"model":model,"messages":[{"role":"system","content":SYSTEM},{"role":"user","content":task['prompt']}],"max_tokens":4000})
    r=subprocess.run(['curl','-sS','-m','300','-X','POST','https://api.concentrate.ai/v1/chat/completions','-H','Authorization: Bearer dummy','-H','Content-Type: application/json','-d',body],capture_output=True,text=True)
    try:
        d=json.loads(r.stdout); return d['choices'][0]['message']['content'].strip(),d.get('usage')
    except Exception as e: return None,(r.stdout[:300] or r.stderr[:300])
out=json.load(open('answers.json')) if os.path.exists('answers.json') else {}
jobs=[(m,t) for t in tasks for m in MODELS if not out.get(t['id'],{}).get(m)]
with cf.ThreadPoolExecutor(8) as ex:
    for (m,t),(txt,meta) in zip(jobs,ex.map(lambda j:ask(*j),jobs)):
        if txt: out.setdefault(t['id'],{})[m]=txt; print(t['id'],m,len(txt.split()),'words',meta)
        else: print('FAILED',t['id'],m,meta)
json.dump(out,open('answers.json','w'),indent=1)
