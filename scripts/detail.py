import json,math,numpy as np,matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
rows=[r for r in json.load(open('rows.json')) if r['fi']==8]
d=json.load(open('data.json'))[8]
BG='#f6f1e7'; INK='#1d1d1b'
lat0=np.mean([p['lat'] for p in d['pts']]); lon0=np.mean([p['lon'] for p in d['pts']])
R=6371.0; EX=12  # curvature exaggeration
def enu(lon,lat):
    x=R*math.radians(lon-lon0)*math.cos(math.radians(lat0)); y=R*math.radians(lat-lat0)
    z=-(x*x+y*y)/(2*R)*EX
    return x,y,z
RAD=math.pi/180/3600; ZS=60  # (x0.1) km per arcsec of excess
fig=plt.figure(figsize=(13,8.2),dpi=160,facecolor=BG); ax=fig.add_subplot(projection='3d',computed_zorder=False); ax.set_facecolor(BG); ax.set_position([-0.08,-0.22,1.16,1.3])
# curved base sheet
X,Y=np.meshgrid(np.linspace(-55,55,23),np.linspace(-125,125,41)); Z=-(X**2+Y**2)/(2*R)*EX
ax.plot_surface(X,Y,Z,color='#e9e2d0',alpha=0.55,linewidth=0,shade=True,zorder=0)
ax.plot_wireframe(X,Y,Z,color='#c9c1ad',linewidth=0.3,rstride=4,cstride=4,zorder=1)
segs=[]
for r in rows:
    P=[enu(c[0],c[1]) for c in r['coords']]
    segs+= [[P[0],P[1]],[P[1],P[2]],[P[2],P[0]]]
ax.add_collection3d(Line3DCollection(segs,colors='#1d1d1b',linewidths=1.0,zorder=3))
for p in d['pts']:
    x,y,z=enu(p['lon'],p['lat']); ax.scatter(x,y,z,s=14,color=INK,zorder=4,depthshade=False)
    ax.text(x,y,z+0.6,p['n'],fontsize=7.5,color='#3b3934',zorder=6)
for r in rows:
    if r['E'] is None: continue
    c=np.mean([enu(cc[0],cc[1]) for cc in r['coords']],axis=0)
    Epred=r['area']*r['Kref']/RAD
    ax.plot([c[0],c[0]],[c[1],c[1]],[c[2],c[2]+Epred*ZS/10],color='#8a8a85',lw=0.8,ls=(0,(2,2)),zorder=6)
    ax.plot([c[0],c[0]],[c[1],c[1]],[c[2],c[2]+r['E']*ZS/ 10],color='#2a78d6',lw=3,solid_capstyle='round',zorder=7)
    ax.scatter(c[0],c[1],c[2]+Epred*ZS/10,marker='D',s=26,color='#eb6834',edgecolor=BG,linewidth=0.8,zorder=8,depthshade=False)
ax.set_xlim(-55,55); ax.set_ylim(-125,125); ax.set_zlim(-25,32); ax.set_box_aspect((110,250,80)); ax.view_init(elev=26,azim=-62)
ax.set_xlabel('east (km)',color='#55524a'); ax.set_ylabel('north (km)',color='#55524a'); ax.set_zticks([])
for a in (ax.xaxis,ax.yaxis,ax.zaxis): a.set_pane_color((0,0,0,0))
ax.grid(False)
fig.text(0.05,0.84,'TRANSVAAL–RHODESIA CONNECTION · GORDON',family='monospace',fontsize=10,color='#2a5fa8')
fig.text(0.05,0.80,'Measured angle excess standing on the curved surface',family='serif',fontsize=21,color=INK)
fig.text(0.05,0.775,f'Surface sag exaggerated ×{EX}.  Blue stem = observed Σangles − 180° per triangle;  orange ◆ = area × K(WGS84).  Stem scale {ZS/10:.0f} km per arc-second; stems pointing down = observed sum below 180°.',fontsize=10,color='#55524a')
fig.savefig('rhodesia_3d.png',facecolor=BG,bbox_inches='tight')

from PIL import Image
im=Image.open('rhodesia_3d.png'); w,h=im.size; im.crop((0,int(h*0.12),w,int(h*0.93))).save('rhodesia_3d.png')
