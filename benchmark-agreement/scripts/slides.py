import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
A=json.load(open('data/audit_fields.json')); C=json.load(open('data/concord.json'))
INK='#0b0b0b'; SEC='#52514e'; MUTE='#8a8983'; GRID='#e6e5e0'; SURF='#fcfcfb'; BLUE='#2a78d6'; GRAY='#b9b8b2'
OUT='/home/user/lawyerbenchmarks/benchmark-agreement/'
def frame(title,sub,foot,bottom=0.2):
    fig,ax=plt.subplots(figsize=(10.5,7.9),dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    plt.subplots_adjust(left=0.135,right=0.965,top=0.74,bottom=bottom)
    ax.axhline(50,color=INK,lw=1.6,ls=(0,(5,3)),zorder=5); ax.set_ylim(0,100)
    ax.set_yticks([0,50,100]); ax.set_yticklabels(['0\nopposite','50\ncoin flip','100\nsame\nranking'],fontsize=10.5,color=SEC,linespacing=1.2); ax.tick_params(axis='y',length=0,pad=8); ax.set_xticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.yaxis.grid(True,color=GRID,lw=0.8,zorder=0); ax.set_axisbelow(True); ax.axhline(0,color=INK,lw=1.2,zorder=5)
    fig.text(0.045,0.955,title,fontsize=30,color=INK,fontweight='bold',ha='left',va='top')
    fig.text(0.045,0.868,sub,fontsize=15.5,color=SEC,ha='left',va='top')
    fig.text(0.045,0.03,foot,fontsize=10,color=MUTE,ha='left',va='bottom'); fig.text(0.965,0.03,"lawyerbenchmarks.com",fontsize=10,color=MUTE,ha='right',va='bottom')
    return fig,ax
# ---- slide 1: fields (every field with 3+ benchmarks; legal = the five on slide 2) ----
F=[('Science',A['science'][0],A['science'][3]),('Coding',A['coding'][0],A['coding'][3]),('Office\nwork',A['office work'][0],A['office work'][3]),('Finance',A['finance'][0],A['finance'][3]),('Legal',C['legal'][1]*100,5)]
fig,ax=frame("The Benchmark of Benchmarks","How often do two benchmarks in the same field agree on which AI is better?","The same 37 AI models in every field, Nov 2026.")
for x,(lab,v,n) in enumerate(F):
    hot=lab=='Legal'
    ax.bar(x,v,width=0.66,color=BLUE if hot else GRAY,zorder=3,linewidth=0)
    ax.text(x,v+2,f"{v:.0f}",ha='center',va='bottom',fontsize=26 if hot else 22,color=INK,fontweight='bold',zorder=6)
    ax.text(x,-6,lab,ha='center',va='top',fontsize=14,color=INK,linespacing=1.15,fontweight='bold' if hot else 'normal')
    ax.text(x,-22,f"{n} benchmarks",ha='center',va='top',fontsize=10,color=MUTE)
ax.set_xlim(-0.55,len(F)-0.45); fig.savefig(OUT+'slide1-benchmark-of-benchmarks.png',facecolor=SURF); plt.close(fig)
# ---- slide 2: the five legal benchmarks ----
NAME={'Vals Legal Research':'Vals\nLegal Research','Mercor APEX law':'Mercor\nAPEX','Harvey LAB':'Harvey\nLAB','Legora BAR':'Legora\nBAR','Certera':'Certera'}
legal=sorted(C['per_legal'].items(),key=lambda kv:-kv[1])
fig,ax=frame("The Benchmark of Legal Benchmarks","How often does each one agree with the other four on which AI is better?","37 AI models, Nov 2026. Gaps between the five are within the margin of error.")
for x,(k,v) in enumerate(legal):
    ax.bar(x,v*100,width=0.66,color=BLUE,zorder=3,linewidth=0)
    ax.text(x,v*100+2,f"{v*100:.0f}",ha='center',va='bottom',fontsize=24,color=INK,fontweight='bold',zorder=6)
    ax.text(x,-6,NAME[k],ha='center',va='top',fontsize=14,color=INK,linespacing=1.15)
    if k=='Harvey LAB': ax.text(x,-22,'run by Vals',ha='center',va='top',fontsize=10,color=MUTE)
ax.set_xlim(-0.55,len(legal)-0.45); fig.savefig(OUT+'slide2-benchmark-of-legal-benchmarks.png',facecolor=SURF); plt.close(fig)
print([(a.replace('\n',' '),round(b,1),c) for a,b,c in F],[(k,round(v*100,1)) for k,v in legal])
