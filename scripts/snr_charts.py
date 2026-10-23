import json,math,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
RAD=math.pi/180/3600; BG='#f6f1e7'; INK='#1d1d1b'; MUT='#5a5650'
R=json.load(open('rule_results.json')); H=R['head']; HR=json.load(open('headline_rows.json'))
allrows=[r for r in json.load(open('rows_t.json')) if r['E'] is not None]
ORDER=['US 39th parallel','US Eastern Oblique','Maclear, Cape 1837–48','Europe 52°N (Helmert)','Transvaal–Rhodesia','India GTS meridional','England OS 1787–96']
COL=dict(zip(ORDER,['#2a78d6','#eb6834','#1baf7a','#eda100','#e87ba4','#008300','#6250d6']))
fig,ax=plt.subplots(figsize=(11,6.4),dpi=160,facecolor=BG); ax.set_facecolor(BG)
kept={(r['survey'],r['name']) for r in HR}
drop=[r for r in allrows if (r['survey'],r['name']) not in kept]
ax.scatter([r['area']/1e6 for r in drop],[r['E'] for r in drop],s=9,color='#b9b4a8',lw=0,label=f'below SNR 2 or excluded (n={len(drop)})',zorder=1)
for sv in ORDER:
    S=[r for r in HR if r['survey']==sv]
    if not S: continue
    ax.scatter([r['A']/1e6 for r in S],[r['E'] for r in S],s=22,color=COL[sv],edgecolor=BG,lw=0.6,label=f'{sv} ({len(S)})',zorder=3)
x=np.linspace(0,15000,10)
ax.plot(x,H['K']*x*1e6/RAD,color=INK,lw=2,zorder=4)
ax.plot(x,H['Kref']*x*1e6/RAD,color=INK,lw=1,ls=(0,(4,3)),zorder=4)
ax.text(14800,H['K']*14.8e9/RAD-7,f"fit K = {H['K']*1e14:.3f} ×10⁻¹⁴ m⁻²",ha='right',va='top',color=INK,fontsize=10)
ax.text(11500,H['Kref']*11.5e9/RAD+3,'ellipsoid 1/(MN)',ha='right',color=INK,fontsize=9.5)
ax.axhline(0,color='#8a8a85',lw=0.8)
ax.set_xlabel('triangle area from printed sides (km²)',color=INK); ax.set_ylabel('observed Σangles − 180° (arc-seconds)',color=INK)
for k in ('top','right'): ax.spines[k].set_visible(False)
ax.grid(color='#e3dccb',lw=0.6); ax.set_axisbelow(True)
ax.legend(frameon=False,fontsize=9,loc='upper left',ncol=1)
fig.text(0.07,0.95,'MAIN RESULT · SNR ≥ 2 · PROVENANCE-WEIGHTED',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.subplots_adjust(top=0.91,left=0.08,right=0.97,bottom=0.1)
fig.savefig('snr_fit.png',facecolor=BG)

# forest: sensitivity + per survey
fig,ax=plt.subplots(figsize=(11,7.2),dpi=160,facecolor=BG); ax.set_facecolor(BG)
items=[('Result (declared rule)',H['q'],H['sq'],'h')]+[(l,o['q'],o['sq'],'s') for l,o in R['sens'] if l!='SNR ≥ 2']
items+=[(None,None,None,'gap')]+[(p['survey']+f"  (n={p['n']}, SNR {p['snr']:.1f})",p['q'],p['sq'],'p') for p in sorted(R['per'],key=lambda p:p['sq'])]
y=len(items)
for lab,q,s,kind in items:
    y-=1
    if kind=='gap': ax.text(-0.02,y,'BY SURVEY, INSIDE THE RESULT CUT',family='monospace',fontsize=8.5,color='#2a5fa8',va='center',ha='right',transform=ax.get_yaxis_transform()); continue
    c='#b24a1e' if kind=='h' else ('#2a78d6' if kind=='p' else INK)
    ax.errorbar(q,y,xerr=s,fmt='o',ms=7 if kind=='h' else 5.5,color=c,ecolor=c,elinewidth=2,capsize=0)
    ax.text(-0.02,y,lab,va='center',ha='right',fontsize=10,color=INK,fontweight='bold' if kind=='h' else 'normal',transform=ax.get_yaxis_transform())
    ax.text(1.555,y,f"{q:.3f} ± {s:.3f}",va='center',ha='right',fontsize=9,color=MUT,family='monospace')
ax.axvline(1,color=INK,lw=1,ls=(0,(3,3))); ax.text(1,-0.9,'ellipsoid',ha='center',fontsize=9,color=INK)
ax.set_xlim(0.55,1.56); ax.set_ylim(-1.3,len(items)); ax.set_yticks([])
for k in ('top','right','left'): ax.spines[k].set_visible(False)
ax.set_xlabel('K_intrinsic / K_ellipsoid',color=INK)
ax.set_xticks([0.8,0.9,1.0,1.1,1.2,1.3])
fig.text(0.02,0.96,'SENSITIVITY OF THE RESULT TO EVERY CHOICE IN THE RULE · ±1σ',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.subplots_adjust(top=0.93,left=0.36,right=0.98,bottom=0.09)
fig.savefig('sensitivity.png',facecolor=BG)
