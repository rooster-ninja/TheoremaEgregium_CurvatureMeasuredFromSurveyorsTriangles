import json,math,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
S=json.load(open('summary.json')); BG='#f6f1e7'; INK='#1d1d1b'
sm=sorted(S['summary'],key=lambda s:s['sq'])
birge=math.sqrt(S['chi']/(len(sm)-1)); qg=S['qg']; sqg=S['sqg']*birge
fig,ax=plt.subplots(figsize=(11,5.6),dpi=160,facecolor=BG); ax.set_facecolor(BG)
for i,s in enumerate(sm):
    y=len(sm)-i
    ax.errorbar(s['q'],y,xerr=s['sq'],fmt='o',ms=7,color='#2a78d6',ecolor='#2a78d6',elinewidth=2,capsize=0)
    ax.text(-0.62,y,f"{s['survey']}",va='center',ha='left',fontsize=10,color=INK)
    ax.text(2.02,y,f"n={s['n']}",va='center',ha='right',fontsize=9,color='#55524a',family='monospace')
ax.axvspan(qg-sqg,qg+sqg,color='#eb6834',alpha=0.25,lw=0)
ax.axvline(qg,color='#eb6834',lw=2); ax.axvline(1,color=INK,lw=1,ls=(0,(3,3))); ax.axvline(0,color='#8a8a85',lw=1)
ax.text(qg+0.03,len(sm)+0.75,f'pooled {qg:.3f} ± {sqg:.3f}',color='#b24a1e',fontsize=10)
ax.text(1.0,0.2,'ellipsoid',ha='center',fontsize=9,color=INK); ax.text(0,0.2,'flat plane',ha='center',fontsize=9,color='#55524a')
ax.set_xlim(-0.65,2.05); ax.set_ylim(-0.1,len(sm)+1.2); ax.set_yticks([])
for k in ('top','right','left'): ax.spines[k].set_visible(False)
ax.set_xlabel('K_intrinsic / K_ellipsoid   (observed angle excess ÷ area, relative to 1/MN)',color=INK)
fig.text(0.02,0.95,'RATIO OF MEASURED TO EXTRINSIC CURVATURE · ±1σ',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.subplots_adjust(left=0.02,right=0.98,top=0.9,bottom=0.12)
fig.savefig('curvature_ratio.png',facecolor=BG)
print(birge,qg,sqg)
