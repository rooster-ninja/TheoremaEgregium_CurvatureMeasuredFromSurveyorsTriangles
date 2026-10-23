import json,math,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from pyproj import Geod
g=Geod(ellps='WGS84'); RAD=math.pi/180/3600; BG='#f6f1e7'; INK='#1d1d1b'; MUT='#5a5650'
R=json.load(open('rule_results.json')); per={p['survey']:p for p in R['per']}
ch=json.load(open('chain_results.json')); sig=json.load(open('angle_err.json'))
rows={(r['survey'],r['name']):r for r in json.load(open('rows_t.json')) if r['E'] is not None}
START={'US 39th parallel':('Cape May',-74.96,38.93),'US Eastern Oblique':('Calais',-67.1,45.1),'Maclear, Cape 1837–48':('North End',18.33,-29.74)}
COL={'US 39th parallel':'#2a78d6','US Eastern Oblique':'#eb6834','Maclear, Cape 1837–48':'#1baf7a'}
def sag(x,L,R): return np.sqrt(R*R-(x-L/2)**2)-math.sqrt(R*R-(L/2)**2)
# ---------- cross-section
fig=plt.figure(figsize=(13,11),dpi=160,facecolor=BG)
for i,sv in enumerate(START):
    nm,lo0,la0=START[sv]; p=per[sv]
    T=[rows[(sv,n)] for n in ch[sv]['names']]; d=np.array([g.inv(lo0,la0,r['lon'],r['lat'])[2]/1e3 for r in T]); L=d.max()
    Kell=p['K']/p['q']; Rm=1/math.sqrt(p['K'])/1e3; Rlo=1/math.sqrt(p['K']+p['sK'])/1e3; Rhi=1/math.sqrt(p['K']-p['sK'])/1e3; Re=1/math.sqrt(Kell)/1e3
    x=np.linspace(0,L,400)
    ax=fig.add_axes([0.07,0.71-i*0.31,0.6,0.2]); ax.set_facecolor(BG)
    ax.plot(x,sag(x,L,Re),color=INK,lw=1,ls=(0,(4,3)),label=f'ellipsoid, R = {Re:,.0f} km')
    ax.fill_between(x,sag(x,L,Rhi),sag(x,L,Rlo),color=COL[sv],alpha=0.25,lw=0)
    ax.plot(x,sag(x,L,Rm),color=COL[sv],lw=2.2,label=f'measured from the angles, R = {Rm:,.0f} km')
    ax.plot([0,L],[0,0],color=MUT,lw=1.2,label='flat Earth (straight line)')
    ax.plot(d,sag(d,L,Rm),'|',color=INK,ms=7,mew=0.8,alpha=0.6)
    h=sag(np.array([L/2]),L,Rm)[0]
    ax.annotate(f'{h:,.0f} km',xy=(L/2,h),xytext=(L/2,h*0.45),ha='center',fontsize=9,color=INK,arrowprops=dict(arrowstyle='<->',color=MUT,lw=0.8))
    ax.annotate('',xy=(L/2,0),xytext=(L/2,h*0.42),arrowprops=dict(arrowstyle='-',color=MUT,lw=0.8))
    ax.set_xlim(-L*0.02,L*1.02); ax.set_ylim(-h*0.08,h*1.25)
    ax.set_title(f"{sv}: {L:,.0f} km of chain from {nm}  ·  K/K_ell = {p['q']:.3f} ± {p['sq']:.3f}",loc='left',fontsize=10.5,color=INK)
    ax.set_ylabel('height above the\nend-to-end chord (km)',fontsize=9,color=INK); ax.set_xlabel('distance along chain (km)',fontsize=9,color=MUT)
    ex=(L/ (0.6*13))/(h*1.33/(0.2*11)); ax.text(0.01,0.93,f'vertical exaggeration ≈ ×{ex:.0f}',transform=ax.transAxes,ha='left',fontsize=8.5,color=MUT,style='italic')
    for k in ('top','right'): ax.spines[k].set_visible(False)
    ax.legend(frameon=False,fontsize=8.5,loc='upper right',bbox_to_anchor=(1.0,1.02))
    # inset: difference measured - ellipsoid
    bx=fig.add_axes([0.74,0.71-i*0.31,0.23,0.2]); bx.set_facecolor(BG)
    bx.fill_between(x,sag(x,L,Rhi)-sag(x,L,Re),sag(x,L,Rlo)-sag(x,L,Re),color=COL[sv],alpha=0.25,lw=0)
    bx.plot(x,sag(x,L,Rm)-sag(x,L,Re),color=COL[sv],lw=2); bx.axhline(0,color=INK,lw=1,ls=(0,(4,3)))
    bx.set_title('measured − ellipsoid (km)',fontsize=9,color=INK,loc='left'); bx.tick_params(labelsize=8)
    for k in ('top','right'): bx.spines[k].set_visible(False)
fig.text(0.02,0.975,'THE CURVE UNDER EACH CHAIN · DRAWN FROM THE CURVATURE THE ANGLES MEASURED',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.text(0.02,0.955,'Coloured arc: radius from the triangles\' measured K (band ±1σ). Dashed: WGS84 ellipsoid. Grey: flat Earth. Ticks: triangles used. Right: the gap between measured and ellipsoid arcs.',fontsize=9.5,color=MUT)
fig.savefig('chain_section.png',facecolor=BG)
# ---------- excess vs cumulative area (straight-line test)
fig,axs=plt.subplots(1,3,figsize=(14,4.8),dpi=160,facecolor=BG)
for ax,sv in zip(axs,START):
    ax.set_facecolor(BG); T=[rows[(sv,n)] for n in ch[sv]['names']]
    nm,lo0,la0=START[sv]
    for r in T: r['d']=g.inv(lo0,la0,r['lon'],r['lat'])[2]; r['A']=r['A_side'] if (r.get('A_side') and r['tier']!='C') else r['area']
    T.sort(key=lambda r:r['d'])
    A=np.cumsum([r['A'] for r in T])/1e3/1e6; Eo=np.cumsum([r['E'] for r in T]); Ep=np.cumsum([r['A']*r['Kref']/RAD for r in T]); n=np.arange(1,len(T)+1)
    s=sig[sv]['sclos']; ax.fill_between(A,Ep-2*s*np.sqrt(n),Ep+2*s*np.sqrt(n),color='#e3dccb',lw=0)
    ax.plot(A,Ep,color=INK,lw=1.6,label='expected (slope = K ellipsoid)'); ax.plot(A,Eo,color=COL[sv],lw=1.6,label='observed')
    ax.set_title(sv,loc='left',fontsize=10,color=INK); ax.set_xlabel('cumulative area (thousand km²)',fontsize=9,color=INK)
    for k in ('top','right'): ax.spines[k].set_visible(False)
    ax.grid(color='#e3dccb',lw=0.6); ax.set_axisbelow(True); ax.tick_params(labelsize=8.5)
    if ax is axs[0]: ax.set_ylabel('cumulative excess (″)',fontsize=9,color=INK); ax.legend(frameon=False,fontsize=8.5,loc='upper left')
fig.text(0.02,0.95,'STRAIGHT-LINE TEST · CONSTANT CURVATURE GIVES A STRAIGHT LINE AGAINST AREA',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.subplots_adjust(top=0.84,left=0.06,right=0.98,bottom=0.14,wspace=0.2)
fig.savefig('chain_area.png',facecolor=BG)
