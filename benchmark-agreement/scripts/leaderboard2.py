import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
C=json.load(open('data/concord.json'))
INK='#0b0b0b'; SEC='#52514e'; MUTE='#8a8983'; GRID='#e6e5e0'; SURF='#fcfcfb'; BLUE='#2a78d6'; ORANGE='#eb6834'
NAME={'Vals Legal Research':'Vals\nLegal Research','Mercor APEX law':'Mercor\nAPEX','Harvey LAB':'Harvey\nLAB','Legora BAR':'Legora\nBAR','Certera':'Certera'}
legal=sorted(C['per_legal'].items(),key=lambda kv:-kv[1])
bars=[('Coding\nbenchmarks',C['coding'][1]*100,ORANGE)]+[(NAME[k],v*100,BLUE) for k,v in legal]
fig,ax=plt.subplots(figsize=(10.5,7.9),dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
plt.subplots_adjust(left=0.135,right=0.965,top=0.74,bottom=0.245)
xs=[0]+[1.45+i for i in range(len(legal))]
for x,(lab,v,col) in zip(xs,bars):
    ax.bar(x,v,width=0.66,color=col,zorder=3,linewidth=0)
    ax.text(x,v+2,f"{v:.0f}",ha='center',va='bottom',fontsize=24,color=INK,fontweight='bold',zorder=6)
    ax.text(x,-6,lab,ha='center',va='top',fontsize=13.5,color=INK,linespacing=1.15,fontweight='bold' if col==ORANGE else 'normal')
    if lab.startswith('Harvey'): ax.text(x,-19.2,'run by Vals',ha='center',va='top',fontsize=10,color=MUTE)
ax.axhline(50,color=INK,lw=1.6,ls=(0,(5,3)),zorder=5)
ax.plot([1.45-0.33,1.45+4+0.33],[-27,-27],color=MUTE,lw=1,clip_on=False); ax.text(1.45+2,-29.5,'Legal benchmarks',ha='center',va='top',fontsize=12.5,color=SEC)
ax.set_xlim(-0.55,xs[-1]+0.55); ax.set_ylim(0,100)
ax.set_yticks([0,50,100]); ax.set_yticklabels(['0\nopposite','50\ncoin flip','100\nsame\nranking'],fontsize=10.5,color=SEC,linespacing=1.2); ax.tick_params(axis='y',length=0,pad=8); ax.set_xticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.yaxis.grid(True,color=GRID,lw=0.8,zorder=0); ax.set_axisbelow(True); ax.axhline(0,color=INK,lw=1.2,zorder=5)
fig.text(0.045,0.955,"The Benchmark of Legal Benchmarks",fontsize=30,color=INK,fontweight='bold',ha='left',va='top')
fig.text(0.045,0.868,"How often does each one agree with the others on which AI is better?",fontsize=15.5,color=SEC,ha='left',va='top')
fig.text(0.045,0.03,"37 AI models, Nov 2026. Gaps between the legal benchmarks are within the margin of error.",fontsize=10,color=MUTE,ha='left',va='bottom')
fig.text(0.965,0.03,"lawyerbenchmarks.com",fontsize=10,color=MUTE,ha='right',va='bottom')
out='/home/user/lawyerbenchmarks/benchmark-agreement/benchmark-of-legal-benchmarks-50.png'
fig.savefig(out,facecolor=SURF); print(out,[(b[0].replace('\n',' '),round(b[1])) for b in bars])
