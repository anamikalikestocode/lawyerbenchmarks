import sys,io,contextlib,numpy as np
sys.path.insert(0,'scripts')
with contextlib.redirect_stdout(io.StringIO()):
    from final import T,LEGAL,CODE,cohort
    from concord import conc,allpairs,pooled
rng=np.random.default_rng(101)
def cross(ms,minn=10):
    v=[conc(LEGAL[a],CODE[b],ms,minn)[0] for a in LEGAL for b in CODE]; v=[q for q in v if q is not None]; return np.mean(v)
ll=pooled(allpairs(LEGAL,cohort))[1]; lc=cross(cohort); d=[]
for _ in range(1000):
    s=list(rng.choice(cohort,len(cohort))); d.append(cross(s,8)-pooled(allpairs(LEGAL,s,8))[1])
sys.stderr.write('legal-legal %.1f  legal-coding %.1f  diff %.1f [%.1f, %.1f]  P(diff<=0)=%.3f\n'%(ll*100,lc*100,(lc-ll)*100,*np.percentile(d,[2.5,97.5])*100,(np.array(d)<=0).mean()))
