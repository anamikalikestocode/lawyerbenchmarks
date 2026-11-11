import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
C=json.load(open('data/concord.json'))
INK='#0b0b0b'; SEC='#52514e'; MUTE='#8a8983'; GRID='#e6e5e0'; SURF='#fcfcfb'; BLUE='#2a78d6'; ORANGE='#eb6834'
sc=lambda x:(2*x-1)*100          # 0 = coin flip, 100 = identical ranking
NAME={'Vals Legal Research':'Vals\nLegal Research','Mercor APEX law':'Mercor\nAPEX','Harvey LAB':'Harvey\nLAB','Legora BAR':'Legora\nBAR','Certera':'Certera'}
legal=sorted(C['per_legal'].items(),key=lambda kv:-kv[1])
bars=[('Coding\nbenchmarks',sc(C['coding'][1]),[sc(x) for x in C['coding_ci']],ORANGE)]+[(NAME[k],sc(v),[sc(x) for x in C['per_legal_ci'][k]],BLUE) for k,v in legal]
fig,ax=plt.subplots(figsize=(10.5,7.6),dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
plt.subplots_adjust(left=0.07,right=0.965,top=0.72,bottom=0.235)
xs=[0]+[1.45+i for i in range(len(legal))]
for x,(lab,v,ci,col) in zip(xs,bars):
    ax.bar(x,v,width=0.66,color=col,zorder=3,linewidth=0)
    ax.text(x,v+1.8,f"{v:.0f}",ha='center',va='bottom',fontsize=24,color=INK,fontweight='bold')
    ax.text(x,-4.5,lab,ha='center',va='top',fontsize=13.5,color=INK,linespacing=1.15,fontweight='bold' if col==ORANGE else 'normal')
ax.axvline(0.72,color=GRID,lw=1.2,zorder=1,ymin=0.0,ymax=0.9)
ax.plot([1.45-0.33,1.45+4+0.33],[-17.2,-17.2],color=MUTE,lw=1,clip_on=False)
ax.text(1.45+2,-19,'Legal benchmarks',ha='center',va='top',fontsize=12.5,color=SEC)
ax.set_xlim(-0.55,xs[-1]+0.55); ax.set_ylim(0,68)
ax.set_yticks([0,25,50]); ax.tick_params(axis='y',length=0,labelsize=10.5,colors=MUTE,pad=4); ax.set_xticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.yaxis.grid(True,color=GRID,lw=0.8,zorder=0); ax.set_axisbelow(True); ax.axhline(0,color=INK,lw=1.2,zorder=5)
fig.text(0.045,0.955,"The Benchmark of Legal Benchmarks",fontsize=30,color=INK,fontweight='bold',ha='left',va='top')
fig.text(0.045,0.868,"How much does each one agree with the others on which AI is better?",fontsize=15.5,color=SEC,ha='left',va='top')
fig.text(0.045,0.812,"0 = coin flip     100 = same ranking",fontsize=12.5,color=MUTE,ha='left',va='top')
fig.text(0.045,0.03,"37 AI models, Nov 2026. Gaps between the legal benchmarks are within the margin of error.",fontsize=10,color=MUTE,ha='left',va='bottom')
fig.text(0.965,0.03,"lawyerbenchmarks.com",fontsize=10,color=MUTE,ha='right',va='bottom')
out='/home/user/lawyerbenchmarks/benchmark-agreement/benchmark-of-legal-benchmarks.png'
fig.savefig(out,facecolor=SURF); print(out,[(b[0].replace('\n',' '),round(b[1]),[round(x) for x in b[2]]) for b in bars])
