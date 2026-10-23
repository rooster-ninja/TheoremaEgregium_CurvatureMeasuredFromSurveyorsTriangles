# Rebuild the Transvaal–Rhodesia network in a plane from printed side lengths ONLY, then compare to KML coordinates.
import json,math,numpy as np,matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
rows=[r for r in json.load(open('rows_t.json')) if r['fi']==8]
edges={}
for r in rows:
    for k,v in r['sides'].items(): edges.setdefault(k,[]).append(v)
L={k:float(np.mean(v)) for k,v in edges.items()}
spread=max((max(v)-min(v))/np.mean(v) for v in edges.values() if len(v)>1)
tri=[[x.strip() for x in r['name'].split(' - ')] for r in rows]
def l(a,b): return L['||'.join(sorted([a,b]))]
pos={}; t0=tri[0]; a,b,c=t0
pos[a]=np.array([0.,0.]); pos[b]=np.array([l(a,b),0.])
def third(p,q,dp,dq,ref):
    d=np.linalg.norm(q-p); x=(dp*dp-dq*dq+d*d)/(2*d); y=math.sqrt(max(dp*dp-x*x,0)); u=(q-p)/d; n=np.array([-u[1],u[0]])
    c1=p+x*u+y*n; c2=p+x*u-y*n
    return (c1,c2)
c1,c2=third(pos[a],pos[b],l(a,c),l(b,c),None); pos[c]=c1
changed=True
while changed:
    changed=False
    for t in tri:
        known=[v for v in t if v in pos]
        if len(known)==2:
            u=[v for v in t if v not in pos][0]; p,q=known
            # choose side opposite to any already-placed triangle sharing edge p-q
            cands=third(pos[p],pos[q],l(p,u),l(q,u),None)
            others=[pos[w] for tt in tri if p in tt and q in tt and tt!=t for w in tt if w not in (p,q) and w in pos]
            if others:
                o=others[0]; side=lambda z: np.sign(np.cross(pos[q]-pos[p],z-pos[p]))
                pos[u]=cands[0] if side(cands[0])!=side(o) else cands[1]
            else: pos[u]=cands[0]
            changed=True
# reference: coordinates -> local plane (azimuthal equidistant about centroid)
from pyproj import Proj
st={}
for r in rows:
    for n,(lo,la,_) in zip([x.strip() for x in r['name'].split(' - ')],r['coords']): st[n]=(lo,la)
lon0=np.mean([v[0] for v in st.values()]); lat0=np.mean([v[1] for v in st.values()])
P=Proj(proj='aeqd',lat_0=lat0,lon_0=lon0,ellps='WGS84')
names=sorted(pos)
X=np.array([pos[n] for n in names]); Y=np.array([P(*st[n]) for n in names])
# best-fit rigid (rotation+translation, reflection allowed, NO scale) Procrustes
Xc=X-X.mean(0); Yc=Y-Y.mean(0); U,S,Vt=np.linalg.svd(Xc.T@Yc); Rm=U@Vt
Xf=Xc@Rm+Y.mean(0); res=np.linalg.norm(Xf-Y,axis=1)
print('stations',len(names),'max side spread between triangles %.2e'%spread,'rms misfit %.1f m  max %.1f m'%(math.sqrt((res**2).mean()),res.max()))
BG='#f6f1e7'; INK='#1d1d1b'
fig,ax=plt.subplots(figsize=(8,10),dpi=160,facecolor=BG); ax.set_facecolor(BG)
for t in tri:
    for i in range(3):
        a,b=t[i],t[(i+1)%3]; ia,ib=names.index(a),names.index(b)
        ax.plot([Y[ia,0]/1e3,Y[ib,0]/1e3],[Y[ia,1]/1e3,Y[ib,1]/1e3],color='#eb6834',lw=4,alpha=0.35,solid_capstyle='round')
        ax.plot([Xf[ia,0]/1e3,Xf[ib,0]/1e3],[Xf[ia,1]/1e3,Xf[ib,1]/1e3],color='#2a78d6',lw=1.2)
for i,n in enumerate(names):
    ax.plot(*Xf[i]/1e3,'o',color=INK,ms=3.5); ax.annotate(f"{n}  {res[i]:.0f} m",Xf[i]/1e3,xytext=(6,-3),textcoords='offset points',fontsize=8,color='#3b3934')
ax.set_aspect('equal'); ax.set_xlabel('east (km)'); ax.set_ylabel('north (km)')
for k in ('top','right'): ax.spines[k].set_visible(False)
ax.plot([],[],color='#2a78d6',lw=1.5,label='rebuilt from printed sides only'); ax.plot([],[],color='#eb6834',lw=4,alpha=0.35,label='KML coordinates')
ax.legend(frameon=False,loc='upper left',bbox_to_anchor=(0.0,1.0))
fig.text(0.08,0.955,'TRANSVAAL–RHODESIA · REBUILT FROM SCRATCH',family='monospace',fontsize=9.5,color='#2a5fa8')
fig.text(0.08,0.925,f'RMS station misfit {math.sqrt((res**2).mean()):.0f} m over 220 km, no scale fitted',family='serif',fontsize=15,color=INK)
fig.subplots_adjust(top=0.9)
fig.savefig('rhodesia_rebuilt.png',facecolor=BG)
json.dump(dict(rms=float(math.sqrt((res**2).mean())),mx=float(res.max()),n=len(names)),open('rebuild.json','w'))
