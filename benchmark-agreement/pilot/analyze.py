"""Read the codes lawyers send back (one per file in results/) and report:
1. how often two lawyers pick the same answer, 2. how the lawyers rank the four models, 3. which benchmark's ranking of those four matches theirs.
usage: analyze.py"""
import json,base64,glob,itertools,collections
key=json.load(open('key.json')); M=['gemini-4-argon','gpt-6.1-sol','claude-opus-5-5','gpt-6-astra','gpt-6-luna']; WEAK='gpt-6-luna'
# rank of each model among the models on all five leaderboards (lower is better), from the write-up, Nov 2026
BENCH={'Harvey LAB':{'gemini-4-argon':1,'claude-opus-5-5':10,'gpt-6-astra':11,'gpt-6.1-sol':12},
 'Vals Legal Research':{'gemini-4-argon':1,'claude-opus-5-5':2,'gpt-6-astra':10,'gpt-6.1-sol':12},
 'Mercor APEX law':{'gpt-6-astra':1,'gemini-4-argon':2,'claude-opus-5-5':4,'gpt-6.1-sol':5},
 'Legora BAR':{'claude-opus-5-5':1,'gpt-6.1-sol':4,'gemini-4-argon':9,'gpt-6-astra':10},
 'Certera':{'gpt-6.1-sol':1,'gpt-6-astra':3,'gemini-4-argon':4,'claude-opus-5-5':6}}
L={}
for f in sorted(glob.glob('results/*')):
    d=json.loads(base64.b64decode(open(f).read().strip())); L[d['who'].get('name') or f]=d
if len(L)<2: raise SystemExit('put each lawyer\'s code in its own file under results/ (need at least two)')
print(len(L),'lawyers:',', '.join(f"{n} ({d['who'].get('area','?')}, {d['who'].get('years','?')} yrs)" for n,d in L.items()))
print('\n0. Checks')
for nm,d in L.items():
    rep=[p for p in key if p.endswith('-again') and d['r'].get(p) in ('L','R') and d['r'].get(p[:-6]) in ('L','R')]
    same=sum((d['r'][p]=='L')!=(d['r'][p[:-6]]=='L') for p in rep)   # sides were swapped, so a consistent lawyer picks the other side
    wk=[p for p in key if WEAK in key[p] and not p.endswith('-again') and d['r'].get(p) in ('L','R')]
    lost=sum(key[p][0 if d['r'][p]=='R' else 1]==WEAK for p in wk)
    print(f"   {nm}: same choice on {same} of {len(rep)} repeated pairs; picked against the weaker model in {lost} of {len(wk)}")
print('\n1. Do lawyers agree with each other?  (top four models only; share of comparisons where both picked the same answer; 50% = coin flip)')
allv=[]
for a,b in itertools.combinations(L,2):
    both=[p for p in key if not p.endswith('-again') and WEAK not in key[p] and L[a]['r'].get(p) in 'LR' and L[b]['r'].get(p) in 'LR' and L[a]['r'].get(p) and L[b]['r'].get(p)]
    same=sum(L[a]['r'][p]==L[b]['r'][p] for p in both); allv.append(same/len(both)); print(f"   {a} & {b}: {100*same/len(both):.0f}%  ({len(both)} comparisons)")
print(f"   average: {100*sum(allv)/len(allv):.0f}%")
def wins(names):
    w=collections.Counter(); n=collections.Counter(); h=collections.defaultdict(lambda:[0,0])
    for nm in names:
        for p,c in L[nm]['r'].items():
            if c not in 'LR' or p not in key or p.endswith('-again'): continue
            l,r=key[p]; win,lose=(l,r) if c=='L' else (r,l); w[win]+=1; n[l]+=1; n[r]+=1; h[tuple(sorted((l,r)))][0 if win==sorted((l,r))[0] else 1]+=1
    return {m:w[m]/n[m] for m in M if n[m]},h
rate,h=wins(L)
print('\n2. How the lawyers rank the models (share of comparisons won)')
for m in sorted(rate,key=rate.get,reverse=True): print(f"   {m:18} {100*rate[m]:.0f}%")
print('\n3. Which benchmark ranks these four models like the lawyers do?  (of the 6 model pairs, how many it orders the same way)')
for b,rk in BENCH.items():
    same=tot=0
    for (x,y),(wx,wy) in h.items():
        if wx==wy or WEAK in (x,y): continue
        tot+=1; same+=(wx>wy)==(rk[x]<rk[y])
    print(f"   {b:20} {same} of {tot}")
print('\nWith four models and a handful of lawyers this is a pilot: read part 3 as a hint, not a result.')
