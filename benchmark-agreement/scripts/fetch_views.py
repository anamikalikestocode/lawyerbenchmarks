import sys,json,glob,os,subprocess,concurrent.futures as cf
sys.path.insert(0,'scripts')
from parse_vals import islands, deser
os.makedirs('raw/vals_views',exist_ok=True); os.makedirs('data/vals_full',exist_ok=True)
jobs=[]
for p in sorted(glob.glob('raw/vals/*.html')):
    slug=os.path.basename(p)[:-5]
    isl,_=islands(p)
    url=None
    for i in isl:
        if isinstance(i,dict) and isinstance(i.get('benchmarkViewUrl'),str): url=i['benchmarkViewUrl']
    if url: jobs.append((slug,url))
def get(j):
    slug,url=j; out=f'raw/vals_views/{slug}.json'
    r=subprocess.run(['curl','-sSL','-m','90','-o',out,'-w','%{http_code}','https://www.vals.ai'+url],capture_output=True,text=True)
    return slug,url,r.stdout,os.path.getsize(out) if os.path.exists(out) else 0
with cf.ThreadPoolExecutor(6) as ex:
    for s,u,c,sz in ex.map(get,jobs): print(s,c,sz,u)
