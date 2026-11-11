import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# values from scripts/fields.py (share of model pairs two benchmarks in the field order the same way, 37 current models)
DATA=[('Science\n& maths',83.1,4),('Coding',78.0,8),('Medicine',77.1,2),('Office\nwork',75.2,5),('Finance',73.5,3),('Legal',60.3,5)]
INK='#0b0b0b'; SEC='#52514e'; MUTE='#8a8983'; GRID='#e6e5e0'; SURF='#fcfcfb'; BLUE='#2a78d6'; GRAY='#b9b8b2'
fig,ax=plt.subplots(figsize=(10.5,7.9),dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
plt.subplots_adjust(left=0.135,right=0.965,top=0.74,bottom=0.2)
for x,(lab,v,n) in enumerate(DATA):
    hot=lab=='Legal'
    ax.bar(x,v,width=0.66,color=BLUE if hot else GRAY,zorder=3,linewidth=0)
    ax.text(x,v+2,f"{v:.0f}",ha='center',va='bottom',fontsize=26 if hot else 22,color=INK,fontweight='bold',zorder=6)
    ax.text(x,-6,lab,ha='center',va='top',fontsize=14,color=INK,linespacing=1.15,fontweight='bold' if hot else 'normal')
    ax.text(x,-22,f"{n} benchmarks",ha='center',va='top',fontsize=10,color=MUTE)
ax.axhline(50,color=INK,lw=1.6,ls=(0,(5,3)),zorder=5)
ax.set_xlim(-0.55,len(DATA)-0.45); ax.set_ylim(0,100)
ax.set_yticks([0,50,100]); ax.set_yticklabels(['0\nopposite','50\ncoin flip','100\nsame\nranking'],fontsize=10.5,color=SEC,linespacing=1.2); ax.tick_params(axis='y',length=0,pad=8); ax.set_xticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.yaxis.grid(True,color=GRID,lw=0.8,zorder=0); ax.set_axisbelow(True); ax.axhline(0,color=INK,lw=1.2,zorder=5)
fig.text(0.045,0.955,"The Benchmark of Benchmarks",fontsize=30,color=INK,fontweight='bold',ha='left',va='top')
fig.text(0.045,0.868,"How often do two benchmarks in the same field agree on which AI is better?",fontsize=15.5,color=SEC,ha='left',va='top')
fig.text(0.045,0.03,"The same 37 AI models in every field, Nov 2026.",fontsize=10,color=MUTE,ha='left',va='bottom')
fig.text(0.965,0.03,"lawyerbenchmarks.com",fontsize=10,color=MUTE,ha='right',va='bottom')
out='/home/user/lawyerbenchmarks/benchmark-agreement/benchmark-of-benchmarks-six-fields.png'
fig.savefig(out,facecolor=SURF); print(out)
