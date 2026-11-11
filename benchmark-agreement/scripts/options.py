import sys,io,contextlib,json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0,'scripts')
with contextlib.redirect_stdout(io.StringIO()):
    from final import T,LEGAL,CODE,cohort
C=json.load(open('data/concord.json'))
INK='#0b0b0b'; SEC='#52514e'; MUTE='#8a8983'; SURF='#fcfcfb'; BLUE='#2a78d6'; ORANGE='#eb6834'; PALE='#cfe0f6'; G1='#e9e8e3'; G2='#d3d2cc'
OUT='/home/user/lawyerbenchmarks/benchmark-agreement/'
NAME={'gemini-4-argon':'Gemini 4 Argon','opus-5-5':'Claude Opus 5.5','gpt-6-astra':'GPT-6 Astra','gpt-6-1-sol':'GPT-6.1 Sol','gemini-3-8-flash':'Gemini 3.8 Flash','muse-wonder':'Muse Wonder','muse-wonder-full':'Muse Wonder Full','grok-4-7':'Grok 4.7','gemini-4-carbon':'Gemini 4 Carbon','gpt-6-sol':'GPT-6 Sol','muse-ember':'Muse Ember','muse-spark-open':'Muse Spark Open','fable-5-2':'Claude Fable 5.2'}
COLS=[('Harvey\nLAB','Harvey LAB'),('Vals','Vals Legal Research'),('Mercor\nAPEX','Mercor APEX law'),('Legora','Legora BAR'),('Certera','Certera')]
com=[m for m in cohort if all(m in T[LEGAL[k]] for _,k in COLS)]; N=len(com)
rank={k:{m:i+1 for i,m in enumerate(sorted(com,key=lambda m:-T[LEGAL[k]][m]))} for _,k in COLS}
# ---------- Option 1: winners grid ----------
winners=[]
for _,k in COLS:
    w=min(com,key=lambda m:rank[k][m])
    if w not in winners: winners.append(w)
fig,ax=plt.subplots(figsize=(10,8.2),dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
plt.subplots_adjust(left=0.27,right=0.96,top=0.70,bottom=0.09)
for r,m in enumerate(winners):
    for c,(_,k) in enumerate(COLS):
        v=rank[k][m]
        if v==1: fc,tc=BLUE,'white'
        elif v<=3: fc,tc=PALE,INK
        else: fc,tc=G1,INK
        ax.scatter(c,r,s=5200,color=fc,linewidths=0,zorder=2)
        ax.text(c,r+0.015,str(v),ha='center',va='center',fontsize=30 if v==1 else 26,color=tc,fontweight='bold',zorder=3)
    ax.text(-0.62,r,NAME[m],ha='right',va='center',fontsize=17,color=INK,fontweight='bold')
for c,(lab,_) in enumerate(COLS): ax.text(c,-0.72,lab,ha='center',va='bottom',fontsize=14,color=SEC,linespacing=1.1)
ax.set_xlim(-0.55,len(COLS)-0.45); ax.set_ylim(len(winners)-0.45,-0.6); ax.axis('off')
fig.text(0.04,0.955,"Which AI is the best lawyer?",fontsize=30,color=INK,fontweight='bold',ha='left',va='top')
fig.text(0.04,0.875,"Five legal benchmarks. Four different winners.",fontsize=17,color=SEC,ha='left',va='top')
fig.text(0.04,0.035,f"Rank out of the {N} AI models all five benchmarks tested. Nov 2026.",fontsize=10.5,color=MUTE,ha='left',va='bottom')
fig.text(0.96,0.035,"lawyerbenchmarks.com",fontsize=10.5,color=MUTE,ha='right',va='bottom')
fig.savefig(OUT+'option1-winners.png',facecolor=SURF); plt.close(fig)
print('winners',winners,{m:[rank[k][m] for _,k in COLS] for m in winners},'N',N)
# ---------- Option 2: 10 dots ----------
rows=[('Two coding benchmarks',round(C['coding'][1]*10),ORANGE),('Two legal benchmarks',round(C['legal'][1]*10),BLUE),('A coin flip',5,MUTE)]
fig,ax=plt.subplots(figsize=(10,6.6),dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
plt.subplots_adjust(left=0.04,right=0.96,top=0.66,bottom=0.1)
for r,(lab,k,col) in enumerate(rows):
    y=r*1.75
    ax.text(0.02,y-0.72,lab,ha='left',va='center',fontsize=17,color=INK,fontweight='bold')
    for i in range(10):
        ax.scatter(i+0.5,y,s=2000,color=col if i<k else G1,linewidths=0)
    ax.text(10.35,y,f"{k} in 10",ha='left',va='center',fontsize=22,color=INK,fontweight='bold')
ax.set_xlim(0,12.2); ax.set_ylim(4.15,-1.1); ax.axis('off')
fig.text(0.04,0.95,"Pick two AIs. Ask two benchmarks\nwhich one is better.",fontsize=27,color=INK,fontweight='bold',ha='left',va='top',linespacing=1.15)
fig.text(0.04,0.755,"How often do they agree?",fontsize=17,color=SEC,ha='left',va='top')
fig.text(0.04,0.035,f"Legal {C['legal'][1]*100:.0f}%, coding {C['coding'][1]*100:.0f}%. 37 AI models, 5 legal and 8 coding benchmarks. Nov 2026.",fontsize=10.5,color=MUTE,ha='left',va='bottom')
fig.text(0.96,0.035,"lawyerbenchmarks.com",fontsize=10.5,color=MUTE,ha='right',va='bottom')
fig.savefig(OUT+'option2-ten-dots.png',facecolor=SURF); plt.close(fig)
# ---------- Option 3: slope, Harvey LAB vs Certera ----------
a,b=LEGAL['Harvey LAB'],LEGAL['Certera']
ms=[m for m in cohort if m in T[a] and m in T[b]]; n=len(ms)
ra={m:i+1 for i,m in enumerate(sorted(ms,key=lambda m:-T[a][m]))}; rb={m:i+1 for i,m in enumerate(sorted(ms,key=lambda m:-T[b][m]))}
hi=[m for m in ms if ra[m]<=3 or rb[m]<=3]
fig,ax=plt.subplots(figsize=(9,9.6),dpi=200); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
plt.subplots_adjust(left=0.30,right=0.70,top=0.76,bottom=0.07)
for m in ms:
    h=m in hi; col=(BLUE if ra[m]<=3 else ORANGE) if h else G2
    ax.plot([0,1],[ra[m],rb[m]],color=col,lw=3.2 if h else 1.2,zorder=3 if h else 1,solid_capstyle='round')
    ax.scatter([0,1],[ra[m],rb[m]],s=120 if h else 22,color=col,zorder=4 if h else 2,linewidths=0)
    if h:
        ax.text(-0.07,ra[m],f"{NAME.get(m,m)}  {ra[m]}",ha='right',va='center',fontsize=12.5,color=INK,fontweight='bold')
        ax.text(1.07,rb[m],f"{rb[m]}  {NAME.get(m,m)}",ha='left',va='center',fontsize=12.5,color=INK,fontweight='bold')
ax.text(0,-0.1,"Harvey LAB",ha='center',va='bottom',fontsize=16,color=INK,fontweight='bold'); ax.text(1,-0.1,"Lawyers' votes",ha='center',va='bottom',fontsize=16,color=INK,fontweight='bold')
ax.set_xlim(-0.05,1.05); ax.set_ylim(n+0.6,-0.2); ax.axis('off')
fig.text(0.04,0.965,"Harvey's benchmark vs. lawyers' votes",fontsize=26,color=INK,fontweight='bold',ha='left',va='top')
fig.text(0.04,0.905,f"The same {n} AI models, ranked 1st to {n}th.",fontsize=16,color=SEC,ha='left',va='top')
fig.text(0.04,0.025,"Harvey LAB as run by Vals. Lawyers' votes: Certera. Nov 2026.",fontsize=10.5,color=MUTE,ha='left',va='bottom')
fig.text(0.96,0.025,"lawyerbenchmarks.com",fontsize=10.5,color=MUTE,ha='right',va='bottom')
fig.savefig(OUT+'option3-harvey-vs-lawyers.png',facecolor=SURF); plt.close(fig)
print('slope n',n,{NAME.get(m,m):(ra[m],rb[m]) for m in hi})
