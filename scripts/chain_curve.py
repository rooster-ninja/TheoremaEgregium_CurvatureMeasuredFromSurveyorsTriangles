# Cumulative excess along each chain: observed vs expected (area x K_ellipsoid), non-overlapping triangles.
import json,math,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from pyproj import Geod
g=Geod(ellps='WGS84'); RAD=math.pi/180/3600; BG='#f6f1e7'; INK='#1d1d1b'; MUT='#5a5650'
ch=json.load(open('chain_results.json')); sig=json.load(open('angle_err.json'))
rows={(r['survey'],r['name']):r for r in json.load(open('rows_t.json')) if r['E'] is not None}
START={'US 39th parallel':('Cape May, NJ',-74.96,38.93),'US Eastern Oblique':('Calais, ME',-67.1,45.1),'Maclear, Cape 1837–48':('North End',18.33,-29.74)}
COL={'US 39th parallel':'#2a78d6','US Eastern Oblique':'#eb6834','Maclear, Cape 1837–48':'#1baf7a'}
fig,axs=plt.subplots(3,1,figsize=(12,12),dpi=160,facecolor=BG)
for ax,sv in zip(axs,START):
    ax.set_facecolor(BG); nm,lo0,la0=START[sv]; s=sig[sv]['sclos']
    T=[rows[(sv,n)] for n in ch[sv]['names']]
    for r in T:
        r['d']=g.inv(lo0,la0,r['lon'],r['lat'])[2]/1e3
        r['A']=r['A_side'] if (r.get('A_side') and r['tier']!='C') else r['area']
    T.sort(key=lambda r:r['d'])
    d=np.array([r['d'] for r in T]); Eo=np.cumsum([r['E'] for r in T]); Ep=np.cumsum([r['A']*r['Kref']/RAD for r in T]); n=np.arange(1,len(T)+1)
    band=2*s*np.sqrt(n)
    ax.fill_between(d,Ep-band,Ep+band,color='#e3dccb',lw=0,step='post',label='expected ± 2σ (angle noise, upper bound)')
    ax.step(d,Ep,where='post',color=INK,lw=2,label='expected: Σ area × K(ellipsoid)')
    ax.step(d,Eo,where='post',color=COL[sv],lw=1.8,label='observed: Σ (angles − 180°)')
    ax.plot(d,np.zeros_like(d),color='#8a8a85',lw=0.8,ls=(0,(3,3)),label='flat plane (K = 0)')
    o=ch[sv]
    tx,ty,ha=(0.99,0.06,'right') if sv=='US 39th parallel' else (0.01,0.9,'left')
    ax.text(tx,ty,f"end of chain: {Eo[-1]:,.0f}″ observed vs {Ep[-1]:,.0f}″ expected  ·  K/K_ell = {o['q']:.3f} ± {o['sq']:.3f}",transform=ax.transAxes,ha=ha,fontsize=9.5,color=INK)
    ax.set_title(f"{sv}  ·  {len(T)} non-overlapping triangles, {o['A']:,.0f} km²",loc='left',fontsize=10.5,color=INK)
    ax.set_ylabel('cumulative excess (″)',color=INK); ax.set_xlabel(f'distance of triangle from {nm} (km)',color=MUT,fontsize=9)
    for k in ('top','right'): ax.spines[k].set_visible(False)
    ax.grid(color='#e3dccb',lw=0.6); ax.set_axisbelow(True); ax.set_xlim(0,d.max()*1.01); ax.set_ylim(min(-20,Eo.min()-10),max(Ep.max(),Eo.max())*1.08)
    if sv=='US 39th parallel': ax.legend(frameon=False,fontsize=9,loc='upper left')
fig.text(0.02,0.975,'CURVATURE EXCESS ACCUMULATED ALONG EACH CHAIN',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.text(0.02,0.958,'Triangles taken in order of distance from the chain start; each step adds one triangle. A flat Earth would stay on the dashed zero line.',fontsize=10,color=MUT)
fig.subplots_adjust(top=0.93,left=0.08,right=0.98,bottom=0.05,hspace=0.42)
fig.savefig('chain_curve.png',facecolor=BG)
