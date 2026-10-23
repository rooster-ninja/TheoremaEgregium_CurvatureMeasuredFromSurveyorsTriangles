import math,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from pyproj import Geod
g=Geod(ellps='WGS84'); BG='#f6f1e7'; INK='#1d1d1b'; MUT='#5a5650'; BLUE='#2a5fa8'
A=('Mount Shasta',41.408944,-122.194997,4.322); B=('Mount Helena (Mount Saint Helena)',38.669341,-122.633488,1.323)
L=g.inv(A[2],A[1],B[2],B[1])[2]/1e3
lat=math.radians((A[1]+B[1])/2); a=6378.137; f=1/298.257223563; e2=f*(2-f); s=math.sin(lat)**2
R=math.sqrt(a*(1-e2)/(1-e2*s)**1.5*a/math.sqrt(1-e2*s)); k=0.13
x=np.linspace(0,L,800); bul=x*(L-x)/(2*R)
los=A[3]+(B[3]-A[3])*x/L; ray=los+k*x*(L-x)/(2*R)
clr_geo=los-bul; clr_ray=ray-bul
i=np.argmin(clr_geo); j=np.argmin(clr_ray)
fig,ax=plt.subplots(figsize=(14,6.4),dpi=160,facecolor=BG); ax.set_facecolor(BG)
ax.fill_between(x,-0.6,bul,color='#d9cfb8',lw=0,zorder=1); ax.plot(x,bul,color='#8a6d3b',lw=1.6,zorder=2,label='sea-level surface (Earth curving away)')
ax.plot([0,L],[0,0],color=MUT,lw=0.9,ls=(0,(4,3)),zorder=2,label='flat-Earth reference (straight chord at sea level)')
# schematic mountains at true height, standing on the curved sea level
for (nm,_,_,h),x0,side in [(A,0,1),(B,L,-1)]:
    w=24 if h>3 else 10
    xm=np.linspace(0,w,80); xx=x0+side*xm; base=xx*(L-xx)/(2*R)
    top=base+h*(1-xm/w)**1.5
    ax.fill_between(xx,-0.6,top,color='#a39a86',zorder=3,lw=0)
    ax.plot(x0,h,'^',color=INK,ms=8,zorder=6)
ax.plot(x,los,color=INK,lw=1.1,ls=(0,(2,2)),zorder=4,label='straight line between summits')
ax.plot(x,ray,color=BLUE,lw=2,zorder=5,label=f'heliotrope light path with normal refraction (k = {k})')
ax.annotate('',xy=(L/2,bul.max()),xytext=(L/2,0),arrowprops=dict(arrowstyle='<->',color='#8a6d3b',lw=1.2),zorder=6)
ax.text(L/2+3,bul.max()/2,f'Earth bulge {bul.max()*1000:,.0f} m\nat the midpoint',fontsize=9.5,color='#6b5228',va='center')
ax.annotate('',xy=(x[j],ray[j]),xytext=(x[j],bul[j]),arrowprops=dict(arrowstyle='<->',color=BLUE,lw=1),zorder=6)
ax.text(x[j]-3,(ray[j]+bul[j])/2,f'light passes {clr_ray[j]*1000:,.0f} m\nabove sea level here\n(straight line: {clr_geo[i]*1000:,.0f} m)',fontsize=9,color=BLUE,va='center',ha='right')
ax.text(0,A[3]+0.25,f'{A[0]}\n{A[3]*1000:,.0f} m',fontsize=10,color=INK,ha='left',va='bottom')
ax.text(L,B[3]+0.55,f'{B[0]}\n{B[3]*1000:,.0f} m',fontsize=10,color=INK,ha='right',va='bottom')
ax.set_xlim(-8,L+8); ax.set_ylim(-0.6,5.6)
ax.set_xlabel(f'distance from Mount Shasta (km)  ·  line length {L:,.0f} km ({L/1.609344:,.0f} miles)',color=INK)
ax.set_ylabel('height above sea level at the line ends (km)',color=INK)
for kk in ('top','right'): ax.spines[kk].set_visible(False)
ax.legend(frameon=False,fontsize=9,loc='upper center',ncol=2,bbox_to_anchor=(0.5,1.0))
ex=(L/12.5)/(6.2/5.0)
ax.text(0.995,0.02,f'vertical exaggeration ≈ ×{ex:.0f}  ·  mountain outlines schematic, heights true  ·  terrain between not drawn',transform=ax.transAxes,ha='right',fontsize=8.5,color=MUT,style='italic')
fig.text(0.02,0.96,'HELIOTROPE LINE, MOUNT SHASTA TO MOUNT HELENA, 1879 · EARTH BULGE BETWEEN',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.subplots_adjust(top=0.9,left=0.07,right=0.98,bottom=0.11)
fig.savefig('shasta_line.png',facecolor=BG)
print(f"L={L:.1f} km R={R:.0f} bulge={bul.max()*1000:.0f} m  min clearance geo {clr_geo[i]*1000:.0f} m at {x[i]:.0f} km; refracted {clr_ray[j]*1000:.0f} m at {x[j]:.0f} km; ex {ex:.0f}")
