import math,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
BG='#f6f1e7'; INK='#1d1d1b'; MUT='#5a5650'; BLUE='#2a5fa8'; BR='#8a6d3b'
L=306.5; R=6374.0; k=0.13; hA=4.322; hB=1.323
def bul(x): return x*(L-x)/(2*R)
def ray(x): return hA+(hB-hA)*x/L+k*x*(L-x)/(2*R)
def mtn(x):  # schematic summits on curved sea level
    y=bul(x).copy()
    m=x<24; y[m]+=hA*(1-x[m]/24)**1.5
    m=x>L-10; y[m]+=hB*(1-(L-x[m])/10)**1.5
    return y
x=np.linspace(0,L,3000)
fig=plt.figure(figsize=(14,5.2),dpi=160,facecolor=BG)
# full line, true scale
ax=fig.add_axes([0.04,0.64,0.92,0.92*14*(5.5/L)/5.2]); ax.set_facecolor(BG)
ax.fill_between(x,-0.5,mtn(x),color='#cfc3a6',lw=0); ax.plot(x,ray(x),color=BLUE,lw=1.2)
ax.set_xlim(0,L); ax.set_ylim(-0.5,5); ax.set_aspect('equal'); ax.axis('off')
fig.text(0.04,0.77,'Whole line, 306 km, true scale: Earth bulge and mountains are a sliver; the light path (blue) barely separates from the ground',fontsize=10.5,color=INK)
ax.text(0,5.2,'Shasta',fontsize=8.5,color=MUT); ax.text(L,5.2,'Helena',fontsize=8.5,color=MUT,ha='right')
sb=fig.add_axes([0.04,0.58,0.92*50/L,0.01]); sb.plot([0,50],[0,0],color=INK,lw=2); sb.set_xlim(0,50); sb.axis('off')
fig.text(0.04,0.535,'50 km',fontsize=9,color=MUT)
# zoom windows, still true scale (same km per inch both ways)
wins=[('Near Mount Shasta (0–30 km)',0,30),('Middle of the line (138–168 km)',138,168),('Lowest clearance (210–240 km)',210,240)]
for i,(t,a,b) in enumerate(wins):
    xa=np.linspace(a,b,600); W=0.29
    bx=fig.add_axes([0.04+i*0.32,0.14,W,W*14*(5.0/(b-a))/5.2]); bx.set_facecolor(BG)
    bx.fill_between(xa,-0.3,mtn(xa),color='#cfc3a6',lw=0); bx.plot(xa,bul(xa),color=BR,lw=1)
    bx.plot(xa,ray(xa),color=BLUE,lw=1.6); bx.plot([a,b],[0,0],color=MUT,lw=0.8,ls=(0,(3,3)))
    bx.set_xlim(a,b); bx.set_ylim(-0.3,4.7); bx.set_aspect('equal')
    for kk in ('top','right'): bx.spines[kk].set_visible(False)
    bx.tick_params(labelsize=8); bx.set_xlabel('km from Shasta',fontsize=8.5,color=MUT)
    if i==0: bx.set_ylabel('height (km)',fontsize=8.5,color=MUT)
    xm=(a+b)/2; c=ray(np.array([xm]))[0]-bul(np.array([xm]))[0]
    bx.set_title(t,fontsize=10,color=INK,loc='left',pad=16); bx.text(0,1.02,f'light {c*1000:,.0f} m above sea level at {xm:.0f} km',transform=bx.transAxes,fontsize=8.5,color=BLUE,va='bottom')
fig.text(0.04,0.43,'Zoomed windows, still true scale (1 km across = 1 km up). Brown: sea-level surface. Blue: heliotrope light path. Dashed: straight chord at sea level between the ends.',fontsize=10,color=MUT)
fig.text(0.02,0.93,'MOUNT SHASTA TO MOUNT HELENA · NO EXAGGERATION',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.savefig('shasta_true.png',facecolor=BG)
