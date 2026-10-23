import json,math,re,html,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
RAD=math.pi/180/3600
rows=[r for r in json.load(open('rows_t.json')) if r['E'] is not None]
ORDER=['US 39th parallel','US Eastern Oblique','Maclear, Cape 1837–48','Europe 52°N (Helmert)','Transvaal–Rhodesia','India GTS meridional','England OS 1787–96','Anglo-French 1787','Cassini–Lacaille 1739']
stats={}
for sv in ORDER:
    S=[r for r in rows if r['survey']==sv]
    res=np.array([r['E']-r['area']*r['Kref']/RAD for r in S]); mx=np.array([max(r['sides'].values())/1e3 if r['sides'] else np.nan for r in S])
    sc=1.4826*np.median(np.abs(res-np.median(res)))
    stats[sv]=dict(n=len(S),res=res,mx=mx,sclos=sc,sang=sc/math.sqrt(3),rms=float(np.sqrt(np.mean(res**2))))
# Helmert per-angle corrections v (final - observed)
d=json.load(open('data.json')); v=[]
for p in d[3]['polys']:
    v+= [float(x.replace(',','.')) for x in re.findall(r'v ([+-]?[\d,]+)\\?"',html.unescape(p['d']))]
v=np.array(v)
print('Helmert per-angle corrections: n=%d  rms %.2f"  median|v| %.2f"  max %.2f"'%(len(v),np.sqrt(np.mean(v**2)),np.median(np.abs(v)),np.abs(v).max()))
for sv in ORDER: s=stats[sv]; print(f"{sv:24s} n={s['n']:4d} σ_closure={s['sclos']:5.2f}\"  σ_angle≈{s['sang']:5.2f}\"  rms={s['rms']:5.2f}")
json.dump({k:dict(n=v_['n'],sclos=v_['sclos'],sang=v_['sang']) for k,v_ in stats.items()},open('angle_err.json','w'))
# ---- figure: small-multiple histograms of closure residuals
BG='#f6f1e7'; INK='#1d1d1b'; MUT='#5a5650'; BLUE='#2a78d6'
show=ORDER[:8]
fig,axs=plt.subplots(2,4,figsize=(14,6.6),dpi=160,facecolor=BG,sharex=True)
bins=np.arange(-8,8.01,0.5)
for ax,sv in zip(axs.flat,show):
    s=stats[sv]; ax.set_facecolor(BG)
    ax.hist(np.clip(s['res'],-7.99,7.99),bins=bins,color=BLUE,edgecolor=BG,lw=1)
    xs=np.linspace(-8,8,200); ax.plot(xs,len(s['res'])*0.5*np.exp(-xs**2/(2*s['sclos']**2))/(s['sclos']*math.sqrt(2*math.pi)),color=INK,lw=1.2)
    ax.axvline(0,color='#8a8a85',lw=0.8)
    ax.set_title(sv,fontsize=10.5,color=INK,loc='left')
    ax.text(0.98,0.95,f"per angle ±{s['sang']:.2f}″\nclosure ±{s['sclos']:.2f}″\nn = {s['n']}",transform=ax.transAxes,ha='right',va='top',fontsize=9,color=MUT,family='monospace')
    for k in ('top','right'): ax.spines[k].set_visible(False)
    ax.tick_params(labelsize=8.5)
for ax in axs[1]: ax.set_xlabel('closure miss (″)',fontsize=9.5,color=INK)
fig.text(0.02,0.965,'HOW FAR EACH TRIANGLE MISSES 180° + EXCESS · OBSERVED ANGLES',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.text(0.02,0.925,'Per-angle error ≈ closure spread ÷ √3. Curve: normal with the robust σ.',fontsize=10,color=MUT)
fig.subplots_adjust(top=0.86,left=0.04,right=0.99,bottom=0.09,hspace=0.38,wspace=0.18)
fig.savefig('angle_error.png',facecolor=BG)
# ---- figure: per-angle sigma dot plot with what 1" means at range
fig,ax=plt.subplots(figsize=(11,5.2),dpi=160,facecolor=BG); ax.set_facecolor(BG)
ys=list(range(len(ORDER)))[::-1]
for y,sv in zip(ys,ORDER):
    s=stats[sv]; ax.plot([0,s['sang']],[y,y],color='#d9d1bf',lw=6,solid_capstyle='round'); ax.plot(s['sang'],y,'o',color=BLUE,ms=8)
    ax.text(-0.15,y,sv,ha='right',va='center',fontsize=10,color=INK)
    ax.text(s['sang']*1.06+0.04,y,f"±{s['sang']:.2f}″",va='center',fontsize=9.5,color=MUT,family='monospace')
ax.plot(np.sqrt(np.mean(v**2)),ys[ORDER.index('Europe 52°N (Helmert)')]-0.35,'D',color='#eb6834',ms=6)
ax.text(np.sqrt(np.mean(v**2))*1.06+0.05,ys[ORDER.index('Europe 52°N (Helmert)')]-0.35,f"Helmert's printed corrections, rms ±{np.sqrt(np.mean(v**2)):.2f}″",va='center',fontsize=8.5,color='#b24a1e')
ax.set_xscale('symlog',linthresh=1); ax.set_xlim(0,20); ax.set_ylim(-0.8,len(ORDER)-0.3); ax.set_yticks([])
ax.set_xticks([0,0.5,1,2,5,10,20]); ax.set_xticklabels(['0','0.5″','1″','2″','5″','10″','20″'])
for k in ('top','right','left'): ax.spines[k].set_visible(False)
ax.set_xlabel('one-sigma error of a single observed angle (arc-seconds)',color=INK)
fig.text(0.02,0.95,'ANGLE PRECISION BY SURVEY · 1″ = 0.24 m AT 50 KM, 1.4 m AT 294 KM',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.subplots_adjust(top=0.9,left=0.27,right=0.97,bottom=0.12)
fig.savefig('angle_sigma.png',facecolor=BG)
