import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
F=json.load(open('data/final.json')); bars=F['bars']; main=F['main']
INK='#0b0b0b'; SEC='#52514e'; MUTE='#8a8983'; GRID='#e6e5e0'; SURF='#fcfcfb'; BLUE='#2a78d6'
LABEL={'Harvey LAB':'Harvey LAB','Vals Legal Research':'Vals Legal Research','Mercor APEX law':'Mercor APEX (corporate law)','Legora BAR':'Legora BAR','GDPx legal':'SemiAnalysis GDPx (legal)','Certera':'Certera (lawyer votes)'}
order=sorted(bars,key=lambda k:bars[k][0])
fig,ax=plt.subplots(figsize=(12,7.4),dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
plt.subplots_adjust(left=0.235,right=0.955,top=0.80,bottom=0.215)
code=main['coding']; rer=(0.83,0.95)
ax.axvspan(rer[0],rer[1],color='#efeeea',zorder=0,lw=0)
ax.axvline(code,color=SEC,lw=1.4,ls=(0,(4,3)),zorder=1)
ax.axvline(0,color=MUTE,lw=1,zorder=1)
for i,k in enumerate(order):
    v,lo,hi,n=bars[k]
    ax.add_patch(FancyBboxPatch((0,i-0.24),v,0.48,boxstyle="round,pad=0,rounding_size=0.012",fc=BLUE,ec='none',zorder=3,mutation_aspect=18))
    ax.add_patch(plt.Rectangle((0,i-0.24),min(v,0.02),0.48,fc=BLUE,ec='none',zorder=3))
    ax.plot([lo,hi],[i,i],color=INK,lw=1.1,zorder=4,solid_capstyle='butt')
    for x in (lo,hi): ax.plot([x,x],[i-0.07,i+0.07],color=INK,lw=1.1,zorder=4)
    ax.text(hi+0.018,i,f"{v:.2f}",va='center',ha='left',fontsize=13,color=INK,fontweight='bold',zorder=5)
    ax.text(-0.235,i+0.07,LABEL[k],va='center',ha='right',fontsize=13,color=INK,transform=ax.get_yaxis_transform() if False else ax.transData)
    ax.text(-0.235,i-0.21,f"{n} of 37 models",va='center',ha='right',fontsize=9.5,color=MUTE)
ax.set_xlim(-0.22,1.0); ax.set_ylim(-0.6,len(order)+0.35)
ax.set_yticks([]); ax.set_xticks([0,0.2,0.4,0.6,0.8,1.0]); ax.tick_params(axis='x',colors=SEC,labelsize=11,length=0,pad=6)
for s in ax.spines.values(): s.set_visible(False)
ax.xaxis.grid(True,color=GRID,lw=0.8,zorder=0); ax.set_axisbelow(True)
top=len(order)-0.38
ax.text(code-0.015,top,f"Coding benchmarks\nagree at {code:.2f}",ha='right',va='bottom',fontsize=10.5,color=SEC,linespacing=1.25)
ax.text(sum(rer)/2,top,"Harvey LAB rerun\nby another evaluator:\n0.83 to 0.95",ha='center',va='bottom',fontsize=10.5,color=SEC,linespacing=1.25)
ax.set_xlabel("Rank agreement with the other five legal benchmarks (0 = unrelated order, 1 = identical order)",fontsize=11,color=SEC,labelpad=10)
fig.text(0.04,0.945,"Legal AI benchmarks don't agree on which model is best",fontsize=21,color=INK,fontweight='bold',ha='left',va='top')
fig.text(0.04,0.892,f"Six legal benchmarks rank the same current models. Typical agreement between two of them is {main['legal']:.2f}.\nFor coding benchmarks on the same models it is {main['coding']:.2f}.",fontsize=13,color=SEC,ha='left',va='top',linespacing=1.4)
fig.text(0.04,0.1,"Each bar: average Spearman rank correlation between that benchmark and the other five, on the models both tested. Lines show 95% intervals from resampling models.\nModels: the 37 that Vals ran on Harvey's LAB, Oct 19 to Nov 9, 2026. Leaderboards retrieved Nov 11, 2026 from the publishers' own sites.\nCoding reference: 8 benchmarks, 28 pairs, same models.",fontsize=8.8,color=MUTE,ha='left',va='top',linespacing=1.5)
fig.text(0.955,0.945,"lawyerbenchmarks.com",fontsize=10,color=MUTE,ha='right',va='top')
out='/home/user/lawyerbenchmarks/benchmark-agreement/legal-benchmarks-agreement.png'
fig.savefig(out,facecolor=SURF); print(out)
