import json,math,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Patch
RAD=math.pi/180/3600; BG='#f6f1e7'; INK='#1d1d1b'; MUT='#5a5650'
CORE={'US 39th parallel':'#2a78d6','US Eastern Oblique':'#eb6834','Maclear, Cape 1837–48':'#1baf7a'}
sig=json.load(open('angle_err.json'))
rows=[r for r in json.load(open('rows_t.json')) if r['E'] is not None and r['survey'] in CORE]
for r in rows: r['P']=r['area']*r['Kref']/RAD; r['s']=sig[r['survey']]['sclos']
rows.sort(key=lambda r:r['P'])
# ---------- Figure 1: every triangle, sorted by expected excess
fig,ax=plt.subplots(figsize=(13,6.6),dpi=160,facecolor=BG); ax.set_facecolor(BG)
x=np.arange(len(rows)); P=np.array([r['P'] for r in rows]); E=np.array([r['E'] for r in rows]); S=np.array([r['s'] for r in rows])
ax.fill_between(x,-S,S,color='#d9d1bf',lw=0,label='noise: ±1σ closure (angle pointing)',zorder=1)
ax.fill_between(x,-2*S,2*S,color='#ebe4d4',lw=0,zorder=0)
for sv,c in CORE.items():
    idx=[i for i,r in enumerate(rows) if r['survey']==sv]
    ax.errorbar(x[idx],E[idx],yerr=S[idx],fmt='o',ms=2.6,color=c,ecolor=c,elinewidth=0.6,alpha=0.85,label=sv,zorder=3)
ax.plot(x,P,color=INK,lw=1.8,label='signal: expected excess = area × K(ellipsoid)',zorder=4)
cross=int(np.searchsorted(P,2*np.median(S)))
ax.axvline(cross,color=MUT,lw=0.8,ls=(0,(3,3)))
ax.text(cross-8,62,'← signal smaller than\n    2× the noise',ha='right',fontsize=9.5,color=MUT)
ax.text(cross+8,62,f'signal clearly above noise →\n{len(rows)-cross} of {len(rows)} triangles',ha='left',fontsize=9.5,color=MUT)
ax.set_xlim(-5,len(rows)+5); ax.set_ylim(-8,80)
ax.set_xlabel('triangles of the three core surveys, sorted by size (smallest → largest)',color=INK)
ax.set_ylabel('angle excess (arc-seconds)',color=INK)
for k in ('top','right'): ax.spines[k].set_visible(False)
ax.legend(frameon=False,loc='upper left',fontsize=9.5)
fig.text(0.02,0.955,'SIGNAL VS NOISE, TRIANGLE BY TRIANGLE · CORE THREE SURVEYS',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.text(0.02,0.918,'Each dot is one triangle\'s measured excess with its ±1σ error bar. The grey band is the measuring noise around zero.',fontsize=10,color=MUT)
fig.subplots_adjust(top=0.88,left=0.06,right=0.98,bottom=0.1)
fig.savefig('signal_vs_noise.png',facecolor=BG)
print('triangles',len(rows),'above 2x noise',len(rows)-cross)
# ---------- Figure 2: error budget for three triangle sizes (in arc-seconds of excess)
def pick(q):
    i=int(q*(len(rows)-1)); return rows[i]
cases=[('Small triangle',pick(0.10)),('Typical triangle',pick(0.5)),('Largest triangle',rows[-1])]
sclos=np.median(S)
fig,axs=plt.subplots(1,3,figsize=(14,5.8),dpi=160,facecolor=BG,sharex=True)
items_def=lambda P,L,h: [
 ('SIGNAL: curvature excess',P,'sig'),
 ('Angle pointing (closure noise)',sclos,'meas'),
 ('Plumb-line deflection',0.3 if h else 0.1,'est'),
 ('Target height above surface',0.3 if h else 0.02,'est'),
 ('Station height on K (≈0.1%)',P*1e-3,'est'),
 ('Base-line scale error (≈3 ppm → area)',P*6e-6,'stated'),
 ('Assumed radius in printed sides',P*1e-5,'est'),
]
COL={'sig':'#1d1d1b','meas':'#2a78d6','est':'#eda100','stated':'#1baf7a'}
for ax,(lab,r) in zip(axs,cases):
    ax.set_facecolor(BG); L=max(r['sides'].values())/1e3 if r['sides'] else math.sqrt(r['area'])/1e3
    high=r['survey']=='US 39th parallel' and r['P']>20
    items=items_def(r['P'],L,high)
    ys=np.arange(len(items))[::-1]
    for y,(name,v,k) in zip(ys,items):
        ax.barh(y,v,color=COL[k],height=0.62,left=1e-7)
        ax.text(v*1.25,y,f"{v:.3g}″" if v>=0.01 else f"{v:.0e}″".replace("e-0","e-"),va='center',fontsize=8.5,color=MUT,family='monospace')
    ax.set_xscale('log'); ax.set_xlim(1e-7,800)
    ax.set_yticks(ys); ax.set_yticklabels([i[0] for i in items] if ax is axs[0] else ['']*len(items),fontsize=9.5)
    ax.set_title(f"{lab}\n{r['name'][:38]}\n{r['area']/1e6:,.0f} km², longest side {L:.0f} km",fontsize=9.5,color=INK,loc='left')
    for k in ('top','right'): ax.spines[k].set_visible(False)
    ax.set_xticks([1e-6,1e-4,1e-2,1,100]); ax.set_xticklabels(['10⁻⁶″','10⁻⁴″','0.01″','1″','100″'],fontsize=8.5)
    ax.axvline(r['P'],color=INK,lw=0.8,ls=(0,(2,3)))
fig.legend(handles=[Patch(color=COL['sig'],label='what is being measured'),Patch(color=COL['meas'],label='error measured from the data'),Patch(color=COL['stated'],label='error stated by the surveyors'),Patch(color=COL['est'],label='error estimated from physics (rough)')],loc='lower center',ncol=4,frameon=False,fontsize=9.5)
fig.text(0.02,0.96,'ERROR BUDGET VS SIGNAL · ARC-SECONDS OF EXCESS, LOG SCALE',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.subplots_adjust(top=0.8,left=0.2,right=0.98,bottom=0.14,wspace=0.08)
fig.savefig('error_budget.png',facecolor=BG)
for lab,r in cases: print(lab,r['name'],round(r['P'],2),round(r['area']/1e6))
