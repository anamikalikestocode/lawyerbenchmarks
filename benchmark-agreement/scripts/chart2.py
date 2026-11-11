import json, matplotlib, numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt
C=json.load(open('data/concord.json'))
INK='#0b0b0b'; SEC='#52514e'; MUTE='#8a8983'; GRID='#e6e5e0'; SURF='#fcfcfb'; BLUE='#2a78d6'; ORANGE='#eb6834'; GRAY='#a9a8a2'
same=[v[0]*100 for v in C['same'].values()]
rows=[  # (label, sublabel, value, lo, hi, color, height)
 ('The same benchmark, run by two evaluators','Harvey LAB (three runs), Terminal-Bench 4 (two runs)',float(np.mean(same)),min(same),max(same),GRAY,0.5),
 ('Two different coding benchmarks','Terminal-Bench 4, Vibe Code, Code Migration, IOI, ProgramBench,\nSWE-bench Multimodal, FrontierCode 2, SciCode',C['coding'][1]*100,C['coding_ci'][0]*100,C['coding_ci'][1]*100,ORANGE,0.5),
 ('Two different legal benchmarks','Harvey LAB, Vals Legal Research, Mercor APEX, Legora BAR,\nSemiAnalysis GDPx, Certera',C['legal'][1]*100,C['legal_ci'][0]*100,C['legal_ci'][1]*100,BLUE,0.5),
]
NAME={'GDPx legal':'SemiAnalysis GDPx (legal)','Vals Legal Research':'Vals Legal Research','Mercor APEX law':'Mercor APEX (corporate law)','Certera':'Certera (lawyer votes)','Legora BAR':'Legora BAR','Harvey LAB':'Harvey LAB'}
per=sorted(C['per_legal'].items(),key=lambda kv:-kv[1])
fig,ax=plt.subplots(figsize=(12,9.2),dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
plt.subplots_adjust(left=0.415,right=0.94,top=0.80,bottom=0.135)
y=0; ys=[]
def bar(y,v,lo,hi,col,h,bold=True):
    ax.barh(y,v-50,left=50,height=h,color=col,zorder=3,linewidth=0)
    ax.plot([lo,hi],[y,y],color=INK,lw=1.1,zorder=4); 
    for x in (lo,hi): ax.plot([x,x],[y-0.09,y+0.09],color=INK,lw=1.1,zorder=4)
    ax.text(max(hi,v)+1.0,y,f"{v:.0f}%",va='center',ha='left',fontsize=15 if bold else 12,color=INK,fontweight='bold' if bold else 'normal',zorder=5)
ypos=[0,1.25,2.5]
for (lab,sub,v,lo,hi,col,h),yy in zip(rows,ypos):
    bar(yy,v,lo,hi,col,0.56)
    ax.text(48.6,yy-0.17,lab,ha='right',va='center',fontsize=13.5,color=INK,fontweight='bold')
    ax.text(48.6,yy+0.2,sub,ha='right',va='top',fontsize=9.3,color=MUTE,linespacing=1.3)
y0=4.35
ax.text(48.6,y0-0.75,'Each legal benchmark against the other five',ha='right',va='center',fontsize=11.5,color=SEC,fontweight='bold')
for i,(k,v) in enumerate(per):
    yy=y0+i*0.62; lo,hi=[x*100 for x in C['per_legal_ci'][k]]
    bar(yy,v*100,lo,hi,BLUE,0.34,bold=False)
    ax.text(48.6,yy,NAME[k],ha='right',va='center',fontsize=12,color=INK)
ax.axvline(50,color=INK,lw=1.2,zorder=5)
ax.set_xlim(50,100); ax.set_ylim(y0+len(per)*0.62-0.2,-0.75)
ax.set_yticks([]); ax.set_xticks([50,60,70,80,90,100]); ax.set_xticklabels(['50%\ncoin flip','60%','70%','80%','90%','100%\nalways agree'],fontsize=10.5,color=SEC); ax.tick_params(axis='x',length=0,pad=7)
for s in ax.spines.values(): s.set_visible(False)
ax.xaxis.grid(True,color=GRID,lw=0.8,zorder=0); ax.set_axisbelow(True)
fig.text(0.04,0.955,"Pick two AI models. Do two benchmarks agree on which is better?",fontsize=20.5,color=INK,fontweight='bold',ha='left',va='top')
fig.text(0.04,0.905,f"Two legal benchmarks agree {C['legal'][1]*100:.0f}% of the time. Two coding benchmarks agree {C['coding'][1]*100:.0f}% of the time, on the same models.\nGuessing would give 50%.",fontsize=13,color=SEC,ha='left',va='top',linespacing=1.4)
fig.text(0.04,0.068,"How to read it: take every pair of models that two benchmarks both tested, and count how often the two benchmarks put that pair in the same order. Bars average this over every pairing of\nbenchmarks in the group. Lines show 95% intervals from resampling models (for the top bar, the range across reruns). Models: the 37 current models Vals ran on Harvey's LAB, Oct 19 to Nov 9, 2026.\nScores retrieved Nov 11, 2026 from the publishers' own sites.",fontsize=8.6,color=MUTE,ha='left',va='top',linespacing=1.5)
fig.text(0.94,0.988,"lawyerbenchmarks.com",fontsize=10,color=MUTE,ha='right',va='top')
out='/home/user/lawyerbenchmarks/benchmark-agreement/legal-benchmarks-agreement.png'
fig.savefig(out,facecolor=SURF); print(out)
