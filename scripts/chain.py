# Whole-chain curvature: pick non-overlapping triangles (largest first, chosen by area only),
# sum their observed excesses and their areas, K = sum(eps)/sum(A).
import json,math,numpy as np
from shapely.geometry import Polygon
from shapely.ops import unary_union
from pyproj import Proj
RAD=math.pi/180/3600
sig=json.load(open('angle_err.json'))
rows=[r for r in json.load(open('rows_t.json')) if r['E'] is not None]
CORE=['US 39th parallel','US Eastern Oblique','Maclear, Cape 1837–48']
out={}; tot=dict(E=0,A=0,AK=0,var=0,n=0)
for sv in CORE:
    S=[r for r in rows if r['survey']==sv]
    lon0=np.mean([r['lon'] for r in S]); lat0=np.mean([r['lat'] for r in S])
    P=Proj(proj='aeqd',lat_0=lat0,lon_0=lon0,ellps='WGS84')
    for r in S: r['poly']=Polygon([P(c[0],c[1]) for c in r['coords'][:3]])
    S.sort(key=lambda r:-r['poly'].area)
    chosen=[]; U=None
    for r in S:
        if U is None or r['poly'].intersection(U).area < 0.01*r['poly'].area:
            chosen.append(r); U=r['poly'] if U is None else unary_union([U,r['poly']])
    A=np.array([r['A_side'] if (r.get('A_side') and r['tier']!='C') else r['area'] for r in chosen])
    E=np.array([r['E'] for r in chosen]); Kell=np.array([r['Kref'] for r in chosen])
    s=sig[sv]['sclos']; n=len(chosen)
    Kc=E.sum()*RAD/A.sum(); sK=s*math.sqrt(n)*RAD/A.sum(); Kr=(A*Kell).sum()/A.sum()
    out[sv]=dict(n=n,ntot=len(S),A=A.sum()/1e6,E=E.sum(),Epred=(A*Kell).sum()/RAD,K=Kc,sK=sK,q=Kc/Kr,sq=sK/Kr,R=1/math.sqrt(Kc)/1e3,names=[r['name'] for r in chosen])
    tot['E']+=E.sum(); tot['A']+=A.sum(); tot['AK']+=(A*Kell).sum(); tot['var']+=n*s*s; tot['n']+=n
    o=out[sv]; print(f"{sv:24s} {n:3d} of {len(S):3d} triangles, area {o['A']:9,.0f} km²  Σε obs {o['E']:8.1f}″  pred {o['Epred']:8.1f}″  ±{s*math.sqrt(n):5.1f}″  K={Kc*1e14:.4f}±{sK*1e14:.4f}  q={o['q']:.4f}±{o['sq']:.4f} z={(o['q']-1)/o['sq']:+.2f}  R={o['R']:.0f} km")
Kc=tot['E']*RAD/tot['A']; sK=math.sqrt(tot['var'])*RAD/tot['A']; Kr=tot['AK']/tot['A']
print(f"{'CORE THREE combined':24s} {tot['n']:3d} triangles, area {tot['A']/1e6:9,.0f} km²  Σε obs {tot['E']:8.1f}″  pred {tot['AK']/RAD:8.1f}″  ±{math.sqrt(tot['var']):5.1f}″  K={Kc*1e14:.4f}±{sK*1e14:.4f}  q={Kc/Kr:.4f}±{sK/Kr:.4f} z={(Kc/Kr-1)/(sK/Kr):+.2f}  R={1/math.sqrt(Kc)/1e3:.0f} km")
out['combined']=dict(n=tot['n'],A=tot['A']/1e6,E=tot['E'],Epred=tot['AK']/RAD,K=Kc,sK=sK,q=Kc/Kr,sq=sK/Kr,R=1/math.sqrt(Kc)/1e3,noise=math.sqrt(tot['var']))
json.dump(out,open('chain_results.json','w'))
