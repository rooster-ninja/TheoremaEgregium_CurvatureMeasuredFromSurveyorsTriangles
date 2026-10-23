# Distance-only curvature: 4 stations with all 6 printed sides -> radius R that makes them lie on a sphere.
# Points on a sphere of radius R: Gram matrix G_ij = cos(s_ij / R) must be singular (rank 3).
import json,itertools,math,mpmath as mp,numpy as np,collections
mp.mp.dps=40
rows=json.load(open('rows_t.json'))
def solve(S):
    def f(R):
        G=mp.matrix(4,4)
        for i in range(4):
            for j in range(4): G[i,j]=mp.cos(mp.mpf(S[i][j])/R) if i!=j else 1
        return mp.det(G)
    # scan for sign change between 2000 km and 50000 km
    grid=[mp.mpf(x)*1000 for x in np.geomspace(2000,200000,400)]
    vals=[f(R) for R in grid]
    for a,b,fa,fb in zip(grid,grid[1:],vals,vals[1:]):
        if fa*fb<0: return float(mp.findroot(f,(a,b),solver='anderson'))
    return None
ell={'clarke1866':(6378206.4,1/294.978698),'bessel1841':(6377397.155,1/299.1528128),'wgs84':(6378137.0,1/298.257223563)}
def gauss_R(ellp,lat):
    a,f=ell[ellp]; e2=f*(2-f); s=math.sin(math.radians(lat))**2
    return math.sqrt(a*(1-e2)/(1-e2*s)**1.5 * a/math.sqrt(1-e2*s))
for sv,ref in [('US 39th parallel','clarke1866'),('US Eastern Oblique','clarke1866'),('Europe 52°N (Helmert)','bessel1841'),('Maclear, Cape 1837–48',None)]:
    L={}; lat={}
    for r in rows:
        if r['survey']!=sv: continue
        for k,v in r['sides'].items(): L.setdefault(k,[]).append(v)
        for n,c in zip([x.strip() for x in r['name'].split(' - ')],r['coords']): lat[n]=c[1]
    L={k:np.mean(v) for k,v in L.items()}
    adj=collections.defaultdict(set)
    for k in L: a,b=k.split('||'); adj[a].add(b); adj[b].add(a)
    quads=set()
    for a in adj:
        for b,c,d in itertools.combinations(sorted(adj[a]),3):
            if c in adj[b] and d in adj[b] and d in adj[c]: quads.add(tuple(sorted((a,b,c,d))))
    out=[]
    for q in sorted(quads):
        S=[[0 if i==j else L['||'.join(sorted([q[i],q[j]]))] for j in range(4)] for i in range(4)]
        R=solve(S)
        if R: out.append((R,np.mean([lat[x] for x in q]),max(max(r) for r in S)))
    if not out: print(sv,'no complete quadrilaterals'); continue
    Rs=np.array([o[0] for o in out]); la=np.mean([o[1] for o in out])
    print(f"{sv:24s} quads={len(out):3d}  median R from printed sides = {np.median(Rs)/1e3:9.1f} km  (IQR {np.percentile(Rs,25)/1e3:.1f}–{np.percentile(Rs,75)/1e3:.1f})")
    for e in ('clarke1866','bessel1841','wgs84'): print(f"      Gaussian radius √(MN) at {la:.1f}°, {e:10s}: {gauss_R(e,la)/1e3:9.1f} km")
