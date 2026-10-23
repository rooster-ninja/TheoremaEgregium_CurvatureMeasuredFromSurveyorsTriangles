import json,numpy as np,matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
d=json.load(open('data.json')); rows=json.load(open('rows.json'))
REG={0:'Europe',2:'Europe',3:'Europe',4:'Europe',5:'Europe',1:'Southern Africa',8:'Southern Africa',6:'India',7:'India',10:'United States',11:'United States'}
COL={'United States':'#2a78d6','Europe':'#eb6834','Southern Africa':'#1baf7a','India':'#e87ba4'}
BG='#f6f1e7'; INK='#1d1d1b'
fig=plt.figure(figsize=(16,8.6),dpi=160,facecolor=BG)
views=[(36,-40,'Atlantic face'),(-2,48,'Indian Ocean face')]
for i,(la,lo,t) in enumerate(views):
    ax=fig.add_axes([0.02+i*0.49,0.07,0.47,0.80]); ax.set_facecolor(BG)
    m=Basemap(projection='ortho',lat_0=la,lon_0=lo,resolution='l',ax=ax)
    m.drawmapboundary(fill_color='#cfdbe6',color='#8a8a85',linewidth=0.8)
    m.fillcontinents(color='#e9e2d0',lake_color='#cfdbe6')
    m.drawcoastlines(color='#9a9488',linewidth=0.4)
    m.drawparallels(range(-80,90,20),color='#b9b4a8',linewidth=0.3,dashes=[1,0])
    m.drawmeridians(range(-180,180,20),color='#b9b4a8',linewidth=0.3,dashes=[1,0])
    # lighting overlay: lambert shade from upper-left
    W=m.urcrnrx; n=600
    xx,yy=np.meshgrid(np.linspace(0,W,n),np.linspace(0,W,n)); r=W/2
    X=(xx-r)/r; Y=(yy-r)/r; Z=np.sqrt(np.clip(1-X**2-Y**2,0,1))
    L=np.array([-0.45,0.55,0.7]); L/=np.linalg.norm(L)
    sh=X*L[0]+Y*L[1]+Z*L[2]
    alpha=np.where(X**2+Y**2<=1,np.clip(0.55-0.75*sh,0,0.55),0)
    img=np.zeros((n,n,4)); img[...,3]=alpha; img[...,:3]=0.08
    ax.imshow(img,extent=(0,W,0,W),origin='lower',zorder=5,interpolation='bilinear')
    spec=np.where(X**2+Y**2<=1,np.clip(sh-0.85,0,1)*2.2,0); im2=np.ones((n,n,4)); im2[...,3]=spec*0.5
    ax.imshow(im2,extent=(0,W,0,W),origin='lower',zorder=5)
    lab={}
    for fi,o in enumerate(d):
        if fi not in REG: continue
        c=COL[REG[fi]]
        for p in o['polys']:
            lo_,la_=zip(*[(x[0],x[1]) for x in p['c']])
            x,y=m(lo_,la_)
            if max(np.abs(x))>1e29: continue
            ax.plot(x,y,color=c,lw=1.6,zorder=8,solid_joinstyle='round')
        for pt in o['pts']:
            x,y=m(pt['lon'],pt['lat'])
            if abs(x)<1e29: ax.plot(x,y,'o',ms=1.8,color=c,zorder=9)

    LABELS={0:[('US 39th parallel',-98,38.9,-112,22),('US Eastern Oblique Arc',-76,37.5,-58,26),('England OS arcs',-2.5,50.6,-38,58),
               ('Anglo-French 1787',0.8,51.1,-30,64),('Helmert 52° N',10,51.6,12,66),('Cassini–Lacaille 1739',4.6,43.6,-40,40),
               ('Brousseaud 45° 43′',2.5,45.4,-40,46),('Maclear, Cape',18.5,-32,-8,-42),('Transvaal–Rhodesia',29.5,-21.2,-12,-12)],
            1:[('Helmert 52° N',14,52,45,62),('England / Anglo-French',-1,51,-24,44),('Cassini–Lacaille, Brousseaud',3.5,44.5,-8,30),
               ('India GTS meridional arc',77.6,13,95,4),('Lambton, Madras–Mangalore',78,12.7,92,22),
               ('Maclear, Cape',18.5,-32,-6,-44),('Transvaal–Rhodesia',29.5,-21.2,52,-26)]}
    for name,lo,la,tlo,tla in LABELS[i]:
        x0,y0=m(lo,la); x1,y1=m(tlo,tla)
        if max(abs(x0),abs(x1))>1e29: continue
        ax.annotate(name,xy=(x0,y0),xytext=(x1,y1),fontsize=9.5,color=INK,zorder=12,ha='center',
            bbox=dict(boxstyle='round,pad=0.25',fc=BG,ec='none',alpha=0.9),
            arrowprops=dict(arrowstyle='-',color=INK,lw=0.7,shrinkA=0,shrinkB=2))
    ax.set_title(t.upper(),fontsize=10,family='monospace',color='#2a5fa8',pad=4)
    ax.axis('off')
fig.text(0.03,0.955,'ARCS OF THE PARALLEL · KML',family='monospace',fontsize=10,color='#2a5fa8')
fig.text(0.03,0.915,'1,005 historical triangles on the WGS84 globe',family='serif',fontsize=22,color=INK)
hs=[plt.Line2D([],[],color=c,lw=3,label=k) for k,c in COL.items()]
fig.legend(handles=hs,loc='lower center',ncol=4,frameon=False,fontsize=11,labelcolor=INK)
fig.savefig('globe_3d_labelled.png',facecolor=BG)
