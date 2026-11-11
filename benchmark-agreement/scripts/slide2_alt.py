"""Slide 2, alternative: same bars, but not framed as a ranking of the five (no leaderboard title, coding shown as the reference)."""
import json, sys, itertools, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
A=json.load(open('data/audit_fields.json')); C=json.load(open('data/concord.json'))
INK='#0b0b0b'; GRID='#e6e5e0'; SURF='#fcfcfb'; BLUE='#2a78d6'; GRAY='#b9b8b2'
order=sys.argv[1]; out=sys.argv[2]; title=sys.argv[3]
coding=A['coding'][0]
NAME={'Vals Legal Research':'Vals\nLegal Research','Mercor APEX law':'Mercor\nAPEX','Harvey LAB':'Harvey\nLAB','Legora BAR':'Legora\nBAR','Certera':'Certera'}
legal=list(C['per_legal'].items())
legal=sorted(legal,key=(lambda kv:NAME[kv[0]].lower()) if order=='alpha' else (lambda kv:-kv[1]))
fig,ax=plt.subplots(figsize=(10.5,7.9),dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
plt.subplots_adjust(left=0.135,right=0.965,top=0.74,bottom=0.17)
ax.set_ylim(0,100); ax.set_xticks([])
ax.set_yticks([0,50,coding,100]); ax.set_yticklabels(['0\nopposite','50\ncoin flip',f'{coding:.0f}\ncoding','100\nsame\nranking'],fontsize=10.5,color=INK,linespacing=1.2); ax.tick_params(axis='y',length=0,pad=8)
for s in ax.spines.values(): s.set_visible(False)
ax.yaxis.grid(True,color=GRID,lw=0.8,zorder=0); ax.set_axisbelow(True); ax.axhline(0,color=INK,lw=1.2,zorder=5)
ax.axhline(50,color=INK,lw=1.6,ls=(0,(5,3)),zorder=5)
ax.axhline(coding,color=GRAY,lw=2.6,zorder=2)
fig.text(0.045,0.955,title,fontsize=30,color=INK,fontweight='bold',ha='left',va='top')
fig.text(0.045,0.868,"How often does each one agree with the other four on which AI is better?",fontsize=15.5,color=INK,ha='left',va='top')
for x,(k,v) in enumerate(legal):
    ax.bar(x,v*100,width=0.66,color=BLUE,zorder=3,linewidth=0)
    ax.text(x,v*100+2,f"{v*100:.0f}",ha='center',va='bottom',fontsize=24,color=INK,fontweight='bold',zorder=6)
    ax.text(x,-6,NAME[k],ha='center',va='top',fontsize=14,color=INK,linespacing=1.15)
    if k=='Harvey LAB': ax.text(x,-22,'run by Vals',ha='center',va='top',fontsize=10,color=INK)
ax.set_xlim(-0.55,len(legal)-0.45); fig.savefig(out,facecolor=SURF); plt.close(fig)
