import json,math,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP
from matplotlib.colors import TwoSlopeNorm
RAD=math.pi/180/3600; BG='#f6f1e7'; INK='#1d1d1b'; MUT='#5a5650'
ch=json.load(open('chain_results.json')); sig=json.load(open('angle_err.json'))
rows=[r for r in json.load(open('rows_t.json')) if r['E'] is not None]
CORE=[('US 39th parallel',(15,4.6)),('US Eastern Oblique',(7,8)),('Maclear, Cape 1837–48',(3.2,6))]
fig=plt.figure(figsize=(15,10),dpi=160,facecolor=BG)
axes=[fig.add_axes([0.05,0.62,0.92,0.2]),fig.add_axes([0.05,0.1,0.5,0.42]),fig.add_axes([0.66,0.1,0.3,0.42])]
norm=TwoSlopeNorm(vmin=-3,vcenter=0,vmax=3); cmap=plt.get_cmap('RdBu_r')
for ax,(sv,_) in zip(axes,CORE):
    ax.set_facecolor(BG); S=[r for r in rows if r['survey']==sv]; chosen=set(ch[sv]['names'])
    for r in S:
        xy=[(c[0],c[1]) for c in r['coords'][:3]]
        if r['name'] in chosen:
            z=(r['E']-r['area']*r['Kref']/RAD)/sig[sv]['sclos']
            ax.add_patch(MP(xy,closed=True,fc=cmap(norm(z)),ec=INK,lw=0.35))
        else: ax.add_patch(MP(xy,closed=True,fill=False,ec='#c9c1ad',lw=0.3))
    ax.autoscale_view(); ax.set_aspect(1/math.cos(math.radians(np.mean([r['lat'] for r in S]))),adjustable='datalim')
    for k in ('top','right'): ax.spines[k].set_visible(False)
    ax.tick_params(labelsize=8)
    o=ch[sv]
    ax.set_title(f"{sv}\n{o['n']} non-overlapping of {o['ntot']} triangles, {o['A']:,.0f} km²\nΣ excess {o['E']:,.1f}″ observed vs {o['Epred']:,.1f}″ expected  \n→  K/K_ell = {o['q']:.3f} ± {o['sq']:.3f}",loc='left',fontsize=9.5,color=INK)
sm=plt.cm.ScalarMappable(norm=norm,cmap=cmap); cax=fig.add_axes([0.3,0.05,0.4,0.013]); cb=fig.colorbar(sm,cax=cax,orientation='horizontal')
cb.set_label('triangle: (observed − expected excess) ÷ noise',fontsize=9); cb.ax.tick_params(labelsize=8)
c=ch['combined']
fig.text(0.02,0.97,'WHOLE-CHAIN MEASUREMENT · SUM OF NON-OVERLAPPING TRIANGLES',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.text(0.02,0.945,f"Core three combined: {c['n']} triangles, {c['A']:,.0f} km², Σ excess {c['E']:,.0f}″ observed vs {c['Epred']:,.0f}″ expected (±{c['noise']:.0f}″)  →  K/K_ell = {c['q']:.3f} ± {c['sq']:.3f}, R = {c['R']:,.0f} km",fontsize=10.5,color=INK)
fig.savefig('chain.png',facecolor=BG)
