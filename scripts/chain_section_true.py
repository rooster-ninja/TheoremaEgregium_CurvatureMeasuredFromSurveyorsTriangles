import json,math,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from pyproj import Geod
g=Geod(ellps='WGS84'); BG='#f6f1e7'; INK='#1d1d1b'; MUT='#5a5650'
R=json.load(open('rule_results.json')); per={p['survey']:p for p in R['per']}
ch=json.load(open('chain_results.json'))
rows={(r['survey'],r['name']):r for r in json.load(open('rows_t.json')) if r['E'] is not None}
START={'US 39th parallel':('Cape May',-74.96,38.93),'US Eastern Oblique':('Calais',-67.1,45.1),'Maclear, Cape 1837–48':('North End',18.33,-29.74)}
COL={'US 39th parallel':'#2a78d6','US Eastern Oblique':'#eb6834','Maclear, Cape 1837–48':'#1baf7a'}
def sag(x,L,R): return np.sqrt(R*R-(x-L/2)**2)-math.sqrt(R*R-(L/2)**2)
fig=plt.figure(figsize=(14,7.2),dpi=160,facecolor=BG)
# common km scale: 39th parallel spans full width
Lmax=4142*1.04; W=0.9; left=0.05
tops=[0.64,0.40,0.22]
for (sv,(nm,lo0,la0)),top in zip(START.items(),tops):
    p=per[sv]; T=[rows[(sv,n)] for n in ch[sv]['names']]
    d=np.array([g.inv(lo0,la0,r['lon'],r['lat'])[2]/1e3 for r in T]); L=d.max()
    Rm=1/math.sqrt(p['K'])/1e3; x=np.linspace(0,L,600); y=sag(x,L,Rm); h=y.max()
    w=W*L/Lmax; ht_in=(w*14)*(h*1.15)/(L*1.0)/7.2     # equal aspect in figure fraction
    ax=fig.add_axes([left,top,w,max(ht_in,0.004)]); ax.set_facecolor(BG)
    ax.fill_between(x,0,y,color=COL[sv],alpha=0.18,lw=0)
    ax.plot(x,y,color=COL[sv],lw=1.6); ax.plot([0,L],[0,0],color=MUT,lw=1)
    ax.set_xlim(0,L); ax.set_ylim(0,h*1.15); ax.set_aspect('equal'); ax.axis('off')
    fig.text(left,top+max(ht_in,0.004)+0.035,f"{sv}: {L:,.0f} km of chain from {nm}",fontsize=10.5,color=INK)
    fig.text(left,top+max(ht_in,0.004)+0.012,f"surface drops {h:,.1f} km below the straight end-to-end line at mid-chain  ·  measured R = {Rm:,.0f} km  ·  true scale, no exaggeration",fontsize=9,color=MUT)
# scale bar
sb=fig.add_axes([left,0.08,W*1000/Lmax,0.02]); sb.plot([0,1000],[0,0],color=INK,lw=2); sb.plot([0,0],[-1,1],color=INK,lw=1.5); sb.plot([1000,1000],[-1,1],color=INK,lw=1.5)
sb.set_xlim(0,1000); sb.set_ylim(-1,1); sb.axis('off'); fig.text(left,0.05,'1,000 km  (same scale in every direction and for all three chains)',fontsize=9,color=MUT)
fig.text(0.02,0.95,'THE CURVE UNDER EACH CHAIN · TRUE SCALE',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.savefig('chain_section_true.png',facecolor=BG)
