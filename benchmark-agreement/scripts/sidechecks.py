"""Side checks on the agreement-share measure: which run of Harvey LAB, same vs different evaluator, three-benchmark subset, legal vs coding."""
import sys,io,contextlib,itertools,numpy as np,json
sys.path.insert(0,'scripts')
with contextlib.redirect_stdout(io.StringIO()):
    from final import T,LEGAL,CODE,cohort
    from concord import conc,allpairs,pooled
rng=np.random.default_rng(81); R={}
C=allpairs(CODE,cohort); R['coding']=pooled(C)[1]*100
R['lab_run']={}
for lab in ['LAB (Vals run)','LAB (Mercor run)','LAB (AA run, ungated)','LAB (AA run, hallucination-gated)']:
    L=dict(LEGAL); L['Harvey LAB']=lab; R['lab_run'][lab]=pooled(allpairs(L,cohort))[1]*100
runner={'Harvey LAB':'Vals','Vals Legal Research':'Vals','Mercor APEX law':'Mercor','Legora BAR':'Legora','Certera':'Certera','Terminal-Bench 4':'Vals','Vibe Code':'Vals','Code Migration':'Vals','IOI':'Vals','ProgramBench':'Vals','SWE-bench Multimodal':'Vals','FrontierCode 2':'AA','SciCode':'AA'}
P=allpairs(LEGAL,cohort)
for name,PP in [('legal',P),('coding',C)]:
    s=[v[0] for (i,j),v in PP.items() if runner[i]==runner[j]]; x=[v[0] for (i,j),v in PP.items() if runner[i]!=runner[j]]
    R[name+'_same_runner']=(float(np.mean(s))*100,len(s)); R[name+'_diff_runner']=(float(np.mean(x))*100,len(x))
L3={k:LEGAL[k] for k in ['Harvey LAB','Vals Legal Research','Mercor APEX law']}; P3=allpairs(L3,cohort)
d=[];l=[]
for _ in range(2000):
    s=list(rng.choice(cohort,len(cohort))); a=pooled(allpairs(L3,s,8))[1]; b=pooled(allpairs(CODE,s,8))[1]; l.append(a); d.append(b-a)
R['three']={'legal':pooled(P3)[1]*100,'ci':[float(x)*100 for x in np.percentile(l,[2.5,97.5])],'gap':(pooled(C)[1]-pooled(P3)[1])*100,'gap_ci':[float(x)*100 for x in np.percentile(d,[2.5,97.5])],'p':float((np.array(d)<=0).mean()),'bars':{k:float(np.mean([x[0] for (i,j),x in P3.items() if k in (i,j)]))*100 for k in L3},'pairs':{f'{i}|{j}':x[0]*100 for (i,j),x in P3.items()}}
def cross(ms,minn=10):
    v=[conc(LEGAL[a],CODE[b],ms,minn)[0] for a in LEGAL for b in CODE]; v=[q for q in v if q is not None]; return np.mean(v),len(v)
lc,n=cross(cohort); ll=pooled(P)[1]; dd=[]
for _ in range(1000):
    s=list(rng.choice(cohort,len(cohort))); dd.append(cross(s,8)[0]-pooled(allpairs(LEGAL,s,8))[1])
R['cross']={'legal_legal':ll*100,'legal_coding':lc*100,'pairs':n,'diff':(lc-ll)*100,'ci':[float(x)*100 for x in np.percentile(dd,[2.5,97.5])],'p':float((np.array(dd)<=0).mean()),'per':{a:float(np.mean([q for q in [conc(LEGAL[a],CODE[b],cohort)[0] for b in CODE] if q is not None]))*100 for a in LEGAL}}
json.dump(R,open('data/sidechecks.json','w'),indent=1); sys.stderr.write(json.dumps(R,indent=1)+'\n')
