"""Slides, restyled: white background, heavier type, one strong accent for legal.
Portrait 7:8 so two images sit side by side in a post without being cropped.
usage: slides_v2.py <baseline: zero|coin> <context colour> <accent colour> <outdir> [suffix]"""
import json, sys, logging, matplotlib
matplotlib.use('Agg'); logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.transforms import IdentityTransform
A=json.load(open('data/audit_fields.json')); C=json.load(open('data/concord.json'))
base,NEU,ACC,OUT=sys.argv[1:5]; SUF=sys.argv[5] if len(sys.argv)>5 else ''
SURF='#ffffff'; INK='#0b0b0b'; GRID='#e1e0d9'
HEAVY=dict(fontfamily='Inter Display',fontweight=800)
W,H,DPI=8.75,10.0,200
B0=50 if base=='coin' else 0
span=100-B0; up=lambda v:v+0.02*span
def lum(h):
    c=[int(h[i:i+2],16)/255 for i in (1,3,5)]; c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]; return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def rbar(ax,x,w,y0,y1,color,r=10,z=3):
    (xa,ya),(xb,yb)=ax.transData.transform([(x-w/2,y0),(x+w/2,y1)]); r=min(r,(xb-xa)/2,max(yb-ya,0.1)); k=0.5523*r
    V=[(xa,ya),(xa,yb-r),(xa,yb-r+k),(xa+r-k,yb),(xa+r,yb),(xb-r,yb),(xb-r+k,yb),(xb,yb-r+k),(xb,yb-r),(xb,ya),(xa,ya)]
    Cc=[Path.MOVETO,Path.LINETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,Path.LINETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,Path.LINETO,Path.CLOSEPOLY]
    ax.add_artist(PathPatch(Path(V,Cc),facecolor=color,edgecolor='none',transform=IdentityTransform(),zorder=z))
def frame(title,sub,n):
    fig,ax=plt.subplots(figsize=(W,H),dpi=DPI); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    plt.subplots_adjust(left=0.165,right=0.955,top=0.645,bottom=0.168)
    ax.set_xlim(-0.6,n-0.4); ax.set_ylim(B0,100); ax.set_xticks([])
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(axis='y',length=0,pad=10)
    ax.axhline(100,color=GRID,lw=1.2,zorder=1)
    fig.text(0.062,0.955,title,fontsize=45,color=INK,ha='left',va='top',linespacing=1.02,**HEAVY)
    fig.text(0.062,0.802,sub,fontsize=18.5,color=INK,ha='left',va='top',linespacing=1.3)
    return fig,ax
def axis_labels(ax,extra=None):
    DASH=(0,(5,3))
    if base=='coin':
        t=[50,100]; l=['50\ncoin flip','100\nsame\nranking']; ax.axhline(50,color=INK,lw=2.4,zorder=6)
    else:
        t=[0,50,100]; l=['0\nopposite','50\ncoin flip','100\nsame\nranking']
        ax.axhline(0,color=INK,lw=1.6,zorder=6)
        if lum(NEU)<0.25:
            ax.axhline(50,color=INK,lw=2.0,ls=DASH,zorder=2)    # black in the gaps, behind dark bars
            ax.axhline(50,color=SURF,lw=2.0,ls=DASH,zorder=5)   # white where it crosses a dark bar
        else: ax.axhline(50,color=INK,lw=2.0,ls=DASH,zorder=5)
    if extra: t.append(extra[0]); l.append(extra[1])
    ax.set_yticks(t); ax.set_yticklabels(l,fontsize=13,color=INK,linespacing=1.2)
# ---- slide 1 ----
F=[('Science',A['science'][0],A['science'][3]),('Coding',A['coding'][0],A['coding'][3]),('Office\nwork',A['office work'][0],A['office work'][3]),('Finance',A['finance'][0],A['finance'][3]),('Legal',C['legal'][1]*100,5)]
fig,ax=frame("The Benchmark\nof Benchmarks","How often do two benchmarks in the same field\nagree on which AI is better?",len(F)); axis_labels(ax)
for x,(lab,v,n) in enumerate(F):
    hot=lab=='Legal'
    rbar(ax,x,0.74,B0,v,ACC if hot else NEU)
    ax.text(x,up(v),f"{v:.0f}",ha='center',va='bottom',fontsize=48 if hot else 31,color=INK,zorder=7,**HEAVY)
    ax.text(x,B0-0.05*span,lab,ha='center',va='top',fontsize=18,color=INK,linespacing=1.12,fontweight='bold' if hot else 'normal')
    ax.text(x,B0-0.215*span,f"{n} benchmarks",ha='center',va='top',fontsize=11.5,color=INK)
fig.savefig(f"{OUT}/slide1{SUF}.png",facecolor=SURF); plt.close(fig)
# ---- slide 2 ----
NAME={'Vals Legal Research':'Vals\nLegal\nResearch','Mercor APEX law':'Mercor\nAPEX','Harvey LAB':'Harvey\nLAB','Legora BAR':'Legora\nBAR','Certera':'Certera'}
legal=sorted(C['per_legal'].items(),key=lambda kv:NAME[kv[0]].lower()); coding=A['coding'][0]
fig,ax=frame("Legal\nBenchmarks","How often does each one agree with the other four\non which AI is better?",len(legal)); axis_labels(ax,(coding,f"{coding:.0f}\ncoding"))
ax.axhline(coding,color=NEU,lw=4,zorder=2)
for x,(k,v) in enumerate(legal):
    rbar(ax,x,0.74,B0,v*100,ACC)
    ax.text(x,up(v*100),f"{v*100:.0f}",ha='center',va='bottom',fontsize=30,color=INK,zorder=7,**HEAVY)
    ax.text(x,B0-0.05*span,NAME[k],ha='center',va='top',fontsize=16.5,color=INK,linespacing=1.12)
    if k=='Harvey LAB': ax.text(x,B0-0.215*span,'run by Vals',ha='center',va='top',fontsize=11.5,color=INK)
fig.savefig(f"{OUT}/slide2{SUF}.png",facecolor=SURF); plt.close(fig)
print('ok',base,NEU,ACC)
